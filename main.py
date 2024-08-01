import streamlit as st
import sqlite3
import os
import pandas as pd
from database_setup import create_database
import matplotlib.pyplot as plt


# Define connection function
def get_connection():
    db_path = 'farm_management.db'
    if not os.path.exists(db_path):
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


# Define pages
def show_home():
    st.title("Welcome to FarmFlow Ghana")
    st.markdown("### Our Motto")
    st.markdown("**Empowering Farmers, Enhancing Yields, Ensuring Prosperity**")


def show_crop_planning():
    st.title("Crop Planning")
    st.write("Manage crop planning here.")
    search_query = st.text_input("Search Crops")

    with st.expander("View Crops"):
        query = "SELECT * FROM Crop WHERE Name LIKE ?"
        data = fetch_data(query, ('%' + search_query + '%',))
        df = pd.DataFrame(data, columns=["CropID", "Name", "Type", "GrowthDuration"])
        st.write(df)

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


def show_inventory_management():
    st.title("Inventory Management")
    st.write("Track and manage inventory here.")
    search_query = st.text_input("Search Inventory")

    with st.expander("View Inventory"):
        query = "SELECT * FROM Inventory WHERE ItemName LIKE ?"
        data = fetch_data(query, ('%' + search_query + '%',))
        df = pd.DataFrame(data, columns=["InventoryID", "ItemName", "Quantity", "Type", "PurchaseDate"])
        st.write(df)

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


def show_financial_records():
    st.title("Financial Records")
    st.write("Manage financial records here.")
    search_query = st.text_input("Search Financial Records")

    with st.expander("View Financial Records"):
        query = "SELECT * FROM FinancialRecord WHERE RecordDate LIKE ?"
        data = fetch_data(query, ('%' + search_query + '%',))
        df = pd.DataFrame(data, columns=["RecordID", "RecordDate", "Income", "Expenses"])
        st.write(df)

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


def show_harvest_tracking():
    st.title("Harvest Tracking")
    st.write("Track and compare harvest yields here.")
    search_query = st.text_input("Search Harvest Records")

    with st.expander("View Harvest Records"):
        query = "SELECT * FROM Harvest WHERE CropID LIKE ?"
        data = fetch_data(query, ('%' + search_query + '%',))
        df = pd.DataFrame(data, columns=["HarvestID", "CropID", "PlotID", "HarvestDate", "Quantity"])
        st.write(df)

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
                                          "Quantity": quantity},
                              {"HarvestID": harvest_id})
                st.success("Harvest record updated successfully!")

    with st.expander("Delete Harvest Record"):
        with st.form("delete_harvest_form"):
            harvest_id = st.number_input("Harvest ID to delete", min_value=1)
            if st.form_submit_button("Delete Harvest Record"):
                delete_record("Harvest", {"HarvestID": harvest_id})
                st.success("Harvest record deleted successfully!")


def show_market_info():
    st.title("Market Information")
    st.write("Manage market data and pricing here.")
    search_query = st.text_input("Search Market Information")

    with st.expander("View Market Information"):
        query = "SELECT * FROM MarketInfo WHERE CropID LIKE ?"
        data = fetch_data(query, ('%' + search_query + '%',))
        df = pd.DataFrame(data, columns=["MarketInfoID", "CropID", "MarketDate", "PricePerUnit"])
        st.write(df)

    with st.expander("Add Market Information"):
        with st.form("add_market_info_form"):
            crop_id = st.number_input("Crop ID", min_value=1)
            market_date = st.date_input("Market Date")
            price_per_unit = st.number_input("Price Per Unit", min_value=0.0)
            if st.form_submit_button("Add Market Information"):
                add_record("MarketInfo", (crop_id, market_date.isoformat(), price_per_unit))
                st.success("Market information added successfully!")

    with st.expander("Update Market Information"):
        with st.form("update_market_info_form"):
            market_info_id = st.number_input("MarketInfo ID to update", min_value=1)
            crop_id = st.number_input("New Crop ID", min_value=1)
            market_date = st.date_input("New Market Date")
            price_per_unit = st.number_input("New Price Per Unit", min_value=0.0)
            if st.form_submit_button("Update Market Information"):
                update_record("MarketInfo", {"CropID": crop_id, "MarketDate": market_date.isoformat(),
                                             "PricePerUnit": price_per_unit},
                              {"MarketInfoID": market_info_id})
                st.success("Market information updated successfully!")

    with st.expander("Delete Market Information"):
        with st.form("delete_market_info_form"):
            market_info_id = st.number_input("MarketInfo ID to delete", min_value=1)
            if st.form_submit_button("Delete Market Information"):
                delete_record("MarketInfo", {"MarketInfoID": market_info_id})
                st.success("Market information deleted successfully!")


