from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QGraphicsDropShadowEffect
from PyQt6.QtGui import QPixmap, QColor, QFont
from PyQt6.QtCore import Qt
import os
from gradient import Gradient

# this script creates the forecast widget that is displayed on the main page of the application.
class forecastWidget(QWidget):
    def __init__(self, day = None, weather_icon = None, day_temp = None, night_temp = None, weather_desc = None, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(300, 300)

        self.setStyleSheet('''
                           QWidget {
                            background-color: 'white';
                            border-radius: 5px;
                            padding: 5px;
                           }
                           QLabel {
                           font-size: 15px;
                           }
        ''')

        # Check if all data is present, if it is, initialize the UI
        if day and weather_icon and day_temp and night_temp and weather_desc:
            self.initUI(day, weather_icon, day_temp, night_temp, weather_desc)

    # this function initializes the UI for the forecast widget (cards)
    def initUI(self, day, weather_icon, day_temp, night_temp, weather_desc):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        print(day, weather_icon, day_temp, night_temp, weather_desc)

        # Setup day label
        day_str = str(day)
        day_label = QLabel(day_str)
        day_label.setFont(QFont('Poppins Medium'))
        day_label.setStyleSheet('color: black;')
        day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(day_label)

        # Setup icon label
        icon_label = QLabel()
        icon_pixmap = QPixmap(weather_icon)
        if icon_pixmap.isNull():
            print(f'Error loading icon {weather_icon}')
        else:
            icon_label.setPixmap(icon_pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio))
        icon_label.setFont(QFont('Poppins Medium'))
        icon_label.setStyleSheet('color: black;')
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(icon_label)

        # Setup temperature layout
        temp_layout = QHBoxLayout()
        day_temp_label = QLabel(f'Day: {day_temp}°C')
        day_temp_label.setFont(QFont('Poppins Medium'))
        day_temp_label.setStyleSheet('color: black;')
        day_temp_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        temp_layout.addWidget(day_temp_label)

        night_temp_label = QLabel(f'Night: {night_temp}°C')
        night_temp_label.setFont(QFont('Poppins Medium'))
        night_temp_label.setStyleSheet('color: black;')
        night_temp_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        temp_layout.addWidget(night_temp_label)
        main_layout.addLayout(temp_layout)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor('black'))
        shadow.setOffset(2)

        self.setGraphicsEffect(shadow)

        self.setLayout(main_layout)



   

