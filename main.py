import streamlit as st
import sqlite3
import os
import pandas as pd
from database_setup import create_database
import matplotlib.pyplot as plt


# Define connection function
def get_connection():
    # Database file path
    db_path = 'farm_management.db'

    # Check if the database file exists
    if not os.path.exists(db_path):
        # If not, create the database
        create_database()

    return sqlite3.connect(db_path)


# Define CRUD functions for each table
def add_record(table, data):
    conn = get_connection()
    cursor = conn.cursor()
    placeholders = ', '.join('?' * len(data))
    cursor.execute(f"INSERT INTO {table} VALUES (NULL, {placeholders})", data)
    conn.commit()
    conn.close()


def update_record(table, set_values, condition):
    conn = get_connection()
    cursor = conn.cursor()
    set_clause = ', '.join([f"{col} = ?" for col in set_values.keys()])
    condition_clause = ' AND '.join([f"{col} = ?" for col in condition.keys()])
    values = list(set_values.values()) + list(condition.values())
    cursor.execute(f"UPDATE {table} SET {set_clause} WHERE {condition_clause}", values)
    conn.commit()
    conn.close()


def delete_record(table, condition):
    conn = get_connection()
    cursor = conn.cursor()
    condition_clause = ' AND '.join([f"{col} = ?" for col in condition.keys()])
    values = list(condition.values())
    cursor.execute(f"DELETE FROM {table} WHERE {condition_clause}", values)
    conn.commit()
    conn.close()


