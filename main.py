import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from auth import register_user, login_user
from firebase_config import auth, db

# Streamlit Page Configuration
st.set_page_config(page_title="Medical Report Visualizer", layout="wide")

# Session State for User Authentication
if "user_logged_in" not in st.session_state:
    st.session_state.user_logged_in = False

# Home Page Function
def home_page():
    st.title("Medical Report Visualizer")

    # Report Type Selection
    report_type = st.radio("Select Report Type:", ["Weekly", "Monthly"])

    # Number of values based on report type
    num_values = 7 if report_type == "Weekly" else 4

    # Report Category Selection
    report_category = st.selectbox("Select Report Category:", ["Sugar Level", "Blood Pressure"])

    # Graph Type Selection
    graph_type = st.selectbox("Select Graph Type", ["Line Graph", "Bar Chart", "Scatter Plot", "Pie Chart", "Histogram", "Box Plot"])

    # User Inputs
    values = []
    st.subheader(f"Enter {num_values} values for {report_type} report")
    for i in range(num_values):
        value = st.number_input(f"Enter value for {'Day' if report_type == 'Weekly' else 'Week'} {i + 1}:", min_value=0, step=1)
        values.append(value)

    # Generate Graph Button
    if st.button("Generate Report"):
        if len(values) == num_values and all(v > 0 for v in values):
            plot_graph(values, report_type, report_category, graph_type)
        else:
            st.error("Please enter all required values!")

# Function to Plot Graph
def plot_graph(values, report_type, report_category, graph_type):
    fig, ax = plt.subplots(figsize=(4, 3))  # Small graph size

    # X-axis labels
    x_labels = [f"Day {i + 1}" if report_type == "Weekly" else f"Week {i + 1}" for i in range(len(values))]

    # Y-axis limits
    y_limit = 600 if report_category == "Sugar Level" else 200

    if graph_type == "Line Graph":
        ax.plot(x_labels, values, marker="o", linestyle="-", color="b", label=report_category)

    elif graph_type == "Bar Chart":
        ax.bar(x_labels, values, color="blue", label=report_category)

    elif graph_type == "Scatter Plot":
        ax.scatter(x_labels, values, color="red", label=report_category)

    elif graph_type == "Pie Chart":
        fig, ax = plt.subplots(figsize=(4, 4))  # Adjust size for Pie Chart
        ax.pie(values, labels=x_labels, autopct="%1.1f%%", colors=['red', 'blue', 'green', 'orange', 'purple', 'yellow', 'pink'])
        ax.set_title(f"{report_category} - {report_type} Report")

    elif graph_type == "Histogram":
        ax.hist(values, bins=5, color='purple', edgecolor='black', alpha=0.7)
        ax.set_xlabel("Value")
        ax.set_ylabel("Frequency")

    elif graph_type == "Box Plot":
        sns.boxplot(data=values, ax=ax)
        ax.set_ylabel(report_category)

    # Apply settings
    if graph_type != "Pie Chart":
        ax.set_ylim([0, y_limit])
        ax.set_xlabel("Time Period")
        ax.set_ylabel(report_category)
        ax.set_title(f"{report_category} - {report_type} Report")
        ax.legend()
        ax.tick_params(axis='both', labelsize=6)  # Reduce label size

    plt.tight_layout()
    st.pyplot(fig)

# Login and Registration Page
def auth_page():
    st.markdown(
        """
        <style>
        .main {text-align: center;}
        .stTextInput, .stButton>button {
            width: 100%;
            border-radius: 10px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            padding: 10px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h2 style='text-align: center; color: #4CAF50;'>Medical Report Visualizer</h2>", unsafe_allow_html=True)

    choice = st.radio("Select an Option:", ["Login", "Register"], horizontal=True)

    with st.container():
        st.markdown("---")  # Adds a line separator
        if choice == "Register":
            st.subheader("Create an Account 👤")
            email = st.text_input("📧 Email")
            password = st.text_input("🔒 Password", type="password")

            if st.button("Register"):
                user_id = register_user(email, password)
                if user_id:
                    st.success("✅ Registration successful! Please log in.")

        elif choice == "Login":
            st.subheader("Welcome Back! 👋")
            email = st.text_input("📧 Email")
            password = st.text_input("🔒 Password", type="password")

            if st.button("Login"):
                if login_user(email, password):
                    st.session_state.user_logged_in = True
                    st.success("✅ Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")

# Run the Application
if __name__ == "__main__":
    if not st.session_state.user_logged_in:
        auth_page()
    else:
        home_page()
