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
    st.session_state["highest_power"] = 0
    st.session_state["highest_torque"] = 0

    st.title("Scenarios")

    st.write("The calculations below are based on the current vehicle configuration, selected requirements, "
             "or a predefined scenario. The highest calculated power and torque values found in the scenarios "
             "are displayed below.")

    st.markdown("---")

    # Inputs
    st.markdown(f"### **Inputs**")
    input1, input2, input3, input4 = st.columns(4)

    with input1:
        current_speed = st.number_input("Speed (km/h)", min_value=0, max_value=400, value=60)
    with input2:
        current_road_angle = st.number_input("Incline (%)", min_value=0.0, max_value=45.0, value=5.0, step=1.0)
    with input3:
        current_acceleration = st.number_input("Acceleration (m/s²)", min_value=0.0, max_value=20.0, value=1.0)
    with input4:
        headwind_speed = st.number_input("Headwind (km/h)", min_value=0, max_value=100, value=0)

    st.write("##")

    # Predefined Scenarios
    scenarios = [
        {
            "name": "Current Situation",
            "speed_kph": current_speed,
            "grade_percent": current_road_angle,
            "acceleration": current_acceleration,
            "headwind_kph": headwind_speed,
        },
        {
            "name": "Static Top Speed Requirement",
            "speed_kph": config.top_speed,
            "grade_percent": 0,
            "acceleration": 0,
            "headwind_kph": headwind_speed,
        },
        {
            "name": f"Time to {config.top_speed if config.top_speed < 100 else 100} km/h in {round(config.time_to_100, 2)} seconds",
            "speed_kph": config.top_speed if config.top_speed < 100 else 100,
            "grade_percent": 0,
            "acceleration": round(config.time_to_100_acceleration, 2),
            "headwind_kph": 0,
        },
        {
            "name": "Flat Roads",
            "speed_kph": config.top_speed if config.top_speed < 100 else 100,
            "grade_percent": 0,
            "acceleration": 0,
            "headwind_kph": headwind_speed,
        },
        {
            "name": "Inclines",
            "speed_kph": 5,
            "grade_percent": 20,
            "acceleration": 0,
            "headwind_kph": headwind_speed,
        },
        {
            "name": "Acceleration",
            "speed_kph": 50,
            "grade_percent": 0,
            "acceleration": 1.5,
            "headwind_kph": headwind_speed,
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
            frontal_area = config.vehicle_height * config.vehicle_width
            drag_force = calculate_aerodynamic_drag_force(relative_speed, frontal_area)

            road_load_force = calculate_road_load_force(rolling_force, gravitational_force, drag_force)
            traction_force = calculate_traction_force(road_load_force, config.mass, scenario["acceleration"], config.km)

            # Power and torque
            power_required = calculate_power_required(traction_force, speed_mps)
            angular_velocity = calculate_angular_velocity(speed_mps, config.wheel_radius)

            if angular_velocity == 0:  # Prevent division by zero for stationary scenarios
                torque_required = 0
            else:
                torque_required = calculate_torque_required(power_required, angular_velocity)

            # if "highest_power" not in st.session_state:
            #     st.session_state["highest_power"] = 0
            # if "highest_torque" not in st.session_state:
            #     st.session_state["highest_torque"] = 0

            if power_required > st.session_state["highest_power"]:
                st.session_state["highest_power"] = power_required
            if torque_required > st.session_state["highest_torque"]:
                st.session_state["highest_torque"] = torque_required

            with col2:
                with st.container():
                    st.success(f"**Required Propulsion Power:** {power_required / 1000:.0f} kW")
                    st.success(f"**Required Torque:** {torque_required:.0f} Nm")

            st.markdown("---")

    st.subheader("Highest Calculated Power and Torque")
    st.error(f"**Power:** {st.session_state['highest_power'] / 1000:.0f} kW")
    st.error(f"**Torque:** {st.session_state['highest_torque']:.0f} Nm")
