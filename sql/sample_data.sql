-- ===================================================
-- SAMPLE DATA FOR CAB SERVICE MANAGEMENT SYSTEM
-- Run this after creating the schema
-- ===================================================

USE cab_service;

-- ===================================================
-- INSERT USERS
-- ===================================================
INSERT INTO User (First_Name, Last_Name, Phone_Number, Email, Registration_Date) VALUES
('Rahul', 'Sharma', '9876543210', 'rahul.sharma@email.com', DATE_SUB(NOW(), INTERVAL 30 DAY)),
('Priya', 'Patel', '9876543211', 'priya.patel@email.com', DATE_SUB(NOW(), INTERVAL 25 DAY)),
('Amit', 'Kumar', '9876543212', 'amit.kumar@email.com', DATE_SUB(NOW(), INTERVAL 20 DAY)),
('Sneha', 'Reddy', '9876543213', 'sneha.reddy@email.com', DATE_SUB(NOW(), INTERVAL 15 DAY)),
('Vikram', 'Singh', '9876543214', 'vikram.singh@email.com', DATE_SUB(NOW(), INTERVAL 10 DAY)),
('Anjali', 'Gupta', '9876543215', 'anjali.gupta@email.com', DATE_SUB(NOW(), INTERVAL 5 DAY)),
('Rohan', 'Mehta', '9876543216', 'rohan.mehta@email.com', DATE_SUB(NOW(), INTERVAL 3 DAY)),
('Kavya', 'Iyer', '9876543217', 'kavya.iyer@email.com', DATE_SUB(NOW(), INTERVAL 2 DAY)),
('Arjun', 'Nair', '9876543218', 'arjun.nair@email.com', DATE_SUB(NOW(), INTERVAL 1 DAY)),
('Pooja', 'Joshi', '9876543219', 'pooja.joshi@email.com', NOW());

-- ===================================================
-- INSERT DRIVERS
-- ===================================================
INSERT INTO Driver (First_Name, Last_Name, Phone_Number, License_Number, Rating, Status, Join_Date) VALUES
('Rajesh', 'Kumar', '9123456780', 'DL-01-2020-001234', 4.8, 'Active', DATE_SUB(NOW(), INTERVAL 180 DAY)),
('Suresh', 'Babu', '9123456781', 'DL-01-2020-001235', 4.6, 'Active', DATE_SUB(NOW(), INTERVAL 150 DAY)),
('Mahesh', 'Rao', '9123456782', 'DL-01-2020-001236', 4.9, 'Active', DATE_SUB(NOW(), INTERVAL 120 DAY)),
('Ramesh', 'Verma', '9123456783', 'DL-01-2020-001237', 4.7, 'Active', DATE_SUB(NOW(), INTERVAL 90 DAY)),
('Ganesh', 'Pillai', '9123456784', 'DL-01-2020-001238', 4.5, 'Active', DATE_SUB(NOW(), INTERVAL 60 DAY)),
('Dinesh', 'Yadav', '9123456785', 'DL-01-2020-001239', 4.4, 'Active', DATE_SUB(NOW(), INTERVAL 45 DAY)),
('Naresh', 'Patil', '9123456786', 'DL-01-2020-001240', 4.8, 'Active', DATE_SUB(NOW(), INTERVAL 30 DAY)),
('Kiran', 'Shah', '9123456787', 'DL-01-2020-001241', 4.6, 'Active', DATE_SUB(NOW(), INTERVAL 20 DAY)),
('Prakash', 'Desai', '9123456788', 'DL-01-2020-001242', 3.9, 'Inactive', DATE_SUB(NOW(), INTERVAL 15 DAY)),
('Anil', 'Chopra', '9123456789', 'DL-01-2020-001243', 4.2, 'Active', DATE_SUB(NOW(), INTERVAL 10 DAY));

