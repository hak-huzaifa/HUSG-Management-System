-- Drop tables if they already exist
IF OBJECT_ID('Cabinet_Chair', 'U') IS NOT NULL DROP TABLE Cabinet_Chair;
IF OBJECT_ID('Meetings', 'U') IS NOT NULL DROP TABLE Meetings;
IF OBJECT_ID('Events_Calendar', 'U') IS NOT NULL DROP TABLE Events_Calendar;
IF OBJECT_ID('Task_Allocation', 'U') IS NOT NULL DROP TABLE Task_Allocation;
IF OBJECT_ID('Cabinet_Member', 'U') IS NOT NULL DROP TABLE Cabinet_Member;
IF OBJECT_ID('Cabinet', 'U') IS NOT NULL DROP TABLE Cabinet;
IF OBJECT_ID('User', 'U') IS NOT NULL DROP TABLE [User];

-- Create tables based on the schema

CREATE TABLE [User] (
    HU_ID INT PRIMARY KEY,
    Password NVARCHAR(50),
    Email NVARCHAR(50),
    Designation NVARCHAR(50),
    ContactNumber BIGINT
);

CREATE TABLE Cabinet (
    Cabinet_ID INT PRIMARY KEY,
    Cabinet_Name NVARCHAR(50),
    Budget INT
);

CREATE TABLE Cabinet_Member (
    HU_ID INT,
    Cabinet_ID INT,
    Cabinet_Name NVARCHAR(50),
    Is_Active BIT,
    Year DATE,
    PRIMARY KEY (HU_ID, Cabinet_ID),
    FOREIGN KEY (HU_ID) REFERENCES [User](HU_ID),
    FOREIGN KEY (Cabinet_ID) REFERENCES Cabinet(Cabinet_ID)
);

CREATE TABLE Task_Allocation (
    Task_ID INT PRIMARY KEY,
    Task_Name NVARCHAR(50),
    Description NVARCHAR(255),
    Deadline DATETIME,
    Status BIT,
    Created_By INT,
    Assigned_To INT,
    FOREIGN KEY (Created_By) REFERENCES [User](HU_ID),
    FOREIGN KEY (Assigned_To) REFERENCES [User](HU_ID)
);

CREATE TABLE Events_Calendar (
    Event_ID INT PRIMARY KEY,
    Event_Name NVARCHAR(50),
    Date DATE,
    Time TIME,
    Location NVARCHAR(100),
    Created_by INT,
    FOREIGN KEY (Created_by) REFERENCES [User](HU_ID)
);

CREATE TABLE Meetings (
    Meeting_ID INT PRIMARY KEY,
    Created_By INT,
    Time TIME,
    Date DATE,
    Invitation_to NVARCHAR(100),
    FOREIGN KEY (Created_By) REFERENCES [User](HU_ID)
);

CREATE TABLE Cabinet_Chair (
    HU_ID INT,
    Cabinet_ID INT,
    Cabinet_Name NVARCHAR(50),
    Role NVARCHAR(50),
    Year DATE,
    Is_Active BIT,
    PRIMARY KEY (HU_ID, Cabinet_ID),
    FOREIGN KEY (HU_ID) REFERENCES [User](HU_ID),
    FOREIGN KEY (Cabinet_ID) REFERENCES Cabinet(Cabinet_ID)
);

-- Insert sample data

-- User entries
INSERT INTO [User] (HU_ID, Password, Email, Designation, ContactNumber) VALUES
(1, 'pass123', 'president@example.com', 'President', 1234567890),
(2, 'pass456', 'vp@example.com', 'Vice President', 1234567891),
(3, 'pass789', 'treasurer@example.com', 'Treasurer', 1234567892),
(4, 'pass101', 'gensec@example.com', 'General Secretary', 1234567893),
(5, 'pass111', 'ra_chair@example.com', 'Chair of Rights Advocacy & Ethos', 1234567894),
(6, 'pass222', 'events_chair@example.com', 'Chair of Events', 1234567895),
(7, 'pass333', 'pr_chair@example.com', 'Chair of Public Relations', 1234567896),
(8, 'pass444', 'academic_chair@example.com', 'Chair of Academic Affairs', 1234567897),
(9, 'pass555', 'food_chair@example.com', 'Chair of Food and Hygiene', 1234567898);

