import numpy as np
from ballistics.environment import StandardAtmosphere, EarthModel
from ballistics.weather import LiveWeather
from ballistics.projectile import Projectile, Aerodynamics
from ballistics.solver import Solver6DoF

def run_weather_comparison():
    print("--- Fetching Live Weather for Leadville, Colorado (High Altitude) ---")
    # Leadville is high altitude (approx 3094m) so pressure should be low
    lat, lon = 39.2508, -106.2925

    try:
        env_atm_live = LiveWeather.fetch_atmosphere(latitude=lat, longitude=lon)
        print(f"Live Temp: {env_atm_live.T0 - 273.15:.1f} °C")
        print(f"Live Pressure: {env_atm_live.P0 / 100.0:.1f} hPa")
        print(f"Live Humidity: {env_atm_live.RH * 100.0:.1f} %")
        props_live = env_atm_live.get_properties(0)
        print(f"Calculated Surface Air Density: {props_live['density']:.3f} kg/m^3")
    except Exception as e:
        print(f"Could not fetch weather: {e}")
        return

    env_atm_std = StandardAtmosphere()
    props_std = env_atm_std.get_properties(0)
    print(f"\nStandard Sea-Level Air Density: {props_std['density']:.3f} kg/m^3")

    # Run simulation
    env_earth = EarthModel()
    proj = Projectile(mass=43.0, diameter=0.155, i_x=0.15, i_y=1.6)
    aero = Aerodynamics.g7()

    t_span = (0, 300)
    pos0 = [0, 0, 0]
    v0 = 800.0
    pitch0 = np.deg2rad(15.0)
    yaw0 = 0.0
    spin = 300.0 * 2 * np.pi

    print("\nSimulating Standard Sea Level...")
    solver_std = Solver6DoF(proj, aero, env_atm_std, env_earth)
    sol_std = solver_std.solve(t_span, pos0, v0, pitch0, yaw0, spin, max_step=1.0)
    print(f"Impact Range (Standard): {sol_std.y[0, -1]:.2f} m")

    print("\nSimulating Live Leadville Weather...")
    solver_live = Solver6DoF(proj, aero, env_atm_live, env_earth)
    sol_live = solver_live.solve(t_span, pos0, v0, pitch0, yaw0, spin, max_step=1.0)
    print(f"Impact Range (Live Leadville): {sol_live.y[0, -1]:.2f} m")

    diff = sol_live.y[0, -1] - sol_std.y[0, -1]
    print(f"\n-> High altitude / live weather resulted in {diff:+.2f} m difference in range.")

if __name__ == "__main__":
    run_weather_comparison()
