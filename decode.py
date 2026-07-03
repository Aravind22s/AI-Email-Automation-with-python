import base64
import os


with open("config/credentials.json", "rb") as f:
    print(base64.b64encode(f.read()).decode())