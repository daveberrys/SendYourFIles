import requests
import os

def catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    with open(file_path, 'rb') as f:
        files = {'fileToUpload': f}
        data = {'reqtype': 'fileupload'}
        response = requests.post(url, data=data, files=files)
        return response.text

def litterbox(file_path, duration="1h"):
    url = "https://litterbox.catbox.moe/resources/internals/api.php"
    with open(file_path, 'rb') as f:
        files = {'fileToUpload': f}
        data = {'reqtype': 'fileupload', 'time': duration}
        response = requests.post(url, data=data, files=files)
        return response.text
    
def buzzheavier(file_path):
    filename = os.path.basename(file_path)
    url = f"https://w.buzzheavier.com/{filename}"
    with open(file_path, 'rb') as f:
        response = requests.put(url, data=f)
        return response.text