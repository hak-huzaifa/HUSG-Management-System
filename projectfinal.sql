
-- Create the database
CREATE DATABASE HUSG;

-- Use the database
USE HUSG;

-- Create the 'User' table
CREATE TABLE [User] (
    HU_ID INT PRIMARY KEY,
    Password VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Designation VARCHAR(50) NOT NULL,  -- Executive Council, Cabinet Chair, Cabinet Member
    ContactNumber VARCHAR(15) NOT NULL
);

CREATE TABLE Cabinet (
    Cabinet_ID INT PRIMARY KEY,
    Cabinet_Name NVARCHAR(50),
    Budget INT
);
-- Create the 'Cabinet_Member' table
CREATE TABLE Cabinet_Member (
    HU_ID INT,
    Cabinet_ID INT,
    Cabinet_Name VARCHAR(100), 
    Is_Active BIT,
    Year  DATE,
    PRIMARY KEY (HU_ID, Cabinet_ID),
    FOREIGN KEY (HU_ID) REFERENCES [User](HU_ID),
    FOREIGN KEY (Cabinet_ID) REFERENCES Cabinet(Cabinet_ID)
);

-- Create the 'Cabinet_Chair' table
CREATE TABLE Cabinet_Chair (
    HU_ID INT,
    Cabinet_ID INT,
    Cabinet_Name VARCHAR(100),
    Role VARCHAR(50), 
    Is_Active BIT,
    Year  DATE,
    PRIMARY KEY (HU_ID, Cabinet_ID),
    FOREIGN KEY (HU_ID) REFERENCES [User](HU_ID),
    FOREIGN KEY (Cabinet_ID) REFERENCES Cabinet(Cabinet_ID)
);

-- Create the 'Meetings' table
CREATE TABLE Meetings (
    Meeting_ID INT PRIMARY KEY,
    Created_By INT,  -- HU_ID of the user creating the meeting
    Time TIME,
    Date DATE,
    Invitation_to VARCHAR(255),  -- Department or Cabinet Name invited
    FOREIGN KEY (Created_By) REFERENCES [User](HU_ID)
);

-- Create the 'Task_Allocation' table
CREATE TABLE Task_Allocation (
    Task_ID INT PRIMARY KEY,
    Task_Name VARCHAR(255),
    Description TEXT,
    Deadline DATE,
    Status INT,  -- 0 for Pending, 1 for Completed, 2 for Dropped
    Created_by INT,  -- HU_ID of the user who created the task
    Assigned_To INT,  -- HU_ID of the user assigned the task
    FOREIGN KEY (Created_by) REFERENCES [User](HU_ID),
    FOREIGN KEY (Assigned_To) REFERENCES [User](HU_ID)
);

-- Create the 'Events_Calendar' table
CREATE TABLE Events_Calendar (
    Event_ID INT PRIMARY KEY,
    Event_Name VARCHAR(255),
    Date DATE,
    Time TIME,
    Location VARCHAR(255),
    Created_by INT,  -- HU_ID of the user who created the event
    FOREIGN KEY (Created_by) REFERENCES [User](HU_ID)
);

-- Insert Users (Executive Council, Cabinet Chairs, Cabinet Members)
-- Executive Council
INSERT INTO [User] (HU_ID, Password, Email, Designation, ContactNumber)
VALUES 
(7220, 'password123', 'af07220@st.habib.edu.pk', 'Executive Council', '1234567890'),
(8425, 'password123', 'rk08425@st.habib.edu.pk', 'Executive Council', '0987654321'),
(7950, 'password123', 'mk07950@st.habib.edu.pk', 'Executive Council', '1122334455'),
(9370, 'password123', 'si09370@st.habib.edu.pk', 'Executive Council', '2233445566');

-- Cabinet Chairs
INSERT INTO [User] (HU_ID, Password, Email, Designation, ContactNumber)
VALUES
(8437, 'password123', 'hk08437@st.habib.edu.pk', 'Cabinet Chair', '5566778899'),
(7937, 'password123', 'jb07937@st.habib.edu.pk', 'Cabinet Chair', '6677889900'),
(7154, 'password123', 'aj07154@st.habib.edu.pk', 'Cabinet Chair', '7788990011'),
(8454, 'password123', 'hk08454@st.habib.edu.pk', 'Cabinet Chair', '8899001122'),
(7690, 'password123', 'ss07690@st.habib.edu.pk', 'Cabinet Chair', '9900112233');

