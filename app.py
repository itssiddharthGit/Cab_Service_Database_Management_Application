"""
Enhanced Cab Service Management System with Multi-Page Navigation
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from database import get_database
from config import APP_TITLE, APP_ICON

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar
)

# Enhanced Custom CSS with modern styling
st.markdown("""
    <style>
    /* Hide sidebar completely */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Modern gradient header */
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        animation: slideDown 0.5s ease-out;
    }
    
    @keyframes slideDown {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Navigation pills */
    .nav-container {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    
    /* Success/Error alerts with icons */
    .stAlert {
        border-radius: 10px;
        padding: 1rem 1.5rem;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Data tables */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Form styling */
    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stNumberInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        transition: border-color 0.3s;
    }
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus, .stNumberInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102,126,234,0.1);
    }
    
    /* Page section headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #333;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    /* Cards for trip requests */
    .trip-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
        transition: all 0.3s;
    }
    
    .trip-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        transform: translateX(5px);
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .status-pending { background: #fff3cd; color: #856404; }
    .status-accepted { background: #d1ecf1; color: #0c5460; }
    .status-in-progress { background: #cce5ff; color: #004085; }
    .status-completed { background: #d4edda; color: #155724; }
    .status-cancelled { background: #f8d7da; color: #721c24; }
    </style>
""", unsafe_allow_html=True)

# Initialize database
db = get_database()

# Initialize session state for notifications and page
if 'show_notification' not in st.session_state:
    st.session_state.show_notification = False
if 'notification_message' not in st.session_state:
    st.session_state.notification_message = ""
if 'notification_type' not in st.session_state:
    st.session_state.notification_type = "success"
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

# Function to show notification
def show_notification(message, notification_type="success"):
    st.session_state.show_notification = True
    st.session_state.notification_message = message
    st.session_state.notification_type = notification_type

# Display notification banner if active
if st.session_state.show_notification:
    if st.session_state.notification_type == "success":
        st.success(f"✅ {st.session_state.notification_message}", icon="✅")
    elif st.session_state.notification_type == "error":
        st.error(f"❌ {st.session_state.notification_message}", icon="❌")
    elif st.session_state.notification_type == "info":
        st.info(f"ℹ️ {st.session_state.notification_message}", icon="ℹ️")
    st.session_state.show_notification = False

# Title
st.markdown(f'<div class="main-header">{APP_ICON} Cab Service Management System</div>', unsafe_allow_html=True)

# Modern Navigation Pills
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

pages = {
    "🏠 Dashboard": col1,
    "👥 Users": col2,
    "🚗 Drivers": col3,
    "🚙 Vehicles": col4,
    "🛣️ Trip Requests": col5,
    "💰 Payments": col6,
    "📊 Analytics": col7
}

for page_name, col in pages.items():
    with col:
        if st.button(page_name, key=f"nav_{page_name}", use_container_width=True):
            st.session_state.current_page = page_name
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Get current page
page = st.session_state.current_page

# =====================================================
# DASHBOARD PAGE
# =====================================================
if page == "🏠 Dashboard":
    st.markdown('<p class="section-header">Dashboard Overview</p>', unsafe_allow_html=True)
    
    # Get statistics
    stats = db.get_dashboard_stats()
    
    # Display metrics with custom styling
    col1, col2, col3, col4 = st.columns(4)
    
    metrics_data = [
        ("👥", "Total Users", stats['total_users'], col1),
        ("🚗", "Active Drivers", stats['active_drivers'], col2),
        ("🚙", "Available Vehicles", stats['available_vehicles'], col3),
        ("⏳", "Pending Requests", stats['pending_trips'], col4)
    ]
    
    for icon, label, value, col in metrics_data:
        with col:
            st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size: 2rem;">{icon}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-label">{label}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    metrics_data2 = [
        ("🔄", "Ongoing Trips", stats['ongoing_trips'], col1),
        ("✅", "Completed Trips", stats['completed_trips'], col2),
        ("💰", "Total Revenue", f"₹{stats['total_revenue']:,.2f}", col3),
        ("📈", "Avg Revenue/Trip", f"₹{stats['total_revenue']/stats['completed_trips'] if stats['completed_trips'] > 0 else 0:,.2f}", col4)
    ]
    
    for icon, label, value, col in metrics_data2:
        with col:
            st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size: 2rem;">{icon}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-label">{label}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Trip Status Distribution")
        trip_dist = db.get_trip_status_distribution()
        if not trip_dist.empty:
            fig = px.pie(trip_dist, values='count', names='Status', 
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        hole=0.4)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No trip data available")
    
    with col2:
        st.subheader("💵 Revenue by Vehicle Type")
        revenue_data = db.get_revenue_by_vehicle_type()
        if not revenue_data.empty:
            fig = px.bar(revenue_data, x='Vehicle_Type', y='Total_Revenue',
                        color='Total_Revenue', 
                        color_continuous_scale='Viridis',
                        labels={'Total_Revenue': 'Revenue (₹)', 'Vehicle_Type': 'Vehicle Type'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No revenue data available")
    
    # Recent Activity
    st.divider()
    st.subheader("🕒 Recent Trips")
    recent_trips = db.get_all_trips().head(10)
    if not recent_trips.empty:
        st.dataframe(recent_trips, use_container_width=True, hide_index=True)
    else:
        st.info("No recent trips")

# =====================================================
# USERS PAGE
# =====================================================
elif page == "👥 Users":
    st.markdown('<p class="section-header">User Management</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 View Users", "➕ Add User", "🔍 Search Users"])
    
    with tab1:
        users_df = db.get_all_users()
        
        if not users_df.empty:
            st.info(f"📊 Total Users: {len(users_df)}")
            st.dataframe(users_df, use_container_width=True, hide_index=True)
            
            # Quick actions
            st.divider()
            st.subheader("⚡ Quick Actions")
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                user_id = st.number_input("Select User ID", min_value=1, step=1, key="user_action_id")
            with col2:
                if st.button("✏️ Edit User", use_container_width=True):
                    st.session_state.edit_user_id = user_id
                    st.rerun()
            with col3:
                if st.button("🗑️ Delete User", use_container_width=True, type="primary"):
                    if db.delete_user(user_id):
                        show_notification(f"User #{user_id} deleted successfully!", "success")
                        st.rerun()
                    else:
                        show_notification("Failed to delete user", "error")
            
            # Edit form if user selected
            if 'edit_user_id' in st.session_state:
                user = db.get_user_by_id(st.session_state.edit_user_id)
                if user:
                    st.divider()
                    with st.form("edit_user_form"):
                        st.subheader(f"✏️ Edit User #{st.session_state.edit_user_id}")
                        col1, col2 = st.columns(2)
                        with col1:
                            first_name = st.text_input("First Name*", value=user['First_Name'])
                            phone = st.text_input("Phone Number*", value=user['Phone_Number'])
                        with col2:
                            last_name = st.text_input("Last Name*", value=user['Last_Name'])
                            email = st.text_input("Email*", value=user['Email'])
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 Update User", use_container_width=True, type="primary"):
                                if db.update_user(st.session_state.edit_user_id, first_name, last_name, phone, email):
                                    show_notification(f"User #{st.session_state.edit_user_id} updated successfully!", "success")
                                    del st.session_state.edit_user_id
                                    st.rerun()
                                else:
                                    show_notification("Failed to update user", "error")
                        with col2:
                            if st.form_submit_button("❌ Cancel", use_container_width=True):
                                del st.session_state.edit_user_id
                                st.rerun()
        else:
            st.info("👋 No users found. Add your first user to get started!")
    
    with tab2:
        with st.form("add_user_form", clear_on_submit=True):
            st.subheader("➕ Add New User")
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name*", placeholder="John")
                phone = st.text_input("Phone Number*", placeholder="9876543210")
            with col2:
                last_name = st.text_input("Last Name*", placeholder="Doe")
                email = st.text_input("Email*", placeholder="john.doe@example.com")
            
            if st.form_submit_button("➕ Add User", type="primary", use_container_width=True):
                if first_name and last_name and phone and email:
                    result = db.create_user(first_name, last_name, phone, email)
                    if result:
                        show_notification(f"✅ User added successfully! User ID: {result}", "success")
                        st.rerun()
                    else:
                        show_notification("❌ Failed to add user. Phone/Email might already exist.", "error")
                else:
                    show_notification("⚠️ Please fill all required fields!", "error")
    
    with tab3:
        st.subheader("🔍 Advanced User Search")
        col1, col2, col3 = st.columns(3)
        with col1:
            search_by = st.selectbox("Search By", ["Name", "Phone", "Email"])
        with col2:
            search_term = st.text_input("Search Term", placeholder="Enter search term...")
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            search_button = st.button("🔍 Search", use_container_width=True)
        
        if search_button and search_term:
            users_df = db.get_all_users()
            if search_by == "Name":
                filtered = users_df[users_df['First_Name'].str.contains(search_term, case=False) | 
                                   users_df['Last_Name'].str.contains(search_term, case=False)]
            elif search_by == "Phone":
                filtered = users_df[users_df['Phone_Number'].str.contains(search_term)]
            else:
                filtered = users_df[users_df['Email'].str.contains(search_term, case=False)]
            
            if not filtered.empty:
                st.success(f"✅ Found {len(filtered)} user(s)")
                st.dataframe(filtered, use_container_width=True, hide_index=True)
            else:
                st.warning("⚠️ No users found matching your search")

# =====================================================
# DRIVERS PAGE
# =====================================================
elif page == "🚗 Drivers":
    st.markdown('<p class="section-header">Driver Management</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 View Drivers", "➕ Add Driver", "🔍 Filter Drivers"])
    
    with tab1:
        drivers_df = db.get_all_drivers()
        
        if not drivers_df.empty:
            st.info(f"📊 Total Drivers: {len(drivers_df)}")
            st.dataframe(drivers_df, use_container_width=True, hide_index=True)
        else:
            st.info("👋 No drivers found. Add your first driver!")
    
    with tab2:
        with st.form("add_driver_form", clear_on_submit=True):
            st.subheader("➕ Add New Driver")
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name*", placeholder="Rajesh")
                phone = st.text_input("Phone Number*", placeholder="9123456789")
                license_number = st.text_input("License Number*", placeholder="DL-01-2020-001234")
            with col2:
                last_name = st.text_input("Last Name*", placeholder="Kumar")
                status = st.selectbox("Status*", ['Active', 'Inactive', 'Suspended'])
                rating = st.number_input("Initial Rating", 0.0, 5.0, 0.0, 0.1)
            
            if st.form_submit_button("➕ Add Driver", type="primary", use_container_width=True):
                if first_name and last_name and phone and license_number:
                    result = db.create_driver(first_name, last_name, phone, license_number, status)
                    if result:
                        show_notification(f"✅ Driver added successfully! Driver ID: {result}", "success")
                        st.rerun()
                    else:
                        show_notification("❌ Failed to add driver. Phone/License might already exist.", "error")
                else:
                    show_notification("⚠️ Please fill all required fields!", "error")
    
    with tab3:
        st.subheader("🔍 Filter Drivers")
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.multiselect("Filter by Status", ['Active', 'Inactive', 'Suspended'], default=['Active'])
        with col2:
            min_rating = st.slider("Minimum Rating", 0.0, 5.0, 0.0, 0.1)
        
        if status_filter:
            drivers_df = db.get_all_drivers()
            filtered = drivers_df[drivers_df['Status'].isin(status_filter)]
            if min_rating > 0:
                filtered = filtered[filtered['Rating'] >= min_rating]
            
            if not filtered.empty:
                st.success(f"✅ Found {len(filtered)} driver(s)")
                st.dataframe(filtered, use_container_width=True, hide_index=True)
            else:
                st.warning("⚠️ No drivers match your filters")

# =====================================================
# VEHICLES PAGE
# =====================================================
elif page == "🚙 Vehicles":
    st.markdown('<p class="section-header">Vehicle Management</p>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📋 View Vehicles", "➕ Add Vehicle"])
    
    with tab1:
        vehicles_df = db.get_all_vehicles()
        
        if not vehicles_df.empty:
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                status_filter = st.multiselect("Filter by Status", ['Available', 'In_Use', 'Maintenance'], 
                                              default=['Available'])
            with col2:
                type_filter = st.multiselect("Filter by Type", 
                                            vehicles_df['Vehicle_Type'].unique().tolist() if 'Vehicle_Type' in vehicles_df else [])
            
            filtered_df = vehicles_df.copy()
            if status_filter:
                filtered_df = filtered_df[filtered_df['Status'].isin(status_filter)]
            if type_filter:
                filtered_df = filtered_df[filtered_df['Vehicle_Type'].isin(type_filter)]
            
            st.info(f"📊 Showing {len(filtered_df)} of {len(vehicles_df)} vehicles")
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        else:
            st.info("👋 No vehicles found. Add your first vehicle!")
    
    with tab2:
        vehicle_types = db.get_vehicle_types()
        
        with st.form("add_vehicle_form", clear_on_submit=True):
            st.subheader("➕ Add New Vehicle")
            col1, col2, col3 = st.columns(3)
            with col1:
                vehicle_number = st.text_input("Vehicle Number*", placeholder="KA-01-AB-1234")
                make = st.text_input("Make*", placeholder="Toyota")
            with col2:
                vehicle_type = st.selectbox("Vehicle Type*", [vt['Vehicle_Type'] for vt in vehicle_types])
                model = st.text_input("Model*", placeholder="Camry")
            with col3:
                year = st.number_input("Year*", 1990, 2030, 2024)
                status = st.selectbox("Status", ['Available', 'In_Use', 'Maintenance'])
            
            driver_id = st.number_input("Assign to Driver ID (optional - leave 0 for unassigned)", 0, step=1)
            
            if st.form_submit_button("➕ Add Vehicle", type="primary", use_container_width=True):
                if vehicle_number and make and model and vehicle_type:
                    driver_id_val = driver_id if driver_id > 0 else None
                    result = db.create_vehicle(driver_id_val, vehicle_type, vehicle_number, 
                                              make, model, year, status)
                    if result:
                        show_notification(f"✅ Vehicle added successfully! Vehicle ID: {result}", "success")
                        st.rerun()
                    else:
                        show_notification("❌ Failed to add vehicle. Vehicle number might already exist.", "error")
                else:
                    show_notification("⚠️ Please fill all required fields!", "error")

# =====================================================
# TRIP REQUESTS PAGE (Enhanced)
# =====================================================
elif page == "🛣️ Trip Requests":
    st.markdown('<p class="section-header">Trip Request Management</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 All Trips", "🆕 Create Trip Request", "⏳ Pending Requests"])
    
    with tab1:
        trips_df = db.get_all_trips()
        
        if not trips_df.empty:
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                status_filter = st.multiselect("Filter by Status", 
                                              ['Pending', 'Accepted', 'In_Progress', 'Completed', 'Cancelled'],
                                              default=['Pending', 'Accepted', 'In_Progress'])
            with col2:
                date_filter = st.date_input("From Date", value=datetime.now().date() - timedelta(days=30))
            with col3:
                search_user = st.text_input("Search by User/Driver Name")
            
            filtered_df = trips_df.copy()
            if status_filter:
                filtered_df = filtered_df[filtered_df['Status'].isin(status_filter)]
            if search_user:
                filtered_df = filtered_df[
                    filtered_df['User_Name'].str.contains(search_user, case=False, na=False) |
                    filtered_df['Driver_Name'].str.contains(search_user, case=False, na=False)
                ]
            
            st.info(f"📊 Showing {len(filtered_df)} of {len(trips_df)} trips")
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        else:
            st.info("👋 No trips found. Create your first trip request!")
    
    with tab2:
        users = db.get_users_list()
        
        with st.form("create_trip_form", clear_on_submit=True):
            st.subheader("🆕 Create New Trip Request")
            
            if users:
                col1, col2 = st.columns(2)
                with col1:
                    user_select = st.selectbox("Select User*", options=[u['user_info'] for u in users])
                    user_id = users[[u['user_info'] for u in users].index(user_select)]['User_ID']
                    pickup_location = st.text_input("Pickup Location*", placeholder="MG Road, Bangalore")
                with col2:
                    st.markdown("<br>" * 2, unsafe_allow_html=True)
                    dropoff_location = st.text_input("Dropoff Location*", placeholder="Koramangala, Bangalore")
                
                # Show available drivers and vehicles
                st.divider()
                st.subheader("🚗 Available Resources (Optional - Assign Now)")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Available Drivers:**")
                    available_drivers = db.get_available_drivers()
                    if available_drivers:
                        driver_options = ["Don't assign now"] + [d['driver_info'] for d in available_drivers]
                        driver_select = st.selectbox("Select Driver (optional)", driver_options)
                        driver_id = None
                        if driver_select != "Don't assign now":
                            driver_id = available_drivers[[d['driver_info'] for d in available_drivers].index(driver_select)]['Driver_ID']
                    else:
                        st.warning("⚠️ No drivers available")
                        driver_id = None
                
                with col2:
                    st.markdown("**Available Vehicles:**")
                    available_vehicles = db.get_available_vehicles()
                    if available_vehicles:
                        vehicle_options = ["Don't assign now"] + [v['vehicle_info'] for v in available_vehicles]
                        vehicle_select = st.selectbox("Select Vehicle (optional)", vehicle_options)
                        vehicle_id = None
                        if vehicle_select != "Don't assign now":
                            vehicle_id = available_vehicles[[v['vehicle_info'] for v in available_vehicles].index(vehicle_select)]['Vehicle_ID']
                    else:
                        st.warning("⚠️ No vehicles available")
                        vehicle_id = None
                
                if st.form_submit_button("🚀 Create Trip Request", type="primary", use_container_width=True):
                    if user_id and pickup_location and dropoff_location:
                        result = db.create_trip(user_id, pickup_location, dropoff_location)
                        if result:
                            # If driver and vehicle selected, assign them
                            if driver_id and vehicle_id:
                                db.assign_driver_vehicle(result, driver_id, vehicle_id)
                                show_notification(f"✅ Trip #{result} created and assigned to driver!", "success")
                            else:
                                show_notification(f"✅ Trip request #{result} created successfully! Awaiting assignment.", "success")
                            st.rerun()
                        else:
                            show_notification("❌ Failed to create trip request", "error")
                    else:
                        show_notification("⚠️ Please fill all required fields!", "error")
            else:
                st.error("❌ No users available. Please add users first.")
    
    with tab3:
        st.subheader("⏳ Pending Trip Requests - Quick Assignment")
        
        # Get pending trips
        pending_query = """
            SELECT 
                t.Trip_ID,
                CONCAT(u.First_Name, ' ', u.Last_Name) AS User_Name,
                u.Phone_Number AS User_Phone,
                t.Pickup_Location,
                t.Dropoff_Location,
                t.Booking_Time,
                t.Status
            FROM Trip t
            JOIN User u ON t.User_ID = u.User_ID
            WHERE t.Status = 'Pending'
            ORDER BY t.Booking_Time ASC
        """
        pending_trips = db.fetch_dataframe(pending_query)
        
        if not pending_trips.empty:
            st.success(f"✅ {len(pending_trips)} pending request(s) waiting for assignment")
            
            for idx, trip in pending_trips.iterrows():
                with st.expander(f"🚕 Trip #{trip['Trip_ID']} - {trip['User_Name']} ({trip['Pickup_Location']} → {trip['Dropoff_Location']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        **📍 Pickup:** {trip['Pickup_Location']}  
                        **📍 Dropoff:** {trip['Dropoff_Location']}  
                        **👤 User:** {trip['User_Name']} ({trip['User_Phone']})  
                        **🕒 Requested:** {trip['Booking_Time']}
                        """)
                    
                    with col2:
                        # Assignment form
                        with st.form(f"assign_trip_{trip['Trip_ID']}"):
                            available_drivers = db.get_available_drivers()
                            available_vehicles = db.get_available_vehicles()
                            
                            if available_drivers and available_vehicles:
                                driver_select = st.selectbox(f"Select Driver", 
                                                            [d['driver_info'] for d in available_drivers],
                                                            key=f"driver_{trip['Trip_ID']}")
                                vehicle_select = st.selectbox(f"Select Vehicle", 
                                                             [v['vehicle_info'] for v in available_vehicles],
                                                             key=f"vehicle_{trip['Trip_ID']}")
                                
                                if st.form_submit_button("✅ Assign & Accept Trip", type="primary", use_container_width=True):
                                    driver_id = available_drivers[[d['driver_info'] for d in available_drivers].index(driver_select)]['Driver_ID']
                                    vehicle_id = available_vehicles[[v['vehicle_info'] for v in available_vehicles].index(vehicle_select)]['Vehicle_ID']
                                    
                                    if db.assign_driver_vehicle(trip['Trip_ID'], driver_id, vehicle_id):
                                        show_notification(f"✅ Trip #{trip['Trip_ID']} assigned successfully!", "success")
                                        st.rerun()
                                    else:
                                        show_notification("❌ Failed to assign trip", "error")
                            else:
                                st.warning("⚠️ No available drivers or vehicles to assign")
        else:
            st.info("✨ No pending requests at the moment!")

# =====================================================
# PAYMENTS PAGE
# =====================================================
elif page == "💰 Payments":
    st.markdown('<p class="section-header">Payment Management</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 All Payments", "➕ Add Payment", "🔍 Payment Analytics"])
    
    with tab1:
        payments_df = db.get_all_payments()
        
        if not payments_df.empty:
            # Filters
            col1, col2 = st.columns(2)
            with col1:
                status_filter = st.multiselect("Filter by Status", 
                                              ['Pending', 'Completed', 'Failed', 'Refunded'],
                                              default=['Pending', 'Completed'])
            with col2:
                mode_filter = st.multiselect("Filter by Payment Mode",
                                            payments_df['Payment_Mode'].unique().tolist() if 'Payment_Mode' in payments_df else [])
            
            filtered_df = payments_df.copy()
            if status_filter:
                filtered_df = filtered_df[filtered_df['Payment_Status'].isin(status_filter)]
            if mode_filter:
                filtered_df = filtered_df[filtered_df['Payment_Mode'].isin(mode_filter)]
            
            st.info(f"📊 Showing {len(filtered_df)} of {len(payments_df)} payments")
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
            
            # Quick status update
            st.divider()
            st.subheader("⚡ Quick Payment Status Update")
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                payment_id = st.number_input("Payment ID", min_value=1, step=1)
            with col2:
                new_status = st.selectbox("New Status", ['Completed', 'Failed', 'Refunded'])
            with col3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("💾 Update", use_container_width=True, type="primary"):
                    if db.update_payment_status(payment_id, new_status):
                        show_notification(f"✅ Payment #{payment_id} status updated to {new_status}", "success")
                        st.rerun()
                    else:
                        show_notification("❌ Failed to update payment status", "error")
        else:
            st.info("👋 No payments recorded yet")
    
    with tab2:
        trips = db.get_completed_trips_without_payment()
        
        with st.form("add_payment_form", clear_on_submit=True):
            st.subheader("➕ Add New Payment")
            
            if trips:
                trip_select = st.selectbox("Select Trip*", [t['trip_info'] for t in trips])
                trip_id = trips[[t['trip_info'] for t in trips].index(trip_select)]['Trip_ID']
                
                col1, col2 = st.columns(2)
                with col1:
                    amount = st.number_input("Amount (₹)*", min_value=0.0, step=10.0)
                    payment_mode = st.selectbox("Payment Mode*", ['Cash', 'Card', 'UPI', 'Wallet', 'Net_Banking'])
                with col2:
                    payment_status = st.selectbox("Payment Status", ['Pending', 'Completed'])
                    reference = st.text_input("Reference Number (optional)")
                
                if st.form_submit_button("➕ Add Payment", type="primary", use_container_width=True):
                    result = db.create_payment(trip_id, amount, payment_mode, payment_status)
                    if result:
                        if reference:
                            db.update_payment_status(result, payment_status, reference)
                        show_notification(f"✅ Payment added successfully! Payment ID: {result}", "success")
                        st.rerun()
                    else:
                        show_notification("❌ Failed to add payment", "error")
            else:
                st.info("✨ All completed trips have payments recorded!")
    
    with tab3:
        st.subheader("📊 Payment Analytics")
        
        # Payment mode distribution
        payments_df = db.get_all_payments()
        if not payments_df.empty:
            completed_payments = payments_df[payments_df['Payment_Status'] == 'Completed']
            
            col1, col2 = st.columns(2)
            
            with col1:
                mode_dist = completed_payments.groupby('Payment_Mode')['Amount'].agg(['count', 'sum']).reset_index()
                mode_dist.columns = ['Payment_Mode', 'Count', 'Total_Amount']
                
                fig = px.pie(mode_dist, values='Count', names='Payment_Mode',
                            title='Payment Mode Distribution',
                            color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(mode_dist, x='Payment_Mode', y='Total_Amount',
                            title='Revenue by Payment Mode',
                            color='Total_Amount',
                            color_continuous_scale='Viridis')
                st.plotly_chart(fig, use_container_width=True)

# =====================================================
# ANALYTICS PAGE
# =====================================================
elif page == "📊 Analytics":
    st.markdown('<p class="section-header">Advanced Analytics & Reports</p>', unsafe_allow_html=True)
    
    stats = db.get_dashboard_stats()
    revenue_data = db.get_revenue_by_vehicle_type()
    
    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    
    kpis = [
        ("✅", "Completed Trips", stats['completed_trips'], col1),
        ("💰", "Total Revenue", f"₹{stats['total_revenue']:,.2f}", col2),
        ("🚗", "Active Drivers", stats['active_drivers'], col3),
        ("📈", "Avg Revenue/Trip", f"₹{stats['total_revenue']/stats['completed_trips'] if stats['completed_trips'] > 0 else 0:,.2f}", col4)
    ]
    
    for icon, label, value, col in kpis:
        with col:
            st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size: 2rem;">{icon}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-label">{label}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Charts
    if not revenue_data.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💵 Revenue Distribution")
            fig = px.pie(revenue_data, values='Total_Revenue', names='Vehicle_Type',
                        title='Revenue by Vehicle Type',
                        color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🚙 Trip Count by Vehicle Type")
            fig = px.bar(revenue_data, x='Vehicle_Type', y='Total_Trips',
                        title='Trips by Vehicle Type',
                        color='Total_Trips',
                        color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Data Export
    st.subheader("📥 Export Data")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        users_df = db.get_all_users()
        if not users_df.empty:
            csv = users_df.to_csv(index=False)
            st.download_button("📥 Export Users", csv, "users.csv", "text/csv", use_container_width=True)
    
    with col2:
        drivers_df = db.get_all_drivers()
        if not drivers_df.empty:
            csv = drivers_df.to_csv(index=False)
            st.download_button("📥 Export Drivers", csv, "drivers.csv", "text/csv", use_container_width=True)
    
    with col3:
        trips_df = db.get_all_trips()
        if not trips_df.empty:
            csv = trips_df.to_csv(index=False)
            st.download_button("📥 Export Trips", csv, "trips.csv", "text/csv", use_container_width=True)
    
    with col4:
        payments_df = db.get_all_payments()
        if not payments_df.empty:
            csv = payments_df.to_csv(index=False)
            st.download_button("📥 Export Payments", csv, "payments.csv", "text/csv", use_container_width=True)

# Footer with animated cab
st.divider()

# Animated cab moving across screen
st.markdown("""
    <style>
    @keyframes drive {
        from {
        transform: translateX(100vw);
    }
    to {
        transform: translateX(-150px);
    }
    }
    
    .cab-container {
        position: relative;
        height: 100px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .animated-cab {
        position: absolute;
        font-size: 5rem;
        animation: drive 8s linear infinite;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.2));
    }
    </style>
    
    <div class="cab-container">
        <div class="animated-cab">🚕</div>
    </div>
    
    <div style='text-align: center; color: gray; padding: 1rem;'>
        🚖 Cab Service Management System v2.0 | Built with ❤️ using Streamlit
    </div>
""", unsafe_allow_html=True)