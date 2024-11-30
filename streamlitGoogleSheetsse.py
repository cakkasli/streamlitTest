import streamlit as st
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

# Password protection function
def check_password():
    # Initialize session state for password
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    # If the password has not been entered yet
    if not st.session_state["password_correct"]:
        # Prompt user for password
        password = st.text_input("Enter the password:", type="password")
        if st.button("Login"):
            if password == "mypassword123":  # Set your password here
                st.session_state["password_correct"] = True
                st.experimental_set_query_params(authorized="true")  # Set query parameter to indicate success
                st.experimental_rerun()  # Trigger a rerun safely after setting session state
            else:
                st.error("Incorrect password.")
        return False
    return True

# Check for query parameters to bypass password input on rerun
if st.experimental_get_query_params().get("authorized") == ["true"]:
    st.session_state["password_correct"] = True

# Main app logic
if check_password():
    # Add a button to clear the cache
    if st.button("Clear Cache"):
        st.cache_data.clear()
        st.success("Cache cleared!")

    # Google Sheets URL
    url = "https://docs.google.com/spreadsheets/d/1acXABDP5REh7SyUuICntxdGzZ0QtD_YPyShohRJGJZU/edit?usp=sharing"

    # Connect to Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Fetch data from Google Sheets
    data = conn.read(spreadsheet=url, usecols=list(range(0, 15)))

    # Check if data is available
    if data is not None and not data.empty:
        # Ensure columns have correct names
        data.columns = ["ID", "SerialNumber", "DateTime", "timeMillisecond", "SessionNumber", 
                         "PumpTemperature", "Pump1Temperature", "Pump2Temperature", 
                         "ModuleTemperature", "SeedTemperature", "PumpCurrent", 
                         "Pump1Current", "Pump2Current", "OutputPower", "PumpPower"]

        # Add a button to download the data as a CSV
        csv = data.to_csv(index=False)  # Convert DataFrame to CSV
        st.download_button(
            label="Download Data as CSV",
            data=csv,
            file_name="data.csv",
            mime="text/csv",
        )

        # Get unique session numbers
        session_numbers = data["SessionNumber"].unique()
        colors = cm.rainbow(np.linspace(0, 1, len(session_numbers)))

        # Plot value vs index
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # 1 row, 2 columns

        # Plot 1: ID vs SeedTemperature with session-based colors
        for session, color in zip(session_numbers, colors):
            session_data = data[data["SessionNumber"] == session]
            axes[0].plot(
                session_data["ID"],
                session_data["SeedTemperature"],
                marker=".",
                linestyle="-",
                color=color
            )
        axes[0].set_xlabel("ID")
        axes[0].set_ylabel("SeedTemperature")
        axes[0].set_title("Seed Temperature")

        # Plot 2: ID vs ModuleTemperature with session-based colors
        for session, color in zip(session_numbers, colors):
            session_data = data[data["SessionNumber"] == session]
            axes[1].plot(
                session_data["ID"],
                session_data["ModuleTemperature"],
                marker=".",
                linestyle="-",
                color=color
            )
        axes[1].set_xlabel("ID")
        axes[1].set_ylabel("ModuleTemperature")
        axes[1].set_title("Module Temperature")

        # Adjust layout for better spacing
        fig.tight_layout()

        # Display the plot in Streamlit
        st.pyplot(fig)
    else:
        st.warning("No data available to plot.")
