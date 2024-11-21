import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# Database connection settings
def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Seifamr02",
        database="Projectmanagement",
    )

# Function to run a query and return the result as a DataFrame
def run_query(query):
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Define SQL queries
queries = {
    "Project Status Report": """
        SELECT 
            p.ProjectID,
            p.ProjectName,
            p.ProjectStartDate,
            p.ProjectEndDate,
            p.ProjectStatus,
            COUNT(t.TaskID) AS TotalTasks,
            COUNT(CASE WHEN t.TaskStatus = 'Completed' THEN 1 END) AS CompletedTasks,
            COUNT(CASE WHEN t.TaskStatus = 'In Progress' THEN 1 END) AS InProgressTasks,
            COUNT(CASE WHEN t.TaskStatus = 'Pending' AND t.TaskDeadline < CURDATE() THEN 1 END) AS OverdueTasks,
            ROUND((COUNT(CASE WHEN t.TaskStatus = 'Completed' THEN 1 END) * 100.0 / COUNT(t.TaskID)), 2) AS PercentageCompleted
        FROM 
            Project p
        LEFT JOIN 
            Task t ON p.ProjectID = t.TaskProjectID
        GROUP BY 
            p.ProjectID, p.ProjectName, p.ProjectStartDate, p.ProjectEndDate, p.ProjectStatus;
    """,
    "Task Completion Report": """
        SELECT 
            t.TaskID,
            t.TaskName,
            p.ProjectName,
            t.TaskStatus,
            t.TaskPriority,
            t.TaskDeadline,
            t.TaskCompletionDate,
            e.EmployeeName AS AssignedTeamMember,
            CASE 
                WHEN t.TaskDeadline < CURDATE() AND t.TaskStatus <> 'Completed' THEN 'Overdue'
                ELSE 'On Track'
            END AS DeadlineStatus
        FROM 
            Task t
        LEFT JOIN 
            Project p ON t.TaskProjectID = p.ProjectID
        LEFT JOIN 
            EmployeeTask et ON t.TaskID = et.TaskID
        LEFT JOIN 
            Employee e ON et.EmployeeID = e.EmployeeID;
    """,
    "Profitability Report": """
        SELECT 
            p.ProjectID,
            p.ProjectName,
            COALESCE(SUM(so.SaleOrderRevenue), 0) AS Revenue,
            COALESCE(p.ProjectLaborCost + SUM(po.PurchaseOrderTotal), 0) AS TotalExpenses,
            COALESCE(SUM(so.SaleOrderRevenue), 0) - COALESCE(p.ProjectLaborCost + SUM(po.PurchaseOrderTotal), 0) AS ProfitMargin
        FROM 
            Project p
        LEFT JOIN 
            SaleOrder so ON p.ProjectSaleOrderID = so.SaleOrderID
        LEFT JOIN 
            PurchaseOrder po ON p.ProjectID = po.PurchaseOrderProjectID
        GROUP BY 
            p.ProjectID, p.ProjectName, p.ProjectLaborCost;
    """,
    "Project Summary Report": """
        SELECT 
            COUNT(*) AS TotalProjects,
            COUNT(CASE WHEN p.ProjectStatus = 'Active' THEN 1 END) AS ActiveProjects,
            COUNT(CASE WHEN p.ProjectStatus = 'Completed' THEN 1 END) AS CompletedProjects,
            ROUND(AVG(DATEDIFF(p.ProjectEndDate, p.ProjectStartDate)), 2) AS AverageProjectDuration,
            ROUND((SUM(CASE WHEN p.ProjectStatus = 'Completed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) AS CompletionRate
        FROM 
            Project p;
    """,
    "Top 5 Projects by Revenue": """
        SELECT 
            p.ProjectID,
            p.ProjectName,
            COALESCE(SUM(so.SaleOrderRevenue), 0) AS Revenue
        FROM 
            Project p
        LEFT JOIN 
            SaleOrder so ON p.ProjectSaleOrderID = so.SaleOrderID
        GROUP BY 
            p.ProjectID, p.ProjectName
        ORDER BY 
            Revenue DESC
        LIMIT 5;
    """,
    "Team Performance Report": """
        SELECT 
            e.EmployeeID,
            e.EmployeeName,
            e.EmployeeRole,
            COUNT(et.TaskID) AS TotalTasksAssigned,
            COUNT(CASE WHEN t.TaskStatus = 'Completed' THEN 1 END) AS TasksCompleted,
            AVG(et.HoursWorked) AS AvgHoursPerTask
        FROM 
            Employee e
        LEFT JOIN 
            EmployeeTask et ON e.EmployeeID = et.EmployeeID
        LEFT JOIN 
            Task t ON et.TaskID = t.TaskID
        GROUP BY 
            e.EmployeeID, e.EmployeeName, e.EmployeeRole;
    """,
    "Workload Report": """
        SELECT 
            e.EmployeeID,
            e.EmployeeName,
            COUNT(et.TaskID) AS TotalAssignedTasks,
            COUNT(CASE WHEN t.TaskPriority = 'High' THEN 1 END) AS HighPriorityTasks,
            COUNT(CASE WHEN t.TaskPriority = 'Medium' THEN 1 END) AS MediumPriorityTasks,
            COUNT(CASE WHEN t.TaskPriority = 'Low' THEN 1 END) AS LowPriorityTasks,
            SUM(et.HoursWorked) AS TotalHoursWorked
        FROM 
            Employee e
        LEFT JOIN 
            EmployeeTask et ON e.EmployeeID = et.EmployeeID
        LEFT JOIN 
            Task t ON et.TaskID = t.TaskID
        GROUP BY 
            e.EmployeeID, e.EmployeeName;
    """,
    "Overdue Payments": """
        SELECT 
            po.PurchaseOrderID,
            s.SupplierName,
            po.PurchaseOrderTotal,
            p.ProjectName,
            pa.PayableStatus,
            pa.PaymentDate
        FROM 
            Payable pa
        LEFT JOIN 
            PurchaseOrder po ON pa.PayablePurchaseOrderID = po.PurchaseOrderID
        LEFT JOIN 
            Supplier s ON po.PurchaseOrderSupplierID = s.SupplierID
        LEFT JOIN 
            Project p ON po.PurchaseOrderProjectID = p.ProjectID
        WHERE 
            pa.PayableStatus = 'Pending';
    """,
    "Overdue Receivables": """
        SELECT 
            so.SaleOrderID,
            c.ClientName,
            so.SaleOrderTotal,
            r.ReceivableAmount,
            r.ReceivableStatus,
            r.PaymentDate
        FROM 
            Receivable r
        LEFT JOIN 
            SaleOrder so ON r.ReceivableSaleOrderID = so.SaleOrderID
        LEFT JOIN 
            Client c ON so.SaleOrderClientID = c.ClientID
        WHERE 
            r.ReceivableStatus = 'Pending';
    """
}

