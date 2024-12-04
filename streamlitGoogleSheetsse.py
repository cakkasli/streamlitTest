import streamlit as st
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt
import hmac
import numpy as np  # Ensure you import numpy for colors
import time
import matplotlib.patches as patches


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
            st.secrets.passwords[st.session_state["username"]],
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
    serial_number = data["SerialNumber"].iloc[0]  # Or use `unique()` if there are multiple

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
                    transform-origin: 50px 50%; /* Adjust rotation origin */
                    display: inline-block;
                }
            </style>
            <div class="rotating-icon">
                <img src="https://raw.githubusercontent.com/cakkasli/streamlitTest/refs/heads/main/NORBLIS_LOGO.ico" 
                     alt="NORBLIS Logo" width="40">
            </div>
            """,
            unsafe_allow_html=True,
        )



    # Add space between the title and the plot
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
   
    # Get unique session numbers and assign rainbow colors
    session_numbers = data["SessionNumber"].unique()
    colors = plt.cm.rainbow(np.linspace(0, 1, len(session_numbers)))


    # Create a 2x2 grid of plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))  # 2 rows, 2 columns

    
    # Plot 1: ID vs ModuleTemperature with session-based colors    
    for session, color in zip(session_numbers, colors):
        session_data = data[data["SessionNumber"] == session]
        axes[0, 0].plot(
            session_data["ID"], 
            session_data["ModuleTemperature"], 
            label=f"Session {session}", 
            color=color
        )
        
        # Add text annotation for every 6th session with adjusted vertical position
        if session % 3 == 1:
            axes[0, 0].text(
                session_data["ID"].iloc[-1],  # Last ID in the session
                43.0,  # Slightly above the y-axis limit for alignment
                str(session), 
                fontsize=10, fontweight='bold', color='black',
                ha='center', va='bottom'  # Bottom-align the text
            )
            axes[0, 0].text(
                session_data["ID"].iloc[-1],  # Last ID in the session
                41.5,  # Slightly above the y-axis limit for alignment
                "ı", 
                fontsize=10, fontweight='normal', color='black',
                ha='center', va='bottom'  # Bottom-align the text
            )
    
    

    
    # Set axis labels
    axes[0, 0].set_xlabel("ID")
    axes[0, 0].set_ylabel("Module Temperature [°C]")
    
    # Adjust y-axis limits to ensure the numbers are closer
    axes[0, 0].set_ylim(10, 41)


    # Plot 2: ID vs SeedTemperature with session-based colors
    for session, color in zip(session_numbers, colors):
        session_data = data[data["SessionNumber"] == session]
        axes[1, 0].plot(
            session_data["ID"], 
            session_data["SeedTemperature"], 
            label=f"Session {session}", 
            color=color
        )
    axes[1, 0].set_xlabel("ID")
    axes[1, 0].set_ylabel("Seed Temperature [°C]")

    # Plot 3: ID vs Pump1Current with session-based colors
    for session, color in zip(session_numbers, colors):
        session_data = data[data["SessionNumber"] == session]
        axes[0, 1].plot(
            session_data["ID"], 
            session_data["Pump1Current"], 
            label=f"Session {session}", 
            color=color
        )

        # Add text annotation for every 6th session with adjusted vertical position
        if session % 3 == 1:
            axes[0, 0].text(
                session_data["ID"].iloc[-1],  # Last ID in the session
                43.0,  # Slightly above the y-axis limit for alignment
                str(session), 
                fontsize=10, fontweight='bold', color='black',
                ha='center', va='bottom'  # Bottom-align the text
            )
            axes[0, 0].text(
                session_data["ID"].iloc[-1],  # Last ID in the session
                41.5,  # Slightly above the y-axis limit for alignment
                "ı", 
                fontsize=10, fontweight='normal', color='black',
                ha='center', va='bottom'  # Bottom-align the text
            )


    

    
    axes[0, 1].set_xlabel("ID")
    axes[0, 1].set_ylabel("Pump1 Current [mA]")

    # Plot 4: ID vs Pump2Current with session-based colors
    for session, color in zip(session_numbers, colors):
        session_data = data[data["SessionNumber"] == session]
        axes[1, 1].plot(
            session_data["ID"], 
            session_data["Pump2Current"], 
            label=f"Session {session}", 
            color=color
        )
    axes[1, 1].set_xlabel("ID")
    axes[1, 1].set_ylabel("Pump2 Current [mA]")


    # Create a rectangle patch
    box_width = 0.41  # 80% of the figure width
    box_height = 0.040  # Height in figure coordinate system
    box_x = 0.078  # Center the box horizontally
    box_y = 0.900  # Position the box near the top
    
    rect = patches.Rectangle((box_x, box_y), box_width, box_height, linewidth=1, edgecolor='black', facecolor='white', alpha=0.5, transform=fig.transFigure)
    
    # Add the rectangle patch to the figure
    fig.patches.append(rect)

    axes[0, 0].text(
    2800,  # Last ID in the session
    46,  # Slightly above the y-axis limit for alignment
    "Session Number", 
    fontsize=11, fontweight='bold', color='black',
    ha='center', va='bottom'  # Bottom-align the text
    )

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
            st.warning("No data available to download.")
else:
    st.warning("No data available to plot.")





