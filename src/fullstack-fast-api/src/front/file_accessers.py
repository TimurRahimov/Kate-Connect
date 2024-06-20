import os

from fastapi import APIRouter
from starlette.responses import FileResponse

router_files = APIRouter()
FILES_ABS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))
include_folders = [
    "css",
    "fonts",
    "images",
    "js",
    "sounds"
]

custom_filenames = {
    "images": {
        "icon.png": "icon.ico"
    }
}

for folder in include_folders:
    FOLDER_ABS_PATH = os.path.join(FILES_ABS_PATH, folder)
    # print(FOLDER_ABS_PATH, "X")
    for path, dirs, files in os.walk(FOLDER_ABS_PATH):
        path_from_js = path.split('front')[1]
        path_list = []
        path_split = os.path.split(path_from_js)
        while path_split[1] != "":
            path_list.insert(0, path_split[1])
            path_split = os.path.split(path_split[0])
        for file in files:
            custom_filenames_ptr = custom_filenames
            front_filename = file
            for path_folder in path_list + [file]:
                if path_folder in custom_filenames_ptr:
                    if isinstance(custom_filenames_ptr[path_folder], str):
                        front_filename = custom_filenames_ptr[path_folder]
                    else:
                        custom_filenames_ptr = custom_filenames_ptr[path_folder]
                        continue
            router_files.get(f"/{'/'.join(path_list)}/{front_filename}")(
                lambda _file=file, _path_tuple=tuple(path_list):
                FileResponse(os.path.join(FILES_ABS_PATH, *_path_tuple, _file))
            )


# JS
# JS_ABS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "js")
#
# for path, dirs, files in os.walk(JS_ABS_PATH):
#     path_from_js = path.split('front')[1]
#     path_list = []
#     path_split = os.path.split(path_from_js)
#     while path_split[1] != "":
#         path_list.insert(0, path_split[1])
#         path_split = os.path.split(path_split[0])
#     for file in files:
#         router_files.get(f"/{'/'.join(path_list)}/{file}")(
#             lambda _file=file, _path_list=tuple(path_list[1:]):
#             FileResponse(os.path.join(JS_ABS_PATH, *_path_list, _file))
#         )

# router_files.get("/js/script.js")(lambda: FileResponse(JS_PATH + "script.js"))
# router_files.get("/js/observers.js")(lambda: FileResponse(JS_PATH + "observers.js"))
# router_files.get("/js/requests.js")(lambda: FileResponse(JS_PATH + "requests.js"))
# router_files.get("/js/button_handlers.js")(lambda: FileResponse(JS_PATH + "button_handlers.js"))
# router_files.get("/js/input_handlers.js")(lambda: FileResponse(JS_PATH + "input_handlers.js"))
# router_files.get("/js/people.js")(lambda: FileResponse(JS_PATH + "people.js"))
# router_files.get("/js/utils.js")(lambda: FileResponse(JS_PATH + "utils.js"))
# router_files.get("/js/elements_factory.js")(lambda: FileResponse(JS_PATH + "elements_factory.js"))
#
# router_files.get("/js/ws/_stub_async.js")(lambda: FileResponse(JS_PATH + "ws/_stub_async.js"))
# router_files.get("/js/ws/notification_ws.js")(lambda: FileResponse(JS_PATH + "ws/notification_ws.js"))
# router_files.get("/js/ws/online_ws.js")(lambda: FileResponse(JS_PATH + "ws/online_ws.js"))


# CSS
# router_files.get("/css/style.css")(lambda: FileResponse("src/front/css/style.css"))
# router_files.get("/css/kaleidoscope-items.css")(lambda: FileResponse("src/front/css/kaleidoscope-items.css"))
# router_files.get("/css/fonts.css")(lambda: FileResponse("src/front/css/fonts.css"))

# Fonts
# router_files.get("/fonts/hello-january.otf")(lambda: FileResponse("src/front/fonts/hello-january.otf"))

# Photos
# router_files.get("/images/icon.ico")(lambda: FileResponse("src/front/images/icon.png"))
# router_files.get("/images/default_avatar.jpg")(lambda: FileResponse("src/front/images/default_avatar.jpg"))
# router_files.get("/images/gay_fox.jpg")(lambda: FileResponse("src/front/images/gay_fox.jpg"))
# router_files.get("/images/404.png")(lambda: FileResponse("src/front/images/404.png"))
# router_files.get("/images/500.gif")(lambda: FileResponse("src/front/images/500.gif"))
# router_files.get("/images/milk.png")(lambda: FileResponse("src/front/images/milk.png"))

# Sounds
# router_files.get("/sounds/ntf1.wav")(lambda: FileResponse("src/front/data/notification1.wav"))
# router_files.get("/sounds/usb_in.wav")(lambda: FileResponse("src/front/data/usb_in.wav"))
# router_files.get("/sounds/usb_out.wav")(lambda: FileResponse("src/front/data/usb_out.wav"))
