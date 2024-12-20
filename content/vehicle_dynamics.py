import streamlit as st
import math
import config
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
from content.velocity_profile import (
    velocity_profile,
    distance_profile,
    tractive_power_profile
)
from constants import AIR_DENSITY, GRAVITY, C_DRAG


def vehicle_dynamics():
    st.title("Vehicle Dynamics")

    # --- User Inputs ---
    st.sidebar.header("Vehicle Parameters")
    debug_mode = st.sidebar.checkbox("Debug Mode", value=False)
    formula_mode = st.sidebar.checkbox("Show Formulas", value=True)

    # Vehicle Inputs
    config.mass = st.sidebar.number_input("Vehicle Mass (kg)", min_value=500, max_value=5000, value=2570)
    config.top_speed = st.sidebar.number_input("Top Speed (km/h)", min_value=50, max_value=400, value=100)
    config.time_to_100 = st.sidebar.number_input("Time to 100 km/h (s)", min_value=1.0, max_value=30.0, value=12.0, step=0.1)
    config.km = st.sidebar.number_input("Rotational Inertia Coefficient (k_m)", min_value=1.0, max_value=1.2, value=1.1,
                                        step=0.01)
    config.current_road_angle = st.sidebar.number_input("Current Road Angle (degrees)", min_value=0.0, max_value=45.0,
                                                        value=5.0)
    config.vehicle_height = st.sidebar.number_input("Vehicle Height (m)", min_value=1.0, max_value=3.0, value=3.0)
    config.vehicle_width = st.sidebar.number_input("Vehicle Width (m)", min_value=1.0, max_value=3.0, value=2.5)
    config.headwind_speed = st.sidebar.number_input("Headwind Speed (km/h)", min_value=0, max_value=100, value=20)
    config.wheel_radius = st.sidebar.number_input("Wheel Radius (m)", min_value=0.1, max_value=1.0, value=0.3, step=0.01)
    config.gradeability_percent = st.sidebar.number_input("Gradeability (%)", min_value=0.0, max_value=100.0, value=25.0)
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
    config.road_load_force = calculate_road_load_force(config.rolling_force, config.gravitational_force, config.drag_force)
    config.traction_force = calculate_traction_force(config.road_load_force, config.mass, config.acceleration, config.km)
    config.power_required = calculate_power_required(config.traction_force, config.top_speed_mps)
    config.required_tractive_force_near_zero = calculate_required_tractive_force_near_zero(config.mass,
                                                                                           config.gradeability_percent)

    # Constants
    config.k1 = calculate_k1(config.traction_force, config.mass, GRAVITY, config.C0)
    config.k2 = calculate_k2(AIR_DENSITY, C_DRAG, config.frontal_area, config.mass, GRAVITY, config.C1)

    # Terminal Velocity and Time to Reach
    config.terminal_velocity = calculate_terminal_velocity(config.k1, config.k2)
    config.time_to_vt = calculate_time_to_terminal_velocity(config.k1, config.k2, config.terminal_velocity)



