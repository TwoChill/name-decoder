import importlib.metadata
import os
import pathlib
import re
import sys
import traceback

# Kivy picks its video provider the first time kivy.core.video is imported, so
# this has to be set before any kivy import below — not after them.
os.environ["KIVY_VIDEO"] = "ffpyplayer"

# SDL2's AAudio backend null-derefs in aaudio_DetectBrokenPlayState during the
# event pump the moment audio starts, hard-crashing the process on Android 13+
# (confirmed via logcat: SIGSEGV in libSDL2 on a Galaxy S24 / Android 16). Force
# the older, stable OpenSL ES backend on Android; irrelevant on desktop.
if hasattr(sys, "getandroidapilevel"):
    os.environ["SDL_AUDIODRIVER"] = "openslES"


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


# On Android the app is packaged by Buildozer (no pip), and input() would hang — skip the check there.
if not hasattr(sys, "getandroidapilevel"):
    _check_requirements()


from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.uix.video import Video
from kivy.uix.videoplayer import VideoPlayer
from kivy.clock import Clock
from kivy.utils import platform
from kivy.logger import Logger
from kivy.core.window import Window

APP_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO = '3.png'

class NameDecoder(App):
    def build(self):
        # Pan the layout up when the soft keyboard opens so it never covers the
        # name field (Android); no-op on desktop.
        Window.softinput_mode = 'below_target'
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

        video_filename = f"{self.calculate_number(self.input_box.text)}.mp4"
        video_path = os.path.join(APP_DIR, "videos", video_filename)
        if not os.path.exists(video_path):
            fallback = os.path.join(APP_DIR, "videos", "not_found.mp4")
            video_path = fallback if os.path.exists(fallback) else None

        if video_path is None:
            self.window.add_widget(Label(text=f"Video '{video_filename}' not found."))
            print(f"Video '{video_filename}' not found.")
            return

        # The heavyweight VideoPlayer (controls + thumbnail) is unreliable on Android;
        # the plain Video widget is the dependable front-end to the same provider.
        # On Android the video is added straight to the Window so it bypasses the
        # centered 0.6x0.7 root layout and fills the screen. Desktop keeps the
        # VideoPlayer inside the window so its behaviour is unchanged.
        try:
            if platform == 'android':
                video_player = Video(source=video_path, state='play', allow_stretch=True)
                Window.add_widget(video_player)
            else:
                video_player = VideoPlayer(source=video_path, state='play')
                video_layout = BoxLayout(orientation='vertical')
                video_layout.add_widget(video_player)
                self.window.add_widget(video_layout)
            self._finished = False

            def finish_video(*_):
                if self._finished:
                    return
                self._finished = True
                Clock.unschedule(check_end)
                video_player.state = 'stop'
                if platform == 'android':
                    Window.remove_widget(video_player)
                    self.return_to_previous_screen()
                else:
                    self.stop()

            def check_end(_dt):
                dur = video_player.duration
                if dur and dur > 0 and video_player.position >= dur - 0.3:
                    finish_video()

            def watchdog(_dt):
                # Nothing decoding after the grace period: show why instead of a black screen.
                if self._finished or (video_player.duration and video_player.duration > 0):
                    return
                if platform == 'android':
                    Window.remove_widget(video_player)
                self._show_error(self.window,
                                 f"Video did not start.\nstate={video_player.state}\n{video_path}")

            Clock.schedule_interval(check_end, 0.25)
            Clock.schedule_once(watchdog, 8)
        except Exception:
            Logger.exception("NameDecoder: video setup failed")
            self._show_error(self.window, traceback.format_exc())

    def _show_error(self, layout, message):
        label = Label(text=message, halign='left', valign='top')
        label.bind(size=lambda widget, *_: setattr(widget, 'text_size', widget.size))
        layout.add_widget(label)

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
