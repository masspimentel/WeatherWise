from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QLinearGradient, QFont, QColor

#used to create custom gradient background for the application
class Gradient(QWidget):
    def paintEvent(self, e):
        self.main_widget = QWidget()
        paint = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), 0) #gradient from left to right, 
                                                          #if you want a vertical gradient, 
                                                          #change self.width() t0 0 and change the second 0 to self.height()
        gradient.setColorAt(0, QColor('#09203F'))
        gradient.setColorAt(1, QColor('537895'))
        paint.fillRect(self.rect(), gradient)
        self.main_widget.setFont(QFont('Poppins Medium', 10))