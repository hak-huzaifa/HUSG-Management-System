from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView, QMessageBox
import sys
import pyodbc

def connect_to_database():
    return pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};"
                          "SERVER=ALISHBA-ZAIDI;"
                          "DATABASE=projectsample;"
                          "Trusted_Connection=yes;")

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Login.ui', self)
        self.Login_pushButton.clicked.connect(self.login)
        self.Reg_pushButton.clicked.connect(self.open_registration_form)
        self.Close_pushButton.clicked.connect(self.close_application)

    def login(self):
        hu_id = self.ID_lineEdit.text()
        password = self.Password_lineEdit.text()

        if not hu_id or not password:
            QtWidgets.QMessageBox.warning(self, "Input Error", "FILL ALL FIELDS!")
            return
        
        if not hu_id.isdigit():
            QtWidgets.QMessageBox.warning(self, "Invalid ID", "Please add a valid HU ID (only integers).")
            return
        
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            query = "SELECT * FROM [User] where HU_ID = ? AND Password = ?"
            cursor.execute(query, (hu_id, password))
            user = cursor.fetchone()

            if user:
                QtWidgets.QMessageBox.information(self, "Login Successful", "Welcome to the Dashboard!")
                self.open_dashboard(hu_id)  # Pass hu_id to DashboardWindow
            else:
                QtWidgets.QMessageBox.warning(self, "Login Failed", "Invalid HU ID or Password!")
            conn.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occured: {e}")

    def open_dashboard(self, hu_id):
        self.dashboard = DashboardWindow(hu_id)  # Pass hu_id to DashboardWindow
        self.dashboard.show()
        self.close()

    def open_registration_form(self):
        self.registration_form = RegistrationWindow()
        self.registration_form.show()
        self.close()

    def close_application(self):
        self.close()

class DashboardWindow(QtWidgets.QMainWindow):
    def __init__(self, current_user_id):  # Accept the current_user_id
        super().__init__()
        uic.loadUi('Dashboard.ui', self)  # Load the Dashboard UI

        # Store the current_user_id for this session
        self.current_user_id = current_user_id

        # Connect push buttons to their respective methods
        self.meetingspush.clicked.connect(self.open_meetings)
        self.Calendarpush.clicked.connect(self.open_events_calendar)
        self.Financepush.clicked.connect(self.open_budget_allocation)
        self.workpush.clicked.connect(self.open_task_allocation)
        self.closeButton.clicked.connect(self.close_application)

    def open_meetings(self):
        # Pass current_user_id to MeetingsWindow
        self.meetings_window = MeetingsWindow(self.current_user_id)  # Pass the current_user_id to the MeetingsWindow
        self.meetings_window.show()
        self.close()

    def open_events_calendar(self):
        self.calendar_window = EventsCalendarWindow(self.current_user_id)
        self.calendar_window.show()
        self.close()

    def open_budget_allocation(self):
        self.budget_window = BudgetAllocationWindow()
        self.budget_window.show()
        self.close()

    def open_task_allocation(self):
        self.tasks_window = TaskAllocationWindow()
        self.tasks_window.show()
        self.close()

    def close_application(self):
        self.close()

class RegistrationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Register.ui',self)
        self.Reg_pushButton.clicked.connect(self.register_user)
        self.Back_pushButton.clicked.connect(self.go_back_to_login)
        
    def register_user(self):
        hu_id = self.IDLineEdit.text()
        password = self.passwordLineEdit.text()
        confirm_password = self.confirmPassLineEdit.text()
        email = self.emailLineEdit.text()
        cabinet_name = self.deptComboBox.currentText().strip()  # Clean the dropdown value
        contact_number = self.contactLineEdit.text()
        #print(f"Selected Cabinet: '{cabinet_name}'")
        if self.EC_radioButton.isChecked():
            designation = "Executive Council"
        elif self.Chair_radioButton.isChecked():
            designation = "Cabinet Chair"
        elif self.Mem_radioButton.isChecked():
            designation = "Cabinet Member"
        else:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please select a designation!")
            return
        if not all([hu_id, password, confirm_password, email, cabinet_name, contact_number, designation]):
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please fill in all fields!")
            return

        if password != confirm_password:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Passwords do not match!")
            return
        cabinet_mapping = {
            "Executive Council": 1,
            "Rights Advocacy & Ethos": 2,
            "Events": 3,
            "Public Relations and Communications": 4,
            "Academic Affairs": 5,
            "Food and Hygiene": 6,
        }
        cabinet_id = cabinet_mapping.get(cabinet_name) 
        if cabinet_id is None:
            QtWidgets.QMessageBox.critical(self, "Error", f"Invalid Cabinet Name: {cabinet_name}")
            return
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            user_query = """INSERT INTO [User] (HU_ID, Password, Email, Designation, ContactNumber) 
                            VALUES (?, ?, ?, ?, ?)"""
            cursor.execute(user_query, (hu_id, password, email, designation, contact_number))
            if designation == "Cabinet Member":
                cabinet_member_query = """INSERT INTO Cabinet_Member (HU_ID, Cabinet_ID, Cabinet_Name, Is_Active, Year) 
                                        VALUES (?, ?, ?, 1, ?)"""
                cursor.execute(cabinet_member_query, (hu_id, cabinet_id, cabinet_name, "2024"))
            elif designation == "Cabinet Chair":
                cabinet_chair_query = """INSERT INTO Cabinet_Chair (HU_ID, Cabinet_ID, Cabinet_Name, Role, Is_Active, Year) 
                                        VALUES (?, ?, ?, ?, 1, ?)"""
                cursor.execute(cabinet_chair_query, (hu_id, cabinet_id, cabinet_name, designation, "2024"))
            conn.commit()
            QtWidgets.QMessageBox.information(self, "Success", "Registration successful! You can now log in.")
            self.go_back_to_login()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")
    def go_back_to_login(self):
        self.close()
        self.login_form = LoginWindow()
        self.login_form.show()
        
