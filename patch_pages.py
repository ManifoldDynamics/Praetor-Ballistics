with open('gui.py', 'r') as f:
    content = f.read()

# Find build_aero_predictor
idx = content.find("def build_aero_predictor(self):")
new_methods = """
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

        self.stacked_widget.addWidget(widget) # Index 1

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
        self.stacked_widget.addWidget(widget) # Index 2

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
        self.stacked_widget.addWidget(widget) # Index 3

"""

with open('gui.py', 'w') as f:
    f.write(content[:idx] + new_methods + content[idx:])