def show_employee_management():
    st.title("Employee Management")
    st.write("Manage employees and their details here.")
    search_query = st.text_input("Search Employees")

    with st.expander("View Employees"):
        query = "SELECT * FROM Employee WHERE FirstName LIKE ? OR LastName LIKE ?"
        data = fetch_data(query, ('%' + search_query + '%', '%' + search_query + '%'))
        df = pd.DataFrame(data, columns=["EmployeeID", "FirstName", "LastName", "Role", "HireDate"])
        st.write(df)

    with st.expander("Add Employee"):
        with st.form("add_employee_form"):
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            role = st.text_input("Role")
            hire_date = st.date_input("Hire Date")
            if st.form_submit_button("Add Employee"):
                add_record("Employee", (first_name, last_name, role, hire_date.isoformat()))
                st.success("Employee added successfully!")

    with st.expander("Update Employee"):
        with st.form("update_employee_form"):
            employee_id = st.number_input("Employee ID to update", min_value=1)
            first_name = st.text_input("New First Name")
            last_name = st.text_input("New Last Name")
            role = st.text_input("New Role")
            hire_date = st.date_input("New Hire Date")
            if st.form_submit_button("Update Employee"):
                update_record("Employee", {"FirstName": first_name, "LastName": last_name, "Role": role,
                                           "HireDate": hire_date.isoformat()},
                              {"EmployeeID": employee_id})
                st.success("Employee updated successfully!")

    with st.expander("Delete Employee"):
        with st.form("delete_employee_form"):
            employee_id = st.number_input("Employee ID to delete", min_value=1)
            if st.form_submit_button("Delete Employee"):
                delete_record("Employee", {"EmployeeID": employee_id})
                st.success("Employee deleted successfully!")


def show_report():
    st.title("Reports")
    st.write("Generate and view reports here.")

    # Example report: Total income vs. total expenses
    st.subheader("Income vs Expenses")

    # Query to fetch data
    query = """
        SELECT strftime('%Y-%m', RecordDate) as Month, 
               SUM(Income) as TotalIncome, 
               SUM(Expenses) as TotalExpenses
        FROM FinancialRecord
        GROUP BY Month
        ORDER BY Month
    """
    data = fetch_data(query)
    df = pd.DataFrame(data, columns=["Month", "TotalIncome", "TotalExpenses"])

    # Create columns for layout
    col1, col2 = st.columns(2)

    # Table in the first column
    with col1:
        st.write(df)

    # Line chart in the second column
    with col2:
        fig, ax = plt.subplots()
        df.plot(x="Month", y=["TotalIncome", "TotalExpenses"], kind="line", ax=ax, marker='o')
        plt.title("Monthly Income vs Expenses")
        plt.xlabel("Month")
        plt.ylabel("Amount")
        st.pyplot(fig)



def main():
    st.sidebar.title("Navigation")
    pages = ["Home", "Crop Planning", "Inventory Management", "Financial Records", "Harvest Tracking",
             "Market Information", "Employee Management", "Report"]
    selection = st.sidebar.radio("Go to", pages)

    if selection == "Home":
        show_home()
    elif selection == "Crop Planning":
        show_crop_planning()
    elif selection == "Inventory Management":
        show_inventory_management()
    elif selection == "Financial Records":
        show_financial_records()
    elif selection == "Harvest Tracking":
        show_harvest_tracking()
    elif selection == "Market Information":
        show_market_info()
    elif selection == "Employee Management":
        show_employee_management()
    elif selection == "Report":
        show_report()


if __name__ == "__main__":
    main()
