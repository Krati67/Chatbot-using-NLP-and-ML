import sys
import os
from PyQt5 import uic
from PyQt5 import QtWidgets as Qtw
from PyQt5 import QtGui as Qtg
from PyQt5 import QtCore as Qtc

# code functions
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

        # Sequence variables

        # chat_bot_sequence will show contain the sequences that program will go through
        self.chat_bot_sequence = ["text_or_speech", "detect_language", ""]

        # we use current sequence to update to the next sequence
        self.current_sequence = self.chat_bot_sequence[0]

        self.send_message(False, "Hey I am Kratzz!")
        self.send_message(False, "I am your personal translator.")

        self.choice_of_input()

        self.sendButton.clicked.connect(lambda: self.send_message(True, message=self.userInputText.toPlainText()))

        self.minimiseButton.clicked.connect(lambda: self.showMinimized())
        self.closeButton.clicked.connect(lambda: self.close())

    def choice_of_input(self):
        self.send_message(False, 'What type of input will you choose?')
        self.send_message(False, '1. Text')
        self.send_message(False, '2. Speech')

    def send_message(self, message_from, message=""):

        correct_input = True  # if invalid input program does not go further

        if message == "" and message_from:
            pass

        else:

            temp_dataset = {1: message_from, 2: message}
            self.messages.append(temp_dataset)

            if temp_dataset[1]:
                # User
                self.text_display += f"<div style='color: #ffa500'>[You]: {temp_dataset[2]}</div> <br />"

                self.chatsText.setText(self.text_display)

                if self.current_sequence == "text_or_speech":

                    human_text = self.userInputText.toPlainText()

                    if human_text.lower() == "text":  # converting to lower case
                        self.selected_text()

                    elif human_text.lower() == "speech":  # converting to lower case
                        # we can define fn to what should happen if user selects speech
                        pass

                    else:
                        # will update the correct_input var so that the program will continue only if there is a valid input
                        correct_input = False
                        self.send_message(False, "Please enter either Text or Speech alone.")

                if self.current_sequence == "detect_language":
                    language_to_detect = self.userInputText.toPlainText()
                    self.detect_language(language_to_detect)

                current_sequence_location = int(self.chat_bot_sequence.index(f"{self.current_sequence}"))

                print(correct_input)

                if correct_input:  # only update to go to the next sequence if all inputs are valid
                    if (current_sequence_location + 1) < len(self.chat_bot_sequence):
                        self.current_sequence = self.chat_bot_sequence[current_sequence_location + 1]

            elif not temp_dataset[1]:
                # Bot
                self.text_display += f"<div style='color: #acc9e6'>[Bot]: {message}</div> <br />"
                self.chatsText.setText(self.text_display)

            self.userInputText.setText("")

    def selected_text(self):
        self.send_message(False, "Please enter the text which you wish to translate: ")

    def detect_language(self, detect_language):
        self.send_message(False, f"User's input lang is: {detect(detect_language)}")

        self.ask_user_about_lang_pref()  # calling kranti fn

    def ask_user_about_lang_pref(self):
        self.send_message(False, "In which language do you wish to translate?")
        self.send_message(False, "1. English")
        self.send_message(False, "2. Hindi")
        self.send_message(False, "3. Deutsch")
        self.send_message(False, "4. French")

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
