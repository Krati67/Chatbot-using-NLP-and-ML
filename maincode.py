from langdetect import detect
from google_trans_new import google_translator
import speech_recognition as sr
from transformers import pipeline
import requests

#pip install langdetect, google_trans_new, speechrecognition, requests, transformers torch senterpiece.

t = google_translator()

# this function will take users choice on input text or speech
def choice_of_input():
    print('What type of input will you choose?')
    print('1. Text')
    print('2. Speech')
    choice_of_input.human_text = input()
    choice_of_input.human_text = choice_of_input.human_text.lower()
    print(choice_of_input.human_text)

# this function will take user's language prefernce and convert it into lower
def ask_user_about_lang_pref():
    print("In which language do you wish to translate?")
    print("1. English")
    print("2. Hindi")
    print("3. Deutsch")
    print("4. French")
    ask_user_about_lang_pref.pref = input("Enter: ")
    ask_user_about_lang_pref.pref = ask_user_about_lang_pref.pref.lower()

#this function will ask whether the user wants to proceed further or not
def to_continue_further():
    print("Do you wish to convert it into any other language?")
    print("Y/N")
    yes_no = input()
    yes_no = yes_no.lower()
    if yes_no == 'y':
        main_function()
        # choice_of_input()
    elif yes_no == 'n':
        print("Thank you! ")
    else:
        print("Sorry, I can't understand")

#this function converts audio into text by using speech recognizing library
def convert_audio_to_text_detect():
    r1 = sr.Recognizer()
    with sr.Microphone() as source:
        print('SPEAK NOW...')
        audio = r1.listen(source)
        try:
            convert_audio_to_text_detect.get = r1.recognize_google(audio)
            print(convert_audio_to_text_detect.get)
            print(detect(convert_audio_to_text_detect.get))
        except sr.UnkownValueError:
            print('error')
        except sr.RequestError as e:
            print('failed'.format(e))

#extra feature added to analyse the sentiments of the text (to tell whether the sentence is negative or positive)
def analyse_sentiments():
    print("Do you want the sentiment analysis of this sentenc?")
    print("Y/N")
    y_n = input()
    y_n = y_n.lower()
    if y_n == 'y':
        my_model = pipeline('sentiment-analysis')
        print(my_model(main_function.detect_language)) #text to be entered
        #how to use the detect_language variable in this function????
        #
    elif y_n == 'n':
        print("Thank you! ")
        to_continue_further()
    else:
        print("Sorry, I can't understand")

# ================================================MAIN FUNCTION =======================================================

def main_function():
    choice_of_input()
    if choice_of_input.human_text == 'text':
        detect_language = input("PLease enter the text which you wish to translate: ")
        print("Language: ", detect(detect_language))
        ask_user_about_lang_pref()
        if ask_user_about_lang_pref.pref == 'english':
            print(t.translate(detect_language, lang_tgt='en'))
            analyse_sentiments() #ADDED FOR TRIAL PURPOSES ONLY
            # to_continue_further()
        elif ask_user_about_lang_pref.pref == 'hindi':
            print(t.translate(detect_language, lang_tgt='hi'))
            to_continue_further()
        elif ask_user_about_lang_pref.pref == 'deutsch':
            print(t.translate(detect_language, lang_tgt='de'))
            to_continue_further()
        elif ask_user_about_lang_pref.pref == 'french':
            print(t.translate(detect_language, lang_tgt='fr'))
            to_continue_further()
        else:
            print('Try Again!')
    elif choice_of_input.human_text == 'speech':
        convert_audio_to_text_detect()
        ask_user_about_lang_pref()
        if ask_user_about_lang_pref.pref == 'english':
            print(t.translate(convert_audio_to_text_detect.get, lang_tgt='en'))
            to_continue_further()
        elif ask_user_about_lang_pref.pref == 'hindi':
            print(t.translate(convert_audio_to_text_detect.get, lang_tgt='hi'))
            to_continue_further()
        elif ask_user_about_lang_pref.pref == 'deutsch':
            print(t.translate(convert_audio_to_text_detect.get, lang_tgt='de'))
            to_continue_further()
        elif ask_user_about_lang_pref.pref == 'french':
            print(t.translate(convert_audio_to_text_detect.get, lang_tgt='fr'))
            to_continue_further()
        else:
            print('Try Again!')
    else:
        print("I am afraid, I can't help you!")

print('Hey I am Kratzz.')
print('I am your personal translator.')
main_function()


