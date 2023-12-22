from flask import Flask, render_template
from flask_socketio import SocketIO
import pygame
import threading
import tkinterweb
import tkinter as tk


app = Flask(__name__)
socket = SocketIO(app=app)

musicMixer = None  # Initialize the global mixer variable

def update_mixer(new_mixer: pygame.mixer):

    global musicMixer  # Reference the global variable
    
    musicMixer = new_mixer
    print("Define Mixer", musicMixer)

def play_music():
    global musicMixer

    print("Play Music")
    print(musicMixer)
    if musicMixer:
        musicMixer.music.unpause()
        print("Playing")

def stop_music():
    global musicMixer
    print("Stop Music")
    print(musicMixer)
    if musicMixer:
        musicMixer.music.pause()
        print("Stopped")

@app.route('/')
def index():
    return render_template('index.html', playing=False)  # Initial playing state is False

@socket.on("playMusic")
def handle_playing():
    play_music()

@socket.on("stopMusic")
def handle_stopping():
    stop_music()

def frame_thread():
    root = tk.Tk()
    root.title("Backgrounder Config")

    print("Thread")

    def create_html_frame():
        frame = tkinterweb.HtmlFrame(root)
        frame.load_website("http://localhost:2010")
        frame.pack(fill="both", expand=True)

    # Schedule the creation of HtmlFrame in the main thread
    root.after(5, create_html_frame)
    root.mainloop()

if __name__ == '__main__':
    frame_thread = threading.Thread(target=frame_thread)
    frame_thread.start()

    
    # Run the Flask app in a separate thread with the built-in development server


    socket.run(app=app, debug=False, port=2010)

    frame_thread.join()
