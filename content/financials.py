import streamlit as st
import math
import pandas as pd
import plotly.graph_objects as go


def financials():
    st.title("Economic Validity of the Delivery System")

    # Description
    st.write(
        "This page calculates the economic feasibility of the delivery system, including investment, ongoing costs, and break-even analysis.")

    st.markdown("---")

    # --- Initial Costs ---
    st.markdown("### **Initial Costs**")
    number_of_cars = st.session_state["total_vans_needed"]
    st.write(f"**Number of vans:** {number_of_cars:.0f}")

    distribution_centre_cost = st.number_input("Distribution Centre Cost (\u20ac):", min_value=0, value=15000000,
                                               step=1000)
    cost_per_car = st.number_input("Cost per Van (\u20ac):", min_value=0, value=20000, step=1000)
    software_cost = st.number_input("Software Cost (\u20ac):", min_value=0, value=100000, step=1000)

    total_investment = distribution_centre_cost + (number_of_cars * cost_per_car) + software_cost
    st.success(f"**Total Investment:** \u20ac{total_investment:,.0f}")

    st.markdown("---")

    # --- Ongoing Costs ---
    st.markdown("### **Ongoing Costs per Month (per car)**")
    battery_capacity_kwh = st.session_state["final_capacity_kwh"]
    st.write(f"**Battery Capacity per Car:** {battery_capacity_kwh} kWh")
    kwh_price = st.number_input("Price per kWh (\u20ac):", min_value=0.0, value=0.35, step=0.01)
    charging_cost = battery_capacity_kwh * kwh_price
    st.write(f"**Charging Cost per Car:** \u20ac{charging_cost:,.2f}")
    maintenance_cost = st.number_input("Maintenance Cost (\u20ac):", min_value=0, value=70, step=1)
    other_costs = st.number_input(
        "Other Costs (e.g., ANWB, Tuv, Toegang stadserf) (\u20ac):", min_value=0, value=14, step=1,
        help="Examples: ANWB, Tuv, and Toegang stadserf in the Netherlands."
    )
    insurance_cost = st.number_input("Insurance Cost (\u20ac):", min_value=0, value=25, step=1)
    road_tax_cost = st.number_input("Road Tax (\u20ac):", min_value=0, value=10, step=1)

    monthly_cost_per_car = charging_cost + maintenance_cost + other_costs + insurance_cost + road_tax_cost
    total_monthly_car_cost = monthly_cost_per_car * number_of_cars

    st.success(f"**Total Monthly Cost for Cars:** \u20ac{total_monthly_car_cost:,.0f}")

    st.markdown("### **Ongoing Costs (Distribution Centre per Month)**")
    hourly_employee_cost = st.number_input("Hourly Cost per Employee (\u20ac):", min_value=0.0, value=30.0, step=0.5)
    # monthly costs driver, car is used for 12 hours a day
    driver_hours_per_day = st.session_state["total_working_hours_per_day"]
    monthly_cost_drivers = number_of_cars * driver_hours_per_day * 30 * hourly_employee_cost
    st.write(f"**Monthly Cost for Drivers:** \u20ac{monthly_cost_drivers:,.0f}")
    distribution_centre_employees = st.number_input("Number of Distribution Centre Employees:", min_value=0, value=80,
                                                    step=1)
    distribution_centre_working_hours_per_day = st.number_input("Working Hours per Day:", min_value=0, value=8, step=1)
    monthly_cost_distribution_centre_employees = distribution_centre_employees * distribution_centre_working_hours_per_day * 30 * hourly_employee_cost

    st.write(
        f"**Monthly Cost for Distribution Centre Employees:** \u20ac{monthly_cost_distribution_centre_employees:,.0f}")

    distribution_centre_kwh_usage = st.number_input("Distribution Centre kWh Usage per Month:", min_value=0,
                                                    value=100000, step=100)
    distribution_centre_energy_cost = distribution_centre_kwh_usage * kwh_price
    st.write(f"**Monthly Energy Cost for Distribution Centre:** \u20ac{distribution_centre_energy_cost:,.0f}")
    extra_maintenance_cost = st.number_input("Extra Maintenance Costs (\u20ac):", min_value=0, value=100000, step=1000)


    total_monthly_distribution_cost = (
            distribution_centre_energy_cost + extra_maintenance_cost + monthly_cost_drivers + monthly_cost_distribution_centre_employees
    )

    st.success(f"**Total Monthly Cost for Distribution Centre:** \u20ac{total_monthly_distribution_cost:,.0f}")

    total_monthly_cost = total_monthly_car_cost + total_monthly_distribution_cost
    st.error(f"**Total Monthly Costs:** \u20ac{total_monthly_cost:,.0f}")

    st.markdown("---")

    # --- Delivery Metrics ---
    st.markdown("### **Delivery Metrics**")
    crates_per_day = st.session_state["restaurant_crates_per_day_in_area"]
    packages_per_day = st.session_state["packages_per_day_in_area"]

    st.write(f"**Crates Delivered Per Day:** {crates_per_day:.0f}")
    st.write(f"**Packages Delivered Per Day:** {packages_per_day:.0f}")

    crates_per_month = crates_per_day * 30
    packages_per_month = packages_per_day * 30

    cost_per_crate = st.number_input("Income per Crate (\u20ac):", min_value=0, value=10, step=1)
    cost_per_package = st.number_input("Income per Package (\u20ac):", min_value=0, value=5, step=1)

    revenue_per_month = (crates_per_month * cost_per_crate) + (packages_per_month * cost_per_package)
    st.success(f"**Revenue per Month:** \u20ac{revenue_per_month:,.2f}")

    break_even_months = total_investment / (revenue_per_month - total_monthly_cost)
    st.success(f"**Break Even Point:** {break_even_months:.2f} months ({break_even_months / 12:.2f} years)")

    st.markdown("---")

    # --- Graph: Budget Over Time ---
    st.markdown("### **Budget Over Time**")
    time_years = 2 * math.ceil(break_even_months / 12)  # Two times the break-even point
    months = list(range(1, time_years * 12 + 1))

    budget_over_time = [-(total_investment + total_monthly_cost * i) + revenue_per_month * i for i in months]
    budget_df = pd.DataFrame({"Month": months, "Budget (\u20ac)": budget_over_time})

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=budget_df["Month"] / 12,
        y=budget_df["Budget (\u20ac)"],
        mode="lines",
        name="Budget Over Time",
        line=dict(color="green")
    ))

    fig.update_layout(
        title="Budget Over Time",
        xaxis_title="Years",
        yaxis_title="Budget (\u20ac)",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)
