import streamlit as st
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt
import hmac
import numpy as np  # Ensure you import numpy for colors
import time
import matplotlib.patches as patches
import matplotlib.ticker as ticker

#st.cache_data()


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
    """Returns `True` if the user entered the correct password."""
    # Show the login form
    def login_form():
        """Form with widgets to collect user information."""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets["passwords"] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False
            st.session_state["login_attempted"] = True  # Track login attempts

    # Ensure the `login_attempted` state exists to track if the user has attempted to log in
    if "login_attempted" not in st.session_state:
        st.session_state["login_attempted"] = False

    # Return True if the user is validated
    if st.session_state.get("password_correct", False):
        return True

    # Show the login form
    login_form()

    # Show an error message only after an incorrect login attempt
    if st.session_state.get("login_attempted", False) and not st.session_state.get(
        "password_correct", False
    ):
        st.error("😕 User not known or password incorrect")

    return False


if not check_password():
    st.stop()


# Set the Streamlit page layout to wide
st.set_page_config(layout="wide")

# Google Sheets URL

# Define the URLs
#url_202203060 = "https://docs.google.com/spreadsheets/d/1aLZykSqi22G89wa2hN7bUMzYcU9oynCCW4Sns_mGYgk/edit?usp=sharing"
#url_202203061 = "https://docs.google.com/spreadsheets/d/1XVxYCNIWTqMNbdV9waWJSm-ee19CY7LVDd1oSIAMXlk/edit?usp=sharing"
url_202311117 = "https://docs.google.com/spreadsheets/d/1zNN-bHdiQNPuNBKC1pRslH-gnyAt-OyG--zetovBW9g/edit?usp=sharing"
url_202203060 = "https://docs.google.com/spreadsheets/d/1ne248c3eLVqmZta4-DcRSQE3blWMELj1ZUEEPKAuZRM/edit?usp=sharing"
url_202212092 = "https://docs.google.com/spreadsheets/d/1JfBPwXXTxIb4Y1BhgEX_jd3_0ZTudnZ0V3vErsUl_DI/edit?usp=sharing"

# Create a dropdown list in the sidebar to select a URL
url_options = {
    "202311117": url_202311117,
    "202203060": url_202203060,
    "202212092": url_202212092
}

# Move dropdown to the sidebar
selected_url_key = st.sidebar.selectbox("Select a LASER Source", options=list(url_options.keys()))

# Set the selected URL based on the dropdown selection
selected_url = url_options[selected_url_key]

# Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Clear the cache before fetching new data
st.cache_data.clear()

# Fetch data from Google Sheets
data = conn.read(spreadsheet=selected_url, usecols=list(range(0, 15)))

# Check if data is available
if data is not None and not data.empty:
    # Ensure columns have correct names
    data.columns = ["ID", "SerialNumber", "DateTime", "timeMillisecond", "SessionNumber", 
                    "PumpTemperature", "Pump1Temperature", "Pump2Temperature", 
                    "ModuleTemperature", "SeedTemperature", "PumpCurrent", 
                    "Pump1Current", "Pump2Current", "OutputPower", "PumpPower"]
    
    
    
    
    
    
    
    
    # Check if data is available
