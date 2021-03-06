import sys
import os
from PyQt5 import uic
from PyQt5 import QtWidgets as Qtw
from PyQt5 import QtGui as Qtg
from PyQt5 import QtCore as Qtc

# code functions
import time
from langdetect import detect
from google_trans_new import google_translator
import speech_recognition as sr
from transformers import pipeline
from iso639 import languages

#before language detection in order to enforce consistent results use DetectorFactory
from langdetect import DetectorFactory
DetectorFactory.seed = 0

# Code to show error, if the app crashes
import cgitb
cgitb.enable(format='text')

#Dependencies to add in the virtual env
# pip install langdetect, google_trans_new, speechrecognition, requests, transformers torch sentencepiece, pyaudio, iso-639.

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
        self.chat_bot_sequence = ["text_or_speech", "detect_language", "translate_to_lang", "analyse_continue", "continue_restart"]

        # we use current sequence to update to the next sequence
        self.current_sequence = self.chat_bot_sequence[0]
        self.user_text = ""
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
        print("Currently at: [choice of input]", self.current_sequence)

    def send_message(self, message_from, message="", show_color=False):
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
                    human_text = human_text.lower()

                    if human_text == "text":  # converting to lower case
                        self.selected_text()

                    elif human_text == "speech":  # converting to lower case
                        self.convert_audio_to_text_detect()
                        self.current_sequence = "from_speech"

                    else:
                        # will update the correct_input var so that the program will continue only if there is a valid input
                        correct_input = False
                        self.send_message(False, "Please enter either Text or Speech alone.")

                if self.current_sequence == "detect_language":
                    language_to_detect = self.userInputText.toPlainText()
                    self.detect_language(language_to_detect)

                if self.current_sequence == "translate_to_lang":
                    translate_to = self.userInputText.toPlainText()
                    verify_var = self.translate_text_to_(translate_to)
                    if not verify_var:
                        correct_input = False

                if self.current_sequence == "analyse_continue":
                    continue_analysis = self.userInputText.toPlainText()
                    verify_var = self.analyse_continue(continue_analysis)

                    if not verify_var:
                        correct_input = False

                if self.current_sequence == "continue_restart":
                    continue_restart = self.userInputText.toPlainText()
                    verify_var = self.restart_continued(continue_restart)

                    if not verify_var:
                        correct_input = False

                if self.current_sequence == "from_speech":
                    translate_to = self.userInputText.toPlainText()
                    verify_var = self.translate_text_to_(translate_to)
                    print("trying " , translate_to)

                    if not verify_var:
                        correct_input = False

                try:
                    current_sequence_location = int(self.chat_bot_sequence.index(f"{self.current_sequence}"))

                except ValueError:
                    current_sequence_location = 2

                print(correct_input)

                if correct_input:  # only update to go to the next sequence if all inputs are valid
                    print("current sequence: ", self.current_sequence)
                    print(f"Current Sequence Location{(current_sequence_location + 1)}, Len of Sequence{len(self.chat_bot_sequence)}")
                    if (current_sequence_location + 1) < len(self.chat_bot_sequence):
                        self.current_sequence = self.chat_bot_sequence[current_sequence_location + 1]
                        print(" updated current sequence: ", self.current_sequence)
                    elif (current_sequence_location + 1) >= len(self.chat_bot_sequence):
                        self.current_sequence = self.chat_bot_sequence[0]

            elif not temp_dataset[1]:
                # Bot
                if show_color:
                    self.text_display += f"<div style='color: #ffa500'>[You]: {message}</div> <br />"
                    self.chatsText.setText(self.text_display)
                else:
                    self.text_display += f"<div style='color: #acc9e6'>[Bot]: {message}</div> <br />"
                    self.chatsText.setText(self.text_display)

            self.userInputText.setText("")

    def selected_text(self):
        self.send_message(False, "Please enter the text which you wish to translate: ")

    # funtion to detect the language used by the user
    def detect_language(self, detect_language):
        self.user_text = detect_language
        #store the value of detected language
        to_get_fullform = detect(detect_language)
        full_form = languages.get(alpha2=to_get_fullform)
        self.send_message(False, f"User's input lang is: {full_form.name}")
        self.ask_user_about_lang_pref()

    # function for printing statement for preferred language
    def ask_user_about_lang_pref(self):
        self.send_message(False, "In which language do you wish to translate?")
        self.send_message(False, "1. English")
        self.send_message(False, "2. Hindi")
        self.send_message(False, "3. Deutsch")
        self.send_message(False, "4. French")

    #function to translate the user's text into the chosen language
    def translate_text_to_(self, user_lang):
        correct_input = True
        t = google_translator()
        user_lang = user_lang.lower()
        if user_lang == 'english':
            self.send_message(False, t.translate(self.user_text, lang_tgt='en'))
            self.analyse_sentiments()  # ADDED FOR TRIAL PURPOSES ONLY

        elif user_lang == 'hindi':
            self.send_message(False, t.translate(self.user_text, lang_tgt='hi'))
            self.analyse_sentiments()

        elif user_lang == 'deutsch':
            self.send_message(False, t.translate(self.user_text, lang_tgt='de'))
            self.analyse_sentiments()

        elif user_lang == 'french':
            self.send_message(False, t.translate(self.user_text, lang_tgt='fr'))
            self.analyse_sentiments()

        else:
            correct_input = False
            #self.send_message(False, 'Try Again!')

        return correct_input

    # function to analyse sentiments of the user (just the print statements)
    def analyse_sentiments(self):
        self.send_message(False, "Do you want the sentiment analysis of this sentence?")
        self.send_message(False, "Y/N")

    # cont.. of sentiment analysis using transformers
    def analyse_continue(self, user_choice):
        correct_input = True
        user_choice = user_choice.lower()

        if user_choice == 'y':
            my_model = pipeline('sentiment-analysis')
            # coverting user text into english first
            t = google_translator()
            temp_text = t.translate(self.user_text, lang_tgt='en')
            temp_var = my_model(temp_text)

            # temp_var = my_model(self.user_text)
            temp_var = temp_var[0]
            temp_score = float(temp_var['score'])
            temp_score *= 100
            temp_score = round(temp_score, 1)
            self.send_message(False, f"The analysis is {temp_var['label']} with score of {temp_score}%")
            self.restart_program()

        elif user_choice == 'n':
            self.send_message(False, "Thank you! ")
            self.restart_program()

        else:
            correct_input = False
            self.send_message(False, "Sorry, I can't understand if I should continue analysing")

        return correct_input

    # to continue further...
    def restart_program(self):
        self.send_message(False, "Do you wish to continue further??")
        self.send_message(False, "Y/N")

    # restart continuation
    def restart_continued(self, user_choice):
        correct_input = True
        user_choice = user_choice.lower()

        if user_choice == 'y':
            self.choice_of_input()

        elif user_choice == 'n':
            self.send_message(False, "Thank you! ")
            time.sleep(2)
            self.close()

        else:
            correct_input = False
            self.send_message(False, "Sorry, I can't understand if I should restart")

        return correct_input

    # function to convert audio into text
    def convert_audio_to_text_detect(self):
        print("TESTING FOR SPEECH TO SEE IF FN IS CALLED")
        self.send_message(False, 'SPEAK NOW...')
        self.send_message(False, 'detecting...')

        r1 = sr.Recognizer()
        with sr.Microphone() as source:
            print("reached here...")
            r1.pause_threshold = 1
            r1.adjust_for_ambient_noise(source)
            audio = r1.listen(source, phrase_time_limit=6)

            try:
                user_audio = r1.recognize_google(audio)
                # self.send_message(f"<div style='color: #ffa500'>[You]:</div>", user_audio)
                self.send_message(False, user_audio, show_color=True)
                self.detect_language(user_audio)

            except sr.UnkownValueError:
                self.send_message(False, 'error')

            except sr.RequestError as e:
                self.send_message(False, 'failed')

            else:
                # self.send_message(False, temp_audio)
                print("correct")

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