import socket
import speech_recognition as sr

HOST = "127.0.0.1"
RECEIVE_PORT = 6000
SEND_PORT = 6001

s_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_receive.bind((HOST, RECEIVE_PORT))
recognizer = sr.Recognizer()

def recognize_speech(audio_data):
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Error: {str(e)}"

while True:
    message, addr = s_receive.recvfrom(1024)
    #print(f"Connected by {addr}")
    #print(f"Message is {message}")

    file_path = message.decode()
    try:
        with sr.AudioFile(file_path) as audio_file:
            audio = recognizer.record(audio_file)
            recognized_text = recognize_speech(audio)
            print(f"{recognized_text}")

            # Sending data to the server
            s_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s_send.sendto(recognized_text.encode(), (HOST, SEND_PORT))
            s_send.close()
    except FileNotFoundError:
        print("File not found")

s_receive.close()