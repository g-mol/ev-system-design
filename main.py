import streamlit as st
from content.vehicle_dynamics import vehicle_dynamics
from content.drive_profile import drive_profile, distance_profile, tractive_power, energy_consumption
from content.power_train_sizing import powertrain_sizing


# Title and Description
st.title("Electric Vehicle System Design Tool")

tabs = st.tabs(["Vehicle Dynamics", "Drive Profile", "Power Train Sizing"])

with tabs[0]:
    vehicle_dynamics()

with tabs[1]:
    drive_profile()
    distance_profile()
    tractive_power()
    energy_consumption()

with tabs[2]:
    powertrain_sizing()


