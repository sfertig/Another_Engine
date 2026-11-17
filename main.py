import pygame
from src.utils import init_save_dir, get_path
from src.Net import Net
from src.projectManager.Manager import ProjectManager
from src.utils.input import Keys

if __name__ == "__main__":

    print("Loading engine...")

    Net.save_dir = get_path()

    if init_save_dir(): print("Save directory already exists.")
    else: print("Save directory created.")

    print("Engine loaded successfully.")
    Keys._add_net(Net)
    ProjectManager().Run()


