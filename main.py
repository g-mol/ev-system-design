import streamlit as st
from content.vehicle_dynamics import vehicle_dynamics
from content.drive_profile import drive_profile
from interface import sidebar_calculations


# Title and Description
st.title("Electric Vehicle System Design Tool")

sidebar_calculations()

tabs = st.tabs(["Vehicle Dynamics", "Drive Profile"])

with tabs[0]:
    vehicle_dynamics()

with tabs[1]:
    drive_profile()