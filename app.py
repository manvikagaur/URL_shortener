# Import necessary libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Dict
import hashlib
import base64
import uvicorn
from collections import defaultdict

# Define the data models
class URLRequest(BaseModel):
    original_url: HttpUrl

class URLResponse(BaseModel):
    original_url: HttpUrl
    shortened_url: str

class OriginalURLResponse(BaseModel):
    original_url: HttpUrl

# Initialize FastAPI app
app = FastAPI()

# Data structure to store URL mappings and statistics
url_store: Dict[str, URLResponse] = {}
access_stats: Dict[str, int] = defaultdict(int)

# Helper function to generate a unique shortened URL
def generate_shortened_url(original_url: str) -> str:
    hash_object = hashlib.sha256(original_url.encode())
    base64_hash = base64.urlsafe_b64encode(hash_object.digest()[:6]).decode('utf-8')
    return base64_hash

# Endpoint to shorten a URL
@app.post("/shorten", response_model=URLResponse)
async def shorten_url(request: URLRequest):
    original_url = request.original_url
    shortened_url = generate_shortened_url(original_url)
    
    # Ensure the shortened URL is unique
    while shortened_url in url_store:
        shortened_url = generate_shortened_url(original_url + str(len(shortened_url)))
    
    response_url = f"http://localhost:8000/{shortened_url}"
    url_response = URLResponse(original_url=original_url, shortened_url=response_url)
    url_store[shortened_url] = url_response
    access_stats[shortened_url] = 0
    
    return url_response

# Endpoint to retrieve the original URL
@app.get("/{shortened_url}", response_model=OriginalURLResponse)
async def redirect_to_original(shortened_url: str):
    if shortened_url in url_store:
        url_response = url_store[shortened_url]
        access_stats[shortened_url] += 1
        return OriginalURLResponse(original_url=url_response.original_url)
    else:
        raise HTTPException(status_code=404, detail="URL not found")

# Endpoint to get statistics
@app.get("/stats/{shortened_url}")
async def get_url_stats(shortened_url: str):
    if shortened_url in url_store:
        return {"shortened_url": url_store[shortened_url].shortened_url, "access_count": access_stats[shortened_url]}
    else:
        raise HTTPException(status_code=404, detail="URL not found")

# Main entry point for running the application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, ssl_keyfile="key.pem", ssl_certfile="cert.pem", ssl_keyfile_password="test")