def fetch_data(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return data


def show_home():

    st.title("Welcome to FarmFlow Ghana")

    st.markdown("### Our Motto")
    st.markdown(
        """
        **Empowering Farmers, Enhancing Yields, Ensuring Prosperity**
        """
    )


def show_crop_planning():
    st.title("Crop Planning")
    st.write("Manage crop planning here.")

    with st.expander("Add Crop"):
        with st.form("add_crop_form"):
            name = st.text_input("Crop Name")
            type_ = st.text_input("Type")
            growth_duration = st.number_input("Growth Duration", min_value=1)
            if st.form_submit_button("Add Crop"):
                add_record("Crop", (name, type_, growth_duration))
                st.success("Crop added successfully!")

    with st.expander("Update Crop"):
        with st.form("update_crop_form"):
            crop_id = st.number_input("Crop ID to update", min_value=1)
            name = st.text_input("New Crop Name")
            type_ = st.text_input("New Type")
            growth_duration = st.number_input("New Growth Duration", min_value=1)
            if st.form_submit_button("Update Crop"):
                update_record("Crop", {"Name": name, "Type": type_, "GrowthDuration": growth_duration},
                              {"CropID": crop_id})
                st.success("Crop updated successfully!")

    with st.expander("Delete Crop"):
        with st.form("delete_crop_form"):
            crop_id = st.number_input("Crop ID to delete", min_value=1)
            if st.form_submit_button("Delete Crop"):
                delete_record("Crop", {"CropID": crop_id})
                st.success("Crop deleted successfully!")

    with st.expander("View Crops"):
        query = "SELECT * FROM Crop"
        data = fetch_data(query)
        df = pd.DataFrame(data, columns=["CropID", "Name", "Type", "GrowthDuration"])
        st.write(df)


def show_inventory_management():
    st.title("Inventory Management")
    st.write("Track and manage inventory here.")

    with st.expander("Add Inventory Item"):
        with st.form("add_inventory_form"):
            item_name = st.text_input("Item Name")
            quantity = st.number_input("Quantity", min_value=1)
            type_ = st.text_input("Type")
            purchase_date = st.date_input("Purchase Date")
            if st.form_submit_button("Add Inventory Item"):
                add_record("Inventory", (item_name, quantity, type_, purchase_date.isoformat()))
                st.success("Inventory item added successfully!")

    with st.expander("Update Inventory Item"):
        with st.form("update_inventory_form"):
            inventory_id = st.number_input("Inventory ID to update", min_value=1)
            item_name = st.text_input("New Item Name")
            quantity = st.number_input("New Quantity", min_value=1)
            type_ = st.text_input("New Type")
            purchase_date = st.date_input("New Purchase Date")
            if st.form_submit_button("Update Inventory Item"):
                update_record("Inventory", {"ItemName": item_name, "Quantity": quantity, "Type": type_,
                                            "PurchaseDate": purchase_date.isoformat()}, {"InventoryID": inventory_id})
                st.success("Inventory item updated successfully!")

    with st.expander("Delete Inventory Item"):
        with st.form("delete_inventory_form"):
            inventory_id = st.number_input("Inventory ID to delete", min_value=1)
            if st.form_submit_button("Delete Inventory Item"):
                delete_record("Inventory", {"InventoryID": inventory_id})
                st.success("Inventory item deleted successfully!")

    with st.expander("View Inventory"):
        query = "SELECT * FROM Inventory"
        data = fetch_data(query)
        df = pd.DataFrame(data, columns=["InventoryID", "ItemName", "Quantity", "Type", "PurchaseDate"])
        st.write(df)


def show_financial_records():
    st.title("Financial Records")
    st.write("Manage financial records here.")

    with st.expander("Add Financial Record"):
        with st.form("add_financial_record_form"):
            record_date = st.date_input("Record Date")
            income = st.number_input("Income", min_value=0.0)
            expenses = st.number_input("Expenses", min_value=0.0)
            if st.form_submit_button("Add Financial Record"):
                add_record("FinancialRecord", (record_date.isoformat(), income, expenses))
                st.success("Financial record added successfully!")

    with st.expander("Update Financial Record"):
        with st.form("update_financial_record_form"):
            record_id = st.number_input("Record ID to update", min_value=1)
            record_date = st.date_input("New Record Date")
            income = st.number_input("New Income", min_value=0.0)
            expenses = st.number_input("New Expenses", min_value=0.0)
            if st.form_submit_button("Update Financial Record"):
                update_record("FinancialRecord",
                              {"RecordDate": record_date.isoformat(), "Income": income, "Expenses": expenses},
                              {"RecordID": record_id})
                st.success("Financial record updated successfully!")

    with st.expander("Delete Financial Record"):
        with st.form("delete_financial_record_form"):
            record_id = st.number_input("Record ID to delete", min_value=1)
            if st.form_submit_button("Delete Financial Record"):
                delete_record("FinancialRecord", {"RecordID": record_id})
                st.success("Financial record deleted successfully!")

    with st.expander("View Financial Records"):
        query = "SELECT * FROM FinancialRecord"
        data = fetch_data(query)
        df = pd.DataFrame(data, columns=["RecordID", "RecordDate", "Income", "Expenses"])
        st.write(df)


def show_harvest_tracking():
    st.title("Harvest Tracking")
    st.write("Track and compare harvest yields here.")

    with st.expander("Add Harvest Record"):
        with st.form("add_harvest_form"):
            crop_id = st.number_input("Crop ID", min_value=1)
            plot_id = st.number_input("Plot ID", min_value=1)
            harvest_date = st.date_input("Harvest Date")
            quantity = st.number_input("Quantity", min_value=1)
            if st.form_submit_button("Add Harvest Record"):
                add_record("Harvest", (crop_id, plot_id, harvest_date.isoformat(), quantity))
                st.success("Harvest record added successfully!")

    with st.expander("Update Harvest Record"):
        with st.form("update_harvest_form"):
            harvest_id = st.number_input("Harvest ID to update", min_value=1)
            crop_id = st.number_input("New Crop ID", min_value=1)
            plot_id = st.number_input("New Plot ID", min_value=1)
            harvest_date = st.date_input("New Harvest Date")
            quantity = st.number_input("New Quantity", min_value=1)
            if st.form_submit_button("Update Harvest Record"):
                update_record("Harvest", {"CropID": crop_id, "PlotID": plot_id, "HarvestDate": harvest_date.isoformat(),
                                          "Quantity": quantity}, {"HarvestID": harvest_id})
                st.success("Harvest record updated successfully!")

    with st.expander("Delete Harvest Record"):
        with st.form("delete_harvest_form"):
            harvest_id = st.number_input("Harvest ID to delete", min_value=1)
            if st.form_submit_button("Delete Harvest Record"):
                delete_record("Harvest", {"HarvestID": harvest_id})
                st.success("Harvest record deleted successfully!")

    with st.expander("View Harvest Records"):
        query = "SELECT * FROM Harvest"
        data = fetch_data(query)
        df = pd.DataFrame(data, columns=["HarvestID", "CropID", "PlotID", "HarvestDate", "Quantity"])
        st.write(df)


def show_market_info():
    st.title("Market Information")
    st.write("Get current market prices and insights here.")

    with st.expander("Add Market Info"):
        with st.form("add_market_info_form"):
            crop_id = st.number_input("Crop ID", min_value=1)
            market_date = st.date_input("Market Date")
            price_per_unit = st.number_input("Price Per Unit", min_value=0.0)
            if st.form_submit_button("Add Market Info"):
                add_record("MarketInfo", (crop_id, market_date.isoformat(), price_per_unit))
                st.success("Market info added successfully!")

    with st.expander("Update Market Info"):
        with st.form("update_market_info_form"):
            market_info_id = st.number_input("Market Info ID to update", min_value=1)
            crop_id = st.number_input("New Crop ID", min_value=1)
            market_date = st.date_input("New Market Date")
            price_per_unit = st.number_input("New Price Per Unit", min_value=0.0)
            if st.form_submit_button("Update Market Info"):
                update_record("MarketInfo",
                              {"CropID": crop_id, "MarketDate": market_date.isoformat(),
                               "PricePerUnit": price_per_unit},
                              {"MarketInfoID": market_info_id})
                st.success("Market info updated successfully!")

    with st.expander("Delete Market Info"):
        with st.form("delete_market_info_form"):
            market_info_id = st.number_input("Market Info ID to delete", min_value=1)
            if st.form_submit_button("Delete Market Info"):
                delete_record("MarketInfo", {"MarketInfoID": market_info_id})
                st.success("Market info deleted successfully!")

    with st.expander("View Market Info"):
        query = "SELECT * FROM MarketInfo"
        data = fetch_data(query)
        df = pd.DataFrame(data, columns=["MarketInfoID", "CropID", "MarketDate", "PricePerUnit"])
        st.write(df)


def generate_financial_report():
    st.title("Financial Report")

    # Define query to fetch financial records
    query = """
    SELECT RecordDate, SUM(Income) as TotalIncome, SUM(Expenses) as TotalExpenses
    FROM FinancialRecord
    GROUP BY RecordDate
    """

    data = fetch_data(query)
    df = pd.DataFrame(data, columns=["RecordDate", "TotalIncome", "TotalExpenses"])

    # Create two columns for the table and chart
    col1, col2 = st.columns([1, 2])

    with col1:
        st.write("### Financial Data")
        st.write(df)

    with col2:
        st.write("### Income and Expenses Over Time")
        # Plotting the data as a line chart
        fig, ax = plt.subplots()
        df.set_index('RecordDate', inplace=True)
        df.plot(y=["TotalIncome", "TotalExpenses"], kind="line", marker='o', ax=ax)
        ax.set_title("Income and Expenses Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Amount")
        ax.grid(True)
        st.pyplot(fig)


# Set the page layout to wide
st.set_page_config(
    layout="wide",
)

# Inject custom CSS to set a medium-wide width
st.markdown(
    """
    <style>
    /* Adjust the width of the main content area */
    .main .block-container {
        max-width: 1200px; /* Set your desired width here */
        padding: 1rem; /* Optional: Adjust padding */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Main function
def main():
    st.title("Farm Management System")

    # Navigation buttons
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 2, 2, 2, 2, 1])

    with col1:
        if st.button("Home"):
            st.session_state['page'] = 'Home'

    with col2:
        if st.button("Crop Planning"):
            st.session_state['page'] = 'Crop Planning'

    with col3:
        if st.button("Inventory Management"):
            st.session_state['page'] = 'Inventory Management'

    with col4:
        if st.button("Financial Records"):
            st.session_state['page'] = 'Financial Records'

    with col5:
        if st.button("Harvest Tracking"):
            st.session_state['page'] = 'Harvest Tracking'

    with col6:
        if st.button("Market Information"):
            st.session_state['page'] = 'Market Information'

    with col7:
        if st.button("Reporting"):
            st.session_state['page'] = 'Reporting'

    # Default page
    if 'page' not in st.session_state:
        st.session_state['page'] = 'Home'

    # Display content based on button click
    if st.session_state['page'] == 'Home':
        show_home()
    elif st.session_state['page'] == 'Crop Planning':
        show_crop_planning()
    elif st.session_state['page'] == 'Inventory Management':
        show_inventory_management()
    elif st.session_state['page'] == 'Financial Records':
        show_financial_records()
    elif st.session_state['page'] == 'Harvest Tracking':
        show_harvest_tracking()
    elif st.session_state['page'] == 'Market Information':
        show_market_info()
    elif st.session_state['page'] == 'Reporting':
        generate_financial_report()


if __name__ == "__main__":
    main()