-- ===================================================
-- INSERT VEHICLES
-- ===================================================
INSERT INTO Vehicle (Driver_ID, Vehicle_Type, Vehicle_Number, Make, Model, Year, Status, Assignment_Date) VALUES
(1, 'Sedan', 'KA-01-AB-1234', 'Toyota', 'Camry', 2022, 'Available', DATE_SUB(NOW(), INTERVAL 180 DAY)),
(2, 'Hatchback', 'KA-01-AB-1235', 'Maruti', 'Swift', 2023, 'Available', DATE_SUB(NOW(), INTERVAL 150 DAY)),
(3, 'SUV', 'KA-01-AB-1236', 'Mahindra', 'XUV700', 2023, 'Available', DATE_SUB(NOW(), INTERVAL 120 DAY)),
(4, 'Sedan', 'KA-01-AB-1237', 'Honda', 'City', 2022, 'Available', DATE_SUB(NOW(), INTERVAL 90 DAY)),
(5, 'Luxury', 'KA-01-AB-1238', 'Mercedes', 'E-Class', 2024, 'Available', DATE_SUB(NOW(), INTERVAL 60 DAY)),
(6, 'Hatchback', 'KA-01-AB-1239', 'Hyundai', 'i20', 2023, 'Available', DATE_SUB(NOW(), INTERVAL 45 DAY)),
(7, 'SUV', 'KA-01-AB-1240', 'Tata', 'Harrier', 2023, 'Available', DATE_SUB(NOW(), INTERVAL 30 DAY)),
(8, 'Auto', 'KA-01-AB-1241', 'Bajaj', 'RE', 2021, 'Available', DATE_SUB(NOW(), INTERVAL 20 DAY)),
(9, 'Sedan', 'KA-01-AB-1242', 'Volkswagen', 'Vento', 2020, 'Maintenance', DATE_SUB(NOW(), INTERVAL 15 DAY)),
(10, 'Bike', 'KA-01-AB-1243', 'Royal Enfield', 'Classic 350', 2023, 'Available', DATE_SUB(NOW(), INTERVAL 10 DAY));

