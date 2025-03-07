import os
import pandas as pd
import streamlit as st
import plotly.graph_objs as go
import config
import numpy as np

DRIVE_PROFILES_DIR = "drive_profiles"


def load_drive_profile(file_path):
    """Load a drive profile CSV file."""
    df = pd.read_csv(
        file_path, sep=';', usecols=[1, 3, 4],
        names=['Time', 'Speed', 'Acceleration'], skiprows=1, decimal=','
    )

    df['Speed'] = pd.to_numeric(df['Speed'], errors='coerce')
    df['Acceleration'] = pd.to_numeric(df['Acceleration'], errors='coerce')
    df['Time'] = pd.to_numeric(df['Time'], errors='coerce')
    # df['Gradient'] = pd.to_numeric(df['Gradient'], errors='coerce')
    # df['Height'] = pd.to_numeric(df['Height'], errors='coerce')
    return df


def drive_profile():
    """Main function to handle drive profile selection and analysis."""

    st.title("Drive Profile")

    st.write(
        "A drive profile is a set of data that describes the speed and acceleration of a vehicle over time. It is "
        "used to simulate the vehicle's performance and energy consumption under normal driving conditions. These "
        "values are ultimately used to size the vehicle's battery.")

    st.markdown("---")

    # --- Drive Profile Selection ---
    # List available drive profiles
    profiles = [f for f in os.listdir(DRIVE_PROFILES_DIR) if f.endswith('.csv')]

    # Set default to 'wltc_drive_profile_low.csv' if available
    default_profile = 'wltc_drive_profile_low.csv' if 'wltc_drive_profile_low.csv' in profiles else None

    # Dropdown to select a drive profile
    selected_profile = st.selectbox("Select Drive Profile", profiles,
                                    index=profiles.index(default_profile) if default_profile else 0)

    # Load the selected drive profile
    file_path = os.path.join(DRIVE_PROFILES_DIR, selected_profile)
    df = load_drive_profile(file_path)

    # Plot and analyze the drive profile
    speed_and_acceleration_profile(df)
    distance_profile(df)
    # tractive_power_profile(df)
    required_energy_profile(df)


def speed_and_acceleration_profile(df):
    # Create the interactive plot
    speedFig = go.Figure()
    accFig = go.Figure()
    # gradientFig = go.Figure()
    # heightFig = go.Figure()

    # Add Speed trace
    speedFig.add_trace(go.Scatter(
        x=df['Time'], y=df['Speed'],
        mode='lines', name='Speed (km/h)',
        line=dict(color='blue')
    ))

    # Add Acceleration trace
    accFig.add_trace(go.Scatter(
        x=df['Time'], y=df['Acceleration'],
        mode='lines', name='Acceleration (m/s²)',
        line=dict(color='orange')
    ))

    # # Add Gradient trace
    # gradientFig.add_trace(go.Scatter(
    #     x=df['Time'], y=df['Gradient'],
    #     mode='lines', name='Gradient (%)',
    #     line=dict(color='purple')
    # ))
    #
    # # Add Height trace
    # heightFig.add_trace(go.Scatter(
    #     x=df['Time'], y=df['Height'],
    #     mode='lines', name='Height (m)',
    #     line=dict(color='green')
    # ))

    # Update layout
    speedFig.update_layout(
        title="Drive Profile Speed",
        xaxis_title="Time (s)",
        yaxis_title="Speed (km/h)",
        legend=dict(x=0, y=1, traceorder="normal"),
        template="plotly_white",
        hovermode="x unified",
    )

    # Update layout
    accFig.update_layout(
        title="Drive Profile Acceleration",
        xaxis_title="Time (s)",
        yaxis_title="Acceleration (m/s²)",
        legend=dict(x=0, y=1, traceorder="normal"),
        template="plotly_white",
        hovermode="x unified",
    )

    # # Update layout
    # gradientFig.update_layout(
    #     title="Drive Profile Gradient",
    #     xaxis_title="Time (s)",
    #     yaxis_title="Gradient (%)",
    #     legend=dict(x=0, y=1, traceorder="normal"),
    #     template="plotly_white",
    #     hovermode="x unified",
    # )
    # #
    # # # Update layout
    # heightFig.update_layout(
    #     title="Drive Profile Height",
    #     xaxis_title="Time (s)",
    #     yaxis_title="Height (m)",
    #     legend=dict(x=0, y=1, traceorder="normal"),
    #     template="plotly_white",
    #     hovermode="x unified",
    # )

    total_time = df['Time'].max()
    max_velocity = df['Speed'].max()
    average_velocity = df['Speed'].mean()

    st.header("Speed and Acceleration Graph")
    st.write(f"**Total Drive Time:** {total_time / 60:.0f} minutes -> {total_time} seconds")
    st.write(f"**Maximum Velocity:** {max_velocity:.2f} km/h")
    st.write(f"**Average Velocity:** {average_velocity:.2f} km/h")

    st.plotly_chart(speedFig)
    st.plotly_chart(accFig)
    # st.plotly_chart(gradientFig)
    # st.plotly_chart(heightFig)


