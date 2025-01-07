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
    calculate_time_to_terminal_velocity,

)
from config import road_angle_rad
from content.velocity_profile import (
    velocity_profile,
    distance_profile,
    tractive_power_profile
)
from constants import AIR_DENSITY, GRAVITY, C_DRAG

# Define the powertrain sizing function
def powertrain_sizing():
    st.title("Powertrain Sizing")

    # Inputs from the config file
    vehicle_mass = config.mass  # Vehicle mass in kg
    top_speed = config.top_speed_mps  # Top speed in m/s
    time_to_top_speed = config.time_to_100  # Time to reach top speed in seconds
    rolling_resistance_force = config.rolling_force  # Rolling resistance force in N
    aerodynamic_drag_force = config.drag_force  # Aerodynamic drag force in N

    # --- Initial Acceleration Calculation ---
    initial_acceleration = top_speed / time_to_top_speed

    # --- Power Rating Calculation ---
    power_constant_torque = (vehicle_mass / 2) * (initial_acceleration**2)
    power_constant_power = (vehicle_mass / (2 * time_to_top_speed)) * (top_speed**2)
    motor_power_rating = power_constant_torque + power_constant_power


    # --- Results Display ---
    st.header("Powertrain Sizing Results")

    # Initial Acceleration
    st.subheader("1. Initial Acceleration")
    st.latex(r"a = \frac{v_y}{t_f}")
    st.success(f"Initial Acceleration: **{initial_acceleration:.2f} m/s²**")
    st.write(f" - Top Speed (v_y): {top_speed:.2f} m/s")
    st.write(f" - Time to Reach Top Speed (t_f): {time_to_top_speed:.2f} s")

    # Motor Power Rating
    st.subheader("2. Motor Power Rating")
    st.latex(r"P_m = \frac{m}{2t_f}(v_m^2 + v_y^2)")
    st.success(f"Motor Power Rating: **{motor_power_rating / 1000:.2f} kW**")
    st.write(f" - Vehicle Mass (m): {vehicle_mass} kg")
    st.write(f" - Time to Reach Top Speed (t_f): {time_to_top_speed:.2f} s")
    st.write(f" - Initial Acceleration (v_m): {initial_acceleration:.2f} m/s²")
    st.write(f" - Top Speed (v_y): {top_speed:.2f} m/s")


