import streamlit as st
import pymysql

# Database connection
def get_connection():
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='Seifamr02',
            database='ProjectManagement'
        )
        return conn
    except pymysql.MySQLError as e:
        st.error(f"Database connection error: {e}")
        return None

# Execute SQL commands
def execute_query(query, params=None):
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                st.success("Operation successful!")
        except Exception as e:
            st.error(f"Error executing query: {e}")
        finally:
            conn.close()

# Fetch data for dropdowns or validation
def fetch_data(query):
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            return []
        finally:
            conn.close()

# Render forms for each table
def client_form():
    st.subheader("Manage Clients")
    
    # Insert form
    with st.form("insert_client"):
        st.write("Insert New Client")
        client_name = st.text_input("Client Name")
        client_contact = st.text_input("Client Contact Info")
        submitted = st.form_submit_button("Add Client")
        if submitted:
            query = "INSERT INTO Client (ClientName, ClientContactInfo) VALUES (%s, %s)"
            execute_query(query, (client_name, client_contact))
    
    # Update form
    with st.form("update_client"):
        st.write("Update Existing Client")
        client_id = st.number_input("Client ID", min_value=1, step=1)
        client_name = st.text_input("New Client Name")
        client_contact = st.text_input("New Client Contact Info")
        submitted = st.form_submit_button("Update Client")
        if submitted:
            query = "UPDATE Client SET ClientName = %s, ClientContactInfo = %s WHERE ClientID = %s"
            execute_query(query, (client_name, client_contact, client_id))
    
    # Delete form
    with st.form("delete_client"):
        st.write("Delete Client")
        client_id = st.number_input("Client ID to Delete", min_value=1, step=1)
        submitted = st.form_submit_button("Delete Client")
        if submitted:
            query = "DELETE FROM Client WHERE ClientID = %s"
            execute_query(query, (client_id,))

def team_form():
    st.subheader("Manage Teams")
    
    # Insert form
    with st.form("insert_team"):
        st.write("Insert New Team")
        team_name = st.text_input("Team Name")
        submitted = st.form_submit_button("Add Team")
        if submitted:
            query = "INSERT INTO Team (TeamName) VALUES (%s)"
            execute_query(query, (team_name,))
    
    # Update form
    with st.form("update_team"):
        st.write("Update Existing Team")
        team_id = st.number_input("Team ID", min_value=1, step=1)
        team_name = st.text_input("New Team Name")
        submitted = st.form_submit_button("Update Team")
        if submitted:
            query = "UPDATE Team SET TeamName = %s WHERE TeamID = %s"
            execute_query(query, (team_name, team_id))
    
    # Delete form
    with st.form("delete_team"):
        st.write("Delete Team")
        team_id = st.number_input("Team ID to Delete", min_value=1, step=1)
        submitted = st.form_submit_button("Delete Team")
        if submitted:
            query = "DELETE FROM Team WHERE TeamID = %s"
            execute_query(query, (team_id,))

def employee_form():
    st.subheader("Manage Employees")
    
    # Insert form
    with st.form("insert_employee"):
        st.write("Insert New Employee")
        employee_name = st.text_input("Employee Name")
        employee_role = st.text_input("Employee Role")
        teams = fetch_data("SELECT TeamID, TeamName FROM Team")
        team_id = st.selectbox("Team", options=[(t[0], t[1]) for t in teams], format_func=lambda x: x[1] if isinstance(x, tuple) else x)
        submitted = st.form_submit_button("Add Employee")
        if submitted:
            query = "INSERT INTO Employee (EmployeeName, EmployeeRole, EmployeeTeamID) VALUES (%s, %s, %s)"
            execute_query(query, (employee_name, employee_role, team_id[0]))
    
    # Update form
    with st.form("update_employee"):
        st.write("Update Existing Employee")
        employee_id = st.number_input("Employee ID", min_value=1, step=1)
        employee_name = st.text_input("New Employee Name")
        employee_role = st.text_input("New Employee Role")
        team_id = st.selectbox("New Team", options=[(t[0], t[1]) for t in teams], format_func=lambda x: x[1] if isinstance(x, tuple) else x)
        submitted = st.form_submit_button("Update Employee")
        if submitted:
            query = "UPDATE Employee SET EmployeeName = %s, EmployeeRole = %s, EmployeeTeamID = %s WHERE EmployeeID = %s"
            execute_query(query, (employee_name, employee_role, team_id[0], employee_id))
    
    # Delete form
    with st.form("delete_employee"):
        st.write("Delete Employee")
        employee_id = st.number_input("Employee ID to Delete", min_value=1, step=1)
        submitted = st.form_submit_button("Delete Employee")
        if submitted:
            query = "DELETE FROM Employee WHERE EmployeeID = %s"
            execute_query(query, (employee_id,))