-- ===================================================
-- INSERT COMPLETED TRIPS (Past trips for history)
-- ===================================================
INSERT INTO Trip (User_ID, Driver_ID, Vehicle_ID, Pickup_Location, Dropoff_Location, Pickup_Time, Dropoff_Time, Booking_Time, Distance, Fare, Status) VALUES
(1, 1, 1, 'MG Road, Bangalore', 'Koramangala, Bangalore', DATE_SUB(NOW(), INTERVAL 25 DAY), DATE_SUB(NOW(), INTERVAL 25 DAY) + INTERVAL 30 MINUTE, DATE_SUB(NOW(), INTERVAL 25 DAY) - INTERVAL 10 MINUTE, 8.5, 85.00, 'Completed'),
(2, 2, 2, 'Electronic City', 'Whitefield', DATE_SUB(NOW(), INTERVAL 23 DAY), DATE_SUB(NOW(), INTERVAL 23 DAY) + INTERVAL 45 MINUTE, DATE_SUB(NOW(), INTERVAL 23 DAY) - INTERVAL 5 MINUTE, 25.3, 202.40, 'Completed'),
(3, 3, 3, 'Indiranagar', 'Airport', DATE_SUB(NOW(), INTERVAL 20 DAY), DATE_SUB(NOW(), INTERVAL 20 DAY) + INTERVAL 50 MINUTE, DATE_SUB(NOW(), INTERVAL 20 DAY) - INTERVAL 15 MINUTE, 35.2, 528.00, 'Completed'),
(4, 4, 4, 'JP Nagar', 'Marathahalli', DATE_SUB(NOW(), INTERVAL 18 DAY), DATE_SUB(NOW(), INTERVAL 18 DAY) + INTERVAL 40 MINUTE, DATE_SUB(NOW(), INTERVAL 18 DAY) - INTERVAL 8 MINUTE, 18.7, 187.00, 'Completed'),
(5, 5, 5, 'UB City', 'Hebbal', DATE_SUB(NOW(), INTERVAL 15 DAY), DATE_SUB(NOW(), INTERVAL 15 DAY) + INTERVAL 35 MINUTE, DATE_SUB(NOW(), INTERVAL 15 DAY) - INTERVAL 12 MINUTE, 12.4, 310.00, 'Completed'),
(6, 6, 6, 'HSR Layout', 'BTM Layout', DATE_SUB(NOW(), INTERVAL 12 DAY), DATE_SUB(NOW(), INTERVAL 12 DAY) + INTERVAL 20 MINUTE, DATE_SUB(NOW(), INTERVAL 12 DAY) - INTERVAL 5 MINUTE, 6.2, 49.60, 'Completed'),
(7, 7, 7, 'Jayanagar', 'Yelahanka', DATE_SUB(NOW(), INTERVAL 10 DAY), DATE_SUB(NOW(), INTERVAL 10 DAY) + INTERVAL 55 MINUTE, DATE_SUB(NOW(), INTERVAL 10 DAY) - INTERVAL 10 MINUTE, 28.9, 433.50, 'Completed'),
(8, 8, 8, 'Malleshwaram', 'Rajajinagar', DATE_SUB(NOW(), INTERVAL 8 DAY), DATE_SUB(NOW(), INTERVAL 8 DAY) + INTERVAL 15 MINUTE, DATE_SUB(NOW(), INTERVAL 8 DAY) - INTERVAL 3 MINUTE, 4.5, 27.00, 'Completed'),
(1, 2, 2, 'Koramangala', 'Electronic City', DATE_SUB(NOW(), INTERVAL 6 DAY), DATE_SUB(NOW(), INTERVAL 6 DAY) + INTERVAL 40 MINUTE, DATE_SUB(NOW(), INTERVAL 6 DAY) - INTERVAL 7 MINUTE, 22.1, 176.80, 'Completed'),
(3, 4, 4, 'Whitefield', 'Indiranagar', DATE_SUB(NOW(), INTERVAL 5 DAY), DATE_SUB(NOW(), INTERVAL 5 DAY) + INTERVAL 45 MINUTE, DATE_SUB(NOW(), INTERVAL 5 DAY) - INTERVAL 10 MINUTE, 24.8, 248.00, 'Completed'),
(2, 1, 1, 'Airport', 'MG Road', DATE_SUB(NOW(), INTERVAL 4 DAY), DATE_SUB(NOW(), INTERVAL 4 DAY) + INTERVAL 50 MINUTE, DATE_SUB(NOW(), INTERVAL 4 DAY) - INTERVAL 15 MINUTE, 36.7, 367.00, 'Completed'),
(5, 6, 6, 'Banashankari', 'Basavanagudi', DATE_SUB(NOW(), INTERVAL 3 DAY), DATE_SUB(NOW(), INTERVAL 3 DAY) + INTERVAL 25 MINUTE, DATE_SUB(NOW(), INTERVAL 3 DAY) - INTERVAL 5 MINUTE, 7.3, 58.40, 'Completed'),
(4, 3, 3, 'Vijayanagar', 'Yeshwanthpur', DATE_SUB(NOW(), INTERVAL 2 DAY), DATE_SUB(NOW(), INTERVAL 2 DAY) + INTERVAL 30 MINUTE, DATE_SUB(NOW(), INTERVAL 2 DAY) - INTERVAL 8 MINUTE, 11.2, 168.00, 'Completed');

-- ===================================================
-- INSERT PENDING TRIPS (Current trip requests)
-- ===================================================
INSERT INTO Trip (User_ID, Pickup_Location, Dropoff_Location, Booking_Time, Status) VALUES
(6, 'Richmond Road', 'Koramangala', DATE_SUB(NOW(), INTERVAL 15 MINUTE), 'Pending'),
(7, 'Bellandur', 'Sarjapur Road', DATE_SUB(NOW(), INTERVAL 10 MINUTE), 'Pending'),
(8, 'Cunningham Road', 'Commercial Street', DATE_SUB(NOW(), INTERVAL 5 MINUTE), 'Pending');

