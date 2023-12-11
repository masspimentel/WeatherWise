from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from gradient import Gradient
from forecast import forecastWidget
from hover_button import HoverButton
from matplotlib.figure import Figure
from weather_fetch import fetch_weather_data
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import os
import sys
import bcrypt
import sqlite3
import requests
import mplcursors
import pandas as pd
import seaborn as sns
import country_converter as coco
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# If users doesnt input a location, use their current location from public IP
def location():
    resp = requests.get('https://ipinfo.io/')
    loc_data = resp.json()
    return loc_data['city'], loc_data['country']

# Login or Register Dialog class, used to initialize the login or register dialog
class LoginOrRegister(QDialog):
    def __init__(self, parent=None):
        super(LoginOrRegister, self).__init__(parent)

        self.is_login_success = False #set to false by default, if user successfully logs in, set to true

        #setting window title, icon, and size
        self.setWindowTitle('Login or Register')
        self.setWindowIcon(QIcon('weatherProj\Main\images\Weather-PNG.png'))
        self.setFixedSize(300, 200)

        #setting login or register layout, buttons, labels, and input fields
        self.titleCard = QLabel('Weather App by Mass', self)
        self.titleCard.setFont(QFont('Poppins SemiBold', 13))
        self.titleCard.setStyleSheet('QLabel { color: #09203F; }')
        self.titleCard.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = QLabel('Sign In', self)
        self.title.setFont(QFont('Poppins SemiBold', 11))
        self.title.setStyleSheet('QLabel { color: #09203F; }')
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setVisible(True)

        self.username_input = QLineEdit(self)
        self.username_input.setStyleSheet('QLineEdit {  color:         black;\n\
                                                        border-radius: 10px;\n\
                                                        padding:       5px;\n\
                                                        border:        1px solid black; }')
        self.password_input = QLineEdit(self)
        self.password_input.setStyleSheet('QLineEdit {  color:         black;\n\
                                                        border-radius: 10px;\n\
                                                        padding:       5px;\n\
                                                        border:        1px solid black; }')

        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button = HoverButton('Login', self)
        self.register_button = HoverButton('Register', self)
        
        #adding widgets to layout
        LogOrRegLayout = QVBoxLayout(self)
        LogOrRegLayout.addWidget(self.titleCard)
        LogOrRegLayout.addWidget(self.title)
        LogOrRegLayout.addWidget(self.username_input)
        LogOrRegLayout.addWidget(self.password_input)
        LogOrRegLayout.addWidget(self.login_button)
        LogOrRegLayout.addWidget(self.register_button)

        #connecting buttons to functions
        self.register_button.clicked.connect(self.register_user)
        self.login_button.clicked.connect(self.login_user)

    #function used to register user
    def register_user(self):
        #getting user input data and assigning to vars
        username = self.username_input.text()
        password = self.password_input.text()

        #setting up salting and hashing for password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)

        #connect to db and insert user, salt, and hashed password into users table
        conn = sqlite3.connect('weatherProj\WeatherApp.db')
        cur = conn.cursor()
        cur.execute('''
                    INSERT INTO users (username, salt_password, hashed_password) VALUES (?, ?, ?)''',
                    (username, salt, hashed_password))
        user_id = cur.lastrowid #get the last row id, which is the user id

        #insert user id into userPref table
        cur.execute('''INSERT INTO userPref (user_id) VALUES (?)''', (user_id,))
        conn.commit()
        conn.close()

        #show message box to user that registration was successful
        msgBox = QMessageBox()
        msgBox.setText('Registration successful')
        msgBox.exec()

    #function used to login user and check if username and password are correct
    def login_user(self):
        #get the user input data and assign to vars
        username = self.username_input.text()
        password = self.password_input.text()

        #connect to db and select the user id, salt, and hashed password from users table where username is equal to the username input
        conn = sqlite3.connect('weatherProj\WeatherApp.db')
        cur = conn.cursor()
        cur.execute('''SELECT user_id, salt_password, hashed_password FROM users WHERE username = ?''', (username,))
        result = cur.fetchone()

        #if the result is none, show message box to user that username or password is incorrect
        if result is None:
            msgBox = QMessageBox()
            msgBox.setText('Username or password is incorrect')
            msgBox.exec()
            self.reject()
            self.is_login_success = False
        #if the result is not none, get the user id, salt, and hashed password from the result
        else:
            user_id, salt_password, hashed_password = result
            if bcrypt.checkpw(password.encode(), hashed_password): #if the password is correct, show message box to user that login was successful and let them into the app
                msgBox = QMessageBox()
                msgBox.setText('Login successful')
                msgBox.exec()
                self.accept()
                self.is_login_success = True
                return user_id
            #if the password is incorrect, show message box to user that username or password is incorrect
            else:
                msgBox = QMessageBox()
                msgBox.setText('Username or password is incorrect')
                msgBox.exec()
            self.login_button.clicked.disconnect(self.login_user)

