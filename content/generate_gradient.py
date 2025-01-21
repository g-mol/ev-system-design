import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go


def generate_gradient_profile(total_time_seconds, step_seconds=1, hill_amplitude=5, hill_frequency=600,
                              noise_level=0.5, noise_width=50):
    """Generate synthetic gradient and height profile for a city."""
    time_steps = np.arange(0, total_time_seconds, step_seconds)

    # Generate base sinusoidal gradient
    gradient = hill_amplitude * np.sin(2 * np.pi * time_steps / hill_frequency)

    # Add smoothed random noise
    random_noise = np.random.normal(0, noise_level, len(time_steps))
    smoothed_noise = np.convolve(random_noise, np.ones(noise_width) / noise_width, mode='same')
    gradient += smoothed_noise

    # Ensure the gradient is realistic (bounded within reasonable limits)
    gradient = np.clip(gradient, -20, 20)

    # Calculate height profile by integrating the gradient
    height = np.cumsum(gradient / 100 * (step_seconds * 10))  # Convert gradient to height over distance

    return pd.DataFrame({"Time (s)": time_steps, "Gradient (%)": gradient, "Height (m)": height})


def generate_gradient():
    st.title("Generate Gradient and Height Profile for a City")
    st.markdown("---")

    # Input settings
    st.subheader("Input Settings")
    total_time_seconds = st.number_input("Total Time (s):", min_value=100, max_value=10000, value=2067, step=10)
    step_seconds = st.number_input("Time Step (s):", min_value=1, max_value=60, value=1, step=1)
    hill_amplitude = st.number_input("Hill Amplitude (%):", min_value=0.0, max_value=20.0, value=5.0, step=0.1)
    hill_frequency = st.number_input("Hill Frequency (s):", min_value=100, max_value=2000, value=600, step=10)
    noise_level = st.number_input("Noise Level (%):", min_value=0.0, max_value=5.0, value=0.5, step=0.1)
    noise_width = st.number_input("Noise Width (Smoothing):", min_value=1, max_value=500, value=50, step=10)

    # Generate gradient profile
    gradient_data = generate_gradient_profile(
        total_time_seconds, step_seconds, hill_amplitude, hill_frequency, noise_level, noise_width
    )

    # Plot the height profile
    st.subheader("Generated Height Profile")
    height_fig = go.Figure()

    # Add Height trace
    height_fig.add_trace(go.Scatter(
        x=gradient_data["Time (s)"],
        y=gradient_data["Height (m)"],
        mode="lines",
        name="Height (m)",
        line=dict(color="green")
    ))

    height_fig.update_layout(
        title="Height Profile",
        xaxis_title="Time (s)",
        yaxis_title="Height (m)",
        template="plotly_white",
        hovermode="x unified"
    )
    st.plotly_chart(height_fig, use_container_width=True)

    # Plot the gradient profile
    st.subheader("Generated Gradient Profile")
    gradient_fig = go.Figure()

    # Add Gradient trace
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
    st.subheader("Download Gradient and Height Data")
    csv_data = gradient_data.to_csv(index=False, sep=';', decimal=',')
    st.download_button(
        label="Download Gradient and Height Profile as CSV",
        data=csv_data,
        file_name="gradient_and_height_profile.csv",
        mime="text/csv"
    )
