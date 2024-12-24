import pandas as pd
import streamlit as st
import plotly.graph_objs as go
import config


def drive_profile():
    file_path = 'wltc_drive_profile_low.csv'

    df = pd.read_csv(
        file_path, sep=';', usecols=[1, 3, 4],
        names=['Time', 'Speed', 'Acceleration'], skiprows=1, decimal=','
    )

    df['Speed'] = pd.to_numeric(df['Speed'], errors='coerce')
    df['Acceleration'] = pd.to_numeric(df['Acceleration'], errors='coerce')
    df['Time'] = pd.to_numeric(df['Time'], errors='coerce')

    speed_and_acceleration_profile(df)
    distance_profile(df)
    tractive_power_profile(df)
    required_energy_profile(df)


def speed_and_acceleration_profile(df):
    # Create the interactive plot
    speedFig = go.Figure()
    accFig = go.Figure()

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

    # Update layout
    speedFig.update_layout(
        title="Drive Profile Speed",
        xaxis_title="Time (s)",
        yaxis_title="Values",
        legend=dict(x=0, y=1, traceorder="normal"),
        template="plotly_white",
        hovermode="x unified",
    )

    # Update layout
    accFig.update_layout(
        title="Drive Profile Acceleration",
        xaxis_title="Time (s)",
        yaxis_title="Values",
        legend=dict(x=0, y=1, traceorder="normal"),
        template="plotly_white",
        hovermode="x unified",
    )

    total_time = df['Time'].max()
    max_velocity = df['Speed'].max()
    average_velocity = df['Speed'].mean()

    st.write(
        "This is the Worldwide Harmonized Light Vehicles Test Cycle with the 'extra high' phase replaced with a "
        "second 'low' phase to make it more fitting for urban driving.")

    st.header("Speed and Acceleration Graph")
    st.write(f"**Total Drive Time:** {total_time / 60:.0f} minutes -> {total_time} seconds")
    st.write(f"**Maximum Velocity:** {max_velocity:.2f} km/h")
    st.write(f"**Average Velocity:** {average_velocity:.2f} km/h")

    st.plotly_chart(speedFig)
    st.plotly_chart(accFig)


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

    # Calculate forces
    rolling_resistance_force = m * g * (C0 + C1 * v ** 2)
    aerodynamic_drag_force = 0.5 * rho * C_D * A_F * v ** 2
    inertial_force = m * dv_dt

    # Total tractive force
    df['Tractive Force (N)'] = inertial_force + aerodynamic_drag_force + rolling_resistance_force

    # Tractive power
    df['Tractive Power (W)'] = df['Tractive Force (N)'] * v
    df['Tractive Power (kW)'] = df['Tractive Power (W)'] / 1000

    # --- Plotting ---
    powerFig = go.Figure()

    # Add Tractive Power trace
    powerFig.add_trace(go.Scatter(
        x=df['Time'], y=df['Tractive Power (kW)'],
        mode='lines', name='Tractive Power (kW)',
        line=dict(color='red')
    ))

    # Update Layout
    powerFig.update_layout(
        title="Tractive Power Over Time",
        xaxis_title="Time (s)",
        yaxis_title="Tractive Power (kW)",
        template="plotly_white",
        legend=dict(x=0, y=1, traceorder="normal"),
        hovermode="x unified",
    )

    # Display the plot
    st.header("Tractive Power Graph")
    st.plotly_chart(powerFig, use_container_width=True)


def required_energy_profile(df):
    # Calculate dynamic tractive force F_TR(t)
    df['Aerodynamic Drag (N)'] = 0.5 * config.AIR_DENSITY * config.C_DRAG * config.frontal_area * df['Speed (m/s)'] ** 2
    df['Rolling Resistance (N)'] = config.mass * config.GRAVITY * (config.C0 + config.C1 * df['Speed (m/s)'] ** 2)
    df['Inertial Force (N)'] = config.mass * df['Acceleration']  # m * dv/dt
    df['Tractive Force (N)'] = df['Aerodynamic Drag (N)'] + df['Rolling Resistance (N)'] + df['Inertial Force (N)']

    # Calculate instantaneous power P_TR(t) = F_TR * v(t)
    df['Tractive Power (W)'] = df['Tractive Force (N)'] * df['Speed (m/s)']

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
    avg_power_kw = df['Tractive Power (W)'].mean() / 1000  # Average power in kW
    kwh_per_km = total_energy_kwh / total_distance_km if total_distance_km > 0 else float('inf')  # Energy per km

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
    st.header("Energy-Time Profile")
    st.plotly_chart(energy_fig, use_container_width=True)

    # --- Display Statistics ---
    st.subheader("Energy Usage Statistics")
    st.write(f"**Total Energy Used:** {total_energy_kwh:.2f} kWh")
    st.write(f"**Total Distance Traveled:** {total_distance_km:.2f} km")
    st.write(f"**Energy Consumption per Kilometer:** {kwh_per_km:.2f} kWh/km")
    st.write(f"**Average Power Usage:** {avg_power_kw:.2f} kW")
    st.write(f"**Average Energy Efficiency:** {1 / kwh_per_km * 100:.2f} km/kWh" if kwh_per_km > 0 else "N/A")