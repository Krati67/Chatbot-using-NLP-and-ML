import sys
import os
from PyQt5 import uic
from PyQt5 import QtWidgets as Qtw
from PyQt5 import QtGui as Qtg
from PyQt5 import QtCore as Qtc

#code functions
from langdetect import detect

# Code to show error, if the app crashes
import cgitb

cgitb.enable(format='text')


# noinspection PyMethodMayBeStatic,PyAttributeOutsideInit
class ChatBox(Qtw.QMainWindow):

    def __init__(self):

        super().__init__()  # avoid code redundancy

        self.messages = []
        self.text_display = ""

        uic.loadUi(r"UI\\Chat Box.ui", self)

        self.setWindowFlag(Qtc.Qt.FramelessWindowHint)

        self.header_frame.mouseMoveEvent = self.move_with_click_title_bar

        self.show()  # show the UI

        self.human_text = ""

        self.send_message(False, "Hey I am Kratzz!")

        self.send_message(False, "I am your personal translator.")

        self.choice_of_input()

        self.pushButton_3.clicked.connect(lambda: self.send_message(True))

        self.minimiseButton.clicked.connect(lambda: self.showMinimized())

        self.closeButton.clicked.connect(lambda: self.close())

    def choice_of_input(self):
        self.send_message(False, 'What type of input will you choose?')
        self.send_message(False, '1. Text')
        self.send_message(False, '2. Speech')

        # human_text = input()
        # human_text = human_text.lower()
        # print(human_text)


    def send_message(self, message_from, message=""):

        text = self.userInputText.toPlainText()

        if text == "" and message_from:
            pass
        else:

            temp_dataset = {1: message_from, 2: text}

            self.messages.append(temp_dataset)

            if temp_dataset[1]: 
                # User
                self.text_display += f"<div style='color: #ffa500'>[You]: {temp_dataset[2]}</div> <br />"
                self.chatsText.setText(self.text_display)

                self.human_text = self.userInputText.toPlainText()

                print("Human Text Value is ", self.human_text)

                if self.human_text == "text":
                    # run code
                    self.selected_text()

                elif self.human_text == "speech":
                    # run code
                    pass

            elif not temp_dataset[1]:
                # Bot
                self.text_display += f"<div style='color: #acc9e6'>[Bot]: {message}</div> <br />"
                self.chatsText.setText(self.text_display)

            # self.userInputText.setText("") 

    def selected_text(self):
        # detect_language = input("PLease enter the text which you wish to translate: ")

        self.send_message(False, "PLease enter the text which you wish to translate: ")

        
        self.detect_language_var = self.userInputText.toPlainText()

    
    # def detect_language(self):




    def move_with_click_title_bar(self, event):

        if event.buttons() == Qtc.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


if __name__ == "__main__":
    app = Qtw.QApplication(sys.argv)
    chat_box = ChatBox()
    sys.exit(app.exec())
