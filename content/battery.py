import streamlit as st
import math
import config


def battery():
    st.title("Battery")
    st.write("The total battery capacity required for the electric vehicle is calculated based on the energy "
             "consumption in the drive profile and the required range. After that the battery pack configuration "
             "is determined based on the motor voltage and cell specifications.")
    st.markdown("---")

    if "wh_per_km" not in st.session_state:
        st.session_state["wh_per_km"] = 1

    # Step 1: Display energy consumption per kilometer
    st.subheader("1: Energy Consumption")
    energy_consumption_per_km = st.session_state["wh_per_km"] / 1000  # Convert Wh/km to kWh/km
    st.write(f"**Energy Consumption per Kilometer:** {st.session_state["wh_per_km"]:.0f} Wh/km")

    # Step 2: Input total distance
    st.subheader("2: Total Distance")
    total_distance_km = st.number_input("Enter the total distance (km):", min_value=10, max_value=1000, value=150,
                                        step=10)
    total_energy_required_kwh = total_distance_km * energy_consumption_per_km
    st.write(f"**Total Energy Required:** {total_energy_required_kwh:.2f} kWh")

    # Step 3: Input battery efficiency
    st.subheader("3: Battery Efficiency")
    battery_efficiency = st.number_input("Enter battery efficiency (%):", min_value=50, max_value=100, value=95,
                                         step=1) / 100
    usable_capacity_kwh = total_energy_required_kwh / battery_efficiency
    st.write(f"**Usable Capacity:** {usable_capacity_kwh:.2f} kWh")

    # Step 4: Calculate total capacity
    st.subheader("4: State of Charge (SoC) Range")
    min_soc = st.number_input("Enter minimum SoC (%):", min_value=0, max_value=100, value=0, step=1) / 100
    max_soc = st.number_input("Enter maximum SoC (%):", min_value=0, max_value=100, value=100, step=1) / 100

    subtotal_capacity_kwh = usable_capacity_kwh / (max_soc - min_soc)
    st.write(f"**Capacity including SoC:** {subtotal_capacity_kwh:.2f} kWh")

    # Step 5: Auxiliary load estimate
    st.subheader("5: Auxiliary Load Estimate")
    auxiliary_load_factor = st.number_input("Auxiliary Load Factor (% increase):", min_value=0, max_value=50, value=10,
                                            step=1) / 100
    total_capacity_kwh = usable_capacity_kwh * (1 + auxiliary_load_factor)

    # Step 6: Summary
    st.subheader("6: Result")
    st.success(f"**Total Capacity:** {total_capacity_kwh:.2f} kWh")

    if max_soc < min_soc:
        st.warning("Max SoC must be greater than Min SoC")

    # st.write(f"**Energy Consumption per Kilometer:** {energy_consumption_per_km:.3f} kWh/km")
    # st.write(f"**Total Distance:** {total_distance_km} km")
    # st.write(f"**Total Energy Required:** {total_energy_required_kwh:.2f} kWh")
    # st.write(f"**Usable Capacity:** {usable_capacity_kwh:.2f} kWh")
    # st.write(f"**Total Capacity:** {total_capacity_kwh:.2f} kWh" if max_soc > min_soc else "N/A")

    st.markdown("---")
    st.title("Battery Pack Configuration")
    st.markdown("---")

    # Inputs for motor voltage and cell specifications
    st.subheader("1: Motor Voltage and Cell Specifications")
    motor_voltage = st.number_input("Desired Nominal Voltage (V):", min_value=100, max_value=1000, value=350, step=10)
    nominal_cell_voltage = st.number_input("Nominal Voltage per Cell (V):", value=3.2, step=0.1)
    charged_cell_voltage = st.number_input("Fully Charged Voltage per Cell (V):", value=3.6, step=0.1)
    discharged_cell_voltage = st.number_input("Fully Discharged Voltage per Cell (V):", value=2.5, step=0.1)
    cell_capacity_ah = st.number_input("Cell Capacity (Ah):", value=100, step=10)

    # Calculate number of cells in series
    st.subheader("2: Number of Cells in Series")
    cells_in_series = motor_voltage / nominal_cell_voltage
    rounded_cells_in_series = math.ceil(cells_in_series)

    st.latex(r"N_s = \frac{\text{Desired Nominal Voltage}}{\text{Nominal Voltage per Cell}}")
    st.success(f"**Number of Cells in Series:** {cells_in_series} -> {rounded_cells_in_series}")

    # Calculate pack voltages
    nominal_pack_voltage = rounded_cells_in_series * nominal_cell_voltage
    charged_pack_voltage = rounded_cells_in_series * charged_cell_voltage
    discharged_pack_voltage = rounded_cells_in_series * discharged_cell_voltage

    st.write(f"**Nominal Pack Voltage:** {nominal_pack_voltage:.2f} V")
    st.write(f"**Fully Charged Pack Voltage:** {charged_pack_voltage:.2f} V")
    st.write(f"**Fully Discharged Pack Voltage:** {discharged_pack_voltage:.2f} V")

    # Calculate energy per string
    st.subheader("3: Energy Per Series String")
    energy_per_string_kwh = nominal_pack_voltage * cell_capacity_ah / 1000  # Convert to kWh

    st.latex(r"\text{Energy per String} = \text{Nominal Pack Voltage} \times \text{Cell Capacity}")
    st.success(f"**Energy per String:** {energy_per_string_kwh:.2f} kWh")

    # Calculate number of parallel strings
    st.subheader("4: Number of Parallel Strings")
    st.write(f"**Total Required Capacity:** {total_capacity_kwh:.2f} kWh")
    parallel_strings = total_capacity_kwh / energy_per_string_kwh
    rounded_parallel_strings = math.ceil(parallel_strings)

    st.latex(r"N_p = \frac{\text{Total Capacity}}{\text{Energy per String}}")
    st.success(f"**Number of Parallel Strings:** {parallel_strings:.2f} -> {rounded_parallel_strings}")

    # Total cells and capacity
    st.subheader("5: Total Cells and Final Capacity")
    total_cells = rounded_cells_in_series * rounded_parallel_strings
    final_capacity_kwh = energy_per_string_kwh * rounded_parallel_strings

    st.write(f"**Total Cells:** {total_cells}")
    st.write(f"**Final Total Capacity:** {final_capacity_kwh:.2f} kWh")

    # Weight and volume calculations
    st.subheader("6: Weight and Volume")
    specific_energy_wh_per_kg = st.number_input("Specific Energy (Wh/kg):", min_value=50, max_value=300, value=120,
                                                step=10)
    energy_density_wh_per_l = st.number_input("Energy Density (Wh/L):", min_value=100, max_value=500, value=235,
                                              step=10)

    weight_kg = total_capacity_kwh * 1000 / specific_energy_wh_per_kg
    volume_l = total_capacity_kwh * 1000 / energy_density_wh_per_l

    st.write(f"**Weight:** {weight_kg:.2f} kg")
    st.write(f"**Volume:** {volume_l:.2f} L")

    # Summary table
    st.subheader("Battery Pack Summary")
    summary_table = f"""
    | Specification      | Value           |
    |--------------------|-----------------|
    | Total Capacity     | **{final_capacity_kwh:.2f} kWh** |
    | Total Cells        | **{total_cells}**                |
    | Architecture       | **{nominal_pack_voltage:.2f} V** |
    | Weight             | **{weight_kg:.2f} kg**           |
    | Volume             | **{volume_l:.2f} L**             |
    """
    st.markdown(summary_table)