-- ===================================================
-- INSERT ACTIVE TRIPS (Ongoing)
-- ===================================================
INSERT INTO Trip (User_ID, Driver_ID, Vehicle_ID, Pickup_Location, Dropoff_Location, Pickup_Time, Booking_Time, Distance, Status) VALUES
(9, 7, 7, 'Hebbal', 'Manyata Tech Park', DATE_SUB(NOW(), INTERVAL 20 MINUTE), DATE_SUB(NOW(), INTERVAL 30 MINUTE), NULL, 'In_Progress'),
(10, 5, 5, 'Palace Road', 'Sadashivanagar', DATE_SUB(NOW(), INTERVAL 10 MINUTE), DATE_SUB(NOW(), INTERVAL 15 MINUTE), NULL, 'Accepted');

-- ===================================================
-- INSERT PAYMENTS (For completed trips)
-- ===================================================
INSERT INTO Payment (Trip_ID, Amount, Payment_Mode, Payment_Status, Payment_DateTime, Reference_Number) VALUES
(1, 85.00, 'UPI', 'Completed', DATE_SUB(NOW(), INTERVAL 25 DAY) + INTERVAL 35 MINUTE, 'PAY00000001'),
(2, 202.40, 'Card', 'Completed', DATE_SUB(NOW(), INTERVAL 23 DAY) + INTERVAL 50 MINUTE, 'PAY00000002'),
(3, 528.00, 'Cash', 'Completed', DATE_SUB(NOW(), INTERVAL 20 DAY) + INTERVAL 55 MINUTE, 'PAY00000003'),
(4, 187.00, 'UPI', 'Completed', DATE_SUB(NOW(), INTERVAL 18 DAY) + INTERVAL 45 MINUTE, 'PAY00000004'),
(5, 310.00, 'Card', 'Completed', DATE_SUB(NOW(), INTERVAL 15 DAY) + INTERVAL 40 MINUTE, 'PAY00000005'),
(6, 49.60, 'Cash', 'Completed', DATE_SUB(NOW(), INTERVAL 12 DAY) + INTERVAL 25 MINUTE, 'PAY00000006'),
(7, 433.50, 'UPI', 'Completed', DATE_SUB(NOW(), INTERVAL 10 DAY) + INTERVAL 60 MINUTE, 'PAY00000007'),
(8, 27.00, 'Cash', 'Completed', DATE_SUB(NOW(), INTERVAL 8 DAY) + INTERVAL 20 MINUTE, 'PAY00000008'),
(9, 176.80, 'Wallet', 'Completed', DATE_SUB(NOW(), INTERVAL 6 DAY) + INTERVAL 45 MINUTE, 'PAY00000009'),
(10, 248.00, 'UPI', 'Completed', DATE_SUB(NOW(), INTERVAL 5 DAY) + INTERVAL 50 MINUTE, 'PAY00000010'),
(11, 367.00, 'Card', 'Completed', DATE_SUB(NOW(), INTERVAL 4 DAY) + INTERVAL 55 MINUTE, 'PAY00000011'),
(12, 58.40, 'Cash', 'Completed', DATE_SUB(NOW(), INTERVAL 3 DAY) + INTERVAL 30 MINUTE, 'PAY00000012'),
(13, 168.00, 'UPI', 'Completed', DATE_SUB(NOW(), INTERVAL 2 DAY) + INTERVAL 35 MINUTE, 'PAY00000013');

-- ===================================================
-- VERIFY DATA INSERTION
-- ===================================================
SELECT 'Users Inserted:' AS Status, COUNT(*) AS Count FROM User
UNION ALL
SELECT 'Drivers Inserted:', COUNT(*) FROM Driver
UNION ALL
SELECT 'Vehicles Inserted:', COUNT(*) FROM Vehicle
UNION ALL
SELECT 'Trips Inserted:', COUNT(*) FROM Trip
UNION ALL
SELECT 'Payments Inserted:', COUNT(*) FROM Payment;

-- ===================================================
-- END OF SAMPLE DATA
-- ===================================================