-- Insert Cabinet Members for Events Cabinet
INSERT INTO [User] (HU_ID, Password, Email, Designation, ContactNumber)
VALUES
(8339, 'password123', 'sz08339@st.habib.edu.pk', 'Cabinet Member', '9988776655'),
(8418, 'password123', 'mq08418@st.habib.edu.pk', 'Cabinet Member', '8877665544'),
(8433, 'password123', 'eq08433@st.habib.edu.pk', 'Cabinet Member', '7766554433'),
(8072, 'password123', 'mh08072@st.habib.edu.pk', 'Cabinet Member', '6655443322'),
(9247, 'password123', 'hm09247@st.habib.edu.pk', 'Cabinet Member', '5544332211'),
(9268, 'password123', 'hn09268@st.habib.edu.pk', 'Cabinet Member', '4433221100'),
(9191, 'password123', 'en09191@st.habib.edu.pk', 'Cabinet Member', '3322119988'),
(8717, 'password123', 'sf08717@st.habib.edu.pk', 'Cabinet Member', '2211008877'),
(9190, 'password123', 'ai09190@st.habib.edu.pk', 'Cabinet Member', '1100992233'),
(8048, 'password123', 'jw08048@st.habib.edu.pk', 'Cabinet Member', '6677881122'),
(8098, 'password123', 'rq08098@st.habib.edu.pk', 'Cabinet Member', '8899002233'),
(8312, 'password123', 'js08312@st.habib.edu.pk', 'Cabinet Member', '7778883344'),
(8748, 'password123', 'ka08748@st.habib.edu.pk', 'Cabinet Member', '9988776655'),
(9216, 'password123', 'sa09216@st.habib.edu.pk', 'Cabinet Member', '7755442233');  

-- Insert Cabinet Members for RAE Cabinet
INSERT INTO [User] (HU_ID, Password, Email, Designation, ContactNumber)
VALUES
(7923, 'password123', 'fs07923@st.habib.edu.pk', 'Cabinet Member', '9988776655'),
(8773, 'password123', 'sj08773@st.habib.edu.pk', 'Cabinet Member', '8877665544'),
(9515, 'password123', 'kh09515@st.habib.edu.pk', 'Cabinet Member', '7766554433'),
(9195, 'password123', 'hs09195@st.habib.edu.pk', 'Cabinet Member', '6655443322'),
(9248, 'password123', 'ff09248@st.habib.edu.pk', 'Cabinet Member', '5544332211'),
(9108, 'password123', 'ar09108@st.habib.edu.pk', 'Cabinet Member', '4433221100'),
(7107, 'password123', 'ma07107@st.habib.edu.pk', 'Cabinet Member', '3322119988');
--PR
INSERT INTO [User] (HU_ID, Password, Email, Designation, ContactNumber)
VALUES
(8438, 'password123', 'mh8438@st.habib.edu.pk', 'Cabinet Member', '9988776655'),
(7933, 'password123', 'hz07933@st.habib.edu.pk', 'Cabinet Member', '9988776655'),
(8242, 'password123', 'sn08242@st.habib.edu.pk', 'Cabinet Member', '9988776655'),
(8026, 'password123', 'fh08026@st.habib.edu.pk', 'Cabinet Member', '9988776655'),
(9384, 'password123', 'am09384@st.habib.edu.pk', 'Cabinet Member', '9988776655');

--AA
INSERT INTO [User] (HU_ID, Password, Email, Designation, ContactNumber)
VALUES
(7473, 'password123', 'sa07473@st.habib.edu.pk', 'Cabinet Member', '9988776658'),
(7888, 'password123', 'sr07888@st.habib.edu.pk', 'Cabinet Member', '9988776658'),
(7202,'password123',  'mk07202@st.habib.edu.pk', 'Cabinet Member', '9988776658'),
(8756, 'password123', 'mh08756@st.habib.edu.pk', 'Cabinet Member', '9988776658'),
(9203, 'password123', 'mk09203@st.habib.edu.pk', 'Cabinet Member', '9988776658');

--fnh
INSERT INTO [User] (HU_ID, Password, Email, Designation, ContactNumber)
VALUES
(7976, 'password123', 'sz07976@st.habib.edu.pk', 'Cabinet Member', '9988776658'),
(9474, 'password123', 'mp09474@st.habib.edu.pk', 'Cabinet Member', '9988776658'),
(8109, 'password123', 'sk08109@st.habib.edu.pk', 'Cabinet Member', '9988776658'),
(8514, 'password123', 'aj08514@st.habib.edu.pk', 'Cabinet Member', '9988776658'),
(8482, 'password123', 'mw08482@st.habib.edu.pk', 'Cabinet Member', '9988776658');

-- Insert Cabinets
INSERT INTO Cabinet (Cabinet_ID, Cabinet_Name, Budget) VALUES
(1, 'Executive Council', 50000),
(2, 'Rights Advocacy & Ethos', 20000),
(3, 'Events', 30000),
(4, 'Public Relations and Communications', 25000),
(5, 'Academic Affairs', 22000),
(6, 'Food and Hygiene', 18000);

