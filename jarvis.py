import tkinter as tk
import speech_recognition as sr
import pyttsx3
import datetime
import os
import webbrowser
import threading
import openai

# ===== SYSTEM CONTROL =====
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc

# ================= OPENAI =================
openai.api_key = "YOUR_OPENAI_API_KEY"

# ================= SPEECH =================
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    status_label.config(text=f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

# ================= VOICE =================
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        status_label.config(text=f"You: {command}")
        return command
    except:
        return ""

# ================= CHATGPT =================
def chatgpt(prompt):
    speak("Processing")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response.choices[0].message.content
    speak(reply)

# ================= VOLUME CONTROL =================
def volume_control(action):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    if action == "up":
        volume.SetMasterVolumeLevelScalar(min(volume.GetMasterVolumeLevelScalar() + 0.1, 1.0), None)
        speak("Volume increased")

    elif action == "down":
        volume.SetMasterVolumeLevelScalar(max(volume.GetMasterVolumeLevelScalar() - 0.1, 0.0), None)
        speak("Volume decreased")

    elif action == "mute":
        volume.SetMute(1, None)
        speak("Volume muted")

# ================= WIFI CONTROL =================
def wifi_control(state):
    if state == "on":
        os.system("netsh interface set interface Wi-Fi enabled")
        speak("WiFi enabled")
    else:
        os.system("netsh interface set interface Wi-Fi disabled")
        speak("WiFi disabled")

# ================= COMMAND HANDLER =================
def process_command(command):

    if "time" in command:
        speak(datetime.datetime.now().strftime("%I:%M %p"))

    elif "volume up" in command:
        volume_control("up")

    elif "volume down" in command:
        volume_control("down")

    elif "mute volume" in command:
        volume_control("mute")

    elif "brightness up" in command:
        sbc.set_brightness(min(sbc.get_brightness()[0] + 10, 100))
        speak("Brightness increased")

    elif "brightness down" in command:
        sbc.set_brightness(max(sbc.get_brightness()[0] - 10, 0))
        speak("Brightness decreased")

    elif "wifi on" in command:
        wifi_control("on")

    elif "wifi off" in command:
        wifi_control("off")

    elif "open chrome" in command:
        os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        speak("Opening Chrome")

    elif "shutdown" in command:
        speak("System shutting down")
        os.system("shutdown /s /t 5")

    elif "exit" in command:
        speak("Goodbye sir")
        root.destroy()

    else:
        chatgpt(command)

# ================= MAIN LOOP =================
def jarvis_loop():
    speak("Jarvis online. Artificial intelligence initialized.")
    while True:
        command = take_command()
        if command:
            process_command(command)

# ================= GUI =================
root = tk.Tk()
root.title("JARVIS HUD AI")
root.geometry("900x550")
root.configure(bg="black")

title = tk.Label(
    root, text="J.A.R.V.I.S.F.O.R.I.L.Y.A.S",
    font=("Orbitron", 36),
    fg="cyan", bg="black"
)
title.pack(pady=20)

status_label = tk.Label(
    root, text="System Online",
    font=("Consolas", 16),
    fg="#00f6ff", bg="black"
)
status_label.pack(pady=10)

canvas = tk.Canvas(root, width=350, height=350, bg="black", highlightthickness=0)
canvas.pack()

canvas.create_oval(20, 20, 330, 330, outline="cyan", width=4)
canvas.create_text(175, 175, text="AI CORE", fill="cyan", font=("Orbitron", 14))

btn = tk.Button(
    root, text="ACTIVATE JARVIS",
    font=("Orbitron", 14),
    bg="black", fg="cyan",
    borderwidth=2,
    command=lambda: threading.Thread(target=jarvis_loop).start()
)
btn.pack(pady=20)

root.mainloop()
