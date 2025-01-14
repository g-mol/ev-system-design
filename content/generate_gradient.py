import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go


def generate_gradient_profile(total_time_seconds, step_seconds=1, hill_amplitude=5, hill_frequency=600,
                              noise_level=0.5):
    """Generate synthetic gradient profile for a city."""
    time_steps = np.arange(0, total_time_seconds, step_seconds)
    gradient = hill_amplitude * np.sin(2 * np.pi * time_steps / hill_frequency)  # Base sinusoidal pattern
    gradient += np.random.normal(0, noise_level, len(time_steps))  # Add random noise
    return pd.DataFrame({"Time (s)": time_steps, "Gradient (%)": gradient})


def generate_gradient():
    st.title("Generate Gradient Profile for a City")
    st.markdown("---")

    # Input settings
    st.subheader("Input Settings")
    total_time_seconds = st.number_input("Total Time (s):", min_value=100, max_value=10000, value=2067, step=10)
    step_seconds = st.number_input("Time Step (s):", min_value=1, max_value=60, value=1, step=1)
    hill_amplitude = st.number_input("Hill Amplitude (%):", min_value=1.0, max_value=20.0, value=5.0, step=0.1)
    hill_frequency = st.number_input("Hill Frequency (s):", min_value=100, max_value=2000, value=600, step=10)
    noise_level = st.number_input("Noise Level (%):", min_value=0.0, max_value=5.0, value=0.5, step=0.1)

    # Generate gradient profile
    gradient_data = generate_gradient_profile(
        total_time_seconds, step_seconds, hill_amplitude, hill_frequency, noise_level
    )

    # Plot the gradient profile
    st.subheader("Generated Gradient Profile")
    gradient_fig = go.Figure()
    gradient_fig.add_trace(go.Scatter(
        x=gradient_data["Time (s)"],
        y=gradient_data["Gradient (%)"],
        mode="lines",
        name="Gradient (%)",
        line=dict(color="purple")
    ))
    gradient_fig.update_layout(
        title="Gradient Profile",
        xaxis_title="Time (s)",
        yaxis_title="Gradient (%)",
        template="plotly_white",
        hovermode="x unified"
    )
    st.plotly_chart(gradient_fig, use_container_width=True)

    # Download the gradient profile as CSV
    st.subheader("Download Gradient Data")
    csv_data = gradient_data.to_csv(index=False, sep=';', decimal=',')
    st.download_button(
        label="Download Gradient Profile as CSV",
        data=csv_data,
        file_name="gradient_profile.csv",
        mime="text/csv"
    )
