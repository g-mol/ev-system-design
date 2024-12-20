import streamlit as st
import plotly.graph_objs as go
import numpy as np
from calculations import calculate_velocity_profile


def velocity_profile(debug_mode, k1, k2):
    time_array = np.linspace(0, 80, 100)

    # Calculate the velocity profile
    profile_ms = calculate_velocity_profile(k1, k2, time_array)

    # Convert velocity to km/h for readability
    velocity_profile_kmh = profile_ms * 3.6

    # --- Plotly Graph ---
    velocity_fig = go.Figure()

    velocity_fig.add_trace(go.Scatter(
        x=time_array,
        y=velocity_profile_kmh,
        mode='lines',
        name='Velocity Profile (v(t))',
        line=dict(color='blue')
    ))

    # Customize layout
    velocity_fig.update_layout(
        title='Velocity-Time Profile',
        xaxis_title='Time (s)',
        yaxis_title='Velocity (km/h)',
        template='plotly_white',
        showlegend=True
    )

    st.plotly_chart(velocity_fig, use_container_width=True)

    # Debugging Information
    if debug_mode:
        st.write("### Debug Information for Velocity Profile")
        st.write(f" - K1: {k1:.5f}")
        st.write(f" - K2: {k2:.5f}")
        st.write(f" - Maximum Velocity: {np.max(velocity_profile_kmh):.2f} km/h")


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
