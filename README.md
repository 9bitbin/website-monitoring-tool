# Website Monitoring Tool

A lightweight website uptime monitoring service built with **Python** and **FastAPI**.  
The application periodically checks website availability, logs status changes, and optionally sends real-time alerts to Discord via webhooks.

This project demonstrates backend API design, HTTP monitoring, logging, and environment-based configuration.

---

## Features

- Monitor one or multiple websites for uptime
- Detects **UP / DOWN** status changes
- Periodic health checks (polling-based)
- Persistent logging for audit and review
- Optional Discord notifications via webhook
- Auto-generated interactive API documentation (Swagger UI)

---

## Tech Stack

- **Python 3**
- **FastAPI** — REST API framework
- **Uvicorn** — ASGI application server
- **httpx** — HTTP client for health checks
- **python-dotenv** — environment variable management

---

## Architecture

## Architecture

Client (Browser / API Consumer)
        |
        v
FastAPI Application (app.py)
        |
        +-- /monitor endpoint
        |       +-- Accepts website URLs
        |
        +-- HTTP health checks (httpx)
        |       +-- Periodic polling
        |
        +-- Logging system
        |       +-- Stores uptime history in logs/
        |
        +-- Alert system (optional)
                +-- Discord webhook notifications


⚠️ **Important details**
- Use **three backticks**, not quotes
- Use `text` after the backticks (helps GitHub)
- Do **not indent** the backticks
- Do **not mix Markdown lists inside the diagram**

---

## Why this version works
- Forces monospaced font
- Preserves spacing and alignment
- Prevents Markdown from interpreting `|`, `+`, or `--`
- Renders consistently on GitHub, mobile, and desktop

---

## If you want it even cleaner (optional)
You can replace the diagram entirely with:


## Architecture

The application follows a simple request-driven architecture:

- Client sends requests via browser or API
- FastAPI exposes a `/monitor` endpoint
- HTTP checks are performed using `httpx`
- Results are logged locally
- Optional Discord alerts notify on status changes


  git clone https://github.com/9bitbin/website-monitoring-tool.git
cd website-monitoring-tool



