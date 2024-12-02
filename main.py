from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView, QMessageBox, QButtonGroup
import sys
import pyodbc

def connect_to_database():
    return pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};"
                          "SERVER=ALISHBA-ZAIDI;"
                          "DATABASE=HUSG;"
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
    def __init__(self, current_user_id):  # Accept current_user_id as a parameter
        super().__init__()
        uic.loadUi('Dashboard.ui', self)  # Load the Dashboard UI

        # Store the current_user_id for this session
        self.current_user_id = current_user_id

        # Check the user's role (Cabinet Chair or Executive Council)
        self.check_user_role()

        # Connect push buttons to their respective methods
        self.meetingspush.clicked.connect(self.open_meetings)
        self.Calendarpush.clicked.connect(self.open_events_calendar)
        self.Financepush.clicked.connect(self.open_budget_allocation)
        self.workpush.clicked.connect(self.open_task_allocation)
        self.closeButton.clicked.connect(self.close_application)

    def check_user_role(self):
        #Check if the user is a Cabinet Chair or Executive Council and allow access to budget allocation.
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # SQL query to check if the current user is a Cabinet Chair or Executive Council
            query = """
                SELECT Designation
                FROM [User]
                WHERE HU_ID = ?
            """
            cursor.execute(query, (self.current_user_id,))
            user = cursor.fetchone()

            if user:
                designation = user[0]
                if designation not in ["Cabinet Chair", "Executive Council"]:
                    # Disable the Finance button for Cabinet Members
                    self.Financepush.setDisabled(True)
                    #QtWidgets.QMessageBox.warning(self, "Permission Denied", "Only Cabinet Chairs and Executive Council members can access the Budget Allocation screen.")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Unable to fetch user role.")
            conn.close()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred while checking user role: {e}")

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
        self.budget_window = BudgetAllocationWindow(self.current_user_id)
        self.budget_window.show()
        self.close()

    def open_task_allocation(self):
        self.tasks_window = TaskAllocationWindow(self.current_user_id)
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
        if not contact_number.isdigit():
            QtWidgets.QMessageBox.warning(self, "Invalid Contact Number", "Please add a valid Contact Number (only integers).")
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

        # Check the user's designation
        self.check_user_role()

        # Connect buttons
        self.Add_pushButton.clicked.connect(self.add_meeting)
        self.Back_pushButton.clicked.connect(self.go_back_to_dashboard)

        # Load existing meetings when the window is initialized
        self.load_existing_meetings()

    def check_user_role(self):
        #Check if the user is a Cabinet Chair or Executive Council and allow adding meetings.
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # SQL query to check if the current user is a Cabinet Chair or Executive Council
            query = """
                SELECT Designation
                FROM [User]
                WHERE HU_ID = ?
            """
            cursor.execute(query, (self.current_user_id,))
            user = cursor.fetchone()

            if user:
                designation = user[0]
                if designation not in ["Cabinet Chair", "Executive Council"]:
                    # If the user is not a Cabinet Chair or Executive Council, disable the Add button
                    self.Add_pushButton.setDisabled(True)
                    self.Add_pushButton.setText("View Only")
                    QtWidgets.QMessageBox.warning(self, "Permission Denied", "Only Cabinet Chairs and Executive Council members can add meetings.")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Unable to fetch user role.")
            conn.close()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred while checking user role: {e}")

    def go_back_to_dashboard(self):
        self.close()
        self.dashboard = DashboardWindow(self.current_user_id)
        self.dashboard.show()

    def load_existing_meetings(self):
        #Load all existing meetings from the database and populate the table.
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
        # Check if user is authorized to add a meeting
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # SQL query to check if the current user is a Cabinet Chair or Executive Council
            query = """
                SELECT Designation
                FROM [User]
                WHERE HU_ID = ?
            """
            cursor.execute(query, (self.current_user_id,))
            user = cursor.fetchone()

            if user:
                designation = user[0]
                if designation not in ["Cabinet Chair", "Executive Council"]:
                    QtWidgets.QMessageBox.warning(self, "Permission Denied", "Only Cabinet Chairs and Executive Council members can add meetings.")
                    conn.close()
                    return
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Unable to fetch user role.")
                conn.close()
                return

            # Proceed with adding meeting if the user is allowed
            meeting_id = self.meetingIDLineEdit.text().strip()
            meeting_date = self.dateEdit.date()  # QDate object
            meeting_time = self.timeEdit.time()  # QTime object
            department = self.deptComboBox.currentText().strip()

            # Retrieve the current user's HU_ID (from the session)
            created_by = self.current_user_id  # Use the actual HU_ID

            # Input validation
            if not all([meeting_id, department]):
                QtWidgets.QMessageBox.warning(self, "Input Error", "Please fill in all fields!")
                return

            # Validate Meeting ID (Ensure it's numeric)
            if not meeting_id.isdigit():
                QtWidgets.QMessageBox.warning(self, "Invalid Meeting ID", "Please enter a valid numeric Meeting ID.")
                return

            # Convert QDate and QTime to strings in the correct format for SQL
            meeting_date_str = meeting_date.toString("yyyy-MM-dd")  # Format the date as 'yyyy-MM-dd'
            meeting_time_str = meeting_time.toString("HH:mm:ss")  # Format the time as 'HH:mm:ss'

            # Add milliseconds (precision) to the time: HH:mm:ss.000 (for SQL Server)
            meeting_time_str_with_precision = f"{meeting_time_str}.000"  # Add 3 digits for milliseconds

            # SQL query to insert the meeting into the database (MeetingDate as datetime)
            query = """
                INSERT INTO Meetings (Meeting_ID, Created_By, Time, Date, Invitation_to)
                VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (meeting_id, created_by, meeting_time_str_with_precision, meeting_date_str, department))
            conn.commit()

            QtWidgets.QMessageBox.information(self, "Success", "Meeting added successfully!")
            self.load_existing_meetings()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred while adding the meeting: {e}")
        finally:
            conn.close()

        # Clear the input fields for the next meeting
        self.meetingIDLineEdit.clear()
        self.dateEdit.setDate(QDate.currentDate())  # Set date to today's date
        self.timeEdit.clear()
        self.deptComboBox.setCurrentIndex(0)  # Reset dropdown to the first option

class EventsCalendarWindow(QtWidgets.QMainWindow):
    def __init__(self, current_user_id):
        super().__init__()
        uic.loadUi('EventsCalender.ui', self)

        # Store the current_user_id for this session
        self.current_user_id = current_user_id

        # Check the user's role (Cabinet Chair or Executive Council)
        self.check_user_role()

        # Connect buttons to their respective methods
        self.Add_pushButton.clicked.connect(self.add_event)
        self.delete_pushButton.clicked.connect(self.delete_event)
        self.Back_pushButton.clicked.connect(self.go_back_to_dashboard)

        # Load existing events when the window is initialized
        self.load_existing_events()

    def check_user_role(self):
        #Check if the user is a Cabinet Chair or Executive Council and allow adding/deleting events.
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # SQL query to check if the current user is a Cabinet Chair or Executive Council
            query = """
                SELECT Designation
                FROM [User]
                WHERE HU_ID = ?
            """
            cursor.execute(query, (self.current_user_id,))
            user = cursor.fetchone()

            if user:
                designation = user[0]
                if designation not in ["Cabinet Chair", "Executive Council"]:
                    # Disable Add and Delete buttons for Cabinet Members
                    self.Add_pushButton.setDisabled(True)
                    self.delete_pushButton.setDisabled(True)
                    QtWidgets.QMessageBox.warning(self, "Permission Denied", "Only Cabinet Chairs and Executive Council members can add or delete events.")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Unable to fetch user role.")
            conn.close()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred while checking user role: {e}")

    def go_back_to_dashboard(self):
        self.close()
        self.dashboard = DashboardWindow(self.current_user_id)
        self.dashboard.show()

    def load_existing_events(self):
        #Load all existing events from the database and populate the table.
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
                self.eventsTable.setItem(row_position, 3, QTableWidgetItem(str(event[4])))  # Time
                self.eventsTable.setItem(row_position, 4, QTableWidgetItem(str(event[3])))  # Location
                self.eventsTable.setItem(row_position, 5, QTableWidgetItem(str(event[5])))  # Created by
            conn.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred while fetching events: {e}")

    def add_event(self):
        #Add a new event to the database and table.
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
    def __init__(self, hu_id):
        super().__init__()
        uic.loadUi('budgetallocation2.ui', self)  # Assuming the UI is in a .ui file
        self.hu_id = hu_id  # The logged-in user's ID

        # Connect buttons to respective functions
        self.deptComboBox.currentTextChanged.connect(self.update_balance)  # No recipient HU ID anymore
        self.allocate_pushButton.clicked.connect(self.allocate_budget)
        self.Back_pushButton.clicked.connect(self.back_button_click)

        # Load cabinets and update total budget
        self.load_cabinets()
        self.update_total_budget()


    def load_cabinets(self):
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # SQL query to fetch all cabinet data
            query = """
                SELECT cabinet_name, budget 
                FROM Cabinet
            """
            cursor.execute(query)
            cabinets = cursor.fetchall()

            # Clear the table first to avoid duplication
            self.tableWidget.setRowCount(0)

            # Add each cabinet to the table
            for cabinet in cabinets:
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)

                # Set the cabinet details in the table
                self.tableWidget.setItem(row_position, 0, QTableWidgetItem(cabinet[0]))  # Cabinet Name
                self.tableWidget.setItem(row_position, 1, QTableWidgetItem(str(cabinet[1])))  # Budget

            conn.close()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"An error occurred while fetching cabinets: {e}")

    def update_balance(self, selected_cabinet_name):
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # Ensure that the cabinet_name is correctly referenced and the budget is a numeric value
            query = '''
                SELECT budget
                FROM cabinet
                WHERE cabinet_name = ?
            '''
            cursor.execute(query, (selected_cabinet_name,))
            result = cursor.fetchone()

            # if result:
            #     cabinet_budget = result[0]
            #     self.balance_label.setText(f"Balance: {cabinet_budget}")

            conn.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"Error updating balance: {e}")

    def update_total_budget(self):
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # Get the sum of all cabinet budgets
            cursor.execute("SELECT SUM(Budget) FROM Cabinet")
            total_budget = cursor.fetchone()[0]

            if total_budget is not None:
                self.lcdNumber.display(total_budget)  # Use display() method for LCDNumber widget
            else:
                self.lcdNumber.display(0)  # Display 0 if there is no budget

            conn.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"Error calculating total budget: {e}")

    def allocate_budget(self):
        selected_cabinet_name = self.deptComboBox.currentText()
        try:
            amount = int(self.ID_lineEdit_2.text())  # Getting the amount to allocate

            if amount != 0:
                conn = connect_to_database()
                cursor = conn.cursor()

                # Get the current budget for the selected cabinet from the database
                cursor.execute('''
                    SELECT budget
                    FROM cabinet
                    WHERE cabinet_name = ?
                ''', (selected_cabinet_name,))
                current_budget = cursor.fetchone()

                if current_budget:
                    new_budget = current_budget[0] + amount  # Add the allocation to the current budget

                    # Update the selected cabinet's budget in the database
                    cursor.execute('''
                        UPDATE cabinet
                        SET budget = ?
                        WHERE cabinet_name = ?
                    ''', (new_budget, selected_cabinet_name))
                    conn.commit()

                    # Refresh the UI with the updated values
                    self.update_balance(selected_cabinet_name)
                    self.update_total_budget()

                    # Now, manually update the table with the new values (refresh the row)
                    for row in range(self.tableWidget.rowCount()):
                        if self.tableWidget.item(row, 0).text() == selected_cabinet_name:
                            # Update the budget column with the new budget value
                            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(new_budget)))  # Update the budget column

                    # Show a success message after updating the budget
                    QtWidgets.QMessageBox.information(self, "Success", "Budget allocated successfully!")

                conn.close()

        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for the amount.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"Error allocating budget: {e}")

    def back_button_click(self):
        """Return to the Dashboard window."""
        self.close()  # Close the current window (Budget Allocation Window)
        self.dashboard_window = DashboardWindow(self.hu_id)  # Assuming DashboardWindow exists
        self.dashboard_window.show()  # Show the Dashboard window

class TaskAllocationWindow(QtWidgets.QMainWindow):
    def __init__(self, current_user_id):
        super().__init__()
        uic.loadUi('taskallocation2.ui', self)

        # Store the current_user_id for this session
        self.current_user_id = current_user_id

        # Check the user's role
        self.check_user_role()

        # Connect buttons to their respective methods
        self.assign_pushButton.clicked.connect(self.assign_task)
        self.Status_pushButton.clicked.connect(self.change_status)
        self.Back_pushButton.clicked.connect(self.go_back_to_dashboard)

        self.status_button_group = QButtonGroup(self)
        self.status_button_group.addButton(self.completed)  # Assuming 'completed' is the objectName of the radio button
        self.status_button_group.addButton(self.Pending)    # Similarly for 'pending'
        self.status_button_group.addButton(self.dropped)    # Similarly for 'dropped'

        # Load existing tasks when the window is initialized
        self.load_existing_tasks()

    def check_user_role(self):
        """Check the user's role (Cabinet Chair or Executive Council) and disable status group box for them."""
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # SQL query to check if the current user is a Cabinet Chair or Executive Council
            query = """
                SELECT Designation
                FROM [User]
                WHERE HU_ID = ?
            """
            cursor.execute(query, (self.current_user_id,))
            user = cursor.fetchone()

            if user:
                designation = user[0]
                if designation in ["Cabinet Chair", "Executive Council"]:
                    # Disable the status combobox for Cabinet Chair or Executive Council
                    self.StatusgroupBox_2.setDisabled(True)  # Disable the group box
                    self.Status_pushButton.setDisabled(True)  # Disable the change status button
                else:
                    # Enable status functionality for Cabinet Members
                    self.StatusgroupBox_2.setEnabled(True)
                    self.Status_pushButton.setEnabled(True)

            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Unable to fetch user role.")

            conn.close()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred while checking user role: {e}")

    def go_back_to_dashboard(self):
        self.close()
        self.dashboard = DashboardWindow(self.current_user_id)
        self.dashboard.show()

    def load_existing_tasks(self):
        """Load all existing tasks from the database and populate the table."""
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # SQL query to fetch tasks for the logged-in user
            query = """
                SELECT Task_ID, Task_Name, Status, Deadline, Assigned_To 
                FROM Task_Allocation
                WHERE Assigned_To = ? OR Created_by = ?
            """
            cursor.execute(query, (self.current_user_id, self.current_user_id))
            tasks = cursor.fetchall()

            # Clear the table first
            self.tableWidget.setRowCount(0)

            # Map the status integer to its string representation
            status_mapping = {
                0: "Pending",
                1: "Completed",
                2: "Dropped"
            }

            # Add each task to the table
            for task in tasks:
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)

                # Set the task details in the table
                self.tableWidget.setItem(row_position, 0, QTableWidgetItem(str(task[0])))  # Task ID
                self.tableWidget.setItem(row_position, 1, QTableWidgetItem(str(task[1])))  # Task Name

                # Map the status integer to a string and insert it into the table
                status_str = status_mapping.get(task[2], "Unknown")  # Default to "Unknown" if invalid status
                self.tableWidget.setItem(row_position, 2, QTableWidgetItem(status_str))  # Status

                self.tableWidget.setItem(row_position, 3, QTableWidgetItem(str(task[3])))  # Deadline
                self.tableWidget.setItem(row_position, 4, QTableWidgetItem(str(task[4])))  # Assigned To

            conn.close()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred while fetching tasks: {e}")

    def assign_task(self):
        """Assign a new task to a cabinet member."""
        hu_id = self.ID_lineEdit.text().strip()
        cabinet_name = self.deptComboBox.currentText().strip()
        task_id = self.TaskID_lineEdit.text().strip()
        task_name = self.TaskName_lineEdit_2.text().strip()
        description = self.Descriptiontext.toPlainText().strip()
        deadline = self.dateEdit.date()  # QDate object

        # Retrieve the current user's HU_ID (from the session)
        created_by = self.current_user_id  # Use the actual HU_ID

        # Input validation
        if not all([hu_id, task_id, task_name, description, deadline]):
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please fill in all fields!")
            return

        # Check the user's role and prevent Cabinet Members from assigning tasks
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # Query to check if the user is a Cabinet Member, EC, or Chair
            cursor.execute("SELECT Designation FROM [User] WHERE HU_ID = ?", (created_by,))
            user_designation = cursor.fetchone()

            if not user_designation:
                QtWidgets.QMessageBox.warning(self, "Invalid User", "User does not exist!")
                return

            # If the user is a Cabinet Member, they cannot assign tasks
            if user_designation[0] == "Cabinet Member":
                QtWidgets.QMessageBox.warning(self, "Permission Denied", "Cabinet Members cannot assign tasks!")
                return

            # Query to check if the HU_ID is valid and if the HU_ID belongs to the selected cabinet
            query = """
                SELECT HU_ID FROM Cabinet_Member 
                WHERE HU_ID = ? AND Cabinet_Name = ?
            """
            cursor.execute(query, (hu_id, cabinet_name))
            result = cursor.fetchone()

            if not result:
                QtWidgets.QMessageBox.warning(self, "Invalid HU ID", f"The HU ID {hu_id} is not part of the {cabinet_name} cabinet.")
                return

            # Convert QDate to string in the correct format for SQL
            deadline_str = deadline.toString("yyyy-MM-dd")  # Format the date as 'yyyy-MM-dd'

            # Set Task Status to Pending (0 by default)
            status = 0  # Pending

            # SQL query to insert the task into the database
            insert_query = """
                INSERT INTO Task_Allocation (Task_ID, Task_Name, Description, Deadline, Status, Created_by, Assigned_To)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, (task_id, task_name, description, deadline_str, status, created_by, hu_id))
            conn.commit()

            QtWidgets.QMessageBox.information(self, "Success", f"Task {task_id} assigned successfully!")

            # Reload tasks to update the table
            self.load_existing_tasks()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        finally:
            # Ensure the connection is always closed properly
            if conn:
                conn.close()

        # Clear input fields for the next task
        self.ID_lineEdit.clear()
        self.TaskID_lineEdit.clear()
        self.TaskName_lineEdit_2.clear()
        self.Descriptiontext.clear()
        self.dateEdit.setDate(QDate.currentDate())  # Set date to today's date

    def change_status(self):
        """Change the status of a task (Completed, Dropped, Pending)."""
        # Get the selected row from the table
        selected_row = self.tableWidget.currentRow()
        if selected_row < 0:
            QtWidgets.QMessageBox.warning(self, "No Selection", "Please select a task to change its status.")
            return

        # Get the Task ID of the selected task
        task_id_item = self.tableWidget.item(selected_row, 0)  # Task_ID column
        if not task_id_item:
            QtWidgets.QMessageBox.warning(self, "Invalid Selection", "Please select a valid task.")
            return
        task_id = task_id_item.text()

        # Check which radio button is selected
        if self.status_button_group.checkedButton() is None:
            QtWidgets.QMessageBox.warning(self, "No Status Selected", "Please select a status (Completed, Pending, Dropped).")
            return

        status_button = self.status_button_group.checkedButton()

        # Determine status value based on the selected radio button text
        if status_button.text() == "Completed":
            status_value = 1  # Completed
        elif status_button.text() == "Dropped":
            status_value = 2  # Dropped
        else:
            status_value = 0  # Pending

        # Update the status in the database
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            # SQL query to update the task status
            update_query = """
                UPDATE Task_Allocation
                SET Status = ?
                WHERE Task_ID = ? AND Assigned_To = ?
            """
            cursor.execute(update_query, (status_value, task_id, self.current_user_id))  # Use current_user_id
            conn.commit()
            QtWidgets.QMessageBox.information(self, "Status Updated", f"The status of task {task_id} has been updated to {status_button.text()}.")
            # Reload tasks to update the table
            self.load_existing_tasks()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

def main():
    app = QApplication(sys.argv)
    loginwindow = LoginWindow()
    loginwindow.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()