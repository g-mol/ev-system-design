import pandas as pd
import streamlit as st
import plotly.graph_objs as go
import config
import constants

import constants
from content.vehicle_dynamics import vehicle_dynamics


def drive_profile():
    file_path = 'wltc_drive_profile_low.csv'

    df = pd.read_csv(
        file_path, sep=';', usecols=[1, 3, 4],
        names=['Time', 'Speed', 'Acceleration'], skiprows=1, decimal=','
    )

    # Ensure numeric conversion for necessary columns
    df['Speed'] = pd.to_numeric(df['Speed'], errors='coerce')
    df['Acceleration'] = pd.to_numeric(df['Acceleration'], errors='coerce')
    df['Time'] = pd.to_numeric(df['Time'], errors='coerce')

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

    st.warning("No vehicle data is used here yet, this is just the drive profile")

    st.header("Speed and Acceleration Graph")
    st.write(f"**Total Drive Time:** {total_time / 60:.0f} minutes -> {total_time} seconds")
    st.write(f"**Maximum Velocity:** {max_velocity:.2f} km/h")
    st.write(f"**Average Velocity:** {average_velocity:.2f} km/h")

    try:
        st.plotly_chart(speedFig)  # Display the graph in Streamlit
        st.plotly_chart(accFig)  # Display the graph in Streamlit
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
    except Exception as e:
        st.error(f"An error occurred: {e}")


def distance_profile():
        file_path = 'wltc_drive_profile_low.csv'

        # Load the CSV file
        df = pd.read_csv(
            file_path, sep=';', usecols=[1, 3, 4],
            names=['Time', 'Speed', 'Acceleration'], skiprows=1, decimal=','
        )

        # Ensure numeric conversion for necessary columns
        df['Speed'] = pd.to_numeric(df['Speed'], errors='coerce')
        df['Time'] = pd.to_numeric(df['Time'], errors='coerce')

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

        try:
            st.plotly_chart(distanceFig)  # Display the Total Distance graph
        except FileNotFoundError:
            st.error(f"File not found: {file_path}")
        except Exception as e:
            st.error(f"An error occurred: {e}")


def tractive_power():
    file_path = 'wltc_drive_profile_low.csv'

    # Load the CSV file
    df = pd.read_csv(
        file_path, sep=';', usecols=[1, 3, 4],
        names=['Time', 'Speed', 'Acceleration'], skiprows=1, decimal=','
    )

    # Ensure numeric conversion for necessary columns
    df['Speed'] = pd.to_numeric(df['Speed'], errors='coerce')
    df['Acceleration'] = pd.to_numeric(df['Acceleration'], errors='coerce')
    df['Time'] = pd.to_numeric(df['Time'], errors='coerce')

    # Convert speed from km/h to m/s
    df['Speed (m/s)'] = df['Speed'] * 1000 / 3600

    # Calculate tractive power
    df['Tractive Power (W)'] = (config.mass * constants.GRAVITY * config.k1 * df['Speed (m/s)'] + 0.5 * config.k1 * df['Speed (m/s)'] ** 2) * df[
        'Acceleration']

    # Create the tractive power plot
    powerFig = go.Figure()

    # Add Tractive Power trace
    powerFig.add_trace(go.Scatter(
        x=df['Time'], y=df['Tractive Power (W)'],
        mode='lines', name='Tractive Power (W)',
        line=dict(color='red')
    ))

    # Update layout for the power graph
    powerFig.update_layout(
        title="Tractive Power Over Time",
        xaxis_title="Time (s)",
        yaxis_title="Tractive Power (W)",
        legend=dict(x=0, y=1, traceorder="normal"),
        template="plotly_white",
        hovermode="x unified",
    )

    # Streamlit output for tractive power
    st.header("Tractive Power Graph")

    try:
        st.plotly_chart(powerFig)  # Display the Tractive Power graph
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
