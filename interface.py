import streamlit as st
import config
import math
from config import AIR_DENSITY, GRAVITY, C_DRAG
from calculations import (
    calculate_rolling_resistance_force,
    calculate_gravitational_force,
    calculate_aerodynamic_drag_force,
    calculate_road_load_force,
    calculate_traction_force,
    calculate_power_required,
    calculate_required_tractive_force_near_zero,
    calculate_k1,
    calculate_k2,
    calculate_terminal_velocity,
    calculate_time_to_terminal_velocity
)


def sidebar_calculations():
    # --- User Inputs ---
    st.sidebar.header("Vehicle Parameters")
    config.debug_mode = st.sidebar.checkbox("Debug Mode", value=False)
    config.formula_mode = st.sidebar.checkbox("Show Formulas", value=True)

    # Vehicle Inputs
    config.mass = st.sidebar.number_input("Vehicle Mass (kg)", min_value=500, max_value=5000, value=2570)
    config.top_speed = st.sidebar.number_input("Top Speed (km/h)", min_value=50, max_value=400, value=100)
    config.time_to_100 = st.sidebar.number_input("Time to 100 km/h (s)", min_value=1.0, max_value=30.0, value=12.0,
                                                 step=0.1)
    config.km = st.sidebar.number_input("Rotational Inertia Coefficient (k_m)", min_value=1.0, max_value=1.2, value=1.1,
                                        step=0.01)
    config.current_road_angle = st.sidebar.number_input("Current Road Angle (degrees)", min_value=0.0, max_value=45.0,
                                                        value=5.0)
    config.vehicle_height = st.sidebar.number_input("Vehicle Height (m)", min_value=1.0, max_value=3.0, value=3.0)
    config.vehicle_width = st.sidebar.number_input("Vehicle Width (m)", min_value=1.0, max_value=3.0, value=2.5)
    config.headwind_speed = st.sidebar.number_input("Headwind Speed (km/h)", min_value=0, max_value=100, value=20)
    config.wheel_radius = st.sidebar.number_input("Wheel Radius (m)", min_value=0.1, max_value=1.0, value=0.3,
                                                  step=0.01)
    config.gradeability_percent = st.sidebar.number_input("Gradeability (%)", min_value=0.0, max_value=100.0,
                                                          value=25.0)
    config.C0 = st.sidebar.number_input("Static Rolling Resistance Coefficient (C0)", min_value=0.005, max_value=0.05,
                                        value=0.008, step=0.001, format="%.3f")
    config.C1 = st.sidebar.number_input("Speed-dependent Coefficient (C1)", min_value=0.0, max_value=0.00001,
                                        value=0.0000016, step=0.000001, format="%.7f")

    # Convert Units
    config.top_speed_mps = config.top_speed / 3.6
    config.headwind_speed_mps = config.headwind_speed / 3.6
    config.relative_speed = config.top_speed_mps + config.headwind_speed_mps
    config.road_angle_rad = math.radians(config.current_road_angle)
    config.frontal_area = config.vehicle_height * config.vehicle_width
    config.acceleration = (27.78 / config.time_to_100)  # 100 km/h in m/s

    # Calculations
    config.rolling_force = calculate_rolling_resistance_force(config.mass, config.road_angle_rad, config.top_speed_mps,
                                                              config.C0, config.C1)
    config.gravitational_force = calculate_gravitational_force(config.mass, config.road_angle_rad)
    config.drag_force = calculate_aerodynamic_drag_force(config.relative_speed, config.frontal_area)
    config.road_load_force = calculate_road_load_force(config.rolling_force, config.gravitational_force,
                                                       config.drag_force)
    config.traction_force = calculate_traction_force(config.road_load_force, config.mass, config.acceleration,
                                                     config.km)
    config.power_required = calculate_power_required(config.traction_force, config.top_speed_mps)
    config.required_tractive_force_near_zero = calculate_required_tractive_force_near_zero(config.mass,
                                                                                           config.gradeability_percent)

    # Constants
    config.k1 = calculate_k1(config.traction_force, config.mass, GRAVITY, config.C0)
    config.k2 = calculate_k2(AIR_DENSITY, C_DRAG, config.frontal_area, config.mass, GRAVITY, config.C1)

    # Terminal Velocity and Time to Reach
    config.terminal_velocity = calculate_terminal_velocity(config.k1, config.k2)
    config.time_to_vt = calculate_time_to_terminal_velocity(config.k1, config.k2, config.terminal_velocity)
