import streamlit as st
import plotly.graph_objs as go
import numpy as np
from calculations import (
    calculate_velocity_profile,
    calculate_instantaneous_power,
    calculate_terminal_power,
    calculate_peak_power,
    calculate_mean_power,
    calculate_terminal_velocity
)


def velocity_profile(debug_mode, k1, k2):
    time_array = np.linspace(0, 80, 100)

    # Calculate the velocity profile
    profile_ms = calculate_velocity_profile(k1, k2, time_array)
    velocity_profile_kmh = profile_ms * 3.6

    # Calculate terminal velocity
    terminal_velocity_ms = calculate_terminal_velocity(k1, k2)
    terminal_velocity_kmh = terminal_velocity_ms * 3.6

    # --- Plotly Graph ---
    velocity_fig = go.Figure()

    # Velocity Profile Plot
    velocity_fig.add_trace(go.Scatter(
        x=time_array,
        y=velocity_profile_kmh,
        mode='lines',
        name='Velocity Profile (v(t))',
        line=dict(color='blue')
    ))

    # Terminal Velocity Dotted Line
    velocity_fig.add_trace(go.Scatter(
        x=[0, time_array[-1]],  # Line from t=0 to the last time point
        y=[terminal_velocity_kmh, terminal_velocity_kmh],
        mode='lines',
        name='Terminal Velocity (V_T)',
        line=dict(color='red', dash='dash')  # Red dashed line
    ))

    # Customize Layout
    velocity_fig.update_layout(
        title='Velocity-Time Profile',
        xaxis_title='Time (s)',
        yaxis_title='Velocity (km/h)',
        template='plotly_white',
        showlegend=True
    )

    # Display in Streamlit
    st.plotly_chart(velocity_fig, use_container_width=True)

    # Debugging Information
    if debug_mode:
        st.write("### Debug Information for Velocity Profile")
        st.write(f" - K1: {k1:.5f}")
        st.write(f" - K2: {k2:.5f}")
        st.write(f" - Terminal Velocity: {terminal_velocity_kmh:.2f} km/h")
        st.write(f" - Maximum Velocity from Profile: {np.max(velocity_profile_kmh):.2f} km/h")


def distance_profile(debug_mode, k2, terminal_velocity):
    # Generate time array
    time_array = np.linspace(0, 80, 100)  # From 0 to 80 seconds, 100 points

    # Calculate the distance profile
    k2_vt_t = k2 * terminal_velocity * time_array
    distance_profile_m = (1 / k2) * np.log(np.cosh(k2_vt_t))

    # --- Plotly Graph ---
    distance_fig = go.Figure()

    distance_fig.add_trace(go.Scatter(
        x=time_array,
        y=distance_profile_m,
        mode='lines',
        name='Distance Profile (s(t))',
        line=dict(color='green')
    ))

    # Customize layout
    distance_fig.update_layout(
        title='Distance-Time Profile',
        xaxis_title='Time (s)',
        yaxis_title='Distance (m)',
        template='plotly_white',
        showlegend=True
    )

    st.plotly_chart(distance_fig, use_container_width=True)

    # Debugging Information
    if debug_mode:
        st.write("### Debug Information for Distance Traversed")
        st.write(f" - K2: {k2:.5f}")
        st.write(f" - Terminal Velocity (V_T): {terminal_velocity:.2f} m/s")
        st.write(f" - Distance at 80s: {distance_profile_m[-1]:.2f} m")


def tractive_power_profile(debug_mode, f_tr, terminal_velocity, k1, k2, tf):
    # Generate time array
    time_array = np.linspace(0, tf, 100)

    # Calculate Instantaneous Power
    instantaneous_power = calculate_instantaneous_power(f_tr, terminal_velocity, k2, time_array)

    # Calculate Terminal Power
    terminal_power = calculate_terminal_power(f_tr, terminal_velocity)

    # Calculate Peak Tractive Power at t_f
    peak_power = calculate_peak_power(f_tr, terminal_velocity, k1, k2, tf)

    # Calculate Mean Tractive Power over interval
    mean_power = calculate_mean_power(f_tr, terminal_velocity, k1, k2, tf)

    # --- Plotly Graph ---
    power_fig = go.Figure()

    # Instantaneous Power Plot
    power_fig.add_trace(go.Scatter(
        x=time_array,
        y=instantaneous_power / 1000,  # Convert to kW
        mode='lines',
        name='Instantaneous Power (P_TR(t))',
        line=dict(color='red')
    ))

    # Terminal Power (Horizontal Line)
    power_fig.add_trace(go.Scatter(
        x=[0, time_array[-1]],
        y=[terminal_power / 1000, terminal_power / 1000],  # Convert to kW
        mode='lines',
        name='Terminal Power (P_T)',
        line=dict(color='blue', dash='dash')
    ))

    # Customize Layout
    power_fig.update_layout(
        title='Tractive Power Over Time',
        xaxis_title='Time (s)',
        yaxis_title='Power (kW)',
        template='plotly_white',
        showlegend=True
    )

    st.plotly_chart(power_fig, use_container_width=True)

    # Display Results
    st.success(f"Terminal Power (P_T): **{terminal_power / 1000:.2f} kW**")
    st.success(f"Peak Tractive Power (P_TRpk): **{peak_power / 1000:.2f} kW**")
    st.success(f"Mean Tractive Power (P̄_TR): **{mean_power / 1000:.2f} kW**")