# Render forms for each table
def sale_order_form():
    st.subheader("Manage Sale Orders")
    
    # Insert form
    with st.form("insert_sale_order"):
        st.write("Insert New Sale Order")
        clients = fetch_data("SELECT ClientID, ClientName FROM Client")
        client_id = st.selectbox("Client", [(c[0], c[1]) for c in clients], format_func=lambda x: x[1] if isinstance(x, tuple) else x)
        sale_date = st.date_input("Sale Order Date")
        total = st.number_input("Total Amount", min_value=0.0)
        submitted = st.form_submit_button("Add Sale Order")
        if submitted:
            query = "INSERT INTO SaleOrder (SaleOrderClientID, SaleOrderDate, SaleOrderTotal) VALUES (%s, %s, %s)"
            execute_query(query, (client_id[0], sale_date, total))
    
    # Update form
    with st.form("update_sale_order"):
        st.write("Update Existing Sale Order")
        sale_order_id = st.number_input("Sale Order ID", min_value=1, step=1)
        sale_date = st.date_input("New Sale Order Date")
        total = st.number_input("New Total Amount", min_value=0.0)
        submitted = st.form_submit_button("Update Sale Order")
        if submitted:
            query = "UPDATE SaleOrder SET SaleOrderDate = %s, SaleOrderTotal = %s WHERE SaleOrderID = %s"
            execute_query(query, (sale_date, total, sale_order_id))
    
    # Delete form
    with st.form("delete_sale_order"):
        st.write("Delete Sale Order")
        sale_order_id = st.number_input("Sale Order ID to Delete", min_value=1, step=1)
        submitted = st.form_submit_button("Delete Sale Order")
        if submitted:
            query = "DELETE FROM SaleOrder WHERE SaleOrderID = %s"
            execute_query(query, (sale_order_id,))

def project_form():
    st.subheader("Manage Projects")
    
    # Insert form
    with st.form("insert_project"):
        st.write("Insert New Project")
        sale_orders = fetch_data("SELECT SaleOrderID, SaleOrderDate FROM SaleOrder")
        sale_order_id = st.selectbox("Sale Order", [(so[0], so[1]) for so in sale_orders], format_func=lambda x: f"Order ID {x[0]} ({x[1]})" if isinstance(x, tuple) else x)
        teams = fetch_data("SELECT TeamID, TeamName FROM Team")
        team_id = st.selectbox("Team", [(t[0], t[1]) for t in teams], format_func=lambda x: x[1] if isinstance(x, tuple) else x)
        project_name = st.text_input("Project Name")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        submitted = st.form_submit_button("Add Project")
        if submitted:
            query = "INSERT INTO Project (ProjectSaleOrderID, ProjectTeamID, ProjectName, ProjectStartDate, ProjectEndDate) VALUES (%s, %s, %s, %s, %s)"
            execute_query(query, (sale_order_id[0], team_id[0], project_name, start_date, end_date))
    
    # Update form
    with st.form("update_project"):
        st.write("Update Existing Project")
        project_id = st.number_input("Project ID", min_value=1, step=1)
        project_name = st.text_input("New Project Name")
        start_date = st.date_input("New Start Date")
        end_date = st.date_input("New End Date")
        submitted = st.form_submit_button("Update Project")
        if submitted:
            query = "UPDATE Project SET ProjectName = %s, ProjectStartDate = %s, ProjectEndDate = %s WHERE ProjectID = %s"
            execute_query(query, (project_name, start_date, end_date, project_id))
    
    # Delete form
    with st.form("delete_project"):
        st.write("Delete Project")
        project_id = st.number_input("Project ID to Delete", min_value=1, step=1)
        submitted = st.form_submit_button("Delete Project")
        if submitted:
            query = "DELETE FROM Project WHERE ProjectID = %s"
            execute_query(query, (project_id,))

def task_form():
    st.subheader("Manage Tasks")
    
    # Insert form
    with st.form("insert_task"):
        st.write("Insert New Task")
        projects = fetch_data("SELECT ProjectID, ProjectName FROM Project")
        project_id = st.selectbox("Project", [(p[0], p[1]) for p in projects], format_func=lambda x: x[1] if isinstance(x, tuple) else x)
        task_name = st.text_input("Task Name")
        submitted = st.form_submit_button("Add Task")
        if submitted:
            query = "INSERT INTO Task (TaskProjectID, TaskName) VALUES (%s, %s)"
            execute_query(query, (project_id[0], task_name))
    
    # Update form
    with st.form("update_task"):
        st.write("Update Existing Task")
        task_id = st.number_input("Task ID", min_value=1, step=1)
        task_name = st.text_input("New Task Name")
        submitted = st.form_submit_button("Update Task")
        if submitted:
            query = "UPDATE Task SET TaskName = %s WHERE TaskID = %s"
            execute_query(query, (task_name, task_id))
    
    # Delete form
    with st.form("delete_task"):
        st.write("Delete Task")
        task_id = st.number_input("Task ID to Delete", min_value=1, step=1)
        submitted = st.form_submit_button("Delete Task")
        if submitted:
            query = "DELETE FROM Task WHERE TaskID = %s"
            execute_query(query, (task_id,))

