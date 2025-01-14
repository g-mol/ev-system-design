import streamlit as st
from content.vehicle_dynamics import vehicle_dynamics
from content.scenarios import scenarios
from content.drive_train import drive_train
from content.drive_profile import drive_profile
from content.battery import battery
from interface import sidebar_calculations

# Title and Description
st.title("Electric Vehicle System Design Tool")

sidebar_calculations()
# "Vehicle Dynamics",
tabs = st.tabs(["Scenarios", "Drive Train", "Drive Profile", "Battery"])

# with tabs[0]:
    # vehicle_dynamics()

with tabs[0]:
    scenarios()

with tabs[1]:
    drive_train()

with tabs[2]:
    drive_profile()

with tabs[3]:
    battery()
