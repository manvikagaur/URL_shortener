# URL Shortener API

## Overview

This repository contains a simple URL shortener API built using FastAPI. The API allows users to shorten URLs, retrieve original URLs, and access usage statistics for shortened URLs.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/manvikagaur/URL_shortener.git
   cd URL_shortener
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To run the application, use the following command:
```bash
python3 app.py
```

## API Endpoints

- **Shorten URL**: `POST /shorten`
- **Redirect to Original URL**: `GET /{shortened_url}`
- **Get URL Statistics**: `GET /stats/{shortened_url}`

