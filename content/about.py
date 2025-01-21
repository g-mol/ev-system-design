import streamlit as st


def about():
    st.write(
        """
        # About

        This tool is designed to help you design an electric vehicle system. You can change the vehicle parameters 
        and requirements in the sidebar to see how they affect the vehicle's performance and needed power, torque, 
        gear ratio, energy usage and battery capacity.
        
        The inputs in the sidebar can be changed and saved as a profile. This profile can be loaded at a later time to
        continue working on the vehicle design or compare different designs.
        
        ## Features
        - **Scenarios**: Explore different driving scenarios and ultimately find the maximum required torque and power 
        at the wheels.
        - **Drive Train**: Calculate the gear ratio and needed torque at the motor using the chosen motors maximum RPM.
        - **Drive Profile**: Calculate the energy usage and battery capacity needed for the chosen driving profile. 
        Different drive profiles can be chosen to see the effect on the energy usage.
        - **Battery**: Calculate the battery capacity based on the energy usage and required range.
        - **Logistics**: Calculate the amount of vehicles needed for the chosen area and the size of the loading area.
        - **Financials**: Calculate the economic feasibility of the delivery system, including investment, ongoing 
        costs, and break-even analysis.
        
        ### Disclaimer
        This tool is created for the course "Electric Vehicle System Design" at the University of Twente. Feel free to
        use this tool for your own projects.
        
        ### Authors
        - Geert Mol
        - Thomas de Rooij
        - Christina Keysers
        - Eneko Urcelay
        """
    )
