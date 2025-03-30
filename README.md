# QuackHacks2025

## Overview

## Project Structure

```
QuackHacks2025/
├── app.py
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── dependencies.py
├── gemini/
│   ├── __init__.py
│   ├── gemini.py
│   └── prompt.txt
├── indeed_scraper/
│   ├── __init__.py
│   └── indeed_scraper.py
├── routes/
│   ├── __init__.py
│   ├── routers.py
│   ├── gemini_routes.py
│   └── indeed_scraper_routes.py
```

## How to Run

- Create Virtual Environment
``` python -m venv env ```
  - Activate in Windows
  ``` env\Scripts\activate ```
  - Activate in Mac
  ``` source env/bin/activate ```
- Download requirements
``` pip install -r requirements.txt ```