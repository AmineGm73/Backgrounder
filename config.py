from flask import Flask, render_template
from flask_socketio import SocketIO
import pygame
import threading
import webview
import tkinter as tk
import time
from json_m import *
import sys
import psutil


app = Flask(__name__)
socket = SocketIO(app=app)



@app.route('/')
def index():
    return render_template('index.html', playing=False)  # Initial playing state is False

@socket.on("playMusic")
def handle_playing():
    print("Playing")
    new_data = {
                "current": json_file("config.json", Operation.GET, "track")["current"],
                "next": json_file("config.json", Operation.GET, "track")["next"],
                "previous": json_file("config.json", Operation.GET, "track")["previous"],
                "playing": True,
                "canChange": True
            }
    json_file("config.json", Operation.CHANGE, "track", new_value=new_data)
    

@socket.on("stopMusic")
def handle_stopping():
    print("Stopping")
    new_data = {
                "current": json_file("config.json", Operation.GET, "track")["current"],
                "next": json_file("config.json", Operation.GET, "track")["next"],
                "previous": json_file("config.json", Operation.GET, "track")["previous"],
                "playing": False,
                "canChange": True
            }
    json_file("config.json", Operation.CHANGE, "track", new_value=new_data)
    

def run_flask():
    socket.run(app=app, debug=False, port=2010)


if __name__ == '__main__':
    
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    time.sleep(1)

    #webview.create_window('Backgrounder Config', 'http://localhost:2010')

    #webview.start()
    
    flask_thread.join()

    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == "Backgrounder Config":
            proc.kill()

    
    
    sys.exit()

    # Run the Flask app in a separate thread with the built-in development server


    