def supplier_form():
    st.subheader("Manage Suppliers")
    
    # Insert form
    with st.form("insert_supplier"):
        st.write("Insert New Supplier")
        supplier_name = st.text_input("Supplier Name")
        supplier_contact = st.text_input("Supplier Contact Info")
        submitted = st.form_submit_button("Add Supplier")
        if submitted:
            query = "INSERT INTO Supplier (SupplierName, SupplierContactInfo) VALUES (%s, %s)"
            execute_query(query, (supplier_name, supplier_contact))
    
    # Update form
    with st.form("update_supplier"):
        st.write("Update Existing Supplier")
        supplier_id = st.number_input("Supplier ID", min_value=1, step=1)
        supplier_name = st.text_input("New Supplier Name")
        supplier_contact = st.text_input("New Supplier Contact Info")
        submitted = st.form_submit_button("Update Supplier")
        if submitted:
            query = "UPDATE Supplier SET SupplierName = %s, SupplierContactInfo = %s WHERE SupplierID = %s"
            execute_query(query, (supplier_name, supplier_contact, supplier_id))
    
    # Delete form
    with st.form("delete_supplier"):
        st.write("Delete Supplier")
        supplier_id = st.number_input("Supplier ID to Delete", min_value=1, step=1)
        submitted = st.form_submit_button("Delete Supplier")
        if submitted:
            query = "DELETE FROM Supplier WHERE SupplierID = %s"
            execute_query(query, (supplier_id,))

def payable_form():
    st.subheader("Manage Payables")
    
    # Insert form
    with st.form("insert_payable"):
        st.write("Insert New Payable")
        purchase_orders = fetch_data("SELECT PurchaseOrderID, PurchaseOrderDate FROM PurchaseOrder")
        purchase_order_id = st.selectbox("Purchase Order", [(po[0], po[1]) for po in purchase_orders], format_func=lambda x: f"Order ID {x[0]} ({x[1]})" if isinstance(x, tuple) else x)
        amount = st.number_input("Payable Amount", min_value=0.0)
        status = st.text_input("Payable Status")
        submitted = st.form_submit_button("Add Payable")
        if submitted:
            query = "INSERT INTO Payable (PayablePurchaseOrderID, PayableAmount, PayableStatus) VALUES (%s, %s, %s)"
            execute_query(query, (purchase_order_id[0], amount, status))
    
    # Update form
    with st.form("update_payable"):
        st.write("Update Existing Payable")
        payable_id = st.number_input("Payable ID", min_value=1, step=1)
        amount = st.number_input("New Payable Amount", min_value=0.0)
        status = st.text_input("New Payable Status")
        submitted = st.form_submit_button("Update Payable")
        if submitted:
            query = "UPDATE Payable SET PayableAmount = %s, PayableStatus = %s WHERE PayableID = %s"
            execute_query(query, (amount, status, payable_id))
    
    # Delete form
    with st.form("delete_payable"):
        st.write("Delete Payable")
        payable_id = st.number_input("Payable ID to Delete", min_value=1, step=1)
        submitted = st.form_submit_button("Delete Payable")
        if submitted:
            query = "DELETE FROM Payable WHERE PayableID = %s"
            execute_query(query, (payable_id,))

