import streamlit as st
import subprocess

def run_reports():
    """Run the reports app."""
    st.success("Launching Reports App...")
    subprocess.run(["streamlit", "run", r"C:\Users\USER\Downloads\thesisDatabase\st_reports\app.py"]) 
def run_forms():
    """Run the forms app."""
    st.success("Launching Forms App...")
    subprocess.run(["streamlit", "run", r"C:\Users\USER\Downloads\thesisDatabase\st_reports\database_management.py"])  

# Main Menu
st.title("Project Management System")

menu_choice = st.sidebar.radio(
    "Choose Application:",
    ["Reports", "Database Management"]
)

if menu_choice == "Reports":
    st.subheader("Reports Application")
    st.write("This will open the reports section.")
    if st.button("Launch Reports App"):
        run_reports()

elif menu_choice == "Database Management":
    st.subheader("Database Management Application")
    st.write("This will open the forms for managing database entries.")
    if st.button("Launch Forms App"):
        run_forms()