def distance_profile(df):
    # Convert speed from km/h to m/s
    df['Speed (m/s)'] = df['Speed'] * 1000 / 3600

    # Calculate time intervals
    df['Time Interval (s)'] = df['Time'].diff().fillna(0)

    # Calculate incremental and total distance
    df['Distance Increment (m)'] = df['Speed (m/s)'] * df['Time Interval (s)']
    df['Total Distance (m)'] = df['Distance Increment (m)'].cumsum()

    # Create the Total Distance plot
    distanceFig = go.Figure()

    # Add Total Distance trace
    distanceFig.add_trace(go.Scatter(
        x=df['Time'], y=df['Total Distance (m)'],
        mode='lines', name='Total Distance (m)',
        line=dict(color='green')
    ))

    # Update layout for the distance graph
    distanceFig.update_layout(
        title="Total Distance Traveled",
        xaxis_title="Time (s)",
        yaxis_title="Distance (m)",
        legend=dict(x=0, y=1, traceorder="normal"),
        template="plotly_white",
        hovermode="x unified",
    )

    # Total distance
    total_distance = df['Total Distance (m)'].iloc[-1]

    # Streamlit output
    st.header("Total Distance Traveled Graph")
    st.write(f"**Total Distance Traveled:** {total_distance:.2f} meters")

    st.plotly_chart(distanceFig)


def tractive_power_profile(df):
    # Convert speed to m/s
    df['Speed (m/s)'] = df['Speed'] * 1000 / 3600

    # Constants
    m = config.mass  # Vehicle mass (kg)
    g = config.GRAVITY  # Gravitational acceleration (m/s^2)
    rho = config.AIR_DENSITY  # Air density (kg/m^3)
    C_D = config.C_DRAG  # Drag coefficient
    A_F = config.frontal_area  # Frontal area (m^2)
    C0 = config.C0  # Static rolling resistance coefficient
    C1 = config.C1  # Speed-dependent rolling resistance coefficient

    # Velocity profile
    v = df['Speed (m/s)']
    dv_dt = df['Acceleration']

    # Calculate road angle in radians
    # road_angle_radians = np.radians(df['Gradient'])

    # Calculate forces
    rolling_resistance_force = m * g * (C0 + C1 * v ** 2)
    aerodynamic_drag_force = 0.5 * rho * C_D * A_F * v ** 2
    inertial_force = m * dv_dt
    # gravitational_force = m * g * np.sin(road_angle_radians)

    # Total tractive force
    # df['Tractive Force (N)'] = inertial_force + aerodynamic_drag_force + rolling_resistance_force + gravitational_force
    df['Tractive Force (N)'] = inertial_force + aerodynamic_drag_force + rolling_resistance_force

    # Tractive power
    df['Tractive Power (W)'] = df['Tractive Force (N)'] * v
    df['Tractive Power (kW)'] = df['Tractive Power (W)'] / 1000

    # --- Plotting ---
    powerFig = go.Figure()

    # Add Tractive Force trace (Primary y-axis)
    powerFig.add_trace(go.Scatter(
        x=df['Time'], y=df['Tractive Force (N)'],
        mode='lines', name='Tractive Force (N)',
        line=dict(color='red'),
        visible='legendonly'  # Hide from legend by default
    ))

    # Add Tractive Power trace (Secondary y-axis)
    powerFig.add_trace(go.Scatter(
        x=df['Time'], y=df['Tractive Power (kW)'],
        mode='lines', name='Tractive Power (kW)',
        line=dict(color='blue'),
        yaxis='y2',  # Bind this trace to the secondary y-axis
    ))

    # Update Layout for secondary y-axis
    powerFig.update_layout(
        title="Tractive Power and Force Over Time",
        xaxis_title="Time (s)",
        yaxis=dict(
            title="Tractive Power (kW)",
            titlefont=dict(color="red"),
            tickfont=dict(color="red"),
        ),
        yaxis2=dict(
            title="Tractive Force (N)",
            titlefont=dict(color="blue"),
            tickfont=dict(color="blue"),
            overlaying="y",  # Overlay on the primary y-axis
            side="right",  # Position on the right side
        ),
        template="plotly_white",
        legend=dict(x=0, y=1, traceorder="normal"),
        hovermode="x unified",
    )

    # Display the plot
    st.header("Tractive Power and Force Graph")
    st.plotly_chart(powerFig, use_container_width=True)


