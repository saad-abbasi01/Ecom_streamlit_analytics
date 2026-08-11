import pandas as pd
import plotly.express as px
import sqlalchemy
import streamlit as st

# Page setup
st.set_page_config(
    page_title="E-commerce Analytics Dashboard", page_icon="📊", layout="wide"
)
st.title("📊 Interactive E-Commerce Sales & Customers Analytics")
st.markdown(
    "Explore customer behavior, purchase counts, and interactive trends."
)
st.divider()


# Helper function to establish connection
def get_db_engine():
    # Database URL format: mysql+mysqlconnector://user:password@host:port/database
    database_url = "mysql+mysqlconnector://root:@localhost:3306/college"
    return sqlalchemy.create_engine(database_url)


# Cache data, not the connection
@st.cache_data(ttl=600)  # Caches output data for 10 minutes
def load_data():
    engine = get_db_engine()

    # Query tables
    user_df = pd.read_sql_query("SELECT * FROM users", engine)
    try:
        sales_df = pd.read_sql_query("SELECT * FROM sales", engine)
    except Exception:
        sales_df = pd.read_sql_query("SELECT * FROM intercations", engine)

    return user_df, sales_df


# Load and render data
try:
    user_df, sales_df = load_data()
    st.success("Successfully connected to MySQL database!")

    st.subheader("Data Preview")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Users Table:**")
        st.dataframe(user_df.head(), use_container_width=True)

    with col2:
        st.write("**Sales / Interactions Table:**")
        st.dataframe(sales_df.head(), use_container_width=True)

except Exception as e:
    # Displaying {e} will now show you the EXACT error!
    st.error(f"Error connecting to MySQL database: {e}")