# --- Results Display ---
    st.header("Calculation Results")
    st.subheader("1. Rolling Resistance Force")
    if formula_mode:
        st.latex(
            r"F_{\text{roll}} = \text{sgn}(v_{xT}) \cdot m \cdot g \cdot \cos(\theta) \cdot \left( C_0 + C_1 v_{xT}^2 \right)")
    st.success(f"Rolling Resistance Force: **{config.rolling_force / 1000:.2f} kN**")
    if debug_mode:
        st.write(f" - Static Coefficient (C0): {config.C0}")
        st.write(f" - Speed-dependent Coefficient (C1): {C1}")
        st.write(f" - Vehicle Mass (m): {config.mass} kg")
        st.write(f" - Gravity (g): {GRAVITY} m/s²")
        st.write(f" - Speed Squared (v_xT²): {config.top_speed_mps ** 2:.2f} (m/s)²")
        st.write(f" - Angle Cosine: {math.cos(config.road_angle_rad):.4f}")

    st.subheader("2. Gravitational Force Along the Road Surface")
    if formula_mode:
        st.latex(r"F_{gravity} = m \cdot g \cdot \sin(\theta)")
    st.success(f"Gravitational Force: **{config.gravitational_force / 1000:.2f} kN**")
    if debug_mode:
        st.write(f" - Vehicle Mass (m): {config.mass} kg")
        st.write(f" - Gravity (g): {GRAVITY} m/s²")
        st.write(f" - Angle (radians): {config.road_angle_rad:.4f}")
        st.write(f" - Angle Sine: {math.sin(config.road_angle_rad):.4f}")

    st.subheader("3. Aerodynamic Drag Force (Including Headwind)")
    if formula_mode:
        st.latex(
            r"F_{drag} = \text{SIGN}(v_{\text{relative}}) \cdot \frac{1}{2} \cdot \rho \cdot C_d \cdot A \cdot v_{\text{relative}}^2")
    st.success(f"Aerodynamic Drag Force: **{config.drag_force / 1000:.2f} kN**")
    if debug_mode:
        st.write(f" - Air Density (ρ): {AIR_DENSITY} kg/m³")
        st.write(f" - Drag Coefficient (C_d): {C_DRAG}")
        st.write(f" - Frontal Area (A): {config.frontal_area:.2f} m²")
        st.write(f" - Relative Speed (v_relative): {config.relative_speed:.2f} m/s")
        st.write(f" - Headwind Speed: {config.headwind_speed} km/h")

    st.subheader("4. Total Road Load Force")
    if formula_mode:
        st.latex(r"F_{RL} = F_{roll} + F_{gravity} + F_{drag}")
    st.success(f"Total Road Load Force: **{config.road_load_force / 1000:.2f} kN**")
    if debug_mode:
        st.write(f" - Rolling Resistance Force: {config.rolling_force:.2f} N")
        st.write(f" - Gravitational Force: {config.gravitational_force:.2f} N")
        st.write(f" - Aerodynamic Drag Force: {config.drag_force:.2f} N")

    st.subheader("5. Required Traction Force")
    if formula_mode:
        st.latex(r"F_{TR} = F_{\text{RL}} + k_m \cdot m \cdot a")
    st.success(f"Traction Force: **{config.traction_force / 1000:.2f} kN**")
    if debug_mode:
        st.write(f" - Road Load Force (F_RL): {config.road_load_force:.2f} N")
        st.write(f" - Rotational Inertia Coefficient (k_m): {km}")
        st.write(f" - Vehicle Mass (m): {config.mass} kg")
        st.write(f" - Time to 100 km/h: {config.time_to_100:.2f} s")
        st.write(f" - Calculated Acceleration (a): {config.acceleration:.2f} m/s²")

    st.subheader("6. Required Propulsion Power")
    if formula_mode:
        st.latex(r"\text{Power} = F_{TR} \cdot V")
    st.success(f"Required Power: **{config.power_required / 1000:.2f} kW**")
    if debug_mode:
        st.write(f" - Traction Force (F_TR): {config.traction_force:.2f} N")
        st.write(f" - Vehicle Speed (v_xT): {config.top_speed_mps:.2f} m/s")

    st.subheader("7. Required Maximum Traction Force for Gradeability")
    if formula_mode:
        st.latex(r"F_{\text{TR}} = \frac{m \cdot g \cdot \tan(\beta)}{\sqrt{1 + \tan^2(\beta)}}")
    st.success(f"Required Tractive Force: **{config.required_tractive_force_near_zero / 1000:.2f} kN**")
    if debug_mode:
        st.write(f" - Vehicle Mass (m): {config.mass} kg")
        st.write(f" - Gravitational Acceleration (g): {GRAVITY} m/s²")
        st.write(
            f" - Input Gradeability: {config.gradeability_percent:.2f} % -> {math.degrees(math.atan(config.gradeability_percent / 100)):.2f}° -> {math.atan(config.gradeability_percent / 100):.2f} rad")

    # --- K1 Calculation ---
    st.subheader("8: K1 Constant")
    if formula_mode:
        st.latex(r"K_1 = \frac{F_{\text{TR}}}{m} - gC_0")
    st.success(f"K1: **{config.k1:.5f}**")
    if debug_mode:
        st.write("### Debug Information for K1")
        st.write(f" - Traction Force (F_TR): {config.traction_force:.2f} N")
        st.write(f" - Vehicle Mass (m): {config.mass} kg")
        st.write(f" - Gravity (g): {GRAVITY} m/s²")
        st.write(f" - Rolling Resistance Coefficient (C0): {config.C0}")

    # --- K2 Calculation ---
    st.subheader("9: K2 Constant")
    if formula_mode:
        st.latex(r"K_2 = \frac{\rho C_D A_F}{2m} + gC_1")
    st.success(f"K2: **{config.k2:.5f}**")
    if debug_mode:
        st.write("### Debug Information for K2")
        st.write(f" - Air Density (ρ): {AIR_DENSITY} kg/m³")
        st.write(f" - Drag Coefficient (C_D): {C_DRAG}")
        st.write(f" - Frontal Area (A_F): {config.frontal_area:.2f} m²")
        st.write(f" - Vehicle Mass (m): {config.mass} kg")
        st.write(f" - Gravity (g): {GRAVITY} m/s²")
        st.write(f" - Speed-dependent Rolling Resistance Coefficient (C1): {config.C1}")

    st.subheader("10: Velocity-Time Profile")
    velocity_profile(debug_mode, config.k1, config.k2)

    st.subheader("11. Terminal Velocity")
    if formula_mode:
        st.latex(r"V_T = \sqrt{\frac{K_1}{K_2}}")
    st.success(f"Terminal Velocity (V_T): **{config.terminal_velocity * 3.6:.2f} km/h**")  # Convert m/s to km/h
    st.write("#### Time to Reach 98% of Terminal Velocity")
    st.latex(r"t_{V_T} = \frac{2.3}{\sqrt{K_1 K_2}}")
    st.success(f"Time to reach 98% of terminal velocity: **{config.time_to_vt:.2f} seconds**")

    if debug_mode:
        st.write("### Debug Information for Terminal Velocity")
        st.write(f" - K1: {config.k1:.5f}")
        st.write(f" - K2: {config.k2:.5f}")
        st.write(f" - Terminal Velocity (V_T): {config.terminal_velocity:.2f} m/s or {config.terminal_velocity * 3.6:.2f} km/h")

    st.subheader("12. Distance-Time Profile")
    distance_profile(debug_mode, config.k2, config.terminal_velocity)

    st.subheader("13. Tractive Power Profile")
    tractive_power_profile(debug_mode, config.traction_force, config.terminal_velocity, config.k1, config.k2, config.time_to_vt)
