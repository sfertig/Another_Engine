import os
import sys

def get_path() -> str: #path of project(s) storage
    """Stores save data in C:/Users/<Username>/.AnotherEngine_projects"""
    user_home = os.path.expanduser("~")
    return os.path.join(user_home, ".AnotherEngine_projects")

def init_save_dir(): 
    """creates the save directory if it doesn't exist"""
    path = get_path()
    exists = os.path.exists(path)
    
    # 1. Safe folder creation
    os.makedirs(path, exist_ok=True)

    return exists

DEFAULTPROJECT = {
  "project_name": "__name__",
  "version": "0.0.1",
  "export": {
    "windows_windowed": True
  },
  "window": {
    "width": 640,
    "height": 360,
    "fullscreen": False,
    "fps": 60,
    "bg_color": [0, 0, 255],
    "title": "__pyscene_default__"
  },
  "include_splashscreen": True,
  "main_scene": "",
  "dirty": True,
  "changed": True,
  "lastOpen": []
}

DEFAULTSCENE = {
    "name": "__name__",
    "objects": {},
    "imports": [],
    "dirty": True,
    "changed": True
}

DEFAULTOBJECT = {
    "name": "__name__",
    "imports": [],
    "dirty": True,
    "changed": True
}
