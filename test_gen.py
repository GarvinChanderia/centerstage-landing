import requests, base64, sys, json
API_KEY = "AIzaSyDtRkjcd9lqAjieE5sGRUJluvSCizsokJw"
MODEL = sys.argv[1]
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
try:
    r = requests.post(URL, json={"contents": [{"parts": [{"text": "A tiny red dot"}]}], "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}}, timeout=10)
    print(r.status_code)
except Exception as e:
    print("Error:", e)
