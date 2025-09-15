import streamlit as st
import sqlite3
import pandas as pd

# Initialize database
def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Add user to database
def add_user(name, role):
    conn = sqlite3.connect('users.db')
    conn.execute('INSERT INTO users (name, role) VALUES (?, ?)', (name, role))
    conn.commit()
    conn.close()

# Get all users from database
def get_users():
    conn = sqlite3.connect('users.db')
    df = pd.read_sql_query('SELECT * FROM users', conn)
    conn.close()
    return df

# Initialize database
init_db()

# App title
st.title("User Management App")

# Create tabs
tab1, tab2 = st.tabs(["Add User", "View Users"])

# Tab 1: Add User
# Tab 1: Add User
with tab1:
    st.header("Add New User")
    
    # Using st.form with clear_on_submit=True for automatic clearing
    with st.form("user_form", clear_on_submit=True):
        name = st.text_input("Name", placeholder="Enter user name")
        role = st.text_input("Role", placeholder="Enter user role")
        
        submitted = st.form_submit_button("Add User", type="primary", use_container_width=True)
        
        if submitted:
            if name and role:
                try:
                    add_user(name.strip(), role.strip())
                    st.success(f"✅ User '{name}' with role '{role}' added successfully!")
                   
                except Exception as e:
                    st.error(f"❌ Error adding user: {str(e)}")
            else:
                st.error("❌ Please fill in both name and role fields.")

# Tab 2: View Users
with tab2:
    st.header("All Users")
    
    df = get_users()
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No users found. Add some users!")
