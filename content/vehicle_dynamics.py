import streamlit as st
import math
from config import AIR_DENSITY, GRAVITY, C_DRAG
import config
from content.velocity_profile import (
    velocity_profile,
    distance_profile,
    tractive_power_profile
)


def vehicle_dynamics():
    st.title("Vehicle Dynamics")

    # --- Results Display ---
    st.header("Calculation Results")
    st.subheader("1. Rolling Resistance Force")
    if config.formula_mode:
        st.latex(
            r"F_{\text{roll}} = \text{sgn}(v_{xT}) \cdot m \cdot g \cdot \cos(\theta) \cdot \left( C_0 + C_1 v_{xT}^2 \right)")
    st.success(f"Rolling Resistance Force: **{config.rolling_force / 1000:.2f} kN**")
    if config.debug_mode:
        st.write(f" - Static Coefficient (C0): {config.C0}")
        st.write(f" - Speed-dependent Coefficient (C1): {config.C1}")
        st.write(f" - Vehicle Mass (m): {config.mass} kg")
        st.write(f" - Gravity (g): {GRAVITY} m/s²")
        st.write(f" - Speed Squared (v_xT²): {config.top_speed_mps ** 2:.2f} (m/s)²")
        st.write(f" - Angle Cosine: {math.cos(config.road_angle_rad):.4f}")

    st.subheader("2. Gravitational Force Along the Road Surface")
    if config.formula_mode:
        st.latex(r"F_{gravity} = m \cdot g \cdot \sin(\theta)")
    st.success(f"Gravitational Force: **{config.gravitational_force / 1000:.2f} kN**")
    if config.debug_mode:
        st.write(f" - Vehicle Mass (m): {config.mass} kg")
        st.write(f" - Gravity (g): {GRAVITY} m/s²")
        st.write(f" - Angle (radians): {config.road_angle_rad:.4f}")
        st.write(f" - Angle Sine: {math.sin(config.road_angle_rad):.4f}")

    st.subheader("3. Aerodynamic Drag Force (Including Headwind)")
    if config.formula_mode:
        st.latex(
            r"F_{drag} = \text{SIGN}(v_{\text{relative}}) \cdot \frac{1}{2} \cdot \rho \cdot C_d \cdot A \cdot v_{\text{relative}}^2")
    st.success(f"Aerodynamic Drag Force: **{config.drag_force / 1000:.2f} kN**")
    if config.debug_mode:
        st.write(f" - Air Density (ρ): {AIR_DENSITY} kg/m³")
        st.write(f" - Drag Coefficient (C_d): {C_DRAG}")
        st.write(f" - Frontal Area (A): {config.frontal_area:.2f} m²")
        st.write(f" - Relative Speed (v_relative): {config.relative_speed:.2f} m/s")
        st.write(f" - Headwind Speed: {config.headwind_speed} km/h")

    st.subheader("4. Total Road Load Force")
    if config.formula_mode:
        st.latex(r"F_{RL} = F_{roll} + F_{gravity} + F_{drag}")
    st.success(f"Total Road Load Force: **{config.road_load_force / 1000:.2f} kN**")
    if config.debug_mode:
        st.write(f" - Rolling Resistance Force: {config.rolling_force:.2f} N")
        st.write(f" - Gravitational Force: {config.gravitational_force:.2f} N")
        st.write(f" - Aerodynamic Drag Force: {config.drag_force:.2f} N")

    st.subheader("5. Required Traction Force")
    if config.formula_mode:
        st.latex(r"F_{TR} = F_{\text{RL}} + k_m \cdot m \cdot a")
    st.success(f"Traction Force: **{config.traction_force / 1000:.2f} kN**")
    if config.debug_mode:
        st.write(f" - Road Load Force (F_RL): {config.road_load_force:.2f} N")
        st.write(f" - Rotational Inertia Coefficient (k_m): {config.km}")
        st.write(f" - Vehicle Mass (m): {config.mass} kg")
        st.write(f" - Time to 100 km/h: {config.time_to_100:.2f} s")
        st.write(f" - Calculated Acceleration (a): {config.current_acceleration:.2f} m/s²")

    st.subheader("6. Required Propulsion Power")
    if config.formula_mode:
        st.latex(r"\text{Power} = F_{TR} \cdot V")
    st.success(f"Required Power: **{config.power_required / 1000:.2f} kW**")
    if config.debug_mode:
        st.write(f" - Traction Force (F_TR): {config.traction_force:.2f} N")
        st.write(f" - Vehicle Speed (v_xT): {config.top_speed_mps:.2f} m/s")

    st.subheader("7. Required Torque for the Wheels")
    if config.formula_mode:
        st.latex(r"\text{Torque} = \frac{\text{Power}}{\omega}")
    st.success(f"Required Torque: **{config.torque_required:.2f} Nm**")
    if config.debug_mode:
        st.write(f" - Required Power: {config.power_required:.2f} W")
        st.write(f" - Angular Velocity (ω): {config.angular_velocity:.2f} rad/s")

    st.subheader("8. Required Maximum Traction Force for Gradeability")
    if config.formula_mode:
        st.latex(r"F_{\text{TR}} = \frac{m \cdot g \cdot \tan(\beta)}{\sqrt{1 + \tan^2(\beta)}}")
    st.success(f"Required Tractive Force: **{config.required_tractive_force_near_zero / 1000:.2f} kN**")
    if config.debug_mode:
        st.write(f" - Vehicle Mass (m): {config.mass} kg")
        st.write(f" - Gravitational Acceleration (g): {GRAVITY} m/s²")
        st.write(
            f" - Input Gradeability: {config.gradeability_percent:.2f} % -> {math.degrees(math.atan(config.gradeability_percent / 100)):.2f}° -> {math.atan(config.gradeability_percent / 100):.2f} rad")

    # --- K1 Calculation ---
    st.subheader("9: K1 Constant")
    if config.formula_mode:
        st.latex(r"K_1 = \frac{F_{\text{TR}}}{m} - gC_0")
    st.success(f"K1: **{config.k1:.5f}**")
    if config.debug_mode:
        st.write("### Debug Information for K1")
        st.write(f" - Traction Force (F_TR): {config.traction_force:.2f} N")
        st.write(f" - Vehicle Mass (m): {config.mass} kg")
        st.write(f" - Gravity (g): {GRAVITY} m/s²")
        st.write(f" - Rolling Resistance Coefficient (C0): {config.C0}")

    # --- K2 Calculation ---
    st.subheader("10: K2 Constant")
    if config.formula_mode:
        st.latex(r"K_2 = \frac{\rho C_D A_F}{2m} + gC_1")
    st.success(f"K2: **{config.k2:.5f}**")
    if config.debug_mode:
        st.write("### Debug Information for K2")
        st.write(f" - Air Density (ρ): {AIR_DENSITY} kg/m³")
        st.write(f" - Drag Coefficient (C_D): {C_DRAG}")
        st.write(f" - Frontal Area (A_F): {config.frontal_area:.2f} m²")
        st.write(f" - Vehicle Mass (m): {config.mass} kg")
        st.write(f" - Gravity (g): {GRAVITY} m/s²")
        st.write(f" - Speed-dependent Rolling Resistance Coefficient (C1): {config.C1}")

    st.subheader("11: Velocity-Time Profile")
    velocity_profile(config.k1, config.k2)

    st.write("##### Terminal Velocity")
    if config.formula_mode:
        st.latex(r"V_T = \sqrt{\frac{K_1}{K_2}}")
    st.success(f"Terminal Velocity (V_T): **{config.terminal_velocity * 3.6:.2f} km/h**")  # Convert m/s to km/h
    st.write("##### Time to Reach 98% of Terminal Velocity")
    st.latex(r"t_{V_T} = \frac{2.3}{\sqrt{K_1 K_2}}")
    st.success(f"Time to reach 98% of terminal velocity: **{config.time_to_vt:.2f} seconds**")

    st.subheader("12. Distance-Time Profile")
    distance_profile(config.k2, config.terminal_velocity)

    st.subheader("13. Tractive Power Profile")
    tractive_power_profile(config.traction_force, config.terminal_velocity, config.k1, config.k2,
                           config.time_to_vt)
