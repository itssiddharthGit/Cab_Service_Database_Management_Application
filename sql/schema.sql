-- ===================================================
-- CAB SERVICE MANAGEMENT SYSTEM - DATABASE SCHEMA
-- ===================================================

-- Drop tables if exist (for clean setup)
DROP TABLE IF EXISTS Payment;
DROP TABLE IF EXISTS Trip;
DROP TABLE IF EXISTS Vehicle;
DROP TABLE IF EXISTS VehicleType;
DROP TABLE IF EXISTS Driver;
DROP TABLE IF EXISTS User;

-- ===================================================
-- TABLE: User
-- ===================================================
CREATE TABLE User (
    User_ID INT PRIMARY KEY AUTO_INCREMENT,
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50) NOT NULL,
    Phone_Number VARCHAR(15) NOT NULL UNIQUE,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Registration_Date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Last_Login DATETIME,
    
    -- Constraints
    CONSTRAINT chk_user_phone CHECK (Phone_Number REGEXP '^[0-9]{10,15}$'),
    CONSTRAINT chk_user_email CHECK (Email LIKE '%@%.%')
);

-- ===================================================
-- TABLE: Driver
-- ===================================================
CREATE TABLE Driver (
    Driver_ID INT PRIMARY KEY AUTO_INCREMENT,
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50) NOT NULL,
    Phone_Number VARCHAR(15) NOT NULL UNIQUE,
    License_Number VARCHAR(20) NOT NULL UNIQUE,
    Rating DECIMAL(2,1) DEFAULT 0.0,
    Status ENUM('Active', 'Inactive', 'Suspended') NOT NULL DEFAULT 'Active',
    Current_Active_Location VARCHAR(200),
    Join_Date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Last_Active DATETIME,
    
    -- Constraints
    CONSTRAINT chk_driver_phone CHECK (Phone_Number REGEXP '^[0-9]{10,15}$'),
    CONSTRAINT chk_driver_rating CHECK (Rating >= 0.0 AND Rating <= 5.0)
);

-- ===================================================
-- TABLE: VehicleType (Lookup Table)
-- ===================================================
CREATE TABLE VehicleType (
    Vehicle_Type VARCHAR(20) PRIMARY KEY,
    Standard_Capacity INT NOT NULL,
    Base_Fare_Per_Km DECIMAL(6,2) NOT NULL,
    Description VARCHAR(100),
    
    -- Constraints
    CONSTRAINT chk_capacity CHECK (Standard_Capacity > 0),
    CONSTRAINT chk_base_fare CHECK (Base_Fare_Per_Km > 0)
);

-- ===================================================
-- TABLE: Vehicle
-- ===================================================
CREATE TABLE Vehicle (
    Vehicle_ID INT PRIMARY KEY AUTO_INCREMENT,
    Driver_ID INT,
    Vehicle_Type VARCHAR(20) NOT NULL,
    Vehicle_Number VARCHAR(20) NOT NULL UNIQUE,
    Make VARCHAR(30),
    Model VARCHAR(30),
    Year INT,
    Status ENUM('Available', 'In_Use', 'Maintenance') NOT NULL DEFAULT 'Available',
    Assignment_Date DATETIME,
    Registration_Date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    CONSTRAINT fk_vehicle_driver 
        FOREIGN KEY (Driver_ID) REFERENCES Driver(Driver_ID)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    
    CONSTRAINT fk_vehicle_type
        FOREIGN KEY (Vehicle_Type) REFERENCES VehicleType(Vehicle_Type)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    
    -- Constraints
    CONSTRAINT chk_vehicle_year CHECK (Year >= 1990 AND Year <= 2030)
);

-- ===================================================
-- TABLE: Trip
-- ===================================================
CREATE TABLE Trip (
    Trip_ID INT PRIMARY KEY AUTO_INCREMENT,
    User_ID INT,
    Driver_ID INT,
    Vehicle_ID INT,
    Pickup_Location VARCHAR(200) NOT NULL,
    Dropoff_Location VARCHAR(200) NOT NULL,
    Pickup_Time DATETIME,
    Dropoff_Time DATETIME,
    Booking_Time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Distance DECIMAL(8,2),
    Fare DECIMAL(10,2),
    Status ENUM('Pending', 'Accepted', 'In_Progress', 'Completed', 'Cancelled') 
        NOT NULL DEFAULT 'Pending',
    
    -- Foreign Keys
    CONSTRAINT fk_trip_user
        FOREIGN KEY (User_ID) REFERENCES User(User_ID)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    
    CONSTRAINT fk_trip_driver
        FOREIGN KEY (Driver_ID) REFERENCES Driver(Driver_ID)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    
    CONSTRAINT fk_trip_vehicle
        FOREIGN KEY (Vehicle_ID) REFERENCES Vehicle(Vehicle_ID)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    
    -- Constraints
    CONSTRAINT chk_trip_distance CHECK (Distance >= 0),
    CONSTRAINT chk_trip_fare CHECK (Fare >= 0),
    CONSTRAINT chk_trip_times CHECK (Dropoff_Time IS NULL OR Dropoff_Time >= Pickup_Time)
);

