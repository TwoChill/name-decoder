import importlib.metadata
import pathlib
import re
import sys


def _check_requirements():
    req = pathlib.Path(__file__).parent / "requirements.txt"
    if not req.exists():
        return
    missing = []
    for line in req.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name = re.split(r"[><=!~\[\s]", line)[0]
        try:
            importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            missing.append(line)
    if missing:
        print("Missing packages:")
        for p in missing:
            print(f"  {p}")
        print("\nInstall with: pip install -r requirements.txt")
        input("\nPress Enter to exit...")
        sys.exit(1)


_check_requirements()


import os
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.uix.videoplayer import VideoPlayer
from kivy.clock import Clock
from moviepy.editor import VideoFileClip

# Install ffpyplayer to play videos.
os.environ["KIVY_VIDEO"] = "ffpyplayer"
LOGO = '3.png'

class NameDecoder(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.60, 0.70)
        self.window.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        return self.window

    def on_start(self):
        self.logo = Image(source=LOGO, opacity=0)
        self.window.add_widget(self.logo)
        fade_in_logo = Animation(opacity=1, duration=3)
        fade_in_input_button = Animation(opacity=1, duration=3)

        def on_logo_fade_in_finish(animation, widget):
            fade_in_input_button.start(self.input_box)
            fade_in_input_button.start(self.convert_button)

        fade_in_logo.bind(on_complete=on_logo_fade_in_finish)

        self.input_box = TextInput(multiline=False,
                                   hint_text='Enter your name',
                                   padding=(10, 20),
                                   size_hint=(1, 0.20),
                                   opacity=0
                                   )

        self.convert_button = Button(text='Convert',
                                     size_hint=(1, 0.20),
                                     bold=True,
                                     background_color=("#FC3030"),
                                     background_normal='',
                                     opacity=0
                                     )

        self.convert_button.bind(on_release=self.convert_name)

        self.window.add_widget(self.input_box)
        self.window.add_widget(self.convert_button)

        fade_in_logo.start(self.logo)

    def convert_name(self, _):
        self.window.clear_widgets()

        video_layout = BoxLayout(orientation='vertical')

        video_filename = f"{self.calculate_number(self.input_box.text)}.mp4"
        video_path = os.path.join(os.path.dirname(__file__), video_filename)
        if os.path.exists(video_path):
            video_player = VideoPlayer(source=video_path, state='play')

            def stop_video(dt):
                video_player.state = 'stop'
                self.return_to_previous_screen()

            def get_video_duration(file_path):
                try:
                    clip = VideoFileClip(file_path)
                    duration = clip.duration
                    clip.close()
                    return duration
                except Exception as e:
                    print(f"Error: {e}")
                    return None

            Clock.schedule_once(stop_video, get_video_duration(video_path))

            video_layout.add_widget(video_player)
            self.window.add_widget(video_layout)
        else:
            not_found_video_path = os.path.join(os.path.dirname(__file__), "not_found.mp4")
            if os.path.exists(not_found_video_path):
                video_player = VideoPlayer(source=not_found_video_path, state='play')
                video_layout.add_widget(video_player)
            else:
                label = Label(text=f"Video '{video_filename}' not found.")
                video_layout.add_widget(label)
                self.window.add_widget(video_layout)
                print(f"Video '{video_filename}' not found.")

    def calculate_number(self, name):
        name = name.upper()
        number_mapping = {
            '1': ['A', 'J', 'S'],
            '2': ['B', 'K', 'T'],
            '3': ['C', 'L', 'U'],
            '4': ['D', 'M', 'V'],
            '5': ['E', 'N', 'W'],
            '6': ['F', 'O', 'X'],
            '7': ['G', 'P', 'Y'],
            '8': ['H', 'Q', 'Z'],
            '9': ['I', 'R']
        }

        special_numbers = ['11', '22', '33']

        total = 0

        for letter in name:
            for number, letters in number_mapping.items():
                if letter in letters:
                    total += int(number)
                    break

        while str(total) not in special_numbers and total > 9:
            total = sum(int(digit) for digit in str(total))

        return str(total)

    def return_to_previous_screen(self):
        self.window.clear_widgets()
        self.window.add_widget(self.logo)
        self.input_box.text = ""
        self.window.add_widget(self.input_box)
        self.window.add_widget(self.convert_button)

if __name__ == '__main__':
    NameDecoder().run()
