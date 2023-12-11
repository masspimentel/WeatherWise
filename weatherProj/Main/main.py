import sys
import schedule
import time
from PyQt6.QtWidgets import QApplication
from gui import GUI
from sched_task import send_daily_notifs
from weatherDB import weatherDB

#main function runs the application and creates the database if it doesn't exist. 
def main():
    weatherDB('weatherProj\WeatherApp.db')
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
