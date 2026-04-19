import sys
import numpy as np
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QGroupBox, QFormLayout, QTextEdit, QComboBox,
                             QStackedWidget, QFileDialog, QMenuBar, QMenu,
                             QTabWidget)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ballistics.environment import StandardAtmosphere, EarthModel, WindProfile
from ballistics.weather import LiveWeather
from ballistics.projectile import Projectile, Aerodynamics
from ballistics.solver import Solver6DoF
from ballistics.targeting import TargetingSystem
from ballistics.project import BallisticsProject
from ballistics.propellants import PROPELLANT_DATABASE, Propellant
from ballistics.interior_ballistics import GunSystem, Charge
from ballistics.interior_solver import InteriorSolver
from ballistics.monte_carlo import MonteCarloSimulator
from ballistics.viz3d import visualize_trajectory_3d
from ballistics.explosives import EXPLOSIVES_DATABASE, Explosive
from ballistics.lethality import FragmentationModel
from ballistics.raytracer import LethalityRayTracer
from ballistics.geometry import ProjectileGeometry
from ballistics.aero_predictor import AeroPredictor
from ballistics.materials import MATERIALS_DATABASE, Material

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=8, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax_side = self.fig.add_subplot(311)
        self.ax_top = self.fig.add_subplot(312)
        self.ax_temp = self.fig.add_subplot(313)
        super().__init__(self.fig)
        self.setParent(parent)
        self.fig.tight_layout(pad=3.0)

    def plot_trajectory(self, sol):
        self.ax_side.clear()
        self.ax_top.clear()
        self.ax_temp.clear()

        x = sol.y[0, :]
        y = sol.y[1, :]
        z = sol.y[2, :]
        t = sol.t

        self.ax_side.plot(x, z, 'r-')
        self.ax_side.set_title('Side Profile (Altitude vs Range)')
        self.ax_side.set_xlabel('Range X (m)')
        self.ax_side.set_ylabel('Altitude Z (m)')
        self.ax_side.grid(True)

        self.ax_top.plot(x, y, 'g-')
        self.ax_top.set_title('Top-Down Profile (Deflection)')
        self.ax_top.set_xlabel('Range X (m)')
        self.ax_top.set_ylabel('Deflection Y (m)')
        self.ax_top.grid(True)

        if len(sol.y) > 13:
            temps = sol.y[13, :]
            self.ax_temp.plot(t, temps, 'orange')

            # Check if we have a material to plot melting point
            mat_name = getattr(self, 'current_material_name', None)
            if mat_name:
                from ballistics.materials import Material
                mat = Material(mat_name)
                self.ax_temp.axhline(mat.melting_point, color='red', linestyle='--', label=f'Melting Point ({mat.melting_point}K)')
                self.ax_temp.legend()

            self.ax_temp.set_title('Nose Tip Temperature vs Time')
            self.ax_temp.set_xlabel('Time (s)')
            self.ax_temp.set_ylabel('Temperature (K)')
            self.ax_temp.grid(True)
            self.ax_temp.set_visible(True)
        else:
            self.ax_temp.set_visible(False)

        self.draw()

    def plot_dispersion(self, mc_res):
        self.ax_side.clear()
        self.ax_top.clear()
        self.ax_temp.clear()

        # Hide the bottom plots for dispersion, we only need a 2D scatter
        self.ax_top.set_visible(False)
        self.ax_temp.set_visible(False)

        # Re-configure top plot (which is actually ax_side)
        ax = self.ax_side

        impacts = mc_res.impacts
        u = impacts[:, 0]
        v = impacts[:, 1]

        ax.scatter(u, v, c='red', alpha=0.5, label='Impacts')
        ax.plot(mc_res.mpi[0], mc_res.mpi[1], 'gx', markersize=10, markeredgewidth=3, label='MPI')

        # Draw CEP circle
        circle = plt.Circle((mc_res.mpi[0], mc_res.mpi[1]), mc_res.cep_50, color='blue', fill=False, linestyle='--', linewidth=2, label=f'CEP50 ({mc_res.cep_50:.2f}m)')
        ax.add_patch(circle)

        if mc_res.target_plane == 'vertical':
            ax.set_xlabel('Deflection Y (m)')
            ax.set_ylabel('Elevation Z (m)')
            ax.set_title('Vertical Impact Plane')
        else:
            ax.set_xlabel('Range X (m)')
            ax.set_ylabel('Deflection Y (m)')
            ax.set_title('Horizontal Ground Impact Plane')

        ax.legend()
        ax.grid(True)
        ax.set_aspect('equal', adjustable='datalim')

        self.draw()

    def reset_layout(self):
        self.ax_top.set_visible(True)
        self.ax_temp.set_visible(True)


import matplotlib.pyplot as plt

class BallisticsGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wilson Ballistic Suite (WBS)")
        self.resize(1200, 800)

        self.project = BallisticsProject()
        self.current_atm = StandardAtmosphere()

        # Stacked Widget to hold different screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Build Screens
        self.build_main_menu()
        self.build_projectile_selection()
        self.build_firearm_designer()
        self.build_projectile_designer()
        self.build_calculator()

        # Build Menu Bar
        self.build_menubar()

        # Start on Main Menu
        self.build_aero_predictor()

        self.page_index_main = 0
        self.page_index_proj_sel = 1
        self.page_index_firearm = 2
        self.page_index_proj_des = 3
        self.page_index_calc = 4
        self.page_index_aero = 5
        self.stacked_widget.setCurrentIndex(0)


    def build_projectile_selection(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Step 1: Select Projectile Category")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 30px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        btn_small = QPushButton("Small Arms (Rifle/Pistol)")
        btn_small.setFixedSize(300, 50)
        btn_small.clicked.connect(lambda: self.select_category("small"))
        layout.addWidget(btn_small, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_arty = QPushButton("Artillery (Howitzer/Cannon)")
        btn_arty.setFixedSize(300, 50)
        btn_arty.clicked.connect(lambda: self.select_category("artillery"))
        layout.addWidget(btn_arty, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_missile = QPushButton("Missile / Guided Munition")
        btn_missile.setFixedSize(300, 50)
        btn_missile.clicked.connect(lambda: self.select_category("missile"))
        layout.addWidget(btn_missile, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_back = QPushButton("Back to Main Menu")
        btn_back.setFixedSize(150, 30)
        btn_back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(self.page_index_main))
        layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

        self.stacked_widget.insertWidget(1, widget)

    def select_category(self, cat):
        # We can prepopulate fields here based on category if needed
        self.stacked_widget.setCurrentIndex(self.page_index_firearm)

    def build_firearm_designer(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title = QLabel("Step 2: Firearm & Barrel Designer")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # We will move the group_int here from calculator later
        self.firearm_layout = QVBoxLayout()
        layout.addLayout(self.firearm_layout)

        nav_layout = QHBoxLayout()
        btn_back = QPushButton("Back")
        btn_back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(self.page_index_proj_sel))
        btn_next = QPushButton("Next")
        btn_next.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(self.page_index_proj_des))
        nav_layout.addWidget(btn_back)
        nav_layout.addWidget(btn_next)

        layout.addLayout(nav_layout)
        self.stacked_widget.insertWidget(2, widget)

    def build_projectile_designer(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title = QLabel("Step 3: Projectile Designer")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.proj_layout = QVBoxLayout()
        layout.addLayout(self.proj_layout)

        nav_layout = QHBoxLayout()
        btn_back = QPushButton("Back")
        btn_back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(self.page_index_firearm))
        btn_next = QPushButton("Next (Simulation Dashboard)")
        btn_next.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(self.page_index_calc))
        nav_layout.addWidget(btn_back)
        nav_layout.addWidget(btn_next)

        layout.addLayout(nav_layout)
        self.stacked_widget.insertWidget(3, widget)

    def build_aero_predictor(self):
        self.aero_widget = QWidget()
        layout = QVBoxLayout(self.aero_widget)

        form_layout = QFormLayout()

        self.input_geo_cal = QLineEdit("0.155")
        self.input_geo_n_len = QLineEdit("0.4")
        self.combo_nose = QComboBox()
        self.combo_nose.addItems(["tangent_ogive", "cone"])
        self.input_geo_meplat = QLineEdit("0.0")
        self.input_geo_b_len = QLineEdit("0.3")
        self.input_geo_bt_len = QLineEdit("0.1")
        self.input_geo_bt_base = QLineEdit("0.13")

        form_layout.addRow("Caliber (m):", self.input_geo_cal)
        form_layout.addRow("Nose Length (m):", self.input_geo_n_len)
        form_layout.addRow("Nose Type:", self.combo_nose)
        form_layout.addRow("Meplat Diameter (m):", self.input_geo_meplat)
        form_layout.addRow("Body Length (m):", self.input_geo_b_len)
        form_layout.addRow("Boattail Length (m):", self.input_geo_bt_len)
        form_layout.addRow("Boattail Base Diam (m):", self.input_geo_bt_base)

        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        btn_calc = QPushButton("Predict Cd vs Mach Curve")
        btn_calc.clicked.connect(self.run_aero_predictor)
        btn_back = QPushButton("Back to Calculator")
        btn_back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        btn_layout.addWidget(btn_calc)
        btn_layout.addWidget(btn_back)
        layout.addLayout(btn_layout)

        self.canvas_aero = MplCanvas(self, width=6, height=4, dpi=100)
        self.canvas_aero.ax_top.set_visible(False)
        layout.addWidget(self.canvas_aero)

        self.stacked_widget.insertWidget(5, self.aero_widget)

    def build_menubar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")

        action_new = QAction("New Project", self)
        action_new.triggered.connect(self.new_project)
        file_menu.addAction(action_new)

        action_open = QAction("Open Project...", self)
        action_open.triggered.connect(self.open_project)
        file_menu.addAction(action_open)

        file_menu.addSeparator()

        action_save = QAction("Save", self)
        action_save.triggered.connect(self.save_project)
        file_menu.addAction(action_save)

        action_save_as = QAction("Save As...", self)
        action_save_as.triggered.connect(self.save_project_as)
        file_menu.addAction(action_save_as)

        file_menu.addSeparator()

        action_exit = QAction("Exit", self)
        action_exit.triggered.connect(self.close)
        file_menu.addAction(action_exit)

    def build_main_menu(self):
        menu_widget = QWidget()
        layout = QVBoxLayout(menu_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("WILSON BALLISTIC SUITE")
        title.setStyleSheet("font-size: 36px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Next-Generation 6-DoF Ballistics & Lethality Engine")
        subtitle.setStyleSheet("font-size: 18px; color: gray; margin-bottom: 40px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        btn_new = QPushButton("New Project")
        btn_new.setFixedSize(300, 60)
        btn_new.setStyleSheet("font-size: 18px;")
        btn_new.clicked.connect(self.new_project)
        layout.addWidget(btn_new, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_open = QPushButton("Open Project")
        btn_open.setFixedSize(300, 60)
        btn_open.setStyleSheet("font-size: 18px;")
        btn_open.clicked.connect(self.open_project)
        layout.addWidget(btn_open, alignment=Qt.AlignmentFlag.AlignCenter)

        self.stacked_widget.insertWidget(0, menu_widget)

    def build_calculator(self):
        calc_widget = QWidget()
        main_layout = QHBoxLayout(calc_widget)

        # Left Panel - Inputs
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setFixedWidth(350)

        # Interior Ballistics Inputs
        group_int = QGroupBox("Interior Ballistics & Barrel Designer")
        form_int = QFormLayout()

        self.input_chamber_vol = QLineEdit("0.018")
        self.input_barrel_len = QLineEdit("5.0")
        self.input_twist = QLineEdit("10.0")
        self.input_engrave_n = QLineEdit("5000.0")
        self.input_frict_n = QLineEdit("1000.0")

        self.combo_powder = QComboBox()
        self.combo_powder.addItems(list(PROPELLANT_DATABASE.keys()))

        self.input_charge_mass = QLineEdit("12.0")
        self.input_web = QLineEdit("0.003")

        self.btn_calc_int = QPushButton("Calculate Muzzle Velocity & Spin")
        self.btn_calc_int.setStyleSheet("background-color: darkblue; color: white;")
        self.btn_calc_int.clicked.connect(self.calculate_interior)

        form_int.addRow("Chamber Vol (m^3):", self.input_chamber_vol)
        form_int.addRow("Barrel Len (m):", self.input_barrel_len)
        form_int.addRow("Rifling Twist (1:X in):", self.input_twist)
        form_int.addRow("Engraving Force (N):", self.input_engrave_n)
        form_int.addRow("Sliding Friction (N):", self.input_frict_n)
        form_int.addRow("Propellant Type:", self.combo_powder)
        form_int.addRow("Charge Mass (kg):", self.input_charge_mass)
        form_int.addRow("Web Thickness (m):", self.input_web)
        form_int.addRow(self.btn_calc_int)

        group_int.setLayout(form_int)
        left_layout.addWidget(group_int)

        # Projectile Inputs
        group_proj = QGroupBox("Exterior Projectile Parameters")
        form_proj = QFormLayout()
        self.input_mass = QLineEdit()
        self.input_diam = QLineEdit()
        self.input_v0 = QLineEdit()
        self.input_spin = QLineEdit()
        self.combo_aero = QComboBox()
        self.combo_aero.addItems(["G7 Standard", "G1 Standard", "Auto-Predicted (Datcom)"])
        form_proj.addRow("Mass (kg):", self.input_mass)
        form_proj.addRow("Caliber (m):", self.input_diam)
        form_proj.addRow("Muzzle Vel (m/s):", self.input_v0)
        form_proj.addRow("Spin Rate (rad/s):", self.input_spin)
        form_proj.addRow("Aero Model:", self.combo_aero)

        self.btn_load_stl = QPushButton("Load Custom CAD (STL)...")
        self.btn_load_stl.clicked.connect(self.load_stl)
        form_proj.addRow(self.btn_load_stl)

        # Datcom Aero Predictor Input Button
        self.btn_aero_predict = QPushButton("Empirical Aero Predictor (Datcom)")
        self.btn_aero_predict.clicked.connect(self.open_aero_predictor)
        form_proj.addRow(self.btn_aero_predict)

        self.btn_run_cfd = QPushButton("Run True 3D CFD")
        self.btn_run_cfd.setStyleSheet("background-color: darkcyan; color: white; font-weight: bold;")
        self.btn_run_cfd.clicked.connect(self.run_cfd_pipeline)
        form_proj.addRow(self.btn_run_cfd)

        group_proj.setLayout(form_proj)
        left_layout.addWidget(group_proj)

        # Hypersonics Inputs
        group_hyper = QGroupBox("Hypersonics & Aerothermodynamics")
        group_hyper.setCheckable(True)
        group_hyper.setChecked(False)
        self.group_hyper = group_hyper
        form_hyper = QFormLayout()
        self.combo_mat = QComboBox()
        self.combo_mat.addItems(list(MATERIALS_DATABASE.keys()))
        self.input_nose_rad = QLineEdit("0.01")
        form_hyper.addRow("Material:", self.combo_mat)
        form_hyper.addRow("Nose Radius (m):", self.input_nose_rad)
        group_hyper.setLayout(form_hyper)
        left_layout.addWidget(group_hyper)

        # Active Propulsion Inputs
        group_prop = QGroupBox("Active Propulsion (Rockets)")
        group_prop.setCheckable(True)
        group_prop.setChecked(False)
        self.group_prop = group_prop
        form_prop = QFormLayout()
        self.input_thrust = QLineEdit("1000.0")
        self.input_burn_time = QLineEdit("2.0")
        self.input_prop_mass = QLineEdit("2.0")
        form_prop.addRow("Thrust (N):", self.input_thrust)
        form_prop.addRow("Burn Time (s):", self.input_burn_time)
        form_prop.addRow("Propellant Mass (kg):", self.input_prop_mass)
        group_prop.setLayout(form_prop)
        left_layout.addWidget(group_prop)

        # Lethality & Fragmentation Inputs
        group_leth = QGroupBox("Lethality & Fragmentation")
        group_leth.setCheckable(True)
        group_leth.setChecked(False)
        self.group_leth = group_leth
        form_leth = QFormLayout()
        self.combo_exp = QComboBox()
        self.combo_exp.addItems(list(EXPLOSIVES_DATABASE.keys()))
        self.input_exp_mass = QLineEdit("5.0")
        self.input_fragments = QLineEdit("500")
        self.input_tgt_armor = QLineEdit("10.0")
        self.btn_load_tgt_stl = QPushButton("Load Target STL...")
        self.btn_load_tgt_stl.clicked.connect(self.load_target_stl)

        # We need a new panel for CFD input params
        self.input_cfd_mach = QLineEdit("2.0")
        self.input_cfd_alt = QLineEdit("0.0")
        self.input_cfd_res = QLineEdit("30")
        form_proj.addRow("CFD Mach:", self.input_cfd_mach)
        form_proj.addRow("CFD Altitude (m):", self.input_cfd_alt)
        form_proj.addRow("CFD Voxel Res:", self.input_cfd_res)

        form_leth.addRow("Explosive Type:", self.combo_exp)
        form_leth.addRow("Explosive Mass (kg):", self.input_exp_mass)
        form_leth.addRow("Fragment Count:", self.input_fragments)
        form_leth.addRow("Target Armor (mm):", self.input_tgt_armor)
        form_leth.addRow("Target Mesh:", self.btn_load_tgt_stl)
        group_leth.setLayout(form_leth)
        left_layout.addWidget(group_leth)

        # Environment Inputs
        group_env = QGroupBox("Environment")
        form_env = QFormLayout()
        self.input_wind_speed = QLineEdit()
        self.input_wind_dir = QLineEdit()
        self.input_lat = QLineEdit()
        self.input_lon = QLineEdit()
        self.btn_live_weather = QPushButton("Fetch Live Weather (Lat/Lon)")
        self.btn_live_weather.clicked.connect(self.fetch_weather)
        self.weather_status = QLabel("Using Standard Sea Level")

        form_env.addRow("Wind Speed (m/s):", self.input_wind_speed)
        form_env.addRow("Wind Dir (deg):", self.input_wind_dir)
        form_env.addRow("Latitude:", self.input_lat)
        form_env.addRow("Longitude:", self.input_lon)
        form_env.addRow(self.btn_live_weather)
        form_env.addRow(self.weather_status)
        group_env.setLayout(form_env)
        left_layout.addWidget(group_env)

        # Target Inputs
        group_target = QGroupBox("Targeting System (Intercept)")
        form_target = QFormLayout()
        self.input_tx = QLineEdit()
        self.input_ty = QLineEdit()
        self.input_tz = QLineEdit()
        self.input_tvx = QLineEdit()
        self.input_tvy = QLineEdit()
        self.input_tvz = QLineEdit()
        form_target.addRow("Target Pos X (m):", self.input_tx)
        form_target.addRow("Target Pos Y (m):", self.input_ty)
        form_target.addRow("Target Pos Z (m):", self.input_tz)
        form_target.addRow("Target Vel X (m/s):", self.input_tvx)
        form_target.addRow("Target Vel Y (m/s):", self.input_tvy)
        form_target.addRow("Target Vel Z (m/s):", self.input_tvz)
        group_target.setLayout(form_target)
        left_layout.addWidget(group_target)

        # Guidance Inputs
        group_guide = QGroupBox("Proportional Navigation Guidance")
        group_guide.setCheckable(True)
        group_guide.setChecked(False)
        self.group_guide = group_guide
        form_guide = QFormLayout()
        self.input_nav_k = QLineEdit("4.0")
        self.input_max_g = QLineEdit("30.0")
        self.input_guide_delay = QLineEdit("0.5")
        form_guide.addRow("Navigation Constant (N):", self.input_nav_k)
        form_guide.addRow("Max Lateral Accel (G):", self.input_max_g)
        form_guide.addRow("Activation Delay (s):", self.input_guide_delay)
        group_guide.setLayout(form_guide)
        left_layout.addWidget(group_guide)

        # Dispersion Inputs
        group_disp = QGroupBox("Monte Carlo Dispersion (Std Dev)")
        form_disp = QFormLayout()
        self.input_sd_v0 = QLineEdit()
        self.input_sd_mass = QLineEdit()
        self.input_sd_wind = QLineEdit()
        self.input_sd_pitch = QLineEdit()
        self.input_sd_yaw = QLineEdit()
        self.input_shots = QLineEdit()
        self.combo_plane = QComboBox()
        self.combo_plane.addItems(["vertical", "horizontal"])

        form_disp.addRow("Shots:", self.input_shots)
        form_disp.addRow("Target Plane:", self.combo_plane)
        form_disp.addRow("SD V0 (m/s):", self.input_sd_v0)
        form_disp.addRow("SD Mass (kg):", self.input_sd_mass)
        form_disp.addRow("SD Wind (m/s):", self.input_sd_wind)
        form_disp.addRow("SD Pitch (deg):", self.input_sd_pitch)
        form_disp.addRow("SD Yaw (deg):", self.input_sd_yaw)
        group_disp.setLayout(form_disp)
        left_layout.addWidget(group_disp)

        # Calculate Buttons
        btn_layout = QHBoxLayout()
        self.btn_calc = QPushButton("Find Firing Solution")
        self.btn_calc.setStyleSheet("background-color: darkred; color: white; font-weight: bold; padding: 10px;")
        self.btn_calc.clicked.connect(self.calculate_solution)

        self.btn_mc = QPushButton("Run Monte Carlo")
        self.btn_mc.setStyleSheet("background-color: darkgreen; color: white; font-weight: bold; padding: 10px;")
        self.btn_mc.clicked.connect(self.run_monte_carlo)

        self.btn_3d = QPushButton("View 3D Trajectory (PyVista)")
        self.btn_3d.setStyleSheet("background-color: darkblue; color: white; font-weight: bold; padding: 10px;")
        self.btn_3d.setEnabled(False) # Will enable after a successful calculation
        self.btn_3d.clicked.connect(self.view_3d_scene)

        self.btn_leth = QPushButton("Run Lethality Analysis")
        self.btn_leth.setStyleSheet("background-color: purple; color: white; font-weight: bold; padding: 10px;")
        self.btn_leth.clicked.connect(self.run_lethality)

        btn_layout.addWidget(self.btn_calc)
        btn_layout.addWidget(self.btn_mc)
        left_layout.addLayout(btn_layout)
        left_layout.addWidget(self.btn_3d)
        left_layout.addWidget(self.btn_leth)

        # We don't add stretch so things compress naturally if window is small
        # Or add scroll area if needed, but it should fit in 800px height.

        # Right Panel - Outputs
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        self.text_output.setFixedHeight(150)
        self.text_output.setStyleSheet("font-family: monospace;")
        right_layout.addWidget(self.text_output)

        self.tabs = QTabWidget()
        self.tab_traj = QWidget()
        self.tab_disp = QWidget()
        self.tabs.addTab(self.tab_traj, "Trajectory Profile")
        self.tabs.addTab(self.tab_disp, "Dispersion Scatter")

        traj_layout = QVBoxLayout(self.tab_traj)
        self.canvas_traj = MplCanvas(self, width=6, height=6, dpi=100)
        traj_layout.addWidget(self.canvas_traj)

        disp_layout = QVBoxLayout(self.tab_disp)
        self.canvas_disp = MplCanvas(self, width=6, height=6, dpi=100)
        disp_layout.addWidget(self.canvas_disp)

        right_layout.addWidget(self.tabs)

        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)

        self.stacked_widget.insertWidget(4, calc_widget)

    def populate_gui_from_project(self):
        state = self.project.state

        # Gun Barrel
        gb = state.get("gun_barrel", {})
        self.input_chamber_vol.setText(str(gb.get("chamber_vol_m3", 0.018)))
        self.input_barrel_len.setText(str(gb.get("barrel_len_m", 5.0)))

        pw_idx = self.combo_powder.findText(gb.get("propellant", "Generic Triple-Base (Artillery)"))
        if pw_idx >= 0:
            self.combo_powder.setCurrentIndex(pw_idx)

        self.input_charge_mass.setText(str(gb.get("charge_mass_kg", 12.0)))
        self.input_web.setText(str(gb.get("web_thickness_m", 0.003)))
        self.input_twist.setText(str(gb.get("twist_rate_in_per_turn", 10.0)))
        self.input_engrave_n.setText(str(gb.get("engraving_force_n", 5000.0)))
        self.input_frict_n.setText(str(gb.get("bore_friction_n", 1000.0)))

        # Projectile
        p = state.get("projectile", {})
        self.input_mass.setText(str(p.get("mass_kg", 43.0)))
        self.input_diam.setText(str(p.get("diameter_m", 0.155)))
        self.input_v0.setText(str(p.get("muzzle_velocity_ms", 800.0)))
        self.input_spin.setText(str(p.get("spin_rate_rads", 1884.95)))
        aero_idx = self.combo_aero.findText(p.get("aero_model", "G7 Standard"))
        if aero_idx >= 0:
            self.combo_aero.setCurrentIndex(aero_idx)

        if p.get("custom_stl_path"):
            self.btn_load_stl.setText(f"STL: {os.path.basename(p['custom_stl_path'])}")

        # Environment
        e = state.get("environment", {})
        self.input_wind_speed.setText(str(e.get("wind_speed_ms", 0.0)))
        self.input_wind_dir.setText(str(e.get("wind_direction_deg", 90.0)))
        self.input_lat.setText(str(e.get("latitude", 39.7392)))
        self.input_lon.setText(str(e.get("longitude", -104.9903)))

        # Target
        t = state.get("target", {})
        self.input_tx.setText(str(t.get("x_m", 2500.0)))
        self.input_ty.setText(str(t.get("y_m", 0.0)))
        self.input_tz.setText(str(t.get("z_m", 0.0)))
        self.input_tvx.setText(str(t.get("vx_ms", 0.0)))
        self.input_tvy.setText(str(t.get("vy_ms", 0.0)))
        self.input_tvz.setText(str(t.get("vz_ms", 0.0)))

        # Guidance
        g = state.get("guidance", {})
        self.group_guide.setChecked(g.get("active", False))
        self.input_nav_k.setText(str(g.get("nav_constant", 4.0)))
        self.input_max_g.setText(str(g.get("max_g", 30.0)))
        self.input_guide_delay.setText(str(g.get("activation_time_s", 0.5)))

        # Dispersion
        d = state.get("dispersion", {})
        self.input_shots.setText(str(d.get("shots", 50)))
        self.input_sd_v0.setText(str(d.get("v0_sd_ms", 2.0)))
        self.input_sd_mass.setText(str(d.get("mass_sd_kg", 0.01)))
        self.input_sd_wind.setText(str(d.get("wind_speed_sd_ms", 1.0)))
        self.input_sd_pitch.setText(str(d.get("pitch_sd_deg", 0.05)))
        self.input_sd_yaw.setText(str(d.get("yaw_sd_deg", 0.05)))
        plane_idx = self.combo_plane.findText(d.get("plane", "vertical"))
        if plane_idx >= 0:
            self.combo_plane.setCurrentIndex(plane_idx)

        # Propulsion
        pr = state.get("propulsion", {})
        self.group_prop.setChecked(pr.get("active", False))
        self.input_thrust.setText(str(pr.get("thrust_n", 1000.0)))
        self.input_burn_time.setText(str(pr.get("burn_time_s", 2.0)))
        self.input_prop_mass.setText(str(pr.get("propellant_mass_kg", 2.0)))

        # Lethality
        l = state.get("lethality", {})
        self.group_leth.setChecked(l.get("active", False))
        exp_idx = self.combo_exp.findText(l.get("explosive", "Composition B"))
        if exp_idx >= 0:
            self.combo_exp.setCurrentIndex(exp_idx)
        self.input_exp_mass.setText(str(l.get("explosive_mass_kg", 5.0)))
        self.input_fragments.setText(str(l.get("fragments", 500)))
        self.input_tgt_armor.setText(str(l.get("target_armor_mm", 10.0)))
        if l.get("target_stl"):
            self.btn_load_tgt_stl.setText(f"Target: {os.path.basename(l['target_stl'])}")

        # Hypersonics
        h = state.get("hypersonics", {})
        self.group_hyper.setChecked(h.get("active", False))
        mat_idx = self.combo_mat.findText(h.get("material", "Tungsten (WHA)"))
        if mat_idx >= 0:
            self.combo_mat.setCurrentIndex(mat_idx)
        self.input_nose_rad.setText(str(h.get("nose_radius_m", 0.01)))

    def populate_project_from_gui(self):
        state = self.project.state
        try:
            state["gun_barrel"]["chamber_vol_m3"] = float(self.input_chamber_vol.text())
            state["gun_barrel"]["barrel_len_m"] = float(self.input_barrel_len.text())
            state["gun_barrel"]["propellant"] = self.combo_powder.currentText()
            state["gun_barrel"]["charge_mass_kg"] = float(self.input_charge_mass.text())
            state["gun_barrel"]["web_thickness_m"] = float(self.input_web.text())
            state["gun_barrel"]["twist_rate_in_per_turn"] = float(self.input_twist.text())
            state["gun_barrel"]["engraving_force_n"] = float(self.input_engrave_n.text())
            state["gun_barrel"]["bore_friction_n"] = float(self.input_frict_n.text())

            state["projectile"]["mass_kg"] = float(self.input_mass.text())
            state["projectile"]["diameter_m"] = float(self.input_diam.text())
            state["projectile"]["muzzle_velocity_ms"] = float(self.input_v0.text())
            state["projectile"]["spin_rate_rads"] = float(self.input_spin.text())
            state["projectile"]["aero_model"] = self.combo_aero.currentText()

            state["environment"]["wind_speed_ms"] = float(self.input_wind_speed.text())
            state["environment"]["wind_direction_deg"] = float(self.input_wind_dir.text())
            state["environment"]["latitude"] = float(self.input_lat.text())
            state["environment"]["longitude"] = float(self.input_lon.text())

            state["target"]["x_m"] = float(self.input_tx.text())
            state["target"]["y_m"] = float(self.input_ty.text())
            state["target"]["z_m"] = float(self.input_tz.text())
            state["target"]["vx_ms"] = float(self.input_tvx.text())
            state["target"]["vy_ms"] = float(self.input_tvy.text())
            state["target"]["vz_ms"] = float(self.input_tvz.text())

            state["guidance"] = {
                "active": self.group_guide.isChecked(),
                "nav_constant": float(self.input_nav_k.text()),
                "max_g": float(self.input_max_g.text()),
                "activation_time_s": float(self.input_guide_delay.text())
            }

            state["dispersion"]["shots"] = int(self.input_shots.text())
            state["dispersion"]["v0_sd_ms"] = float(self.input_sd_v0.text())
            state["dispersion"]["mass_sd_kg"] = float(self.input_sd_mass.text())
            state["dispersion"]["wind_speed_sd_ms"] = float(self.input_sd_wind.text())
            state["dispersion"]["pitch_sd_deg"] = float(self.input_sd_pitch.text())
            state["dispersion"]["yaw_sd_deg"] = float(self.input_sd_yaw.text())
            state["dispersion"]["plane"] = self.combo_plane.currentText()

            state["propulsion"] = {
                "active": self.group_prop.isChecked(),
                "thrust_n": float(self.input_thrust.text()),
                "burn_time_s": float(self.input_burn_time.text()),
                "propellant_mass_kg": float(self.input_prop_mass.text())
            }

            state["lethality"]["active"] = self.group_leth.isChecked()
            state["lethality"]["explosive"] = self.combo_exp.currentText()
            state["lethality"]["explosive_mass_kg"] = float(self.input_exp_mass.text())
            state["lethality"]["fragments"] = int(self.input_fragments.text())
            state["lethality"]["target_armor_mm"] = float(self.input_tgt_armor.text())

            state["hypersonics"]["active"] = self.group_hyper.isChecked()
            state["hypersonics"]["material"] = self.combo_mat.currentText()
            state["hypersonics"]["nose_radius_m"] = float(self.input_nose_rad.text())
        except ValueError:
            pass # Ignore conversion errors when typing

    def new_project(self):
        self.project = BallisticsProject()
        self.populate_gui_from_project()
        # Navigate to the new Projectile Selection screen instead of calculator
        self.stacked_widget.setCurrentIndex(self.page_index_proj_sel)
        self.setWindowTitle("Wilson Ballistic Suite - New Project")

    def open_project(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Open Ballistics Project", "", "Ballistics Project (*.blst);;JSON Files (*.json);;All Files (*)")
        if filepath:
            try:
                self.project = BallisticsProject()
                self.project.load(filepath)
                self.populate_gui_from_project()
                self.stacked_widget.setCurrentIndex(1)
                self.setWindowTitle(f"Wilson Ballistic Suite - {os.path.basename(filepath)}")
            except Exception as e:
                self.text_output.setText(f"Error loading project: {e}")

    def save_project(self):
        if self.project.filepath:
            self.populate_project_from_gui()
            self.project.save()
            self.text_output.setText(f"Saved to {self.project.filepath}")
        else:
            self.save_project_as()

    def save_project_as(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Ballistics Project", "", "Ballistics Project (*.blst)")
        if filepath:
            if not filepath.endswith(".blst"):
                filepath += ".blst"
            self.populate_project_from_gui()
            self.project.save(filepath)
            self.setWindowTitle(f"Wilson Ballistic Suite - {os.path.basename(filepath)}")
            self.text_output.setText(f"Saved to {filepath}")

    def load_stl(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Load STL Mesh", "", "STL Files (*.stl)")
        if filepath:
            try:
                # Load with default Lead density for demo
                proj = Projectile.from_stl(filepath, density_kg_m3=11340.0)
                self.input_mass.setText(f"{proj.mass:.4f}")
                self.input_diam.setText(f"{proj.diameter:.4f}")
                self.btn_load_stl.setText(f"STL: {os.path.basename(filepath)}")
                self.project.state["projectile"]["custom_stl_path"] = filepath
            except Exception as e:
                self.text_output.setText(f"Failed to load STL: {e}")

    def open_aero_predictor(self):
        self.stacked_widget.setCurrentIndex(2)

    def run_aero_predictor(self):
        try:
            geo = ProjectileGeometry(
                caliber_m=float(self.input_geo_cal.text()),
                nose_length_m=float(self.input_geo_n_len.text()),
                nose_type=self.combo_nose.currentText(),
                meplat_diameter_m=float(self.input_geo_meplat.text()),
                body_length_m=float(self.input_geo_b_len.text()),
                boattail_length_m=float(self.input_geo_bt_len.text()),
                boattail_base_diameter_m=float(self.input_geo_bt_base.text())
            )

            # Predict based on current atmosphere
            props = self.current_atm.get_properties(0)
            predictor = AeroPredictor(geo, density_sl=props['density'], sound_speed_sl=props['speed_of_sound'])

            self.custom_aero_model = predictor.predict_aerodynamics(num_points=100, max_mach=5.0)

            # Set the combo box to Auto Predicted
            idx = self.combo_aero.findText("Auto-Predicted (Datcom)")
            if idx >= 0:
                self.combo_aero.setCurrentIndex(idx)

            # Plot the results
            self.canvas_aero.ax_side.clear()
            machs = np.linspace(0.1, 5.0, 100)
            cds = [self.custom_aero_model.cd(m) for m in machs]

            self.canvas_aero.ax_side.plot(machs, cds, 'b-')
            self.canvas_aero.ax_side.set_title('Predicted Drag Coefficient ($C_D$) vs Mach')
            self.canvas_aero.ax_side.set_xlabel('Mach Number')
            self.canvas_aero.ax_side.set_ylabel('$C_D$')
            self.canvas_aero.ax_side.grid(True)
            self.canvas_aero.draw()

        except Exception as e:
            print(f"Error predicting aero: {e}")

    def load_target_stl(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Load Target STL", "", "STL Files (*.stl)")
        if filepath:
            self.project.state["lethality"]["target_stl"] = filepath
            self.btn_load_tgt_stl.setText(f"Target: {os.path.basename(filepath)}")

    def fetch_weather(self):
        self.weather_status.setText("Fetching...")
        QApplication.processEvents()
        try:
            lat = float(self.input_lat.text())
            lon = float(self.input_lon.text())
            self.current_atm = LiveWeather.fetch_atmosphere(lat, lon)
            props = self.current_atm.get_properties(0)
            self.weather_status.setText(f"Live Weather Loaded.\nTemp: {props['temperature']-273.15:.1f}C, Density: {props['density']:.3f} kg/m^3")
        except Exception as e:
            self.weather_status.setText(f"Error: {e}")
            self.current_atm = StandardAtmosphere()

    def calculate_interior(self):
        try:
            chamber_vol = float(self.input_chamber_vol.text())
            barrel_len = float(self.input_barrel_len.text())
            bore_diam = float(self.input_diam.text())
            proj_mass = float(self.input_mass.text())
            twist = float(self.input_twist.text())
            engrave = float(self.input_engrave_n.text())
            frict = float(self.input_frict_n.text())

            # Simple inertia fallback for spin calculation
            ix = 0.5 * proj_mass * (bore_diam/2)**2

            powder_name = self.combo_powder.currentText()
            charge_mass = float(self.input_charge_mass.text())
            web_thick = float(self.input_web.text())

            gun = GunSystem(
                chamber_vol, barrel_len, bore_diam, proj_mass,
                bullet_ix_kgm2=ix, twist_rate_in_per_turn=twist,
                engraving_force_n=engrave, bore_friction_n=frict
            )
            prop = Propellant(powder_name)
            charge = Charge(prop, charge_mass, web_thick)

            solver = InteriorSolver(gun, charge)
            res = solver.solve()

            if res.success:
                self.input_v0.setText(f"{res.muzzle_velocity:.1f}")
                self.input_spin.setText(f"{res.spin_rate_rads:.1f}")

                out = "--- INTERIOR BALLISTICS & BARREL ---\n"
                out += f"Propellant: {powder_name}\n"
                out += f"Muzzle Velocity: {res.muzzle_velocity:.1f} m/s\n"
                out += f"Spin Rate:       {res.spin_rate_rads:.1f} rad/s\n"
                out += f"Peak Pressure:   {res.peak_pressure / 1e6:.1f} MPa\n"
                out += f"Fraction Burned: {res.fraction_burned[-1]*100.0:.1f}%\n"
                self.text_output.setText(out)

                # Plot P-T Curve
                self.canvas_traj.reset_layout()
                self.canvas_traj.ax_side.clear()
                self.canvas_traj.ax_top.clear()

                # We will just reuse the top/side axes for interior plotting temporarily
                self.canvas_traj.ax_side.plot(res.travel_m, res.pressure_pa / 1e6, 'b-')
                self.canvas_traj.ax_side.set_title('Pressure Curve')
                self.canvas_traj.ax_side.set_xlabel('Travel (m)')
                self.canvas_traj.ax_side.set_ylabel('Pressure (MPa)')
                self.canvas_traj.ax_side.grid(True)

                self.canvas_traj.ax_top.plot(res.travel_m, res.velocity_ms, 'g-')
                self.canvas_traj.ax_top.set_title('Velocity Curve')
                self.canvas_traj.ax_top.set_xlabel('Travel (m)')
                self.canvas_traj.ax_top.set_ylabel('Velocity (m/s)')
                self.canvas_traj.ax_top.grid(True)

                self.canvas_traj.draw()
                self.tabs.setCurrentIndex(0)
            else:
                self.text_output.setText("Interior Solver Failed.")
        except Exception as e:
            self.text_output.setText(f"ERROR in Interior Ballistics: {e}")

    def calculate_solution(self):
        self.btn_calc.setText("Calculating (Please wait)...")
        self.btn_calc.setEnabled(False)
        self.text_output.setText("Running 6-DoF Optimization...")
        QApplication.processEvents()

        # Save state to memory model
        self.populate_project_from_gui()
        state = self.project.state

        try:
            # Re-read from state model
            mass = state["projectile"]["mass_kg"]
            diam = state["projectile"]["diameter_m"]
            v0 = state["projectile"]["muzzle_velocity_ms"]
            spin = state["projectile"]["spin_rate_rads"]

            # Simple inertia fallback (if STL wasn't loaded)
            ix = 0.5 * mass * (diam/2)**2
            iy = ix * 10.0

            # If STL path exists, calculate real inertia
            stl_path = state["projectile"].get("custom_stl_path", "")
            if stl_path and os.path.exists(stl_path):
                stl_proj = Projectile.from_stl(stl_path, density_kg_m3=11340.0)
                ix, iy = stl_proj.i_x, stl_proj.i_y

            mat = None
            nose_r = 0.0
            if state.get("hypersonics", {}).get("active", False):
                mat = Material(state["hypersonics"]["material"])
                nose_r = state["hypersonics"]["nose_radius_m"]
                self.canvas_traj.current_material_name = mat.name
            else:
                self.canvas_traj.current_material_name = None

            proj = Projectile(mass=mass, diameter=diam, i_x=ix, i_y=iy, material=mat, nose_radius_m=nose_r)

            if "G7" in state["projectile"]["aero_model"]:
                aero = Aerodynamics.g7()
            elif "Auto-Predicted" in state["projectile"]["aero_model"] and hasattr(self, 'custom_aero_model'):
                aero = self.custom_aero_model
            else:
                aero = Aerodynamics.g1()

            env_earth = EarthModel()

            wind = WindProfile()
            w_speed = state["environment"]["wind_speed_ms"]
            w_dir = state["environment"]["wind_direction_deg"]
            if w_speed > 0:
                wind.set_wind_layers_polar([0], [w_speed], [w_dir])

            propulsion = state.get("propulsion", None)

            solver = Solver6DoF(proj, aero, self.current_atm, env_earth, environment_wind=wind, propulsion=propulsion)
            targeting = TargetingSystem(solver)

            tx = state["target"]["x_m"]
            ty = state["target"]["y_m"]
            tz = state["target"]["z_m"]

            # Run Targeting
            res = targeting.find_firing_solution(
                [tx, ty, tz], v0, spin,
                penetration_model='demarre'
            )

            if res.success:
                out = "--- FIRING SOLUTION FOUND ---\n"
                out += f"Elevation (Pitch): {np.rad2deg(res.pitch):.3f} degrees\n"
                out += f"Azimuth (Yaw):     {np.rad2deg(res.yaw):.3f} degrees\n"
                out += f"Time of Flight:    {res.time_of_flight:.2f} seconds\n"
                out += f"Terminal Velocity: {res.terminal_velocity:.1f} m/s\n"
                out += f"Terminal Energy:   {res.terminal_energy / 1000.0:.1f} kJ\n"
                if res.penetration_mm:
                    out += f"Armor Penetration: {res.penetration_mm:.1f} mm (De Marre)\n"

                self.text_output.setText(out)
                self.canvas_traj.reset_layout()
                self.canvas_traj.plot_trajectory(res.trajectory)
                self.tabs.setCurrentIndex(0)

                # Store successful trajectory for 3D viz
                self.last_trajectory = res.trajectory
                self.btn_3d.setEnabled(True)
            else:
                self.text_output.setText(f"FAILED TO FIND SOLUTION: {res.message}")
                self.btn_3d.setEnabled(False)

        except Exception as e:
            self.text_output.setText(f"ERROR: {e}")

        finally:
            self.btn_calc.setText("Find Firing Solution")
            self.btn_calc.setEnabled(True)

    def view_3d_scene(self):
        if hasattr(self, 'last_trajectory') and self.last_trajectory is not None:
            visualize_trajectory_3d(self.last_trajectory)

    def run_lethality(self):
        self.btn_leth.setText("Running Ray-Tracer...")
        self.btn_leth.setEnabled(False)
        self.text_output.setText("Calculating Fragmentation and Intercept...")
        QApplication.processEvents()

        self.populate_project_from_gui()
        state = self.project.state

        try:
            if not state["lethality"]["target_stl"]:
                raise ValueError("A Target STL mesh must be loaded for lethality analysis.")

            # We need a firing solution first to get terminal parameters
            # Reusing the setup logic
            mass = state["projectile"]["mass_kg"]
            diam = state["projectile"]["diameter_m"]
            v0 = state["projectile"]["muzzle_velocity_ms"]
            spin = state["projectile"]["spin_rate_rads"]

            ix = 0.5 * mass * (diam/2)**2
            iy = ix * 10.0

            proj = Projectile(mass=mass, diameter=diam, i_x=ix, i_y=iy)

            if "G7" in state["projectile"]["aero_model"]:
                aero = Aerodynamics.g7()
            elif "Auto-Predicted" in state["projectile"]["aero_model"] and hasattr(self, 'custom_aero_model'):
                aero = self.custom_aero_model
            else:
                aero = Aerodynamics.g1()

            env_earth = EarthModel()

            wind = WindProfile()
            w_speed = state["environment"]["wind_speed_ms"]
            w_dir = state["environment"]["wind_direction_deg"]
            if w_speed > 0:
                wind.set_wind_layers_polar([0], [w_speed], [w_dir])

            propulsion = state.get("propulsion", None)

            from ballistics.guidance import ProportionalNavigation
            guidance = None
            if state.get("guidance", {}).get("active", False):
                g = state["guidance"]
                guidance = ProportionalNavigation(g["nav_constant"], g["max_g"], g["activation_time_s"])

            tx = state["target"]["x_m"]
            ty = state["target"]["y_m"]
            tz = state["target"]["z_m"]
            tvx = state["target"].get("vx_ms", 0.0)
            tvy = state["target"].get("vy_ms", 0.0)
            tvz = state["target"].get("vz_ms", 0.0)

            target_state = {'pos': [tx, ty, tz], 'vel': [tvx, tvy, tvz]}

            solver = Solver6DoF(proj, aero, self.current_atm, env_earth, environment_wind=wind, propulsion=propulsion, guidance=guidance, target_state=target_state)
            targeting = TargetingSystem(solver)

            res = targeting.find_firing_solution([tx, ty, tz], v0, spin)

            if not res.success:
                raise Exception(f"Failed to find intercept solution: {res.message}")

            # Now we have the intercept. Setup Lethality.
            exp_name = state["lethality"]["explosive"]
            exp_mass = state["lethality"]["explosive_mass_kg"]
            num_frags = state["lethality"]["fragments"]
            tgt_armor = state["lethality"]["target_armor_mm"]

            exp_data = Explosive(exp_name)
            metal_mass = mass - exp_mass

            if metal_mass <= 0:
                raise ValueError("Explosive mass cannot exceed total projectile mass.")

            g_vel = FragmentationModel.gurney_velocity(exp_mass, metal_mass, exp_data.gurney_constant)
            frag_props = FragmentationModel.generate_fragments(metal_mass, num_frags)
            spray_vecs = FragmentationModel.spray_vectors(num_frags, g_vel)

            tracer = LethalityRayTracer(state["lethality"]["target_stl"], [tx, ty, tz], tgt_armor)

            # terminal pos and velocity
            term_pos = res.trajectory.y[0:3, -1]
            term_vel = res.trajectory.y[3:6, -1]
            term_quat = res.trajectory.y[6:10, -1]

            leth_res = tracer.analyze_lethality(term_pos, term_vel, term_quat, frag_props["mass_kg"], frag_props["diameter_m"], spray_vecs)

            out = "--- LETHALITY ANALYSIS ---\n"
            out += f"Explosive: {exp_name} ({exp_mass}kg)\n"
            out += f"Gurney Velocity: {g_vel:.1f} m/s\n"
            out += f"Total Fragments Generated: {leth_res.total_fragments}\n"
            out += f"Fragments Hit Target: {leth_res.hit_count}\n"
            out += f"Fragments Penetrated: {leth_res.penetration_count} (> {tgt_armor}mm RHA)\n"
            self.text_output.setText(out)

            # Visualize
            self.last_lethality_result = leth_res
            import pyvista as pv
            plotter = pv.Plotter(title="Wilson Ballistic Suite - Lethality Analysis")
            plotter.add_mesh(tracer.mesh, color="gray", opacity=0.5, label="Target Mesh")
            if leth_res.hit_count > 0:
                # Plot hits
                hits_pcc = pv.PolyData(leth_res.hit_points)
                plotter.add_mesh(hits_pcc, color="yellow", point_size=10, render_points_as_spheres=True, label="Bounced")
            if leth_res.penetration_count > 0:
                pen_pcc = pv.PolyData(leth_res.penetrated_points)
                plotter.add_mesh(pen_pcc, color="red", point_size=15, render_points_as_spheres=True, label="Penetrated")

            # Plot blast origin
            plotter.add_mesh(pv.Sphere(radius=0.5, center=term_pos), color="orange", label="Detonation")
            plotter.add_axes()
            plotter.add_legend()
            plotter.show()

        except Exception as e:
            self.text_output.setText(f"ERROR in Lethality: {e}")
        finally:
            self.btn_leth.setText("Run Lethality Analysis")
            self.btn_leth.setEnabled(True)

    def run_cfd_pipeline(self):
        self.btn_run_cfd.setText("Running 3D CFD...")
        self.btn_run_cfd.setEnabled(False)
        self.text_output.setText("Voxelizing mesh and executing C++ Navier-Stokes Solver. This may take a minute...")
        QApplication.processEvents()

        try:
            self.populate_project_from_gui()
            state = self.project.state

            stl_path = state["projectile"].get("custom_stl_path", "")
            if not stl_path or not os.path.exists(stl_path):
                raise ValueError("You must load a Custom CAD (STL) file before running CFD.")

            mach = float(self.input_cfd_mach.text())
            altitude = float(self.input_cfd_alt.text())
            res_val = int(self.input_cfd_res.text())

            from ballistics.cfd_pipeline import CFDPipeline
            from ballistics.environment import StandardAtmosphere

            pipeline = CFDPipeline(stl_path, pitch_deg=0.0)

            # Run C++ Solver
            res = pipeline.run_simulation(mach, altitude, self.current_atm, grid_resolution=res_val)

            out = "--- 3D CFD ANALYSIS COMPLETE ---\n"
            out += f"Grid Dimensions: {res['pressure_slice_z'].shape}\n"
            out += f"Freestream Mach: {mach}\n"
            out += f"Calculated Drag Force: {res['drag_force']:.2f} N\n"
            out += f"Calculated Lift Force: {res['lift_force']:.2f} N\n"
            out += f"Calculated Form Cd: {res['cd']:.4f}\n"

            self.text_output.setText(out)

            # Visualize the pressure slice
            self.canvas_traj.reset_layout()
            self.canvas_traj.ax_side.clear()
            self.canvas_traj.ax_top.clear()

            self.canvas_traj.ax_side.imshow(res['pressure_slice_z'].T, cmap='jet', origin='lower')
            self.canvas_traj.ax_side.set_title(f'Midplane Pressure Slice (Mach {mach})')
            self.canvas_traj.ax_side.set_xlabel('X (voxels)')
            self.canvas_traj.ax_side.set_ylabel('Y (voxels)')

            self.canvas_traj.draw()
            self.tabs.setCurrentIndex(0)

        except Exception as e:
            self.text_output.setText(f"CFD ERROR: {e}")
        finally:
            self.btn_run_cfd.setText("Run True 3D CFD")
            self.btn_run_cfd.setEnabled(True)

    def run_monte_carlo(self):
        self.btn_mc.setText("Running Monte Carlo...")
        self.btn_mc.setEnabled(False)
        self.text_output.setText("Running Monte Carlo (Parallel Processing)...")
        QApplication.processEvents()

        self.populate_project_from_gui()
        state = self.project.state

        try:
            # 1. Build Base Solver
            mass = state["projectile"]["mass_kg"]
            diam = state["projectile"]["diameter_m"]
            v0 = state["projectile"]["muzzle_velocity_ms"]
            spin = state["projectile"]["spin_rate_rads"]

            ix = 0.5 * mass * (diam/2)**2
            iy = ix * 10.0

            stl_path = state["projectile"].get("custom_stl_path", "")
            if stl_path and os.path.exists(stl_path):
                stl_proj = Projectile.from_stl(stl_path, density_kg_m3=11340.0)
                ix, iy = stl_proj.i_x, stl_proj.i_y

            proj = Projectile(mass=mass, diameter=diam, i_x=ix, i_y=iy)
            aero = Aerodynamics.g7() if "G7" in state["projectile"]["aero_model"] else Aerodynamics.g1()
            env_earth = EarthModel()

            wind = WindProfile()
            w_speed = state["environment"]["wind_speed_ms"]
            w_dir = state["environment"]["wind_direction_deg"]
            if w_speed > 0:
                wind.set_wind_layers_polar([0], [w_speed], [w_dir])

            propulsion = state.get("propulsion", None)

            from ballistics.guidance import ProportionalNavigation
            guidance = None
            if state.get("guidance", {}).get("active", False):
                g = state["guidance"]
                guidance = ProportionalNavigation(g["nav_constant"], g["max_g"], g["activation_time_s"])

            tx = state["target"]["x_m"]
            ty = state["target"]["y_m"]
            tz = state["target"]["z_m"]
            tvx = state["target"].get("vx_ms", 0.0)
            tvy = state["target"].get("vy_ms", 0.0)
            tvz = state["target"].get("vz_ms", 0.0)

            target_state = {'pos': [tx, ty, tz], 'vel': [tvx, tvy, tvz]}

            solver = Solver6DoF(proj, aero, self.current_atm, env_earth, environment_wind=wind, propulsion=propulsion, guidance=guidance, target_state=target_state)

            # Base angles (we assume 0 pitch and yaw to measure raw dispersion from a fixed mount,
            # or the user can manually enter values if they want. For simplicity, we center around 0)
            base_pitch = 0.0
            base_yaw = 0.0

            mc = MonteCarloSimulator(solver)

            shots = state["dispersion"]["shots"]
            plane = state["dispersion"]["plane"]
            target_dist = state["target"]["x_m"]

            res = mc.run(
                num_shots=shots,
                target_plane=plane,
                target_distance=target_dist,
                base_v0=v0,
                base_pitch_rad=base_pitch,
                base_yaw_rad=base_yaw,
                base_spin_rads=spin,
                sd_v0_ms=state["dispersion"]["v0_sd_ms"],
                sd_mass_kg=state["dispersion"]["mass_sd_kg"],
                sd_wind_speed_ms=state["dispersion"]["wind_speed_sd_ms"],
                sd_pitch_rad=np.deg2rad(state["dispersion"]["pitch_sd_deg"]),
                sd_yaw_rad=np.deg2rad(state["dispersion"]["yaw_sd_deg"])
            )

            out = f"--- MONTE CARLO RESULTS ({plane.upper()} PLANE) ---\n"
            out += res.message + "\n"
            out += f"Mean Point of Impact: [{res.mpi[0]:.2f}m, {res.mpi[1]:.2f}m]\n"
            out += f"CEP50 (50% Hit Radius): {res.cep_50:.2f} meters\n"

            self.text_output.setText(out)

            if len(res.impacts) > 0:
                self.canvas_disp.plot_dispersion(res)
                self.tabs.setCurrentIndex(1)

        except Exception as e:
            self.text_output.setText(f"ERROR in Monte Carlo: {e}")
        finally:
            self.btn_mc.setText("Run Monte Carlo")
            self.btn_mc.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BallisticsGUI()
    window.show()
    sys.exit(app.exec())