-- ===================================================
-- TABLE: Payment
-- ===================================================
CREATE TABLE Payment (
    Payment_ID INT PRIMARY KEY AUTO_INCREMENT,
    Trip_ID INT NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    Payment_Mode VARCHAR(20) NOT NULL,
    Payment_Status ENUM('Pending', 'Completed', 'Failed', 'Refunded') 
        NOT NULL DEFAULT 'Pending',
    Payment_DateTime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Reference_Number VARCHAR(50) UNIQUE,
    
    -- Foreign Keys
    CONSTRAINT fk_payment_trip
        FOREIGN KEY (Trip_ID) REFERENCES Trip(Trip_ID)
        ON DELETE RESTRICT  -- Cannot delete trip if payment exists
        ON UPDATE CASCADE,
    
    -- Constraints
    CONSTRAINT chk_payment_amount CHECK (Amount >= 0),
    CONSTRAINT chk_payment_mode CHECK (Payment_Mode IN ('Cash', 'Card', 'UPI', 'Wallet', 'Net_Banking'))
);

-- ===================================================
-- INDEXES FOR PERFORMANCE
-- ===================================================

-- User Indexes
CREATE INDEX idx_user_phone ON User(Phone_Number);
CREATE INDEX idx_user_email ON User(Email);
CREATE INDEX idx_user_registration ON User(Registration_Date);

-- Driver Indexes
CREATE INDEX idx_driver_phone ON Driver(Phone_Number);
CREATE INDEX idx_driver_license ON Driver(License_Number);
CREATE INDEX idx_driver_status ON Driver(Status);
CREATE INDEX idx_driver_rating ON Driver(Rating);

-- Vehicle Indexes
CREATE INDEX idx_vehicle_driver ON Vehicle(Driver_ID);
CREATE INDEX idx_vehicle_type ON Vehicle(Vehicle_Type);
CREATE INDEX idx_vehicle_status ON Vehicle(Status);
CREATE INDEX idx_vehicle_number ON Vehicle(Vehicle_Number);

-- Trip Indexes (Critical for performance)
CREATE INDEX idx_trip_user ON Trip(User_ID);
CREATE INDEX idx_trip_driver ON Trip(Driver_ID);
CREATE INDEX idx_trip_vehicle ON Trip(Vehicle_ID);
CREATE INDEX idx_trip_status ON Trip(Status);
CREATE INDEX idx_trip_booking_time ON Trip(Booking_Time);
CREATE INDEX idx_trip_driver_status ON Trip(Driver_ID, Status);  -- Composite index
CREATE INDEX idx_trip_user_status ON Trip(User_ID, Status);      -- Composite index

-- Payment Indexes
CREATE INDEX idx_payment_trip ON Payment(Trip_ID);
CREATE INDEX idx_payment_status ON Payment(Payment_Status);
CREATE INDEX idx_payment_datetime ON Payment(Payment_DateTime);
CREATE INDEX idx_payment_mode ON Payment(Payment_Mode);

-- ===================================================
-- SAMPLE DATA INSERTION (VehicleType Lookup)
-- ===================================================

INSERT INTO VehicleType (Vehicle_Type, Standard_Capacity, Base_Fare_Per_Km, Description) VALUES
('Hatchback', 4, 8.00, 'Compact car for city rides'),
('Sedan', 4, 10.00, 'Comfortable sedan for standard rides'),
('SUV', 6, 15.00, 'Large vehicle for groups'),
('Luxury', 4, 25.00, 'Premium luxury vehicle'),
('Auto', 3, 6.00, 'Three-wheeler auto-rickshaw'),
('Bike', 1, 5.00, 'Two-wheeler for single passenger');

-- ===================================================
-- USEFUL VIEWS
-- ===================================================

-- View: Active Trips with Details
CREATE VIEW vw_active_trips AS
SELECT 
    t.Trip_ID,
    t.Status,
    u.First_Name AS User_Name,
    u.Phone_Number AS User_Phone,
    d.First_Name AS Driver_Name,
    d.Phone_Number AS Driver_Phone,
    v.Vehicle_Number,
    vt.Vehicle_Type,
    t.Pickup_Location,
    t.Dropoff_Location,
    t.Booking_Time,
    t.Fare
FROM Trip t
LEFT JOIN User u ON t.User_ID = u.User_ID
LEFT JOIN Driver d ON t.Driver_ID = d.Driver_ID
LEFT JOIN Vehicle v ON t.Vehicle_ID = v.Vehicle_ID
LEFT JOIN VehicleType vt ON v.Vehicle_Type = vt.Vehicle_Type
WHERE t.Status IN ('Pending', 'Accepted', 'In_Progress');

-- View: Driver Earnings Summary
CREATE VIEW vw_driver_earnings AS
SELECT 
    d.Driver_ID,
    d.First_Name,
    d.Last_Name,
    COUNT(t.Trip_ID) AS Total_Trips,
    SUM(CASE WHEN t.Status = 'Completed' THEN t.Fare ELSE 0 END) AS Total_Earnings,
    AVG(CASE WHEN t.Status = 'Completed' THEN t.Fare ELSE NULL END) AS Avg_Fare_Per_Trip,
    d.Rating
FROM Driver d
LEFT JOIN Trip t ON d.Driver_ID = t.Driver_ID
GROUP BY d.Driver_ID, d.First_Name, d.Last_Name, d.Rating;

-- View: Payment Summary
CREATE VIEW vw_payment_summary AS
SELECT 
    p.Payment_ID,
    p.Trip_ID,
    t.User_ID,
    u.First_Name AS User_Name,
    p.Amount,
    p.Payment_Mode,
    p.Payment_Status,
    p.Payment_DateTime,
    t.Fare AS Trip_Fare,
    (p.Amount - t.Fare) AS Discount_Applied
FROM Payment p
JOIN Trip t ON p.Trip_ID = t.Trip_ID
LEFT JOIN User u ON t.User_ID = u.User_ID;

-- ===================================================
-- END OF SCHEMA
-- ===================================================