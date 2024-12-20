import streamlit as st
from content.vehicle_dynamics import vehicle_dynamics
from content.drive_profile import drive_profile, distance_profile, tractive_power, energy_consumption

# Title and Description
st.title("Electric Vehicle System Design Tool")

tabs = st.tabs(["Vehicle Dynamics", "Drive Profile"])

with tabs[0]:
    vehicle_dynamics()

with tabs[1]:
    drive_profile()
    distance_profile()
    tractive_power()
    energy_consumption()
