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
