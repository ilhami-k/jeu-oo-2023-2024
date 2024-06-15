import json
import os
from game import *

class SaveSystem:
    def __init__(self, file_extension, save_folder):
        self.file_extension = file_extension
        self.save_folder = save_folder
    
    def save_data(self, data, name):
        data_file_path = self.save_folder + name + self.file_extension
        with open(data_file_path, "w") as data_file:
            json.dump(data, data_file)
    
    def load_data(self, name):
        data_file_path = self.save_folder + name + self.file_extension
        print("Loading data from:", data_file_path)
        try:
            with open(data_file_path, "r") as data_file:
                data = json.load(data_file)
                return data
        except FileNotFoundError or json.decoder.JSONDecodeError:
            print('No save found, Creating a new one.')
            default_data = None
            self.save_data(default_data, name)
            return default_data
    def delete_data(self, name):
        data_file_path = self.save_folder + name + self.file_extension
        if os.path.exists(data_file_path):
            os.remove(data_file_path)
            print(f"Save file {data_file_path} deleted successfully.")
        else:
            print(f"No save file found at {data_file_path}.")
