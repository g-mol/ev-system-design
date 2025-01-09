import streamlit as st
from content.vehicle_dynamics import vehicle_dynamics
from content.scenarios import scenarios
from content.drive_profile import drive_profile
from interface import sidebar_calculations

# Title and Description
st.title("Electric Vehicle System Design Tool")

sidebar_calculations()

tabs = st.tabs(["Vehicle Dynamics", "Scenarios", "Drive Profile"])

with tabs[0]:
    vehicle_dynamics()

with tabs[1]:
    scenarios()

with tabs[2]:
    drive_profile()