# Streamlit app
st.title("Comprehensive MySQL Reports")

# Sidebar for selecting a report
report_name = st.sidebar.selectbox("Select a Report", list(queries.keys()))

# Display selected report
st.header(f"Report: {report_name}")
query = queries[report_name]

try:
    # Run the query and display the results
    df = run_query(query)
    st.write("Query Results:", df)

    # Generate visualizations for reports
    if report_name == "Project Status Report":
        fig = px.bar(df, x="ProjectName", y="PercentageCompleted", title="Project Completion Percentage")
        st.plotly_chart(fig)

    elif report_name == "Top 5 Projects by Revenue":
        fig = px.bar(df, x="ProjectName", y="Revenue", title="Top 5 Projects by Revenue")
        st.plotly_chart(fig)

    elif report_name == "Profitability Report":
        fig = px.pie(df, values="ProfitMargin", names="ProjectName", title="Profit Margin by Project")
        st.plotly_chart(fig)

    elif report_name == "Team Performance Report":
        fig = px.bar(df, x="EmployeeName", y="TasksCompleted", title="Team Performance - Tasks Completed")
        st.plotly_chart(fig)

    elif report_name == "Workload Report":
        fig = px.bar(df, x="EmployeeName", y="TotalAssignedTasks", title="Employee Workload")
        st.plotly_chart(fig)

    elif report_name == "Overdue Payments":
        fig = px.bar(df, x="SupplierName", y="PurchaseOrderTotal", title="Overdue Payments by Supplier")
        st.plotly_chart(fig)

    elif report_name == "Overdue Receivables":
        fig = px.bar(df, x="ClientName", y="SaleOrderTotal", title="Overdue Receivables by Client")
        st.plotly_chart(fig)

    else:
        st.write("No specific visualization available for this report.")

except Exception as e:
    st.error(f"An error occurred: {e}")


