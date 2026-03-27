import requests

BACKEND_URL = "http://backend:8000"

def get_prediction(payload):
    response = requests.post(f"{BACKEND_URL}/classify", json=payload)
    return response.json()

# def upload_batch(file):
#     files = {'file': file}
#     response = requests.post(f"{BACKEND_URL}/batch-upload", files=files)
#     return response.json()

def upload_batch(file):
    files = {'file': (file.name, file.getvalue(), 'text/csv')}
    response = requests.post(f"{BACKEND_URL}/batch-upload", files=files)
    
    if response.status_code == 200:
        return response.json()
    else:
        # This will help us see if it's a 400, 422, or 500 error
        raise Exception(f"Server returned {response.status_code}: {response.text}")