def receivable_form():
    st.subheader("Manage Receivables")
    
    # Insert form
    with st.form("insert_receivable"):
        st.write("Insert New Receivable")
        sale_orders = fetch_data("SELECT SaleOrderID, SaleOrderDate FROM SaleOrder")
        sale_order_id = st.selectbox("Sale Order", [(so[0], so[1]) for so in sale_orders], format_func=lambda x: f"Order ID {x[0]} ({x[1]})" if isinstance(x, tuple) else x)
        amount = st.number_input("Receivable Amount", min_value=0.0)
        status = st.text_input("Receivable Status")
        submitted = st.form_submit_button("Add Receivable")
        if submitted:
            query = "INSERT INTO Receivable (ReceivableSaleOrderID, ReceivableAmount, ReceivableStatus) VALUES (%s, %s, %s)"
            execute_query(query, (sale_order_id[0], amount, status))
    
    # Update form
    with st.form("update_receivable"):
        st.write("Update Existing Receivable")
        receivable_id = st.number_input("Receivable ID", min_value=1, step=1)
        amount = st.number_input("New Receivable Amount", min_value=0.0)
        status = st.text_input("New Receivable Status")
        submitted = st.form_submit_button("Update Receivable")
        if submitted:
            query = "UPDATE Receivable SET ReceivableAmount = %s, ReceivableStatus = %s WHERE ReceivableID = %s"
            execute_query(query, (amount, status, receivable_id))
    
    # Delete form
    with st.form("delete_receivable"):
        st.write("Delete Receivable")
        receivable_id = st.number_input("Receivable ID to Delete", min_value=1, step=1)
        submitted = st.form_submit_button("Delete Receivable")
        if submitted:
            query = "DELETE FROM Receivable WHERE ReceivableID = %s"
            execute_query(query, (receivable_id,))

def purchase_order_form():
    st.subheader("Manage Purchase Orders")
    
    # Insert form
    with st.form("insert_purchase_order"):
        st.write("Insert New Purchase Order")
        create_new_supplier = st.checkbox("Create New Supplier?")
        
        if create_new_supplier:
            # Fields for creating a new Supplier
            supplier_name = st.text_input("Supplier Name")
            supplier_contact = st.text_input("Supplier Contact Info")
        else:
            # Dropdown to select existing Supplier
            suppliers = fetch_data("SELECT SupplierID, SupplierName FROM Supplier")
            supplier_id = st.selectbox(
                "Supplier", 
                [(s[0], s[1]) for s in suppliers], 
                format_func=lambda x: x[1] if isinstance(x, tuple) else x
            )
        
        # Fields for PurchaseOrder
        purchase_order_date = st.date_input("Purchase Order Date")
        purchase_order_total = st.number_input("Purchase Order Total", min_value=0.0)
        submitted = st.form_submit_button("Add Purchase Order")
        
        if submitted:
            if create_new_supplier:
                # Insert new Supplier
                supplier_query = """
                    INSERT INTO Supplier (SupplierName, SupplierContactInfo) 
                    VALUES (%s, %s)
                """
                execute_query(supplier_query, (supplier_name, supplier_contact))
                # Retrieve the ID of the newly created Supplier
                supplier_id = fetch_data("SELECT LAST_INSERT_ID()")[0][0]
            
            # Insert PurchaseOrder
            po_query = """
                INSERT INTO PurchaseOrder (PurchaseOrderSupplierID, PurchaseOrderDate, PurchaseOrderTotal) 
                VALUES (%s, %s, %s)
            """
            execute_query(po_query, (supplier_id[0], purchase_order_date, purchase_order_total))
    
    # Update form
    with st.form("update_purchase_order"):
        st.write("Update Existing Purchase Order")
        purchase_order_id = st.number_input("Purchase Order ID", min_value=1, step=1)
        purchase_order_date = st.date_input("New Purchase Order Date")
        purchase_order_total = st.number_input("New Purchase Order Total", min_value=0.0)
        submitted = st.form_submit_button("Update Purchase Order")
        
        if submitted:
            query = """
                UPDATE PurchaseOrder 
                SET PurchaseOrderDate = %s, PurchaseOrderTotal = %s 
                WHERE PurchaseOrderID = %s
            """
            execute_query(query, (purchase_order_date, purchase_order_total, purchase_order_id))
    
    # Delete form
    with st.form("delete_purchase_order"):
        st.write("Delete Purchase Order")
        purchase_order_id = st.number_input("Purchase Order ID to Delete", min_value=1, step=1)
        submitted = st.form_submit_button("Delete Purchase Order")
        
        if submitted:
            query = "DELETE FROM PurchaseOrder WHERE PurchaseOrderID = %s"
            execute_query(query, (purchase_order_id,))


# Main app layout
st.title("Database Management System")

# Sidebar navigation
table_choice = st.sidebar.selectbox(
    "Choose a table to manage",
    ["Client", "Team", "Employee", "SaleOrder", "Project", "Task", "Supplier", "Payable", "Receivable", "PurchaseOrder"]
)


if table_choice == "Client":
    client_form()
elif table_choice == "Team":
    team_form()
elif table_choice == "Employee":
    employee_form()
elif table_choice == "SaleOrder":
    sale_order_form()
elif table_choice == "Project":
    project_form()
elif table_choice == "Task":
    task_form()
elif table_choice == "Supplier":
    supplier_form()
elif table_choice == "Payable":
    payable_form()
elif table_choice == "Receivable":
    receivable_form()
elif table_choice == "PurchaseOrder":
    purchase_order_form()

    