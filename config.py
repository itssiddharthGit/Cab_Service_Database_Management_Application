"""
Configuration file for Cab Service Management System
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'cab_service'),
    'port': int(os.getenv('DB_PORT', 3307))
}

# App Configuration
APP_TITLE = "🚖 Cab Service Management System"
APP_ICON = "🚖"

# Status Options
TRIP_STATUS = ['Pending', 'Accepted', 'In_Progress', 'Completed', 'Cancelled']
PAYMENT_STATUS = ['Pending', 'Completed', 'Failed', 'Refunded']
DRIVER_STATUS = ['Active', 'Inactive', 'Suspended']
VEHICLE_STATUS = ['Available', 'In_Use', 'Maintenance']
PAYMENT_MODES = ['Cash', 'Card', 'UPI', 'Wallet', 'Net_Banking']

# Pagination
RECORDS_PER_PAGE = 10