import sys
import pyodbc
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox

# Database connection function
def connect_to_db():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=HAK-PC\\HAKSERVER;"  # Double backslash for the server name
        "DATABASE=PROJECT;"
        "Trusted_Connection=yes;"
    )

# Main Application Runner
def main():
    app = QtWidgets.QApplication(sys.argv)
    login = LoginScreen()
    login.show()
    print("Showing Login Screen...")  # Debugging print statement
    sys.exit(app.exec())




# Login Screen
class LoginScreen(QMainWindow):
    def _init_(self):
        super(LoginScreen, self)._init_()
        print("Loading Login UI...")  # Debugging print statement
        uic.loadUi('Login.ui', self)
        self.show()  # Show the UI after loading# Debugging print statement
        # Connect the login button to the login method
        self.btnLogin.clicked.connect(self.login)
        print("Login Screen loaded successfully.")  # Debugging print statement

    def login(self):
        print("Login button clicked.")  # Debugging print statement
        user_id = self.txtHU_ID.text()
        password = self.txtPassword.text()
        print(f"User ID: {user_id}, Password: {password}")  # Debugging print statement
        try:
            connection = connect_to_db()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM [User] WHERE HU_ID = ? AND Password = ?", (user_id, password))
            result = cursor.fetchone()
            connection.close()
            if result:
                print("Login successful. Opening Dashboard...")  # Debugging print statement
                self.main_window = MainWindow()
                self.main_window.show()
                self.close()
            else:
                print("Login failed. Invalid HU ID or password.")  # Debugging print statement
                QMessageBox.warning(self, "Login Failed", "Invalid HU ID or password.")
        except Exception as e:
            print(f"Error during login: {e}")  # Debugging print statement

# Main Dashboard
class MainWindow(QMainWindow):
    def _init_(self):
        super(MainWindow, self)._init_()
        print("Loading Dashboard UI...")  # Debugging print statement
        try:
            uic.loadUi('Dashboard.ui', self)
            self.show()  # Show the UI after loading
            print("Dashboard Screen loaded successfully.")  # Debugging print statement
        except Exception as e:
            print(f"Error loading Dashboard UI: {e}")  # Debugging print statement

# Corrected main function call
if __name__ == "__main__":
    main()