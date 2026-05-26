[app]

# (str) Title of your application
title = NameDecoder

# (str) Package name
package.name = namedecoder

# (str) Package domain (needed for android/ios packaging)
package.domain = org.twochill

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,mp4

# (str) Application versioning
version = 1.0

# (list) Application requirements
# moviepy is intentionally NOT here: the app reads video duration via Kivy itself.
requirements = python3,kivy,ffpyplayer

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = all

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) The Android archs to build for
android.archs = arm64-v8a

# (bool) Enable AndroidX support.
android.enable_androidx = True

# (bool) allow backup
android.allow_backup = True

# (str) python-for-android branch/tag to use.
# Pinned to a release whose FFmpeg recipe (4.3.1) still ships libavcodec/avfft.h.
# Current p4a builds FFmpeg 8, which removed avfft.h, breaking the ffpyplayer compile.
p4a.branch = v2024.01.21

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
