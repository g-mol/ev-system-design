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
    calculate_angular_velocity,
    calculate_torque_required,
)


def scenarios():
    st.title("Vehicle Scenarios")
    st.markdown("---")

    # Interactive Scenario
    st.markdown("### **Custom Scenario**")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        custom_speed_kph = st.number_input("Speed (km/h):", min_value=0, max_value=300, value=50, step=1)
    with col2:
        custom_grade_percent = st.number_input("Incline (%):", min_value=-30, max_value=100, value=0, step=1)
    with col3:
        custom_acceleration = st.number_input("Acceleration (m/s²):", min_value=0.0, max_value=20.0, value=1.0, step=0.1)
    with col4:
        custom_headwind_kph = st.number_input("Headwind (km/h):", min_value=0, max_value=100, value=25, step=1)

    speed_mps = custom_speed_kph / 3.6
    headwind_mps = custom_headwind_kph / 3.6
    relative_speed = speed_mps + headwind_mps
    angle_rad = math.atan(custom_grade_percent / 100)

    rolling_force = calculate_rolling_resistance_force(config.mass, angle_rad, speed_mps, config.C0, config.C1)
    gravitational_force = calculate_gravitational_force(config.mass, angle_rad)
    drag_force = calculate_aerodynamic_drag_force(relative_speed, config.frontal_area)

    road_load_force = calculate_road_load_force(rolling_force, gravitational_force, drag_force)
    traction_force = calculate_traction_force(road_load_force, config.mass, custom_acceleration, config.km)

    power_required = calculate_power_required(traction_force, speed_mps)
    angular_velocity = calculate_angular_velocity(speed_mps, config.wheel_radius)

    if angular_velocity == 0:
        torque_required = 0
    else:
        torque_required = calculate_torque_required(power_required, angular_velocity)

    st.success(f"**Required Propulsion Power:** {power_required/1000:.0f} kW")
    st.success(f"**Required Torque:** {torque_required:.0f} Nm")

    if config.debug_mode:
        st.markdown("---")
        st.write(f"**Rolling Resistance Force:** {rolling_force:.2f} N")
        st.write(f"**Gravitational Force:** {gravitational_force:.2f} N")
        st.write(f"**Aerodynamic Drag Force:** {drag_force:.2f} N")
        st.write(f"**Road Load Force:** {road_load_force:.2f} N")
        st.write(f"**Traction Force:** {traction_force:.2f} N")
        st.markdown("---")

    st.markdown("---")

    # Predefined Scenarios
    scenarios = [
        {
            "name": "Flat Roads",
            "speed_kph": 100,
            "grade_percent": 0,
            "acceleration": 0,
            "headwind_kph": 25,
        },
        {
            "name": "Inclines",
            "speed_kph": 5,
            "grade_percent": 20,
            "acceleration": 0,
            "headwind_kph": 25,
        },
        {
            "name": "Acceleration",
            "speed_kph": 50,
            "grade_percent": 0,
            "acceleration": 1.5,
            "headwind_kph": 25,
        },
    ]

    for scenario in scenarios:
        with st.container():
            st.markdown(f"### **{scenario['name']}**")

            # Layout for inputs and results
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**Speed**: {scenario['speed_kph']} km/h")
                st.markdown(f"**Incline**: {scenario['grade_percent']}%")
                st.markdown(f"**Acceleration**: {scenario['acceleration']} m/s²")
                st.markdown(f"**Headwind**: {scenario['headwind_kph']} km/h")

            speed_mps = scenario["speed_kph"] / 3.6
            headwind_mps = scenario["headwind_kph"] / 3.6
            relative_speed = speed_mps + headwind_mps
            angle_rad = math.atan(scenario["grade_percent"] / 100)

            rolling_force = calculate_rolling_resistance_force(config.mass, angle_rad, speed_mps, config.C0, config.C1)
            gravitational_force = calculate_gravitational_force(config.mass, angle_rad)
            drag_force = calculate_aerodynamic_drag_force(relative_speed, config.frontal_area)

            road_load_force = calculate_road_load_force(rolling_force, gravitational_force, drag_force)
            traction_force = calculate_traction_force(road_load_force, config.mass, scenario["acceleration"], km=1)

            # Power and torque
            power_required = calculate_power_required(traction_force, speed_mps)
            angular_velocity = calculate_angular_velocity(speed_mps, config.wheel_radius)

            if angular_velocity == 0:  # Prevent division by zero for stationary scenarios
                torque_required = 0
            else:
                torque_required = calculate_torque_required(power_required, angular_velocity)

            with col2:
                with st.container():
                    st.success(f"**Required Propulsion Power:** {power_required / 1000:.0f} kW")
                    st.success(f"**Required Torque:** {torque_required:.0f} Nm")

            st.markdown("---")
