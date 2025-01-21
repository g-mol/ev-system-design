import streamlit as st
import math
import config


def logistics():
    st.title("Logistics")

    # Description
    st.write("The calculations below are based on the current area population size, the amount of packages delivered "
             "per person per day, and the amount of restaurant crates delivered per person per day. The calculations "
             "are used to determine the amount of vans needed to deliver the packages and crates in the area.")

    st.markdown("---")

    st.markdown(f"### **Given**")
    packages_per_person_per_day = st.number_input(
        "Packages delivered per person per day (based on data in the Netherlands)", min_value=0.0,
        value=0.062837753, format="%.5f")

    st.markdown("---")
    st.markdown(f"### **Inputs**")
    population = st.number_input("Area population size", min_value=0, value=159640)

    packages_per_day_in_area = population * packages_per_person_per_day

    st.markdown("")
    st.markdown("")
    st.success(f"**Total packages per day in area:** {packages_per_day_in_area:.0f} packages")

    st.markdown("---")
    st.markdown(f"### **Requirements**")
    packaged_per_hour = st.number_input("Packages delivered per hour", min_value=0, value=15)
    shift_length = st.number_input("Shift length per day in hours", min_value=0, value=4)
    amount_of_shifts = st.number_input("Amount of shifts per day", min_value=0, value=3)
    total_working_hours_per_day = shift_length * amount_of_shifts

    minimum_vans_needed = math.ceil(packages_per_day_in_area / (packaged_per_hour * total_working_hours_per_day))
    st.success(f"**Minimum needed vans for normal packages in area:** {minimum_vans_needed} vans")

    theoretical_amount_of_vans = minimum_vans_needed * amount_of_shifts

    st.markdown("---")
    st.markdown(f"### **Volume packages**")

    # maximum_packages_per_van = st.number_input("Maximum packages per van", min_value=0, value=180)
    packages_per_van = math.ceil(packages_per_day_in_area / theoretical_amount_of_vans)

    st.success(f"**Minimum packages per van in current scenario:** {packages_per_van} packages")

    selected_amount_of_packages_per_van = st.number_input("Selected amount of packages per van", min_value=0, value=80)

    package_size = st.number_input("Average package size (m³)", min_value=0.0, value=0.027)

    package_volume = selected_amount_of_packages_per_van * package_size
    package_volume_safety_factor = st.number_input("Package volume safety factor", min_value=0.0, value=1.2)
    total_package_volume = package_volume * package_volume_safety_factor

    st.markdown("")
    st.success(f"**Total volume of packages per van:** {package_volume:.2f} m³ -> {total_package_volume:.2f} m³")

    st.markdown("---")
    st.markdown(f"### **Crates**")
    crate_depth = st.number_input("Crate depth (m)", min_value=0.0, value=0.4)
    crate_width = st.number_input("Crate width (m)", min_value=0.0, value=0.6)
    crate_height = st.number_input("Crate height + shelf height + air gap (m)", min_value=0.0, value=0.3)
    internal_crate_volume = st.number_input("Internal crate volume (m³)", min_value=0.001, value=0.045)

    amount_of_crates = math.ceil(total_package_volume / internal_crate_volume)
    st.success(f"**Amount of crates needed:** {amount_of_crates}")

    st.markdown("---")
    st.markdown(f"### **Van size**")
    van_height = st.number_input("Van height (m)", min_value=0.1, value=1.5)
    van_width = 2 * crate_width
    st.success(f"**Internal van width:** {van_width:.2f} m")
    amount_of_crates_vertically = math.floor(van_height / crate_height)
    st.success(f"**Amount of crates vertically:** {amount_of_crates_vertically}")

    amount_of_crates_lengthwise = math.ceil(amount_of_crates / amount_of_crates_vertically / 2)
    st.success(f"**Needed amount of crates lengthwise:** {amount_of_crates_lengthwise}")

    van_length = amount_of_crates_lengthwise * crate_depth

    st.success(f"**Needed internal van length:** {van_length:.2f} m")

    st.markdown("---")
    st.markdown(f"### **Restaurants**")

    restaurant_crates_per_person_per_day = st.number_input(
        "Restaurant crates delivered per person per day (based on data in the Netherlands)", min_value=0.0,
        value=0.007774, format="%.8f")

    restaurant_crates_per_day_in_area = population * restaurant_crates_per_person_per_day

    st.success(f"**Total restaurant crates per day in area:** {restaurant_crates_per_day_in_area:.0f} crates")

    minimum_vans_needed_restaurant = math.ceil(restaurant_crates_per_day_in_area / amount_of_crates)

    st.success(f"**Minimum needed vans for restaurant crates in area:** {minimum_vans_needed_restaurant} vans")

    st.markdown("---")
    st.markdown(f"### **Total needed vans**")
    total_vans_needed = minimum_vans_needed + minimum_vans_needed_restaurant
    st.error(f"**Total needed vans in area:** {total_vans_needed} vans")
