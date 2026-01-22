"""
Database connection and operations for Cab Service Management System
"""
import mysql.connector
from mysql.connector import Error
import pandas as pd
import streamlit as st
from config import DB_CONFIG


class Database:
    """Database connection and operations handler"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                return True
        except Error as e:
            st.error(f"Database connection error: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            if self.cursor:
                self.cursor.close()
            self.connection.close()
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute a query and return results"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            self.cursor.execute(query, params or ())
            
            if fetch:
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                return self.cursor.lastrowid
                
        except Error as e:
            st.error(f"Query execution error: {e}")
            self.connection.rollback()
            return None
    
    def fetch_dataframe(self, query, params=None):
        """Execute query and return pandas DataFrame"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            return pd.read_sql(query, self.connection, params=params)
        except Error as e:
            st.error(f"DataFrame fetch error: {e}")
            return pd.DataFrame()
    
    # ==================== USER OPERATIONS ====================
    
    def create_user(self, first_name, last_name, phone, email):
        """Create new user"""
        query = """
            INSERT INTO User (First_Name, Last_Name, Phone_Number, Email)
            VALUES (%s, %s, %s, %s)
        """
        return self.execute_query(query, (first_name, last_name, phone, email))
    
    def get_all_users(self):
        """Get all users"""
        query = """
            SELECT User_ID, First_Name, Last_Name, Phone_Number, Email, 
                   Registration_Date, Last_Login
            FROM User
            ORDER BY Registration_Date DESC
        """
        return self.fetch_dataframe(query)
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        query = "SELECT * FROM User WHERE User_ID = %s"
        result = self.execute_query(query, (user_id,), fetch=True)
        return result[0] if result else None
    
    def update_user(self, user_id, first_name, last_name, phone, email):
        """Update user details"""
        query = """
            UPDATE User 
            SET First_Name = %s, Last_Name = %s, Phone_Number = %s, Email = %s
            WHERE User_ID = %s
        """
        return self.execute_query(query, (first_name, last_name, phone, email, user_id))
    
    def delete_user(self, user_id):
        """Delete user"""
        query = "DELETE FROM User WHERE User_ID = %s"
        return self.execute_query(query, (user_id,))
    
    # ==================== DRIVER OPERATIONS ====================
    
    def create_driver(self, first_name, last_name, phone, license_number, status='Active'):
        """Create new driver"""
        query = """
            INSERT INTO Driver (First_Name, Last_Name, Phone_Number, License_Number, Status)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (first_name, last_name, phone, license_number, status))
    
    def get_all_drivers(self):
        """Get all drivers with vehicle info"""
        query = """
            SELECT 
                d.Driver_ID, d.First_Name, d.Last_Name, d.Phone_Number,
                d.License_Number, d.Rating, d.Status, d.Join_Date,
                v.Vehicle_Number, v.Make, v.Model, vt.Vehicle_Type
            FROM Driver d
            LEFT JOIN Vehicle v ON d.Driver_ID = v.Driver_ID
            LEFT JOIN VehicleType vt ON v.Vehicle_Type = vt.Vehicle_Type
            ORDER BY d.Join_Date DESC
        """
        return self.fetch_dataframe(query)
    
    def get_driver_by_id(self, driver_id):
        """Get driver by ID"""
        query = "SELECT * FROM Driver WHERE Driver_ID = %s"
        result = self.execute_query(query, (driver_id,), fetch=True)
        return result[0] if result else None
    
    def update_driver(self, driver_id, first_name, last_name, phone, license_number, status, rating=None):
        """Update driver details"""
        query = """
            UPDATE Driver 
            SET First_Name = %s, Last_Name = %s, Phone_Number = %s, 
                License_Number = %s, Status = %s, Rating = %s
            WHERE Driver_ID = %s
        """
        return self.execute_query(query, (first_name, last_name, phone, license_number, 
                                         status, rating, driver_id))
    
    def delete_driver(self, driver_id):
        """Delete driver"""
        query = "DELETE FROM Driver WHERE Driver_ID = %s"
        return self.execute_query(query, (driver_id,))
    
    def get_available_drivers(self):
        """Get available drivers not on active trip"""
        query = """
            SELECT d.Driver_ID, CONCAT(d.First_Name, ' ', d.Last_Name, ' - ', d.Phone_Number) AS driver_info
            FROM Driver d
            WHERE d.Status = 'Active'
              AND d.Driver_ID NOT IN (
                  SELECT Driver_ID FROM Trip 
                  WHERE Status IN ('Accepted', 'In_Progress') AND Driver_ID IS NOT NULL
              )
            ORDER BY d.Rating DESC
        """
        return self.execute_query(query, fetch=True)
    
    # ==================== VEHICLE OPERATIONS ====================
    
    def create_vehicle(self, driver_id, vehicle_type, vehicle_number, make, model, year, status='Available'):
        """Create new vehicle"""
        query = """
            INSERT INTO Vehicle (Driver_ID, Vehicle_Type, Vehicle_Number, Make, Model, Year, Status, Assignment_Date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """
        return self.execute_query(query, (driver_id, vehicle_type, vehicle_number, 
                                         make, model, year, status))
    
    def get_all_vehicles(self):
        """Get all vehicles"""
        query = """
            SELECT 
                v.Vehicle_ID, v.Vehicle_Number, v.Make, v.Model, v.Year,
                vt.Vehicle_Type, vt.Standard_Capacity, v.Status,
                CONCAT(d.First_Name, ' ', d.Last_Name) AS Driver_Name,
                d.Phone_Number AS Driver_Phone
            FROM Vehicle v
            JOIN VehicleType vt ON v.Vehicle_Type = vt.Vehicle_Type
            LEFT JOIN Driver d ON v.Driver_ID = d.Driver_ID
            ORDER BY v.Registration_Date DESC
        """
        return self.fetch_dataframe(query)
    
    def get_vehicle_types(self):
        """Get all vehicle types"""
        query = "SELECT Vehicle_Type, Standard_Capacity, Base_Fare_Per_Km FROM VehicleType"
        return self.execute_query(query, fetch=True)
    
    def get_vehicle_by_id(self, vehicle_id):
        """Get vehicle by ID"""
        query = "SELECT * FROM Vehicle WHERE Vehicle_ID = %s"
        result = self.execute_query(query, (vehicle_id,), fetch=True)
        return result[0] if result else None
    
    def update_vehicle(self, vehicle_id, driver_id, vehicle_type, vehicle_number, 
                      make, model, year, status):
        """Update vehicle details"""
        query = """
            UPDATE Vehicle 
            SET Driver_ID = %s, Vehicle_Type = %s, Vehicle_Number = %s,
                Make = %s, Model = %s, Year = %s, Status = %s
            WHERE Vehicle_ID = %s
        """
        return self.execute_query(query, (driver_id, vehicle_type, vehicle_number, 
                                         make, model, year, status, vehicle_id))
    
    def delete_vehicle(self, vehicle_id):
        """Delete vehicle"""
        query = "DELETE FROM Vehicle WHERE Vehicle_ID = %s"
        return self.execute_query(query, (vehicle_id,))
    
    def get_available_vehicles(self):
        """Get available vehicles"""
        query = """
            SELECT v.Vehicle_ID, 
                   CONCAT(v.Vehicle_Number, ' - ', v.Make, ' ', v.Model, ' (', vt.Vehicle_Type, ')') AS vehicle_info
            FROM Vehicle v
            JOIN VehicleType vt ON v.Vehicle_Type = vt.Vehicle_Type
            WHERE v.Status = 'Available'
            ORDER BY vt.Vehicle_Type
        """
        return self.execute_query(query, fetch=True)
    
    # ==================== TRIP OPERATIONS ====================
    
    def create_trip(self, user_id, pickup_location, dropoff_location):
        """Create new trip"""
        query = """
            INSERT INTO Trip (User_ID, Pickup_Location, Dropoff_Location, Status)
            VALUES (%s, %s, %s, 'Pending')
        """
        return self.execute_query(query, (user_id, pickup_location, dropoff_location))
    
    def get_all_trips(self):
        """Get all trips with details"""
        query = """
            SELECT 
                t.Trip_ID, t.Status,
                CONCAT(u.First_Name, ' ', u.Last_Name) AS User_Name,
                CONCAT(d.First_Name, ' ', d.Last_Name) AS Driver_Name,
                v.Vehicle_Number,
                t.Pickup_Location, t.Dropoff_Location,
                t.Booking_Time, t.Pickup_Time, t.Dropoff_Time,
                t.Distance, t.Fare
            FROM Trip t
            LEFT JOIN User u ON t.User_ID = u.User_ID
            LEFT JOIN Driver d ON t.Driver_ID = d.Driver_ID
            LEFT JOIN Vehicle v ON t.Vehicle_ID = v.Vehicle_ID
            ORDER BY t.Booking_Time DESC
        """
        return self.fetch_dataframe(query)
    
    def get_trip_by_id(self, trip_id):
        """Get trip by ID"""
        query = "SELECT * FROM Trip WHERE Trip_ID = %s"
        result = self.execute_query(query, (trip_id,), fetch=True)
        return result[0] if result else None
    
    def update_trip_status(self, trip_id, status, driver_id=None, vehicle_id=None, 
                          distance=None, fare=None):
        """Update trip status and details"""
        query = """
            UPDATE Trip 
            SET Status = %s, Driver_ID = %s, Vehicle_ID = %s, Distance = %s, Fare = %s
            WHERE Trip_ID = %s
        """
        return self.execute_query(query, (status, driver_id, vehicle_id, distance, fare, trip_id))
    
    def assign_driver_vehicle(self, trip_id, driver_id, vehicle_id):
        """Assign driver and vehicle to trip"""
        query = """
            UPDATE Trip 
            SET Driver_ID = %s, Vehicle_ID = %s, Status = 'Accepted', Pickup_Time = NOW()
            WHERE Trip_ID = %s
        """
        return self.execute_query(query, (driver_id, vehicle_id, trip_id))
    
    def complete_trip(self, trip_id, distance, fare):
        """Complete trip"""
        query = """
            UPDATE Trip 
            SET Status = 'Completed', Dropoff_Time = NOW(), Distance = %s, Fare = %s
            WHERE Trip_ID = %s
        """
        return self.execute_query(query, (distance, fare, trip_id))
    
    def delete_trip(self, trip_id):
        """Delete trip"""
        query = "DELETE FROM Trip WHERE Trip_ID = %s"
        return self.execute_query(query, (trip_id,))
    
    def get_users_list(self):
        """Get users for dropdown"""
        query = "SELECT User_ID, CONCAT(First_Name, ' ', Last_Name, ' - ', Phone_Number) AS user_info FROM User"
        return self.execute_query(query, fetch=True)
    
    # ==================== PAYMENT OPERATIONS ====================
    
    def create_payment(self, trip_id, amount, payment_mode, payment_status='Pending'):
        """Create payment"""
        query = """
            INSERT INTO Payment (Trip_ID, Amount, Payment_Mode, Payment_Status)
            VALUES (%s, %s, %s, %s)
        """
        return self.execute_query(query, (trip_id, amount, payment_mode, payment_status))
    
    def get_all_payments(self):
        """Get all payments"""
        query = """
            SELECT 
                p.Payment_ID, p.Trip_ID, p.Amount, p.Payment_Mode,
                p.Payment_Status, p.Payment_DateTime, p.Reference_Number,
                CONCAT(u.First_Name, ' ', u.Last_Name) AS User_Name,
                t.Fare AS Trip_Fare
            FROM Payment p
            JOIN Trip t ON p.Trip_ID = t.Trip_ID
            LEFT JOIN User u ON t.User_ID = u.User_ID
            ORDER BY p.Payment_DateTime DESC
        """
        return self.fetch_dataframe(query)
    
    def get_payment_by_id(self, payment_id):
        """Get payment by ID"""
        query = "SELECT * FROM Payment WHERE Payment_ID = %s"
        result = self.execute_query(query, (payment_id,), fetch=True)
        return result[0] if result else None
    
    def update_payment_status(self, payment_id, payment_status, reference_number=None):
        """Update payment status"""
        query = """
            UPDATE Payment 
            SET Payment_Status = %s, Reference_Number = %s, Payment_DateTime = NOW()
            WHERE Payment_ID = %s
        """
        return self.execute_query(query, (payment_status, reference_number, payment_id))
    
    def delete_payment(self, payment_id):
        """Delete payment"""
        query = "DELETE FROM Payment WHERE Payment_ID = %s"
        return self.execute_query(query, (payment_id,))
    
    def get_completed_trips_without_payment(self):
        """Get completed trips without payment"""
        query = """
            SELECT t.Trip_ID, 
                   CONCAT('Trip #', t.Trip_ID, ' - ', u.First_Name, ' ', u.Last_Name, 
                          ' (₹', t.Fare, ')') AS trip_info
            FROM Trip t
            LEFT JOIN Payment p ON t.Trip_ID = p.Trip_ID
            LEFT JOIN User u ON t.User_ID = u.User_ID
            WHERE t.Status = 'Completed' AND p.Payment_ID IS NULL
            ORDER BY t.Dropoff_Time DESC
        """
        return self.execute_query(query, fetch=True)
    
    # ==================== ANALYTICS ====================
    
    def get_dashboard_stats(self):
        """Get dashboard statistics"""
        stats = {}
        
        # Total counts
        stats['total_users'] = self.execute_query("SELECT COUNT(*) as count FROM User", fetch=True)[0]['count']
        stats['total_drivers'] = self.execute_query("SELECT COUNT(*) as count FROM Driver", fetch=True)[0]['count']
        stats['total_vehicles'] = self.execute_query("SELECT COUNT(*) as count FROM Vehicle", fetch=True)[0]['count']
        stats['total_trips'] = self.execute_query("SELECT COUNT(*) as count FROM Trip", fetch=True)[0]['count']
        
        # Active counts
        stats['active_drivers'] = self.execute_query(
            "SELECT COUNT(*) as count FROM Driver WHERE Status = 'Active'", fetch=True)[0]['count']
        stats['available_vehicles'] = self.execute_query(
            "SELECT COUNT(*) as count FROM Vehicle WHERE Status = 'Available'", fetch=True)[0]['count']
        
        # Trip stats
        stats['pending_trips'] = self.execute_query(
            "SELECT COUNT(*) as count FROM Trip WHERE Status = 'Pending'", fetch=True)[0]['count']
        stats['ongoing_trips'] = self.execute_query(
            "SELECT COUNT(*) as count FROM Trip WHERE Status IN ('Accepted', 'In_Progress')", fetch=True)[0]['count']
        stats['completed_trips'] = self.execute_query(
            "SELECT COUNT(*) as count FROM Trip WHERE Status = 'Completed'", fetch=True)[0]['count']
        
        # Revenue
        revenue_result = self.execute_query(
            "SELECT COALESCE(SUM(Amount), 0) as total FROM Payment WHERE Payment_Status = 'Completed'", 
            fetch=True)
        stats['total_revenue'] = revenue_result[0]['total'] if revenue_result else 0
        
        return stats
    
    def get_trip_status_distribution(self):
        """Get trip status distribution for charts"""
        query = """
            SELECT Status, COUNT(*) as count
            FROM Trip
            GROUP BY Status
        """
        return self.fetch_dataframe(query)
    
    def get_revenue_by_vehicle_type(self):
        """Get revenue by vehicle type"""
        query = """
            SELECT 
                vt.Vehicle_Type,
                COUNT(t.Trip_ID) AS Total_Trips,
                COALESCE(SUM(t.Fare), 0) AS Total_Revenue
            FROM VehicleType vt
            LEFT JOIN Vehicle v ON vt.Vehicle_Type = v.Vehicle_Type
            LEFT JOIN Trip t ON v.Vehicle_ID = t.Vehicle_ID AND t.Status = 'Completed'
            GROUP BY vt.Vehicle_Type
            ORDER BY Total_Revenue DESC
        """
        return self.fetch_dataframe(query)


# Singleton instance
@st.cache_resource
def get_database():
    """Get cached database instance"""
    db = Database()
    db.connect()
    return db