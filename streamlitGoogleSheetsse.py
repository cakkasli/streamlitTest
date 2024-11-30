import streamlit as st
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt


# Add a button to clear the cache
if st.button("Clear Cache"):
    st.cache_data.clear()
    st.success("Cache cleared!")

# Google Sheets URL
#url = "https://docs.google.com/spreadsheets/d/1Ettpgs-yXvLTPNFNQtJvEMNUcHf2Pa6saqVU0WFkR7k/edit?gid=1310051949#gid=1310051949"
url = "https://docs.google.com/spreadsheets/d/1acXABDP5REh7SyUuICntxdGzZ0QtD_YPyShohRJGJZU/edit?usp=sharing"

# Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch data from Google Sheets
data = conn.read(spreadsheet=url, usecols=list(range(0, 15)))

# Display the data in a table
#st.dataframe(data

# Check if data is available
if data is not None and not data.empty:
    # Ensure columns have correct names
    data.columns = ["ID", "SerialNumber", "DateTime", "timeMillisecond", "SessionNumber", 
                     "PumpTemperature", "Pump1Temperature", "Pump2Temperature", 
                     "ModuleTemperature", "SeedTemperature", "PumpCurrent", 
                     "Pump1Current", "Pump2Current", "OutputPower", "PumpPower"]

    # Convert the 'value' column to a numeric type
    #data["value"] = data["value"].str.replace(",", ".").astype(float)

    # Plot value vs index
    # Assuming 'data' is the DataFrame already loaded
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # 1 row, 2 columns
    
    # Plot 1: ID vs SeedTemperature
    axes[0].plot(data["ID"], data["SeedTemperature"], marker=".", linestyle="-", color="blue", label="SeedTemperature")
    axes[0].set_xlabel("ID")
    axes[0].set_ylabel("SeedTemperature")
    axes[0].set_title("ID vs SeedTemperature")
    axes[0].legend()
    
    # Plot 2: ID vs ModuleTemperature
    axes[1].plot(data["ID"], data["ModuleTemperature"], marker=".", linestyle="-", color="green", label="ModuleTemperature")
    axes[1].set_xlabel("ID")
    axes[1].set_ylabel("ModuleTemperature")
    axes[1].set_title("ID vs ModuleTemperature")
    axes[1].legend()

    # Adjust layout for better spacing
    fig.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)
else:
    st.warning("No data available to plot.")
