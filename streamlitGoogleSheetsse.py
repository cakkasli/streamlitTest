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
data = conn.read(spreadsheet=url, usecols=[0, 1])

# Display the data in a table
#st.dataframe(data)


# Check if data is available
if data is not None and not data.empty:
    # Ensure columns have correct names
    data.columns = ["index", "value"]
    # Convert the 'value' column to a numeric type
    if data["value"].str.contains(",").any():
        data["value"] = data["value"].str.replace(",", ".").astype(float)


    # Plot value vs index
    fig, ax = plt.subplots()
    ax.plot(data["index"], data["value"], marker="o", linestyle="-", label="Value vs Index")
    ax.set_xlabel("Index")
    ax.set_ylabel("Value")
    ax.set_title("Value vs Index Plot")
    ax.legend()

    # Display the plot in Streamlit
    st.pyplot(fig)
else:
    st.warning("No data available to plot.")
