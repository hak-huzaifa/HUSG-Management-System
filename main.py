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
        uic.loadUi('Login.ui',self)
        self.Login_pushButton.clicked.connect(self.login)
        self.Reg_pushButton.clicked.connect(self.open_registration_form)
        self.Close_pushButton.clicked.connect(self.close_application)

    def login(self):
        hu_id=self.ID_lineEdit.text()
        password=self.Password_lineEdit.text()

        if not hu_id or not password:
            QtWidgets.QMessageBox.warning(self,"Input Error","FILL ALL FIELDS!")
            return
        
        try:
            conn=connect_to_database()
            cursor=conn.cursor()

            query="SELECT * FROM [User] where HU_ID = ? AND Password = ?"
            cursor.execute(query,(hu_id,password))
            user = cursor.fetchone()

            if user:
                QtWidgets.QMessageBox.information(self,"Login Successful","Welcome to the Dashboard!")
                self.open_dashboard()
            else:
                QtWidgets.QMessageBox.warning(self,"Login Failed","Invalid HU ID or Password!")
            conn.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self,"Error",f"An error occured: {e}")

    def open_dashboard(self):
        self.dashboard = DashboardWindow()
        self.dashboard.show()
        self.close()
    
    def open_registration_form(self):
        self.registration_form = RegistrationWindow()
        self.registration_form.show()
        self.close()

    def close_application(self):
        self.close()


class DashboardWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Dashboard.ui', self)  # Load the Dashboard UI
        
        # Connect push buttons to their respective methods
        self.meetingspush.clicked.connect(self.open_meetings)
        self.Calendarpush.clicked.connect(self.open_events_calendar)
        self.Financepush.clicked.connect(self.open_budget_allocation)
        self.workpush.clicked.connect(self.open_task_allocation)
        self.closeButton.clicked.connect(self.close_application)

    def open_meetings(self):
        self.meetings_window = MeetingsWindow()
        self.meetings_window.show()
        self.close()

    def open_events_calendar(self):
        self.calendar_window = EventsCalendarWindow()
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
    def __init__(self):
        super().__init__()
        uic.loadUi('Meetings.ui', self)
        self.Back_pushButton.clicked.connect(self.go_back_to_dashboard)
        self.Add_pushButton.clicked.connect(self.add_meeting)

    def add_meeting(self):
        # Retrieve input data
        meeting_id = self.meetingIDLineEdit.text().strip()  # Get the meeting ID
        meeting_date = self.dateEdit.date()  # Get QDate object from dateEdit
        meeting_time = self.timeEdit.time()  # Get QTime object from timeEdit
        department = self.deptComboBox.currentText().strip()  # Clean the dropdown value

        # Input validation
        if not all([meeting_id, meeting_date, meeting_time, department]):
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please fill in all fields!")
            return

        # Ensure the meeting ID is a valid integer (if needed)
        try:
            int_meeting_id = int(meeting_id)  # Validate that the meeting ID is an integer
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Meeting ID must be a number!")
            return

        # Map department names to queries for Cabinet Members and Cabinet Chairs
        department_mapping = {
            "All EC": "SELECT HU_ID, Cabinet_ID FROM Cabinet_Member WHERE Cabinet_Name = 'Executive Council'",
            "EC + Cabinet Chairs": "SELECT HU_ID, Cabinet_ID FROM Cabinet_Member WHERE Cabinet_Name = 'Executive Council' OR Cabinet_Name = 'Cabinet Chair'",
            "Rights Advocacy & Ethos": "SELECT HU_ID, Cabinet_ID FROM Cabinet_Member WHERE Cabinet_Name = 'Rights Advocacy & Ethos'",
            "Events": "SELECT HU_ID, Cabinet_ID FROM Cabinet_Member WHERE Cabinet_Name = 'Events'",
            "Academic Affairs": "SELECT HU_ID, Cabinet_ID FROM Cabinet_Member WHERE Cabinet_Name = 'Academic Affairs'",
            "Food and Hygiene": "SELECT HU_ID, Cabinet_ID FROM Cabinet_Member WHERE Cabinet_Name = 'Food and Hygiene'",
            "Public Relations and Communications": "SELECT HU_ID, Cabinet_ID FROM Cabinet_Member WHERE Cabinet_Name = 'Public Relations and Communications'"
        }

        # Check if the selected department exists in the dictionary
        if department not in department_mapping:
            QtWidgets.QMessageBox.warning(self, "Error", f"Invalid Cabinet Name: {department}")
            return

        # Get the query for the selected department
        query = department_mapping[department]

        try:
            # Execute the query to get the Cabinet Members and Chairs for the selected department
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()

            if results:
                for result in results:
                    hu_id, cabinet_id = result
                    self.insert_meeting(int_meeting_id, meeting_date, meeting_time, department, hu_id, cabinet_id)
            else:
                QtWidgets.QMessageBox.warning(self, "Error", f"No members found for {department}")
                return

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        finally:
            conn.close()

        # Clear input fields for the next entry
        self.meetingIDLineEdit.clear()
        self.dateEdit.setDate(QDate.currentDate())  # Set date to today's date
        self.timeEdit.clear()
        self.deptComboBox.setCurrentIndex(0)  # Reset dropdown to the first option

    def insert_meeting(self, meeting_id, meeting_date, meeting_time, department, hu_id, cabinet_id):
        """Helper function to insert meeting into the database."""
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # Insert the meeting into the Meetings table
            meeting_query = """INSERT INTO Meetings (MeetingID, MeetingDate, MeetingTime, Department)
                            VALUES (?, ?, ?, ?)"""
            cursor.execute(meeting_query, (meeting_id, meeting_date.toString("yyyy-MM-dd"), meeting_time.toString("HH:mm"), department))

            # Commit the transaction
            conn.commit()

            # Insert the meeting into the Cabinet_Member or Cabinet_Chair table
            if department == "Executive Council" or department == "EC + Cabinet Chairs":
                cabinet_member_query = """INSERT INTO Cabinet_Member (HU_ID, Cabinet_ID, Cabinet_Name, Is_Active, Year) 
                                        VALUES (?, ?, ?, 1, ?)"""
                cursor.execute(cabinet_member_query, (hu_id, cabinet_id, department, "2024"))
            elif department == "Cabinet Chair" or department == "EC + Cabinet Chairs":
                cabinet_chair_query = """INSERT INTO Cabinet_Chair (HU_ID, Cabinet_ID, Cabinet_Name, Role, Is_Active, Year) 
                                        VALUES (?, ?, ?, ?, 1, ?)"""
                cursor.execute(cabinet_chair_query, (hu_id, cabinet_id, department, "Cabinet Chair", "2024"))

            # Update the meetings table on UI
            row_position = self.meetingsTable.rowCount()
            self.meetingsTable.insertRow(row_position)
            self.meetingsTable.setItem(row_position, 0, QTableWidgetItem(str(meeting_id)))
            self.meetingsTable.setItem(row_position, 1, QTableWidgetItem(meeting_date.toString("yyyy-MM-dd")))
            self.meetingsTable.setItem(row_position, 2, QTableWidgetItem(meeting_time.toString("HH:mm")))
            self.meetingsTable.setItem(row_position, 3, QTableWidgetItem(department))

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        finally:
            conn.close()


    def go_back_to_dashboard(self):
        self.close()
        self.dashboard = DashboardWindow()
        self.dashboard.show()



class EventsCalendarWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('EventsCalender.ui',self)
        self.Back_pushButton.clicked.connect(self.go_back_to_dashboard)

    def go_back_to_dashboard(self):
        self.close()
        self.dashboard = DashboardWindow()
        self.dashboard.show()

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