if data is not None and not data.empty:
    # Ensure columns have correct names
    data.columns = ["ID", "SerialNumber", "DateTime", "timeMillisecond", "SessionNumber", 
                    "PumpTemperature", "Pump1Temperature", "Pump2Temperature", 
                    "ModuleTemperature", "SeedTemperature", "PumpCurrent", 
                    "Pump1Current", "Pump2Current", "OutputPower", "PumpPower"]
    



    
    # Extract SerialNumber (assuming you want to use the first unique SerialNumber)
    serial_number = int(data["SerialNumber"].iloc[0])  # Convert to integer

    # Use columns to layout the title and the rotating icon side by side
    col_title, col_icon = st.columns([8, 1])  # Adjust proportions as needed
    
    # Title in the first column
    with col_title:
        st.markdown(
            f"""
            <div style="font-family: 'Courier Sans', monospace; font-size: 2.5em; color: #85a3e0; text-align: left;">
                Serial No: {serial_number}
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    
    # Rotating icon in the second column
    with col_icon:
        st.markdown(
            """
            <style>
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                .rotating-icon {
                    animation: spin 5s linear infinite; /* Rotate every 5 seconds */
                    transform-origin: center center; /* Rotate around the center */
                    display: inline-block;
                }
            </style>
            <div class="rotating-icon">
                <img src="https://raw.githubusercontent.com/cakkasli/streamlitTest/refs/heads/main/NORBLIS_LOGO.ico" 
                     alt="NORBLIS Logo" width="50">
            </div>
            """,
            unsafe_allow_html=True,
        )
    


    # Add space between the title and the plot
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    

# Filter the data where PumpPower is 16000.0
filtered_data = data[data["PumpPower"] == 16000]
filtered_data = data


# Define the number of samples per hour
samples_per_hour = 120
x_hours = range(len(filtered_data["SeedTemperature"]))
# Create an array for the x-axis that corresponds to hours
x_hours_in_hours = [i / samples_per_hour for i in x_hours]  # Convert samples to hours

# Get unique session numbers and assign rainbow colors
session_numbers = data["SessionNumber"].unique()
colors = plt.cm.rainbow(np.linspace(0, 1, len(session_numbers)))


# Ensure the data has been filtered
if not filtered_data.empty:
    # Create a continuous x-axis (ID) and plot all sessions on it
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))  # 2 rows, 2 columns

    # Plot 1: ID vs ModuleTemperature (continuous plot)
    # axes[0, 0].plot(
    #     x_hours_in_hours,
    #     filtered_data["ModuleTemperature"], 
    #     label="Module Temperature", 
    #     color='blue'
    # )
    last_time = 0  # Initialize the last time variable
    
    for session, color in zip(session_numbers, colors):
        session_data = data[data["SessionNumber"] == session]
        x_hours = range(len(session_data["ModuleTemperature"]))
        
        # Convert samples to hours and adjust for continuity
        hours = [(i / samples_per_hour) + last_time for i in x_hours]  # Add last_time to ensure continuity
        
        # Plot the data for the current session
        axes[0, 0].plot(
            hours, 
            session_data["ModuleTemperature"], 
            label=f"Session {session}", 
            color=color
        )
        
    
        # Update last_time to the end of the current session
        last_time = hours[-1]

        

    # Set labels
    #axes[0, 0].set_xlabel("Run time [Hour]")
    axes[0, 0].set_ylabel("Module Temperature [°C]", fontweight='bold', fontsize='large')
    # axes[0, 0].set_ylim(20, 45)
    # axes[0, 0].set_yticks([20, 25, 30, 35, 40, 45])
    axes[0, 0].autoscale(axis='y', tight=True)
    axes[0, 0].yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
    axes[0, 0].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.0f}'))
    

    # Plot 2: ID vs SeedTemperature (continuous plot)
    # axes[1, 0].plot(
    #     x_hours_in_hours,
    #     filtered_data["SeedTemperature"], 
    #     label="Seed Temperature", 
    #     color='green'
    # )
    # axes[1, 0].set_xlabel("Run time [Hour]", fontweight='bold', fontsize='large')
    # axes[1, 0].set_ylabel("Seed Temperature [°C]", fontweight='bold', fontsize='large')
    # axes[1, 0].autoscale(axis='y', tight=True)
    # axes[1, 0].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.1f}'))
    
    
    
    last_time = 0  # Initialize the last time variable
    
    for session, color in zip(session_numbers, colors):
        session_data = data[data["SessionNumber"] == session]
        x_hours = range(len(session_data["SeedTemperature"]))
        
        # Convert samples to hours and adjust for continuity
        hours = [(i / samples_per_hour) + last_time for i in x_hours]  # Add last_time to ensure continuity
        
        # Plot the data for the current session
        axes[1, 0].plot(
            hours, 
            session_data["SeedTemperature"], 
            label=f"Session {session}", 
            color=color
        )
        
    
        # Update last_time to the end of the current session
        last_time = hours[-1]
        
    axes[1, 0].set_ylabel("Seed Temperature [°C]", fontweight='bold', fontsize='large')
        # axes[0, 0].set_ylim(20, 45)
        # axes[0, 0].set_yticks([20, 25, 30, 35, 40, 45])
    axes[1, 0].autoscale(axis='y', tight=True)
    axes[1, 0].yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
    # axes[1, 0].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.1f}'))
    


    # Get the current limits
    current_ylim = axes[1, 0].get_ylim()
    
    # Apply some padding (for example, 10% more space above and below)
    padding = 0.5 * (current_ylim[1] - current_ylim[0])
    axes[1, 0].set_ylim(current_ylim[0] - padding, current_ylim[1] + padding)
    new_ylim_min = current_ylim[0] - padding
    new_ylim_max = current_ylim[1] + padding
    axes[1, 0].yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
    axes[1, 0].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.1f}'))
    axes[1, 0].set_xlabel("Run time [Hour]", fontweight='bold', fontsize='large')

    # axes[1, 0].set_ylim(30, 32)
    # axes[1, 0].set_yticks([30.0, 30.5, 31.0, 31.5, 32.0])

    # Plot 3: ID vs Pump1Current (continuous plot)
    last_time = 0  # Initialize the last time variable
    
    for session, color in zip(session_numbers, colors):
        session_data = data[data["SessionNumber"] == session]
        x_hours = range(len(session_data["Pump1Current"]))
        
        # Convert samples to hours and adjust for continuity
        hours = [(i / samples_per_hour) + last_time for i in x_hours]  # Add last_time to ensure continuity
        
        # Plot the data for the current session
        axes[0, 1].plot(
            hours, 
            session_data["Pump1Current"] / 1000, 
            label=f"Session {session}", 
            color=color
        )
        
    
        # Update last_time to the end of the current session
        last_time = hours[-1]
        
    #axes[0, 1].set_xlabel("Run time [Hour]")
    axes[0, 1].set_ylabel("Pump1 Current [A]", fontweight='bold', fontsize='large')
    # First, autoscale but without the 'tight' option
    #axes[0, 1].autoscale(axis='y', tight=False)
    
    # Get the current limits
    current_ylim = axes[0, 1].get_ylim()
    
    # Apply some padding (for example, 10% more space above and below)
    padding = 0.5 * (current_ylim[1] - current_ylim[0])
    axes[0, 1].set_ylim(current_ylim[0] - padding, current_ylim[1] + padding)
    new_ylim_min = current_ylim[0] - padding
    new_ylim_max = current_ylim[1] + padding
    axes[0, 1].yaxis.set_major_locator(ticker.MaxNLocator(nbins=6))
    axes[0, 1].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.2f}'))
    

    # Plot 4: ID vs Pump2Current (continuous plot)
    last_time = 0  # Initialize the last time variable
    
    for session, color in zip(session_numbers, colors):
        session_data = data[data["SessionNumber"] == session]
        x_hours = range(len(session_data["Pump2Current"]))
        
        # Convert samples to hours and adjust for continuity
        hours = [(i / samples_per_hour) + last_time for i in x_hours]  # Add last_time to ensure continuity
        
        # Plot the data for the current session
        axes[1, 1].plot(
            hours, 
            session_data["Pump2Current"] /1000, 
            label=f"Session {session}", 
            color=color
        )
        
    
        # Update last_time to the end of the current session
        last_time = hours[-1]
    
    
    axes[1, 1].set_xlabel("Run time [Hour]", fontweight='bold', fontsize='large')
    axes[1, 1].set_ylabel("Pump2 Current [A]", fontweight='bold', fontsize='large')
    # axes[1, 1].set_ylim(9.6, 10.0)
    # axes[1, 1].set_yticks([9.6, 9.7, 9.8, 9.9, 10.0])
    axes[1, 1].autoscale(axis='y', tight=False)

    # Get the current limits
    current_ylim = axes[1, 1].get_ylim()
    
    # Apply some padding (for example, 10% more space above and below)
    padding = 0.5 * (current_ylim[1] - current_ylim[0])
    axes[1, 1].set_ylim(current_ylim[0] - padding, current_ylim[1] + padding)
    new_ylim_min = current_ylim[0] - padding
    new_ylim_max = current_ylim[1] + padding
    axes[1, 1].yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
    axes[1, 1].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.1f}'))

    # Adjust layout for better spacing
    fig.tight_layout(pad=2.0)  # Add padding between subplots

    # Display the plots in Streamlit
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
    st.warning("No data available to plot where PumpPower is 16000.0.")

