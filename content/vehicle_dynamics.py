import streamlit as st
import math
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
    calculate_terminal_velocity
)
from content.velocity_profile import velocity_profile
from constants import AIR_DENSITY, GRAVITY, C_DRAG


def vehicle_dynamics():
    st.title("Vehicle Dynamics")

    # --- User Inputs ---
    st.sidebar.header("Vehicle Parameters")
    debug_mode = st.sidebar.checkbox("Debug Mode", value=False)
    formula_mode = st.sidebar.checkbox("Show Formulas", value=True)

    # Vehicle Inputs
    mass = st.sidebar.number_input("Vehicle Mass (kg)", min_value=500, max_value=5000, value=2570)
    top_speed = st.sidebar.number_input("Top Speed (km/h)", min_value=50, max_value=400, value=100)
    time_to_100 = st.sidebar.number_input("Time to 100 km/h (s)", min_value=1.0, max_value=30.0, value=12.0, step=0.1)
    km = st.sidebar.number_input("Rotational Inertia Coefficient (k_m)", min_value=1.0, max_value=1.2, value=1.1,
                                 step=0.01)
    current_road_angle = st.sidebar.number_input("Current Road Angle (degrees)", min_value=0.0, max_value=45.0,
                                                 value=5.0)
    vehicle_height = st.sidebar.number_input("Vehicle Height (m)", min_value=1.0, max_value=3.0, value=3.0)
    vehicle_width = st.sidebar.number_input("Vehicle Width (m)", min_value=1.0, max_value=3.0, value=2.5)
    headwind_speed = st.sidebar.number_input("Headwind Speed (km/h)", min_value=0, max_value=100, value=20)
    wheel_radius = st.sidebar.number_input("Wheel Radius (m)", min_value=0.1, max_value=1.0, value=0.3, step=0.01)
    gradeability_percent = st.sidebar.number_input("Gradeability (%)", min_value=0.0, max_value=100.0, value=25.0)
    C0 = st.sidebar.number_input("Static Rolling Resistance Coefficient (C0)", min_value=0.005, max_value=0.05,
                                 value=0.008, step=0.001, format="%.3f")
    C1 = st.sidebar.number_input("Speed-dependent Coefficient (C1)", min_value=0.0, max_value=0.00001, value=0.0000016,
                                 step=0.000001, format="%.7f")

    # Convert Units
    top_speed_mps = top_speed / 3.6
    headwind_speed_mps = headwind_speed / 3.6
    relative_speed = top_speed_mps + headwind_speed_mps
    road_angle_rad = math.radians(current_road_angle)
    frontal_area = vehicle_height * vehicle_width
    acceleration = (27.78 / time_to_100)  # 100 km/h in m/s

    # --- Calculations ---
    rolling_force = calculate_rolling_resistance_force(mass, road_angle_rad, top_speed_mps, C0, C1)
    gravitational_force = calculate_gravitational_force(mass, road_angle_rad)
    drag_force = calculate_aerodynamic_drag_force(relative_speed, frontal_area)
    road_load_force = calculate_road_load_force(rolling_force, gravitational_force, drag_force)
    traction_force = calculate_traction_force(road_load_force, mass, acceleration, km)
    power_required = calculate_power_required(traction_force, top_speed_mps)
    required_tractive_force_near_zero = calculate_required_tractive_force_near_zero(mass, gradeability_percent)
    k1 = calculate_k1(traction_force, mass, GRAVITY, C0)
    k2 = calculate_k2(AIR_DENSITY, C_DRAG, frontal_area, mass, GRAVITY, C1)
    terminal_velocity = calculate_terminal_velocity(k1, k2)

    # --- Results Display ---
    st.header("Calculation Results")
    st.subheader("1. Rolling Resistance Force")
    if formula_mode:
        st.latex(
            r"F_{\text{roll}} = \text{sgn}(v_{xT}) \cdot m \cdot g \cdot \cos(\theta) \cdot \left( C_0 + C_1 v_{xT}^2 \right)")
    st.success(f"Rolling Resistance Force: **{rolling_force / 1000:.2f} kN**")
    if debug_mode:
        st.write(f" - Static Coefficient (C0): {C0}")
        st.write(f" - Speed-dependent Coefficient (C1): {C1}")
        st.write(f" - Vehicle Mass (m): {mass} kg")
        st.write(f" - Gravity (g): {GRAVITY} m/s²")
        st.write(f" - Speed Squared (v_xT²): {top_speed_mps ** 2:.2f} (m/s)²")
        st.write(f" - Angle Cosine: {math.cos(road_angle_rad):.4f}")

    st.subheader("2. Gravitational Force Along the Road Surface")
    if formula_mode:
        st.latex(r"F_{gravity} = m \cdot g \cdot \sin(\theta)")
    st.success(f"Gravitational Force: **{gravitational_force / 1000:.2f} kN**")
    if debug_mode:
        st.write(f" - Vehicle Mass (m): {mass} kg")
        st.write(f" - Gravity (g): {GRAVITY} m/s²")
        st.write(f" - Angle (radians): {road_angle_rad:.4f}")
        st.write(f" - Angle Sine: {math.sin(road_angle_rad):.4f}")

    st.subheader("3. Aerodynamic Drag Force (Including Headwind)")
    if formula_mode:
        st.latex(
            r"F_{drag} = \text{SIGN}(v_{\text{relative}}) \cdot \frac{1}{2} \cdot \rho \cdot C_d \cdot A \cdot v_{\text{relative}}^2")
    st.success(f"Aerodynamic Drag Force: **{drag_force / 1000:.2f} kN**")
    if debug_mode:
        st.write(f" - Air Density (ρ): {AIR_DENSITY} kg/m³")
        st.write(f" - Drag Coefficient (C_d): {C_DRAG}")
        st.write(f" - Frontal Area (A): {frontal_area:.2f} m²")
        st.write(f" - Relative Speed (v_relative): {relative_speed:.2f} m/s")
        st.write(f" - Headwind Speed: {headwind_speed} km/h")

    st.subheader("4. Total Road Load Force")
    if formula_mode:
        st.latex(r"F_{RL} = F_{roll} + F_{gravity} + F_{drag}")
    st.success(f"Total Road Load Force: **{road_load_force / 1000:.2f} kN**")
    if debug_mode:
        st.write(f" - Rolling Resistance Force: {rolling_force:.2f} N")
        st.write(f" - Gravitational Force: {gravitational_force:.2f} N")
        st.write(f" - Aerodynamic Drag Force: {drag_force:.2f} N")

    st.subheader("5. Required Traction Force")
    if formula_mode:
        st.latex(r"F_{TR} = F_{\text{RL}} + k_m \cdot m \cdot a")
    st.success(f"Traction Force: **{traction_force / 1000:.2f} kN**")
    if debug_mode:
        st.write(f" - Road Load Force (F_RL): {road_load_force:.2f} N")
        st.write(f" - Rotational Inertia Coefficient (k_m): {km}")
        st.write(f" - Vehicle Mass (m): {mass} kg")
        st.write(f" - Time to 100 km/h: {time_to_100:.2f} s")
        st.write(f" - Calculated Acceleration (a): {acceleration:.2f} m/s²")

    st.subheader("6. Required Propulsion Power")
    if formula_mode:
        st.latex(r"\text{Power} = F_{TR} \cdot v_{xT}")
    st.success(f"Required Power: **{power_required / 1000:.2f} kW**")
    if debug_mode:
        st.write(f" - Traction Force (F_TR): {traction_force:.2f} N")
        st.write(f" - Vehicle Speed (v_xT): {top_speed_mps:.2f} m/s")

    st.subheader("7. Required Maximum Traction Force for Gradeability")
    if formula_mode:
        st.latex(r"F_{\text{TR}} = \frac{m \cdot g \cdot \tan(\beta)}{\sqrt{1 + \tan^2(\beta)}}")
    st.success(f"Required Tractive Force: **{required_tractive_force_near_zero / 1000:.2f} kN**")
    if debug_mode:
        st.write(f" - Vehicle Mass (m): {mass} kg")
        st.write(f" - Gravitational Acceleration (g): {GRAVITY} m/s²")
        st.write(
            f" - Input Gradeability: {gradeability_percent:.2f} % -> {math.degrees(math.atan(gradeability_percent / 100)):.2f}° -> {math.atan(gradeability_percent / 100):.2f} rad")

    # --- K1 Calculation ---
    st.subheader("8: K1 Constant")
    if formula_mode:
        st.latex(r"K_1 = \frac{F_{\text{TR}}}{m} - gC_0")
    st.success(f"K1: **{k1:.5f}**")
    if debug_mode:
        st.write("### Debug Information for K1")
        st.write(f" - Traction Force (F_TR): {traction_force:.2f} N")
        st.write(f" - Vehicle Mass (m): {mass} kg")
        st.write(f" - Gravity (g): {GRAVITY} m/s²")
        st.write(f" - Rolling Resistance Coefficient (C0): {C0}")

    # --- K2 Calculation ---
    st.subheader("9: K2 Constant")
    if formula_mode:
        st.latex(r"K_2 = \frac{\rho C_D A_F}{2m} + gC_1")
    st.success(f"K2: **{k2:.5f}**")
    if debug_mode:
        st.write("### Debug Information for K2")
        st.write(f" - Air Density (ρ): {AIR_DENSITY} kg/m³")
        st.write(f" - Drag Coefficient (C_D): {C_DRAG}")
        st.write(f" - Frontal Area (A_F): {frontal_area:.2f} m²")
        st.write(f" - Vehicle Mass (m): {mass} kg")
        st.write(f" - Gravity (g): {GRAVITY} m/s²")
        st.write(f" - Speed-dependent Rolling Resistance Coefficient (C1): {C1}")

    st.subheader("10: Velocity-Time Profile")
    velocity_profile(debug_mode, k1, k2)

    st.subheader("11. Terminal Velocity")
    if formula_mode:
        st.latex(r"V_T = \sqrt{\frac{K_1}{K_2}}")
    st.success(f"Terminal Velocity (V_T): **{terminal_velocity * 3.6:.2f} km/h**")  # Convert m/s to km/h

    if debug_mode:
        st.write("### Debug Information for Terminal Velocity")
        st.write(f" - K1: {k1:.5f}")
        st.write(f" - K2: {k2:.5f}")
        st.write(f" - Terminal Velocity (V_T): {terminal_velocity:.2f} m/s or {terminal_velocity * 3.6:.2f} km/h")
