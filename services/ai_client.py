import os
import requests
from fastapi import UploadFile

AI_URL = os.getenv("AI_SERVICE_URL", "http://localhost:8000/detect")


def call_ai(file: UploadFile, timeout: int = 10) -> dict:
    """Forward the uploaded file to the AI service and return parsed JSON.

    Expects the AI service to accept multipart form with key 'file'.
    """
    # Ensure file pointer at start
    try:
        file.file.seek(0)
    except Exception:
        pass

    files = {"file": (file.filename, file.file, file.content_type)}
    resp = requests.post(AI_URL, files=files, timeout=timeout)
    resp.raise_for_status()
    return resp.json()

print("Calling AI at:", AI_URL)

