import streamlit as st
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt
import hmac

def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


if not check_password():
    st.stop()

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

    
    # Add a button to download the data as a CSV
    csv = data.to_csv(index=False)  # Convert DataFrame to CSV
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name="data.csv",
        mime="text/csv",
    )
    
    # Convert the 'value' column to a numeric type
    #data["value"] = data["value"].str.replace(",", ".").astype(float)

    # Plot value vs index
    # Assuming 'data' is the DataFrame already loaded
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # 1 row, 2 columns
    
    # Plot 1: ID vs SeedTemperature
    axes[0].plot(data["ID"], data["SeedTemperature"], marker=".", linestyle="-", color="blue", label="SeedTemperature")
    axes[0].set_xlabel("ID")
    axes[0].set_ylabel("SeedTemperature")
    axes[0].set_title("Seed Temperature")
    
    # Plot 2: ID vs ModuleTemperature
    axes[1].plot(data["ID"], data["ModuleTemperature"], marker=".", linestyle="-", color="green", label="ModuleTemperature")
    axes[1].set_xlabel("ID")
    axes[1].set_ylabel("ModuleTemperature")
    axes[1].set_title("Module Temperature")

    # Adjust layout for better spacing
    fig.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)
else:
    st.warning("No data available to plot.")
