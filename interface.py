import os
import json
import streamlit as st
import config

# Directory and file paths
PROFILES_DIR = "vehicles"
CURRENT_CONFIG_FILE = os.path.join(PROFILES_DIR, "current.json")

# Ensure directories exist
os.makedirs(PROFILES_DIR, exist_ok=True)


def load_current_config():
    """Load the current configuration from a JSON file and set values in config.py."""
    if os.path.exists(CURRENT_CONFIG_FILE):
        with open(CURRENT_CONFIG_FILE, "r") as f:
            current_config = json.load(f)

    # Set the config values
    config.mass = current_config.get("mass", 2570)
    config.vehicle_height = current_config.get("vehicle_height", 3.0)
    config.vehicle_width = current_config.get("vehicle_width", 2.5)
    config.wheel_radius = current_config.get("wheel_radius", 0.3)
    config.top_speed = current_config.get("top_speed", 100)
    config.time_to_100 = current_config.get("time_to_100", 12.0)
    config.gradeability_percent = current_config.get("gradeability_percent", 25.0)

    return current_config


def save_current_config(config_data):
    """Save the current configuration to a JSON file."""
    with open(CURRENT_CONFIG_FILE, "w") as f:
        json.dump(config_data, f)


def save_profile(profile_name):
    config_data = {
        "mass": config.mass,
        "vehicle_height": config.vehicle_height,
        "vehicle_width": config.vehicle_width,
        "wheel_radius": config.wheel_radius,
        "top_speed": config.top_speed,
        "time_to_100": config.time_to_100,
        "gradeability_percent": config.gradeability_percent,
    }

    """Save the current configuration as a named profile."""
    profile_path = os.path.join(PROFILES_DIR, f"{profile_name}.json")
    with open(profile_path, "w") as f:
        json.dump(config_data, f)
    save_current_config(config_data)  # Update current config
    st.rerun()  # Reload the app to update UI


def load_profile(profile_name):
    """Load a profile and save it as the current configuration."""
    profile_path = os.path.join(PROFILES_DIR, f"{profile_name}.json")
    if os.path.exists(profile_path):
        with open(profile_path, "r") as f:
            profile_data = json.load(f)
        save_current_config(profile_data)  # Update current config
        st.rerun()  # Reload the app to update UI
    else:
        st.error(f"Profile '{profile_name}' not found!")


def sidebar_calculations():
    current_config = load_current_config()

    st.sidebar.header("Vehicle Parameters")

    # Vehicle Inputs
    config.mass = st.sidebar.number_input("Vehicle Mass (kg)", min_value=500, max_value=5000, value=config.mass)
    config.vehicle_height = st.sidebar.number_input("Vehicle Height (m)", min_value=1.0, max_value=3.0,
                                                    value=config.vehicle_height)
    config.vehicle_width = st.sidebar.number_input("Vehicle Width (m)", min_value=1.0, max_value=3.0,
                                                   value=config.vehicle_width)

    config.wheel_radius = st.sidebar.number_input("Wheel Radius (m)", min_value=0.1, max_value=1.0,
                                                  value=config.wheel_radius,
                                                  step=0.01)

    st.sidebar.header("Vehicle Requirements")
    config.top_speed = st.sidebar.number_input("Top Speed (km/h)", min_value=0, max_value=400, value=config.top_speed)
    config.time_to_100 = st.sidebar.number_input("Time to 100 km/h (s)", min_value=1.0, max_value=30.0,
                                                 value=config.time_to_100,
                                                 step=1.0)
    config.gradeability_percent = st.sidebar.number_input("Gradeability (%)", min_value=0, max_value=100,
                                                          value=config.gradeability_percent)

    save_current_config(current_config)

    # --- Profile Management ---
    st.sidebar.header("Profile Management")

    # Ensure session state for tracking the last selected profile
    if "last_selected_profile" not in st.session_state:
        st.session_state["last_selected_profile"] = None

    # Get a list of existing vehicles
    profiles = [f.replace(".json", "") for f in os.listdir(PROFILES_DIR) if f.endswith(".json")]
    profiles = [profile for profile in profiles if profile != "current"]

    # Dropdown to select a profile
    selected_profile = st.sidebar.selectbox("Select Profile", options=profiles, index=0)

    # Load the profile only if it is different from the last selected profile
    if selected_profile != st.session_state["last_selected_profile"]:
        st.session_state["last_selected_profile"] = selected_profile  # Update the last selected profile
        load_profile(selected_profile)  # Load the selected profile
        st.rerun()  # Trigger a rerun to update the UI with the new profile values

    # Text input for saving a new profile
    profile_name = st.sidebar.text_input("New Profile Name")

    # Save Profile Button
    if st.sidebar.button("Save Profile"):
        if profile_name.strip():
            save_profile(profile_name.strip())
            st.success(f"Profile '{profile_name.strip()}' saved!")
        else:
            st.error("Please enter a valid profile name to save!")

    st.sidebar.write("#")
    st.sidebar.write("#")
    st.sidebar.write("#")

    st.sidebar.header("Vehicle Coefficients")
    config.km = st.sidebar.number_input("Rotational Inertia Coefficient (k_m)", min_value=1.0, max_value=1.2, value=1.1,
                                        step=0.01)
    config.C0 = st.sidebar.number_input("Static Rolling Resistance Coefficient (C0)", min_value=0.005, max_value=0.05,
                                        value=0.008, step=0.001, format="%.3f")
    config.C1 = st.sidebar.number_input("Speed-dependent Coefficient (C1)", min_value=0.0, max_value=0.00001,
                                        value=0.0000016, step=0.000001, format="%.7f")

    # Convert Units
    config.top_speed_mps = config.top_speed / 3.6
    config.frontal_area = config.vehicle_height * config.vehicle_width
    config.time_to_100_acceleration = (27.78 / config.time_to_100)  # 100 km/h in m/s
