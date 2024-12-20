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