-- Cabinet entries
INSERT INTO Cabinet (Cabinet_ID, Cabinet_Name, Budget) VALUES
(1, 'Executive Council', 50000),
(2, 'Rights Advocacy & Ethos', 20000),
(3, 'Events', 30000),
(4, 'Public Relations and Communications', 25000),
(5, 'Academic Affairs', 22000),
(6, 'Food and Hygiene', 18000);

-- Cabinet_Member entries
INSERT INTO Cabinet_Member (HU_ID, Cabinet_ID, Cabinet_Name, Is_Active, Year) VALUES
(1, 1, 'Executive Council', 1, '2023-01-01'),
(2, 1, 'Executive Council', 1, '2023-01-01'),
(3, 1, 'Executive Council', 1, '2023-01-01'),
(4, 1, 'Executive Council', 1, '2023-01-01'),
(5, 2, 'Rights Advocacy & Ethos', 1, '2023-01-01'),
(6, 3, 'Events', 1, '2023-01-01'),
(7, 4, 'Public Relations and Communications', 1, '2023-01-01'),
(8, 5, 'Academic Affairs', 1, '2023-01-01'),
(9, 6, 'Food and Hygiene', 1, '2023-01-01');

-- Task_Allocation entries
INSERT INTO Task_Allocation (Task_ID, Task_Name, Description, Deadline, Status, Created_By, Assigned_To) VALUES
(1, 'Organize Annual Event', 'Organize the main annual event', '2023-12-01 10:00:00', 0, 1, 6),
(2, 'Advocacy Workshop', 'Conduct a workshop on rights advocacy', '2023-11-15 09:00:00', 1, 5, 5),
(3, 'Budget Report', 'Prepare annual budget report', '2023-11-10 17:00:00', 1, 1, 3);

-- Events_Calendar entries
INSERT INTO Events_Calendar (Event_ID, Event_Name, Date, Time, Location, Created_by) VALUES
(1, 'Welcome Ceremony', '2023-09-10', '10:00:00', 'Main Hall', 6),
(2, 'Rights Awareness Session', '2023-10-05', '14:00:00', 'Auditorium', 5),
(3, 'PR Workshop', '2023-11-20', '15:00:00', 'Conference Room', 7);

-- Meetings entries
INSERT INTO Meetings (Meeting_ID, Created_By, Time, Date, Invitation_to) VALUES
(1, 1, '09:00:00', '2023-09-01', 'Executive Council Members'),
(2, 2, '14:00:00', '2023-09-15', 'Rights Advocacy & Ethos Cabinet'),
(3, 3, '10:00:00', '2023-10-01', 'Public Relations and Communications Cabinet');

-- Cabinet_Chair entries
INSERT INTO Cabinet_Chair (HU_ID, Cabinet_ID, Cabinet_Name, Role, Year, Is_Active) VALUES
(1, 1, 'Executive Council', 'President', '2023-01-01', 1),
(2, 1, 'Executive Council', 'Vice President', '2023-01-01', 1),
(3, 1, 'Executive Council', 'Treasurer', '2023-01-01', 1),
(4, 1, 'Executive Council', 'General Secretary', '2023-01-01', 1),
(5, 2, 'Rights Advocacy & Ethos', 'Chair', '2023-01-01', 1),
(6, 3, 'Events', 'Chair', '2023-01-01', 1),
(7, 4, 'Public Relations and Communications', 'Chair', '2023-01-01', 1),
(8, 5, 'Academic Affairs', 'Chair', '2023-01-01', 1),
(9, 6, 'Food and Hygiene', 'Chair', '2023-01-01', 1);