-- Insert the Cabinet Members
INSERT INTO Cabinet_Member (HU_ID, Cabinet_ID, Cabinet_Name, Is_Active, Year) VALUES
--Fnh
(7976, 6, 'Food and Hygiene', 1, '2024-01-01'),
(9474, 6, 'Food and Hygiene', 1, '2024-01-01'),
(8109, 6, 'Food and Hygiene', 1, '2024-01-01'),
(8514, 6, 'Food and Hygiene', 1, '2024-01-01'),
(8482, 6, 'Food and Hygiene', 1, '2024-01-01'),

--AA
(7473, 5, 'Academic Affairs', 1, '2024-01-01'),
(7888, 5, 'Academic Affairs', 1, '2024-01-01'),
(7202, 5, 'Academic Affairs', 1, '2024-01-01'),
(8756, 5, 'Academic Affairs', 1, '2024-01-01'),
(9203, 5, 'Academic Affairs', 1, '2024-01-01'),

--PR
(8438, 4, 'Public Relations and Communications', 1, '2024-01-01'),
(7933, 4, 'Public Relations and Communications', 1, '2024-01-01'),
(8242, 4, 'Public Relations and Communications', 1, '2024-01-01'),
(8026, 4, 'Public Relations and Communications', 1, '2024-01-01'),
(9384, 4, 'Public Relations and Communications', 1, '2024-01-01'),

--Events
(8339, 3, 'Events', 1, '2024-01-01'),
(8418, 3, 'Events', 1, '2024-01-01'),
(8433, 3, 'Events', 1, '2024-01-01'),
(8072, 3, 'Events', 1, '2024-01-01'),
(9247, 3, 'Events', 1, '2024-01-01'),
(9268, 3, 'Events', 1, '2024-01-01'),
(9191, 3, 'Events', 1, '2024-01-01'),
(8717, 3, 'Events', 1, '2024-01-01'),
(9190, 3, 'Events', 1, '2024-01-01'),
(8048, 3, 'Events', 1, '2024-01-01'),
(8098, 3, 'Events', 1, '2024-01-01'),
(8312, 3, 'Events', 1, '2024-01-01'),
(8748, 3, 'Events', 1, '2024-01-01'),
(9216, 3, 'Events', 1, '2024-01-01'),
--RAE
(7923, 2, 'Rights Advocacy & Ethos', 1, '2024-01-01'),
(8773, 2, 'Rights Advocacy & Ethos', 1, '2024-01-01'),
(9515, 2, 'Rights Advocacy & Ethos', 1, '2024-01-01'),
(9195, 2, 'Rights Advocacy & Ethos', 1, '2024-01-01'),
(9248, 2, 'Rights Advocacy & Ethos', 1, '2024-01-01'),
(9108, 2, 'Rights Advocacy & Ethos', 1, '2024-01-01'),
(7107, 2, 'Rights Advocacy & Ethos', 1, '2024-01-01');

-- Insert the Cabinet Chair associations
INSERT INTO Cabinet_Chair (HU_ID, Cabinet_ID, Cabinet_Name, Role, Year, Is_Active) VALUES
(7220, 1, 'Executive Council', 'President', '2024-01-01', 1),
(8425, 1, 'Executive Council', 'Vice President', '2024-01-01', 1),
(7950, 1, 'Executive Council', 'Treasurer', '2024-01-01', 1),
(9370, 1, 'Executive Council', 'General Secretary', '2024-01-01', 1),
(7937, 2, 'Rights Advocacy & Ethos', 'Chair', '2024-01-01', 1),
(8437, 3, 'Events', 'Chair', '2024-01-01', 1),
(7154, 4, 'Public Relations and Communications', 'Chair', '2024-01-01', 1),
(8454, 5, 'Academic Affairs', 'Chair', '2024-01-01', 1),
(7690, 6, 'Food and Hygiene', 'Chair', '2024-01-01', 1);

-- Insert sample Meetings Data
INSERT INTO Meetings (Meeting_ID, Created_By, Time, Date, Invitation_to)
VALUES
(1, 7220, '10:00:00', '2024-05-15', 'Executive Council'),
(2, 8437, '11:00:00', '2024-06-10', 'Events');

-- Insert sample Task Allocation Data
INSERT INTO Task_Allocation (Task_ID, Task_Name, Description, Deadline, Status, Created_by, Assigned_To)
VALUES
(1, 'Task 1', 'Task description 1', '2024-06-01', 0, 7220, 8339),
(2, 'Task 2', 'Task description 2', '2024-06-10', 1, 8437, 8418);

-- Insert sample Event Data
INSERT INTO Events_Calendar (Event_ID, Event_Name, Date, Time, Location, Created_by)
VALUES
(1, 'Event 1', '2024-06-05', '09:00:00', 'Hall 1', 7220),
(2, 'Event 2', '2024-06-10', '14:00:00', 'Hall 2', 8437);

