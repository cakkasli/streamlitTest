import streamlit as st
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt
import hmac
import numpy as np  # Ensure you import numpy for colors
import time


# Initialize session state keys
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None
if "password" not in st.session_state:
    st.session_state["password"] = None
if "logoff" not in st.session_state:
    st.session_state["logoff"] = False


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


    # Extract SerialNumber (assuming you want to use the first unique SerialNumber)
    str_serial_num = data["SerialNumber"].iloc[0]  # Or use `unique()` if there are multiple

    # Add the title
    st.markdown(
        f"""
        <div style="
            font-family: 'Courier Sans', monospace; 
            font-size: 2.5em; 
            color: #85a3e0;
            text-align: left;
        ">
            Laser Data Analysis
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Get unique session numbers
    session_numbers = data["SessionNumber"].unique()
    colors = plt.cm.rainbow(np.linspace(0, 1, len(session_numbers)))

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

    # Add buttons after the plot
    col1, col2, col3 = st.columns([1, 1, 1])  # Create three equally spaced columns

    with col1:
        if st.button("Clear Cache"):
            st.cache_data.clear()
            st.success("Cache cleared!")

    with col2:
        if st.button("Log Off"):
            # Reset session state
            st.session_state["password_correct"] = False
            st.session_state["username"] = None
            st.session_state["password"] = None
            st.session_state["logoff"] = False  # Reset the logoff flag

            # Provide feedback to the user
            st.success("You have been logged off successfully! Redirecting...")
            time.sleep(1)  # Wait 1 second for feedback to be visible
            st.rerun()  # Rerun to clear the interface

            # Stop execution
            st.stop()

    with col3:
        # Add a button to download the data as a CSV
        if data is not None and not data.empty:  # Ensure there's data to download
            csv = data.to_csv(index=False)  # Convert DataFrame to CSV
            st.download_button(
                label="Download Data as CSV",
                data=csv,
                file_name="data.csv",
                mime="text/csv",
            )
        else:
            st.warning("No data available to download.")
else:
    st.warning("No data available to plot.")
