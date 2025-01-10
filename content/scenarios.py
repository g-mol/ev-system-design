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

    st.write("The calculations below are based on the current vehicle configuration, selected requirements, "
             "or a predefined scenario. The highest calculated power and torque values found in the scenarios "
             "are displayed below.")

    st.markdown("---")

    # Predefined Scenarios
    scenarios = [
        {
            "name": "Current Situation",
            "speed_kph": config.current_speed,
            "grade_percent": config.current_road_angle,
            "acceleration": config.current_acceleration,
            "headwind_kph": config.headwind_speed,
        },
        {
            "name": "Static Top Speed Requirement",
            "speed_kph": config.top_speed,
            "grade_percent": 0,
            "acceleration": 0,
            "headwind_kph": config.headwind_speed,
        },
        {
            "name": f"Time to 100 km/h in {round(config.time_to_100, 2)} seconds",
            "speed_kph": 100,
            "grade_percent": 0,
            "acceleration": round(config.time_to_100_acceleration, 2),
            "headwind_kph": config.headwind_speed,
        },
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
            traction_force = calculate_traction_force(road_load_force, config.mass, scenario["acceleration"], config.km)

            # Power and torque
            power_required = calculate_power_required(traction_force, speed_mps)
            angular_velocity = calculate_angular_velocity(speed_mps, config.wheel_radius)

            if angular_velocity == 0:  # Prevent division by zero for stationary scenarios
                torque_required = 0
            else:
                torque_required = calculate_torque_required(power_required, angular_velocity)

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
