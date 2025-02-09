import os

ROOT_FOLDER = os.path.dirname(os.path.dirname(__file__))
CONTENT_FOLDER = os.path.join(ROOT_FOLDER, "vr-resources")
MEDIA_FOLDER = os.path.join(CONTENT_FOLDER, "media")
PATTERN_FOLDER = os.path.join(CONTENT_FOLDER, "pattern")
AUDIO_FOLDER = os.path.join(CONTENT_FOLDER, "audio")
TEMPLATE_FOLDER = os.path.join(ROOT_FOLDER, "backend", "templates")
JS_FOLDER = os.path.join(ROOT_FOLDER, "front", "js")

folders = (
    ROOT_FOLDER,
    CONTENT_FOLDER,
    MEDIA_FOLDER,
    PATTERN_FOLDER,
    AUDIO_FOLDER,
    TEMPLATE_FOLDER,
    JS_FOLDER,
)

for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created directory: {folder}")
    else:
        print(f"Directory already exists: {folder}")
