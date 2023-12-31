import pygame
import os
import random
import time
import keyboard
import subprocess
from json_m import Operation, json_file
import sys
import eyed3
from PIL import Image
from io import BytesIO
import psutil
import os

# Initialize Pygame
pygame.init()

# Create a Pygame mixer
pygame.mixer.init()


playing = json_file("config.json", Operation.GET, "track")["playing"]
can_stop = False


def extract_cover_image(mp3_file_path, output_image_path):
    audiofile = eyed3.load(mp3_file_path)

    if audiofile.tag and audiofile.tag.frame_set:
        # Get the first image frame from the tag
        image_frame = audiofile.tag.frame_set.get(b'APIC', None)

        if image_frame:
            # Extract the image data
            image_data = image_frame[0].image_data

            # Convert the image data to a BytesIO object
            image_io = BytesIO(image_data)

            # Open the image using PIL
            image = Image.open(image_io)

            # Save the image to a file
            image.save(output_image_path, format="PNG")

            print(f"Cover image extracted and saved to: {output_image_path}")
        else:
            print("No cover image found in the MP3 file.")
    else:
        print("No tag information found in the MP3 file.")


def load_sounds_from_folder(folder_path):
    sounds = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.mp3') and file_name.startswith("Random Other Key"):
            file_path = os.path.join(folder_path, file_name)
            sound = pygame.mixer.Sound(file_path)
            sounds.append(sound)
    return sounds

def play_meditation_music(music_folder, enter_key_press_sound, other_key_press_sounds):
    global playing
    global can_stop

    # Get a list of music files in the specified folder
    music_files = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]

    if not music_files:
        print("No MP3 files found in the specified folder.")
        return

    # Start playing from a random file
    current_index = random.randint(0, len(music_files) - 1)
    current_music = os.path.join(music_folder, music_files[current_index])
    pygame.mixer.music.load(current_music)

    # Set up a custom event to detect the end of a track
    MUSIC_END = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(MUSIC_END)

    # Load the key press sounds
    enter_key_press_sound = pygame.mixer.Sound(enter_key_press_sound)
    other_key_press_sounds = load_sounds_from_folder(other_key_press_sounds)

    # Play the first track
    print(f"Playing : {music_files[current_index]}")
    pygame.mixer.music.play()
    playing = True
    # Update the mixer in the config module
    

    # Set the initial volume (between 0.0 and 1.0)
    volume = 0.5
    pygame.mixer.music.set_volume(volume)

    # Keep the script running to allow playback

    json_file("config.json", Operation.CHANGE, "track", {
                    "current": music_files[current_index],
                    "next": music_files[current_index + 1],
                    "previous": music_files[current_index - 1],
                    "playing": playing,
                    "canChange": can_stop
                })
    is_up = True

    extract_cover_image("music\\"+music_files[current_index], "music\\cover.png")

    #update_mixer(pygame.mixer.music)
    while True:
        track_dict = json_file("config.json", Operation.GETALL)
        time.sleep(0.01)
        playing = json_file("config.json", Operation.GETALL)["track"]["playing"]
        can_stop = json_file("config.json", Operation.GETALL)["track"]["canChange"]

        if playing == False and can_stop == True and pygame.mixer.music.get_busy() == True:
            pygame.mixer.music.pause()
            can_stop = False
            new_value = {
                "current": music_files[current_index],
                "next": music_files[current_index + 1],
                "previous": music_files[current_index - 1],
                "playing": playing,
                "canChange": can_stop
            }
            json_file("config.json", Operation.CHANGE, "track", new_value)
        elif playing and can_stop and not pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
            can_stop = False
            new_value = {
                "current": music_files[current_index],
                "next": music_files[current_index + 1],
                "previous": music_files[current_index - 1],
                "playing": playing,
                "canChange": can_stop
            }
            json_file("config.json", Operation.CHANGE, "track", new_value)


        pressed_keys = list(keyboard._pressed_events)
        for event in pygame.event.get():
            if event.type == MUSIC_END:
                # Switch to the next track
                json_file("config.json", Operation.CHANGE, "track", {
                    "current": music_files[current_index],
                    "next": music_files[current_index + 1],
                    "previous": music_files[current_index - 1],
                    "playing": playing,
                    "canChange": can_stop
                })
                current_index = (current_index + 1) % len(music_files)
                current_music = os.path.join(music_folder, music_files[current_index])
                print(f"Playing : {music_files[current_index]}")
                pygame.mixer.music.load(current_music)
                
                pygame.mixer.music.play()
                playing = True
                extract_cover_image("music\\"+music_files[current_index], "music\\cover.png")
                #update_mixer(pygame.mixer.music)
        if len(pressed_keys) == 0:
            is_up = True

        # Check for key pressesfg
        

        for key in pressed_keys:
            if key == 28 and is_up:
                pygame.mixer.Sound.set_volume(enter_key_press_sound, 0.4)
                enter_key_press_sound.play()
                time.sleep(0.1)  # Optional delay to avoid rapid key presses
                is_up = False
            elif key == 14 and is_up:
                pygame.mixer.Sound.set_volume(enter_key_press_sound, 0.2)
                enter_key_press_sound.play()
                time.sleep(0.15)

            elif is_up:
                # Play a random sound from the other key press sounds
                pygame.mixer.Sound.set_volume(enter_key_press_sound, 0.2)
                random_sound = random.choice(other_key_press_sounds)
                random_sound.play()  # Optional delay to avoid rapid key presses
                is_up = False

        # Adjust volume with arrow keys
        if keyboard.is_pressed('w') and keyboard.is_pressed("shift") and keyboard.is_pressed("alt"):
            volume = min(1.5, volume + 0.1)
            pygame.mixer.music.set_volume(volume)
            print(f"Volume increased to {volume}")
            time.sleep(0.07)

        if keyboard.is_pressed('s') and keyboard.is_pressed("shift") and keyboard.is_pressed("alt"):
            volume = max(0.0, volume - 0.1)
            pygame.mixer.music.set_volume(volume)
            print(f"Volume decreased to {volume}")
            time.sleep(0.07)
            # Adjust the sleep duration as needed

# Replace 'path/to/your/meditation_music' with the actual path to your music folder
# Replace 'path/to/enter_key_press_sound.wav' with the actual path to your Enter key press sound file
# Replace 'path/to/other_key_press_sounds' with the actual path to the folder containing other key press sound files
music_folder = f'{os.path.dirname(os.path.abspath(__file__))}\music'
enter_key_press_sound = f'{os.path.dirname(os.path.abspath(__file__))}\effects\Enter Key Sound.mp3'
other_key_press_sounds_folder = f'{os.path.dirname(os.path.abspath(__file__))}\effects'

subprocess.Popen([json_file("config.json", Operation.GET, "app")["python"],json_file("config.json", Operation.GET, "app")["config_script_path"]])
play_meditation_music(music_folder, enter_key_press_sound, other_key_press_sounds_folder)
for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == "Backgrounder Config":
            proc.kill()

os.kill()
sys.exit()