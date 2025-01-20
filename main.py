import streamlit as st
from content.about import about
from content.scenarios import scenarios
from content.drive_train import drive_train
from content.drive_profile import drive_profile
from content.battery import battery
from content.generate_gradient import generate_gradient
from content.logistics import logistics
from interface import sidebar_calculations

# Title and Description
st.title("Electric Vehicle System Design Tool")

sidebar_calculations()
# "Vehicle Dynamics",
tabs = st.tabs(["About", "Scenarios", "Drive Train", "Drive Profile", "Battery", "Logistics"])

with tabs[0]:
    about()
    # vehicle_dynamics()

with tabs[1]:
    scenarios()

with tabs[2]:
    drive_train()

with tabs[3]:
    drive_profile()

with tabs[4]:
    battery()

# with tabs[5]:
#     generate_gradient()

with tabs[5]:
    logistics()