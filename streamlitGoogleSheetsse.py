import streamlit as st
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt

def generate_drive_download_link(file_url):
    import re

    # Extract the file ID using regex
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', file_url)
    if not match:
        return "Invalid Google Drive URL"
    
    file_id = match.group(1)

    # Construct the direct download link
    download_link = f"https://drive.google.com/uc?export=download&id={file_id}"
    return download_link

# Google Sheets URL
#url = "https://docs.google.com/spreadsheets/d/1Ettpgs-yXvLTPNFNQtJvEMNUcHf2Pa6saqVU0WFkR7k/edit?gid=1310051949#gid=1310051949"
google_drive_url = "https://drive.google.com/file/d/1-MQjsdPqBiTg2trAzWimGstqQ5vAwFez/view?usp=drive_link"
url = generate_drive_download_link(google_drive_url)

# Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch data from Google Sheets
data = conn.read(spreadsheet=url, usecols=[0, 1])

# Display the data in a table
#st.dataframe(data)



# Check if data is available
if data is not None and not data.empty:
    # Ensure columns have correct names
    data.columns = ["index", "value"]
    # Convert the 'value' column to a numeric type
    data["value"] = data["value"].str.replace(",", ".").astype(float)

    # Plot value vs index
    fig, ax = plt.subplots()
    ax.plot(data["index"], data["value"], marker="o", linestyle="-", label="Value vs Index edit1")
    ax.set_xlabel("Index")
    ax.set_ylabel("Value")
    ax.set_title("Value vs Index Plot")
    ax.legend()

    # Display the plot in Streamlit
    st.pyplot(fig)
else:
    st.warning("No data available to plot.")