#GUI class, used to initialize the main GUI, do all the calculations, and update the GUI
class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.user_id = None
        self.login_dialog = LoginOrRegister(self)

        #while the user has not logged in or registered, show the login dialog
        while True:
            result = self.login_dialog.exec()
            #if the user has logged in successfully, break out of the loop
            if result == QDialog.DialogCode.Accepted and self.login_dialog.is_login_success:
                self.user_id = self.login_dialog.login_user()
                break
            #if the user has not logged in successfully, show message box to user that they must login or register to use the app
            elif result == QDialog.DialogCode.Rejected:
                response = QMessageBox.critical(self, 'Error.', 'You must login or register to use this app.', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                # if the user select No, exit the app
                if response == QMessageBox.StandardButton.No:
                    sys.exit(0)

        #create main layout and initialize all the variables
        self.layout = QGridLayout()
        self.weather_data = []
        self.current_index = 0
        self.current_date = None
        self.city = ''
        self.countryCode = ''
        self.current_page = 0
        self.weather_info = pd.DataFrame()

        font = QFont('Poppins Medium', 10)
            
        #setting window title and icon
        self.setWindowTitle('Weather App')
        self.setWindowIcon(QIcon('weatherProj\Main\images\Weather-PNG.png'))

        #setting up the main layout, buttons, labels, and input fields
        self.name = QLabel(f'Welcome, {self.login_dialog.username_input.text()}')
        self.name.setFont(font)
        self.name.setStyleSheet('QLabel { color: white; }')
        self.name.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.name)
        
        self.weather_label = QLabel("Weather Info")
        self.weather_label.setFont(QFont('Poppins SemiBold', 13))
        self.weather_label.setStyleSheet('QLabel { color: white; }')
        self.weather_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.weather_label)

        self.get_weather_button = HoverButton('Get Weather')
        self.get_weather_button.setFont(font)
        self.get_weather_button.clicked.connect(self.update_gui)
        self.layout.addWidget(self.get_weather_button)

        '''Gradient.main_widget.setLayout(self.layout)
        self.setCentralWidget(Gradient.main_widget)'''

        self.main_widget = Gradient()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

        self.enter_text_label = QLabel('Enter City and Country Code')
        self.enter_text_label.setFont(font)
        self.enter_text_label.setStyleSheet('QLabel { color: white; }')
        self.enter_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.enter_text_label)

        self.notice_label = QLabel('(If you leave the fields blank, your current location will be used)')
        self.notice_label.setFont(QFont('Poppins Medium', 8))
        self.notice_label.setStyleSheet('QLabel { color: white; }')
        self.notice_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.notice_label)

        self.getCityInput = QLineEdit()
        self.getCityInput.setPlaceholderText('Enter City')
        self.getCityInput.setFont(font)
        self.getCityInput.setStyleSheet('QLineEdit { border-radius: 10px;\n\
                                                    padding:       5px;\n\
                                                    border:        0px; }')
        self.layout.addWidget(self.getCityInput)

        self.getCountryInput = QLineEdit() 
        self.getCountryInput.setPlaceholderText('Enter Country Code')
        self.getCountryInput.setFont(font)
        self.getCountryInput.setStyleSheet('QLineEdit { border-radius: 10px;\n\
                                                        padding:       5px;\n\
                                                        border:        0px; }')
        self.layout.addWidget(self.getCountryInput)

        self.next_page = HoverButton('Next Page')
        self.next_page.setFont(font)
        self.next_page.clicked.connect(self.next_page_func)
        self.next_page.setVisible(False)
        self.layout.addWidget(self.next_page)

        self.prev_page = HoverButton('Previous Page')
        self.prev_page.setFont(font)
        self.prev_page.clicked.connect(self.prev_page_func)
        self.prev_page.setVisible(False)
        self.layout.addWidget(self.prev_page)

        self.next_day_button = HoverButton('Next Day')
        self.next_day_button.clicked.connect(self.click_next_day)
        self.next_day_button.setFlat(True)
        self.next_day_button.setFont(font)
        self.next_day_button.setVisible(False)
        self.layout.addWidget(self.next_day_button)

        self.figure = Figure()

        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumSize(500, 400)
        self.canvas.setVisible(False)

        self.show_graphs = HoverButton('Show Graphs')
        self.show_graphs.setFont(font)
        self.show_graphs.clicked.connect(self.show_graphs_func)
        self.show_graphs.setVisible(False)
        self.layout.addWidget(self.show_graphs)

        self.forecast_layout = QVBoxLayout()
        self.forecast_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.forecast_container = QWidget()
        self.forecast_container.setLayout(self.forecast_layout)

        self.add_phone_num = HoverButton('Add Phone Number')
        self.add_phone_num.setFont(font)
        self.add_phone_num.clicked.connect(self.add_phone_num_func)
        self.layout.addWidget(self.add_phone_num)

        self.write_phone_num = HoverButton('Add Number?')
        self.write_phone_num.setFont(font)
        self.write_phone_num.setVisible(False)
        self.write_phone_num.clicked.connect(self.write_phone_num_func)
        self.layout.addWidget(self.write_phone_num)

        self.layout.addWidget(self.forecast_container)
        
    #function used to add phone number input field
    def add_phone_num_func(self):
        self.phone_num_input = QLineEdit()
        self.phone_num_input.setPlaceholderText('Enter Phone Number')
        self.phone_num_input.setFont(QFont('Poppins Medium', 10))
        self.phone_num_input.setStyleSheet('QLineEdit { border-radius: 10px;\n\
                                                        padding:       5px;\n\
                                        }')
        self.layout.addWidget(self.phone_num_input)
        #if add phone num button is clicked then hide the add phone num button and show the phone num input field
        if self.add_phone_num.clicked:
            self.write_phone_num.setVisible(True)
            self.add_phone_num.setVisible(False)

    #function used to write the phone number to the database
    def write_phone_num_func(self):
        conn = sqlite3.connect('weatherProj\WeatherApp.db')
        cur = conn.cursor()
        cur.execute('''SELECT user_id FROM users''')
        cur.execute('''UPDATE userPref SET phone_num = ? WHERE user_id = ?''', (self.phone_num_input.text(), self.user_id))
        conn.commit()
        conn.close()
        #set both buttons to invisible
        if self.write_phone_num.clicked:
            self.write_phone_num.setVisible(False)
            self.phone_num_input.setVisible(False)

    #function used to assign weather types to a weather icon
    def get_weather_icon(self, description):
        if 'clear' in description or 'sunny' in description:
                icon_filename = 'sunny.png'
        elif 'rain' in description or 'showers' in description or 'drizzle' in description:
            icon_filename = 'rain.png'
        elif 'clouds' in description or 'overcast' in description or 'cloudy' in description or 'cloud' in description:
            icon_filename = 'cloudy.png'
        elif 'snow' in description or 'blizzard' in description:
            icon_filename = 'snow.png'
        elif 'thunder' in description or 'storm' in description or 'thunderstorm' in description:
            icon_filename = 'thunder.png'
        else:
            icon_filename = 'Weather-PNG.png'

        return os.path.join(BASE_PATH, 'images', icon_filename)

    #function used to create the forecast cards
    def create_forecast_cards(self, weather_data):
        temp = 0
        night_temp = 0

        #when the user switches 'pages', it will delete the 'old' card
        while self.forecast_layout.count() > 0:
            item = self.forecast_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        #for each day in the weather data, create a forecast card
        for data in weather_data:
            day, weather_icon, day_temp, night_temp, weather_desc = data
            card = self.create_forecast_card(day, weather_icon, day_temp, night_temp, weather_desc)
            self.forecast_layout.addWidget(card)

    #function used to create the forecast card, styling, and layout
    def create_forecast_card(self, day, weather_icon, day_temp, night_temp, weather_desc):
        card = forecastWidget(day, weather_icon, str(day_temp), str(night_temp), weather_desc, parent = self.forecast_container)
        card_layout = QVBoxLayout()
        card.setStyleSheet('''QWidget { 
                        background-color: 'white'; 
                        border-radius: 10px; 
                        padding: 10px;
                        margin: 5px;
                        }  QLabel  {
                        font-size: 16px; 
                        }''')
        return card
    
    #function used to get the location data
    def get_location_data(self, city, countryCode):
        self.city = city
        self.countryCode = countryCode
        return self.city, self.countryCode

    #function used to make sure the current index does not exceed the length of the weather data, if it does, set it back to 0
    def next_index(self):
        if self.current_index < len(self.weather_data[1]) - 1:
            self.current_index += 1
        else:
            self.current_index = 0
    
    #function used for the 'Next' button to get the next day's weather data, connects to that button
    def click_next_day(self):
        self.next_index()
        self.update_label()
        if self.canvas.isVisible():
            self.plot_data(self.weather_info)

    #function used to update the GUI
    def next_page_func(self):
        self.current_page += 1    
        self.plot_data(self.weather_info) 
        #self.plot_data(self.weather_info)

    #function used to update the GUI
    def prev_page_func(self):
        self.current_page -= 1     
        self.plot_data(self.weather_info)   
        #self.plot_data(self.weather_info)

    #function used to plot data in the graphs 'area'
    def plot_data(self, df):
        self.next_page.setVisible(True)
        self.prev_page.setVisible(True)

        #if the df is not empty then transpose the df, set the columns to the first row, and set the df to the rest of the rows
        if not df.empty:
            df = df.transpose()
            df.columns = df.iloc[0]
            df = df[1:]
            #df = df[(df['City:'] == city) & (df['Country:'] == coco.convert(names=country, to='name_short'))]

            columns_to_convert = ['Temperature during the day:', 'Average Temperature:', 'Low Temperature:', 'High Temperature:', 'Humidity:', 'Wind Speed:', 'What it feels like in the morning:', 'What it feels like in the day:', 'What it feels like in the evening:', 'What it feels like at night:']

            #for each column in the df, if the column is of object type, then extract the numbers from the string and convert to float
            for column in columns_to_convert:
                if df[column].dtype == object:  # Check if the column is of object (string) type
                    df[column] = df[column].str.extract('([-+]?\d*\.\d+|\d+)').astype(float)
        else: 
            print('DF is empty')
            return

        self.figure.clear()
        axs = self.figure.add_subplot(111)
        
        #set the different 'pages' to different graphs
        
        if self.current_page == 0:
            bars = df[['Temperature during the day:', 'Average Temperature:', 'Low Temperature:', 'High Temperature:']].plot(kind='bar', ax=axs)
            axs.set_ylabel('Temperature (°C)')
            df['Date:'] = pd.to_datetime(df['Date:'], format='%Y-%m-%d', errors='coerce')
            df['Date:'].fillna(pd.to_datetime('2000-01-01'), inplace=True)
            #axs.set_xlabel('Date:', rotation=0)
            plt.xticks(df['Date:'], rotation=0)
            axs.legend(title='Temperatures', loc='upper right', fontsize='5')
            cursor = mplcursors.cursor(bars, hover=True)
            cursor.connect("add", lambda sel: sel.annotation.set_text('Date: {} \nValue: {}°C'.format(df.index[sel.target.index], sel.target[1])))
            axs.yaxis.set_major_formatter(ticker.ScalarFormatter())
            axs.yaxis.get_major_formatter().set_scientific(False)

        elif self.current_page == 1:
            bars = df['Humidity:'].plot(kind='bar', ax=axs)
            axs.set_ylabel('Humidity (%)')
            df['Date:'] = pd.to_datetime(df['Date:'], format='%Y-%m-%d')
            plt.xticks(df['Date:'], rotation=0)
            cursor = mplcursors.cursor(bars, hover=True)
            cursor.connect("add", lambda sel: sel.annotation.set_text('Date: {} \nValue: {}%'.format(df.index[sel.target.index], sel.target[1])))
            axs.yaxis.set_major_formatter(ticker.ScalarFormatter())
            axs.yaxis.get_major_formatter().set_scientific(False)

        elif self.current_page == 2:
            bars = df['Wind Speed:'].plot(kind='bar', ax=axs)
            axs.set_ylabel('Wind Speed (km/h)')
            df['Date:'] = pd.to_datetime(df['Date:'], format='%Y-%m-%d')
            plt.xticks(df['Date:'], rotation=0)
            cursor = mplcursors.cursor(bars, hover=True)
            cursor.connect("add", lambda sel: sel.annotation.set_text('Date: {} \nValue: {}KM/H'.format(df.index[sel.target.index], sel.target[1])))
            axs.yaxis.set_major_formatter(ticker.ScalarFormatter())
            axs.yaxis.get_major_formatter().set_scientific(False)

        else:
            self.current_page = 0
            bars = df[['Temperature during the day:', 'Average Temperature:', 'Low Temperature:', 'High Temperature:']].plot(kind='bar', ax=axs)
            axs.set_ylabel('Temperature (°C)')
            df['Date:'] = pd.to_datetime(df['Date:'], format='%Y-%m-%d')
            axs.legend(title='Temperatures', loc='upper right', fontsize='5')
            plt.xticks(df['Date:'], rotation=0)
            cursor = mplcursors.cursor(bars, hover=True)
            cursor.connect("add", lambda sel: sel.annotation.set_text('Date: {} \nValue: {}°C'.format(df.index[sel.target.index], sel.target[1])))
            axs.yaxis.set_major_formatter(ticker.ScalarFormatter())
            axs.yaxis.get_major_formatter().set_scientific(False)


        self.layout.removeWidget(self.canvas)
        self.canvas.setVisible(True)
        
        self.forecast_container.setVisible(False)
        self.layout.addWidget(self.canvas)
        self.setCentralWidget(self.main_widget)
        self.canvas.draw()

    #function used to show the graphs, connects to the 'Show Graphs' button
    def show_graphs_func(self):
        self.plot_data(self.weather_info)
        self.canvas.setVisible(True)
        
    #function used to update the layouts with the weather data
    def update_label(self):
        print(self.weather_data[1])
        print(self.current_index)

        if self.weather_data and 'currWeatherDF' in self.weather_data[0]:
            #curr_weather = self.weather_data[1]
            curr_weather = self.weather_data[1]
            date = curr_weather['dt'].iloc[self.current_index]
            temp_dict = curr_weather['temp'].iloc[self.current_index]
            mean_of_temp = round(temp_dict['min'] + temp_dict['max'], 2) / 2
            min_temp = temp_dict['min']
            max_temp = temp_dict['max']
            day = temp_dict['day']
            feels_like_dict = curr_weather['feels_like'].iloc[self.current_index]
            morn_feels_like = feels_like_dict['morn']
            day_feels_like = feels_like_dict['day']
            eve_feels_like = feels_like_dict['eve']
            night_feels_like = feels_like_dict['night']
            humidity = curr_weather['humidity'].iloc[self.current_index]
            wind_speed = curr_weather['windspeed'].iloc[self.current_index]
            #print('test', curr_weather)
            weather_desc = curr_weather['weather_description'].iloc[self.current_index]
            self.weather_info = pd.DataFrame([('City:', f'{self.city}'),
                            ('Country:', f'{coco.convert(names=self.countryCode, to="name_short")}'),
                            ('Date:', f'{date}'),
                            ('Temperature during the day:', f'{day}°C'),
                            ('Average Temperature:', f'{mean_of_temp}°C'),
                            ('Low Temperature:', f'{min_temp}°C'),
                            ('High Temperature:', f'{max_temp}°C'),
                            ('What it feels like in the morning:', f'{morn_feels_like}°C'),
                            ('What it feels like in the day:', f'{day_feels_like}°C'),
                            ('What it feels like in the evening:', f'{eve_feels_like}°C'),
                            ('What it feels like at night:', f'{night_feels_like}°C'),
                            ('Humidity:', f'{humidity}%'),
                            ('Wind Speed:', f'{wind_speed} km/h'),
                            ('Weather Description:', f'{weather_desc}')], columns=['Attribute', 'Value'])
        # self.update_forecast_widget(self.weather_info)
            
        else:
            raise Exception('No weather data found')
        
        #set the weather icon, day, night, and weather description to the card var
        card = self.create_forecast_card(date, self.get_weather_icon(weather_desc), day, night_feels_like, weather_desc)

        #had to to do this because the card was not updating, so I had to delete the old card and add the new one
        while self.forecast_layout.count() > 0:
            child = self.forecast_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        #add the card to the layout
        self.forecast_layout.addWidget(card)

        #weather_info_tabulate = tabulate(weather_info, tablefmt='plain')
        
        #self.weather_label.setText(weather_info_tabulate)
        self.weather_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    #function used to update the GUI determind by user input
    def update_gui(self):
        if self.getCityInput.text() and self.getCountryInput.text():
            self.city = self.getCityInput.text()
            self.countryCode = self.getCountryInput.text()
        else: self.city, self.countryCode = location()
        choice = '1'  # Use metric units
        callAmount = 1  # Only fetch current weather data
        realTime = None  # Use current time

        #get weather data from the fetch_weather_data function in the weather_fetch.py file. set error message if city & country code are invalid.
        try:
            self.weather_data = fetch_weather_data(choice, self.city, self.countryCode, callAmount, realTime)
        except Exception as e:
            QMessageBox.critical(self, 'Error.', 'Is your city and country correct?', QMessageBox.StandardButton.Retry)
            return
        self.update_label()

        #if user id is not none connect to the db and update the city and country code in the userPref table
        if self.user_id is not None:
            conn = sqlite3.connect('weatherProj\WeatherApp.db')
            cur = conn.cursor()
            try:
                cur.execute('''UPDATE userPref SET city = ?, country_code = ? WHERE user_id = ?''', (self.city, self.countryCode, self.user_id))
            except Exception as e:
                print(f'Error updating database: {e}')
            conn.commit()
            conn.close()

        #setting labels and buttons to visible or invisible
        self.enter_text_label.setVisible(False)
        self.notice_label.setVisible(False)
        self.getCityInput.setVisible(False)
        self.getCountryInput.setVisible(False)
        self.get_weather_button.setVisible(False)
        self.name.setVisible(False)
        self.next_day_button.setVisible(True)
        self.show_graphs.setVisible(True)
        self.forecast_container.setVisible(True)
        self.forecast_container.repaint()
        self.adjustSize()

        #print('!!!!!!!!', self.weather_data) 