def required_energy_profile(df):
    st.header("Energy-Time Profile")

    # Add input for regenerative braking efficiency
    regen_efficiency = st.number_input("Regenerative Braking Efficiency (%):", min_value=0, max_value=100, value=65,
                                       step=1) / 100.0

    # Calculate dynamic tractive force F_TR(t)
    df['Aerodynamic Drag (N)'] = 0.5 * config.AIR_DENSITY * config.C_DRAG * config.frontal_area * df['Speed (m/s)'] ** 2
    df['Rolling Resistance (N)'] = config.mass * config.GRAVITY * (config.C0 + config.C1 * df['Speed (m/s)'] ** 2)
    df['Inertial Force (N)'] = config.mass * df['Acceleration']  # m * dv/dt
    # road_angle_radians = np.radians(df['Gradient'])
    # df['Gravitational Force (N)'] = config.mass * config.GRAVITY * np.sin(road_angle_radians)
    # df['Tractive Force (N)'] = df['Aerodynamic Drag (N)'] + df['Rolling Resistance (N)'] + df['Inertial Force (N)'] + \
    #                            df['Gravitational Force (N)']
    df['Tractive Force (N)'] = df['Aerodynamic Drag (N)'] + df['Rolling Resistance (N)'] + df['Inertial Force (N)']

    # Calculate instantaneous power P_TR(t) = F_TR * v(t)
    df['Tractive Power (W)'] = df['Tractive Force (N)'] * df['Speed (m/s)']

    # Adjust for regenerative braking efficiency
    df['Tractive Power (W)'] = df['Tractive Power (W)'].apply(lambda x: x * regen_efficiency if x < 0 else x)

    # Integrate power over time to calculate energy
    df['Time Interval (s)'] = df['Time'].diff().fillna(0)  # Time intervals
    df['Energy Increment (J)'] = df['Tractive Power (W)'] * df['Time Interval (s)']  # Incremental energy
    df['Total Energy (J)'] = df['Energy Increment (J)'].cumsum()  # Cumulative energy

    # Convert total energy to kWh for readability
    df['Total Energy (kWh)'] = df['Total Energy (J)'] / (3.6e6)

    # Calculate distance traveled (m and km)
    df['Distance Increment (m)'] = df['Speed (m/s)'] * df['Time Interval (s)']
    df['Total Distance (m)'] = df['Distance Increment (m)'].cumsum()
    df['Total Distance (km)'] = df['Total Distance (m)'] / 1000  # Convert to km

    # --- Statistics ---
    total_energy_kwh = df['Total Energy (kWh)'].iloc[-1]
    total_distance_km = df['Total Distance (km)'].iloc[-1]
    kwh_per_km = total_energy_kwh / total_distance_km if total_distance_km > 0 else float('inf')  # Energy per km

    # Save wh per km to session state
    st.session_state["wh_per_km"] = kwh_per_km * 1000

    # --- Plotly Graph ---
    energy_fig = go.Figure()

    # Add Total Energy trace
    energy_fig.add_trace(go.Scatter(
        x=df['Time'],
        y=df['Total Energy (kWh)'],
        mode='lines',
        name='Total Energy (kWh)',
        line=dict(color='green')
    ))

    # Customize layout
    energy_fig.update_layout(
        title='Energy-Time Profile',
        xaxis_title='Time (s)',
        yaxis_title='Energy (kWh)',
        template='plotly_white'
    )

    # Display in Streamlit
    st.plotly_chart(energy_fig, use_container_width=True)

    # --- Display Statistics ---
    st.subheader("Energy Usage Statistics")
    st.write(f"**Total Energy Used:** {total_energy_kwh:.2f} kWh")
    st.write(f"**Total Distance Traveled:** {total_distance_km:.2f} km")
    st.write(f"**Average Energy Efficiency:** {1 / kwh_per_km:.2f} km/kWh" if kwh_per_km > 0 else "N/A")
    average_energy_efficiency = 1 / kwh_per_km if kwh_per_km > 0 else 0
    st.session_state["average_energy_efficiency"] = average_energy_efficiency
    # st.write(f"**Energy Consumption per Kilometer:** {kwh_per_km * 1000:.0f} Wh/km")

    st.success(f"**Energy Consumption per Kilometer:** {kwh_per_km * 1000:.0f} Wh/km")
    # st.write(f"**Energy Consumption per 100 Kilometer:** {kwh_per_km * 100:.2f} kWh/100 km")