class MeetingsWindow(QtWidgets.QMainWindow):
    def __init__(self, current_user_id):  # Accept current_user_id as a parameter
        super().__init__()
        uic.loadUi('Meetings.ui', self)

        # Store the current_user_id for this session
        self.current_user_id = current_user_id

        # Connect buttons
        self.Add_pushButton.clicked.connect(self.add_meeting)
        self.Back_pushButton.clicked.connect(self.go_back_to_dashboard)

        # Load existing meetings when the window is initialized
        self.load_existing_meetings()

    def go_back_to_dashboard(self):
        self.close()
        self.dashboard = DashboardWindow(self.current_user_id)
        self.dashboard.show()

    def load_existing_meetings(self):
        """Load all existing meetings from the database and populate the table."""
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # SQL query to fetch meetings for the logged-in user (or all meetings if needed)
            query = """
                SELECT Meeting_ID, Created_By, Time, Date, Invitation_to 
                FROM Meetings
            """
            cursor.execute(query)
            meetings = cursor.fetchall()

            # Clear the table first
            self.meetingsTable.setRowCount(0)

            # Add each meeting to the table
            for meeting in meetings:
                row_position = self.meetingsTable.rowCount()
                self.meetingsTable.insertRow(row_position)

                self.meetingsTable.setItem(row_position, 0, QTableWidgetItem(str(meeting[0])))  # Meeting ID
                self.meetingsTable.setItem(row_position, 1, QTableWidgetItem(str(meeting[1])))  # Created By
                self.meetingsTable.setItem(row_position, 2, QTableWidgetItem(str(meeting[2])))  # Time
                self.meetingsTable.setItem(row_position, 3, QTableWidgetItem(str(meeting[3])))  # Date
                self.meetingsTable.setItem(row_position, 4, QTableWidgetItem(str(meeting[4])))  # Invitation To

            conn.close()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred while fetching meetings: {e}")

    def add_meeting(self):
        # Disable the Add button immediately after it's clicked to prevent multiple clicks
        self.Add_pushButton.setDisabled(True)

        # Get the user input values from the UI
        meeting_id = self.meetingIDLineEdit.text().strip()
        meeting_date = self.dateEdit.date()  # QDate object
        meeting_time = self.timeEdit.time()  # QTime object
        department = self.deptComboBox.currentText().strip()

        # Retrieve the current user's HU_ID (from the session)
        created_by = self.current_user_id  # Use the actual HU_ID

        # Input validation
        if not all([meeting_id, department]):
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please fill in all fields!")
            self.Add_pushButton.setEnabled(True)  # Re-enable the button
            return

        # Validate Meeting ID (Ensure it's numeric)
        if not meeting_id.isdigit():
            QtWidgets.QMessageBox.warning(self, "Invalid Meeting ID", "Please enter a valid numeric Meeting ID.")
            self.Add_pushButton.setEnabled(True)  # Re-enable the button
            return

        # Convert QDate and QTime to strings in the correct format for SQL
        meeting_date_str = meeting_date.toString("yyyy-MM-dd")  # Format the date as 'yyyy-MM-dd'
        meeting_time_str = meeting_time.toString("HH:mm:ss")  # Format the time as 'HH:mm:ss'

        # Add milliseconds (precision) to the time: HH:mm:ss.000 (for SQL Server)
        meeting_time_str_with_precision = f"{meeting_time_str}.000"  # Add 3 digits for milliseconds

        # Debugging: Print the formatted values before insertion
        print(f"Inserting Meeting: {meeting_id}, {created_by}, {meeting_time_str_with_precision}, {meeting_date_str}, {department}")

        # Handle department-based mapping to fetch Cabinet Members and Cabinet Chairs
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # Define SQL queries for each department to fetch Cabinet Members and Chairs
            if department == "All EC":
                query = """
                    SELECT HU_ID, Cabinet_ID FROM Cabinet_Member 
                    WHERE Cabinet_Name = 'Executive Council'
                """
            elif department == "EC + Cabinet Chairs":
                query = """
                    SELECT HU_ID, Cabinet_ID FROM Cabinet_Member 
                    WHERE Cabinet_Name = 'Executive Council'
                    UNION
                    SELECT HU_ID, Cabinet_ID FROM Cabinet_Member 
                    WHERE Cabinet_Name = 'Cabinet Chair'
                """
            elif department == "Rights Advocacy & Ethos":
                query = """
                    SELECT HU_ID, Cabinet_ID FROM Cabinet_Member 
                    WHERE Cabinet_Name = 'Rights Advocacy & Ethos'
                """
            elif department == "Events":
                query = """
                    SELECT HU_ID, Cabinet_ID FROM Cabinet_Member 
                    WHERE Cabinet_Name = 'Events'
                """
            elif department == "Academic Affairs":
                query = """
                    SELECT HU_ID, Cabinet_ID FROM Cabinet_Member 
                    WHERE Cabinet_Name = 'Academic Affairs'
                """
            elif department == "Food and Hygiene":
                query = """
                    SELECT HU_ID, Cabinet_ID FROM Cabinet_Member 
                    WHERE Cabinet_Name = 'Food and Hygiene'
                """
            elif department == "Public Relations and Communications":
                query = """
                    SELECT HU_ID, Cabinet_ID FROM Cabinet_Member 
                    WHERE Cabinet_Name = 'Public Relations and Communications'
                """
            else:
                QtWidgets.QMessageBox.warning(self, "Error", f"Invalid Cabinet Name: {department}")
                self.Add_pushButton.setEnabled(True)  # Re-enable the button
                return

            # Execute the query and fetch results
            cursor.execute(query)
            results = cursor.fetchall()

            if results:
                # Insert the meeting for each Cabinet Member and Cabinet Chair
                for result in results:
                    hu_id, cabinet_id = result
                    self.insert_meeting_into_table(meeting_id, created_by, meeting_time_str_with_precision, meeting_date_str, department, hu_id, cabinet_id)

                # Optionally, insert into the database as well
                self.insert_meeting_into_db(meeting_id, created_by, meeting_time_str_with_precision, meeting_date_str, department)

            else:
                QtWidgets.QMessageBox.warning(self, "Error", f"No members found for {department}")
                self.Add_pushButton.setEnabled(True)  # Re-enable the button
                return

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            self.Add_pushButton.setEnabled(True)  # Re-enable the button
        finally:
            conn.close()

        # Re-enable the Add button and clear the input fields for the next entry
        self.Add_pushButton.setEnabled(True)
        self.meetingIDLineEdit.clear()
        self.dateEdit.setDate(QDate.currentDate())  # Set date to today's date
        self.timeEdit.clear()
        self.deptComboBox.setCurrentIndex(0)  # Reset dropdown to the first option

    def insert_meeting_into_table(self, meeting_id, created_by, meeting_time, meeting_date, department, hu_id, cabinet_id):
        """Insert the meeting data into the table (UI)."""
        row_position = self.meetingsTable.rowCount()
        self.meetingsTable.insertRow(row_position)

        # Insert the values into the new row in the table
        self.meetingsTable.setItem(row_position, 0, QTableWidgetItem(meeting_id))
        self.meetingsTable.setItem(row_position, 1, QTableWidgetItem(str(created_by)))  # Ensure created_by is int
        self.meetingsTable.setItem(row_position, 2, QTableWidgetItem(meeting_time))
        self.meetingsTable.setItem(row_position, 3, QTableWidgetItem(meeting_date))
        self.meetingsTable.setItem(row_position, 4, QTableWidgetItem(department))

    def insert_meeting_into_db(self, meeting_id, created_by, meeting_time, meeting_date, department):
        """Insert the meeting details into the database."""
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # SQL query to insert meeting data into the database (MeetingDate as datetime)
            query = """
                INSERT INTO Meetings (Meeting_ID, Created_By, Time, Date, Invitation_to)
                VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (meeting_id, int(created_by), meeting_time, meeting_date, department))  # Ensure created_by is an integer
            conn.commit()

            QtWidgets.QMessageBox.information(self, "Success", "Meeting added successfully!")

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        finally:
            conn.close()

class EventsCalendarWindow(QtWidgets.QMainWindow):
    def __init__(self, current_user_id):
        super().__init__()
        uic.loadUi('EventsCalender.ui', self)
        
        # Store the current_user_id for this session
        self.current_user_id = current_user_id

        # Connect buttons to their respective methods
        self.Add_pushButton.clicked.connect(self.add_event)
        self.delete_pushButton.clicked.connect(self.delete_event)
        self.Back_pushButton.clicked.connect(self.go_back_to_dashboard)

        # Load existing events when the window is initialized
        self.load_existing_events()

    def go_back_to_dashboard(self):
        self.close()
        self.dashboard = DashboardWindow(self.current_user_id)
        self.dashboard.show()

    def load_existing_events(self):
        """Load all existing events from the database and populate the table."""
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # SQL query to fetch events for the logged-in user (or all events if needed)
            query = """
                SELECT Event_ID, Event_Name, Date, Time, Location, Created_by 
                FROM Events_Calendar
            """
            cursor.execute(query)
            events = cursor.fetchall()

            # Clear the table first
            self.eventsTable.setRowCount(0)

            # Add each event to the table
            for event in events:
                row_position = self.eventsTable.rowCount()
                self.eventsTable.insertRow(row_position)

                self.eventsTable.setItem(row_position, 0, QTableWidgetItem(str(event[0])))  # Event ID
                self.eventsTable.setItem(row_position, 1, QTableWidgetItem(str(event[1])))  # Event Name
                self.eventsTable.setItem(row_position, 2, QTableWidgetItem(str(event[2])))  # Date
                self.eventsTable.setItem(row_position, 3, QTableWidgetItem(str(event[3])))  # Time
                self.eventsTable.setItem(row_position, 4, QTableWidgetItem(str(event[4])))  # Location
                self.eventsTable.setItem(row_position, 5, QTableWidgetItem(str(event[5])))  # Created by

            conn.close()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred while fetching events: {e}")

    def add_event(self):
        """Add a new event to the database and table."""
        # Get the user input values from the UI
        event_name = self.locationLineEdit.text().strip()
        event_date = self.dateEdit.date()  # QDate object
        event_time = self.timeEdit.time()  # QTime object
        location = self.locationLineEdit_2.text().strip()

        # Retrieve the current user's HU_ID (from the session)
        created_by = self.current_user_id  # Use the actual HU_ID

        # Input validation
        if not all([event_name, event_date, event_time, location]):
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please fill in all fields!")
            return

        # Convert QDate and QTime to strings in the correct format for SQL
        event_date_str = event_date.toString("yyyy-MM-dd")  # Format the date as 'yyyy-MM-dd'
        event_time_str = event_time.toString("HH:mm:ss")  # Format the time as 'HH:mm:ss'

        # Add milliseconds (precision) to the time: HH:mm:ss.000 (for SQL Server)
        event_time_str_with_precision = f"{event_time_str}.000"  # Add 3 digits for milliseconds

        # Get the next available Event_ID based on the number of rows in the table
        event_id = self.eventsTable.rowCount() + 1  # Add 1 to the current row count

        # Debugging: Print the formatted values before insertion
        print(f"Inserting Event: {event_id}, {event_name}, {event_date_str}, {event_time_str_with_precision}, {location}, {created_by}")

        # Insert the event into the database
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # SQL query to insert event data into the database (EventDate as datetime)
            query = """
                INSERT INTO Events_Calendar (Event_ID, Event_Name, Date, Time, Location, Created_by)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (event_id, event_name, event_date_str, event_time_str_with_precision, location, created_by))
            conn.commit()

            QtWidgets.QMessageBox.information(self, "Success", "Event added successfully!")

            # Reload events to update the table
            self.load_existing_events()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        finally:
            conn.close()

        # Clear the input fields for the next event
        self.locationLineEdit.clear()
        self.locationLineEdit_2.clear()
        self.dateEdit.setDate(QDate.currentDate())  # Set date to today's date
        self.timeEdit.clear()
        
    def delete_event(self):
        # Get selected row from the table
        selected_row = self.eventsTable.currentRow()
        
        if selected_row < 0:
            QtWidgets.QMessageBox.warning(self, "No Selection", "Please select an event to delete.")
            return

        # Get the Event ID of the selected event
        event_id = self.eventsTable.item(selected_row, 0).text()

        # Confirm deletion
        response = QtWidgets.QMessageBox.question(
            self, 
            "Delete Event", 
            f"Are you sure you want to delete the event with ID {event_id}?", 
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No, 
            QtWidgets.QMessageBox.StandardButton.No
        )

        if response == QtWidgets.QMessageBox.StandardButton.Yes:
            try:
                conn = connect_to_database()
                cursor = conn.cursor()

                # Delete the event from the database using Event ID
                delete_query = "DELETE FROM Events_Calendar WHERE Event_ID = ?"
                cursor.execute(delete_query, (event_id,))
                conn.commit()

                # Remove the event from the table
                self.eventsTable.removeRow(selected_row)
                QtWidgets.QMessageBox.information(self, "Event Deleted", f"Event with ID {event_id} has been deleted.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred while deleting the event: {e}")
            finally:
                conn.close()
        else:
            # If the user clicks 'No', do nothing
            pass

class BudgetAllocationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('budgetallocation2.ui',self)
        self.Back_pushButton.clicked.connect(self.go_back_to_dashboard)
    
    def go_back_to_dashboard(self):
        self.close()
        self.dashboard = DashboardWindow()
        self.dashboard.show()

class TaskAllocationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('taskallocation2.ui',self)
        self.Back_pushButton.clicked.connect(self.go_back_to_dashboard)

    def go_back_to_dashboard(self):
        self.close()
        self.dashboard = DashboardWindow()
        self.dashboard.show()

def main():
    app = QApplication(sys.argv)
    loginwindow = LoginWindow()
    loginwindow.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()