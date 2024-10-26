from flask import request
from flask_socketio import emit
import wave
import time
import io
import base64
import requests
from pydub import AudioSegment
import numpy as np

from .extensions import socketio

users = {}

@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("user_join")
def handle_user_join(username):
    print(f"User {username} joined!")
    users[username] = request.sid

@socketio.on("new_message")
def handle_new_message(message):
    print(f"New message: {message}")
    username = None 
    for user in users:
        if users[user] == request.sid:
            username = user
    emit("chat", {"message": message, "username": username}, broadcast=True)


# @socketio.on("get_audio")
# def handle_audio(data):
#     # print(data)
#     audio_data = data
#     print(f"Received audio data of length: {len(data)}")
    
#     if audio_data:
#         audio_data = audio_data
#         # print(audio_data.split(','))
#         audio_bytes = io.BytesIO(audio_data)

#         timestamp = int(time.time())
#         filename = f"output_{timestamp}.wav"
    
#         with wave.open(filename, 'wb') as wav_file:
#             print("Kenil")
#             wav_file.setnchannels(1)
#             wav_file.setsampwidth(2)   
#             wav_file.setframerate(44100)  
#             wav_file.writeframes(audio_bytes.read())
        
#         url = "https://4710-34-173-137-208.ngrok-free.app/transcibe"
#         files = {'file': open(filename, 'rb')}
        
#         try:
#             response = requests.post(url, files=files)
#             if response.status_code == 200:
#                 transcription = response.json()  # Assuming the response is JSON
#                 print("Transcription result:", transcription)
                
#                 # Optionally send the transcription back to the client
#                 socketio.emit("transcription_result", transcription)
#             else:
#                 print("Error with API response:", response.status_code, response.text)
#         except Exception as e:
#             print("An error occurred while calling the API:", str(e))
#     else:
#         print("No audio data found in the received data.")

def convert_wav_to_mp3(wav_file_path, mp3_file_path):
    # Load the WAV file
    audio = AudioSegment.from_wav(wav_file_path)
    
    # Export as MP3
    audio.export(mp3_file_path, format='mp3')
    
    print(f"Converted {wav_file_path} to {mp3_file_path}")

# @socketio.on("get_audio")
# def handle_audio(data):
#     print(f"Received audio data of length: {len(data)}")

#     if data:
#         audio_bytes = io.BytesIO(data)  # Create a BytesIO object from the incoming data
#         print(audio_bytes)
#         timestamp = int(time.time())
#         filename = f"output_{timestamp}.wav"

#         try:
#             with wave.open(filename, 'wb') as wav_file:
#                 wav_file.setnchannels(1)  # 1 for mono
#                 wav_file.setsampwidth(2)   # 2 bytes for 16-bit audio
#                 wav_file.setframerate(44100)  # Sample rate
#                 audio_bytes.seek(0)  # Ensure we're at the start of the BytesIO
#                 wav_file.writeframes(audio_bytes.read()) # Write the audio data to the WAV file

#             convert_wav_to_mp3(filename, 'output.mp3')

#             # Call the transcription API
#             url = "https://983a-34-173-137-208.ngrok-free.app/transcribe"
#             with open(filename, 'rb') as f:
#                 files = {'file': f}
#                 print(files)
#                 response = requests.post(url, files=files)
                
#             if response.status_code == 200:
#                 transcription = response.json()  # Assuming the response is JSON
#                 print("Transcription result:", transcription)

#                 # Optionally send the transcription back to the client
#                 socketio.emit("transcription_result", transcription)
#             else:
#                 print("Error with API response:", response.status_code, response.text)

#         except Exception as e:
#             print("An error occurred while processing audio data:", str(e))
#     else:
#         print("No audio data found in the received data.")


@socketio.on("get_audio")
def handle_audio(data):
    print(f"Received audio data of length: {len(data)}")

    if data:
        audio_bytes = io.BytesIO(data)  # Create a BytesIO object from the incoming data
        timestamp = int(time.time())
        filename = f"output_{timestamp}.wav"

        try:
            # Set up WAV file parameters
            with wave.open(filename, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono audio
                wav_file.setsampwidth(2)   # 2 bytes (16 bits) for PCM format
                wav_file.setframerate(44100)  # Sample rate
                audio_bytes.seek(0)  # Ensure we're at the start of the BytesIO

                # Write data in chunks to reduce memory load
                while chunk := audio_bytes.read(1024):
                    wav_file.writeframes(chunk)

            print("WAV file saved successfully:", filename)

            # Convert WAV to MP3 or other processing, as needed
            # Call transcription API
            url = "https://983a-34-173-137-208.ngrok-free.app/transcribe"
            with open(filename, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, files=files)
                
            if response.status_code == 200:
                transcription = response.json()  # Assuming JSON response
                print("Transcription result:", transcription)

                # Send transcription back to the client
                socketio.emit("transcription_result", transcription)
            else:
                print("API response error:", response.status_code, response.text)

        except Exception as e:
            print("Error processing audio data:", str(e))
    else:
        print("No audio data found in the received data.")
    
