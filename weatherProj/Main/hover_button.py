from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import QPropertyAnimation, pyqtProperty, QAbstractAnimation


#creates a custom button that changes color when hovered over
class HoverButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initUi()

    # this initializes the button animation, through color changes.
    def __initUi(self):
        self.__defaultColor = QColor('#09203F')
        self.__animation = QPropertyAnimation(self, b"bgColor")
        self.__animation.valueChanged.connect(self.__setBgColor)
        #self.__animation.valueChanged.connect(self.__setOpacity)
        self.__animation.setStartValue(self.__defaultColor)
        self.__animation.setEndValue(QColor('#7897b0'))
        self.__animation.setDuration(200)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.ButtonText, QColor('white'))
        self.setPalette(palette)

    #style the button
    def __styleInit(self, color: QColor):
        style = f'QPushButton {{ background-color: {color.name()};' \
                f'border: 0;' \
                f'padding: 5;' \
                f'border-radius: 10; }}'
        self.setStyleSheet(style)

    def enterEvent(self, e):                                                #
        self.__animation.setDirection(QAbstractAnimation.Direction.Forward) #
        self.__animation.start()                                            #
        return super().enterEvent(e)                                        #
                                                                            # -- this starts and ends the animation
    def leaveEvent(self, e):                                                #
        self.__animation.setDirection(QAbstractAnimation.Direction.Backward)#
        self.__animation.start()                                            #
        return super().leaveEvent(e)                                        #

    '''def __setOpacity(self, opacity):
        self.__styleInit(opacity)'''
    
    #setting bg colors
    def __setBgColor(self, color):
        self.__styleInit(color)

    @pyqtProperty(QColor)
    def bgColor(self):
        return self.__defaultColor
    
    @bgColor.setter
    def bgColor(self, color):
        self.__defaultColor = color
        self.__styleInit(color)

