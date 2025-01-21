import streamlit as st
import math
import config


def drive_train():
    st.title("Drive Train")

    st.write(
        "The calculation below helps determine the required gear ratio for the electric vehicle based on the required "
        "top speed, current wheel radius, and motor maximum RPM.")

    st.markdown("---")

    # Inputs from config
    top_speed_mps = config.top_speed_mps  # Assume top_speed is in m/s
    wheel_radius = config.wheel_radius  # Assume wheel_radius is in meters

    # New input for motor max RPM
    motor_max_rpm = st.number_input("Motor Max RPM:", min_value=1000, max_value=20000, value=7000, step=100)

    st.markdown(f"- **Top Speed:** {config.top_speed} km/h -> {top_speed_mps:.2f} m/s")
    st.markdown(f"- **Wheel Radius:** {wheel_radius:.2f} m")

    st.latex(
        r"R = \frac{\omega_{\text{motor}} \cdot r \cdot 2\pi}{v_{\text{max}} \cdot 60}"
    )

    # Gear ratio calculation
    gear_ratio = (motor_max_rpm * wheel_radius * 2 * math.pi) / (top_speed_mps * 60)

    # Display inputs
    # st.markdown("### Inputs")

    # Display result
    st.markdown("### Result")
    st.success(f"**Required Gear Ratio:** {gear_ratio:.1f}")

    st.write(f"**Theoretical Motor Torque:** "
             f"{st.session_state['highest_torque'] / gear_ratio:.0f} Nm")
    drivetrain_efficiency = st.number_input("Drivetrain Efficiency (%):", min_value=0, max_value=100, value=90,
                                            step=1) / 100
    st.success(f"**Required Motor Torque:** "
               f"{st.session_state['highest_torque'] / gear_ratio / drivetrain_efficiency:.0f} Nm")
