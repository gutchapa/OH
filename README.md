# OpenHands (OH) Deployment Guide

This repository provides an end-to-end skeleton for deploying the OpenHands backend and agent-server in one shot.

## Prerequisites

- Git
- Docker & Docker Compose
 
- MongoDB (required for cache persistence).  
  To run locally:
  ```bash
  # Install on Ubuntu/Debian
  sudo apt-get update && sudo apt-get install -y mongodb
  sudo systemctl start mongodb
  # or run manually
  mongod --dbpath ~/oh-deployment/data/db
  ```  
  Or via Docker:
  ```bash
  docker run -d --name mongo -p 27017:27017 -v ~/oh-deployment/data/db:/data/db mongo:6.0
  ```
- Pull OpenHands runtime image: `docker pull ghcr.io/openhands/runtime:0.61-nikolaik`
- Pull OpenHands agent-server image: `docker pull ghcr.io/openhands/agent-server:latest`
## Getting Started

1. Clone this repo on your VPS or local machine:

   ```bash
   git clone <this-repo-url> oh-deployment && cd oh-deployment
   ```

2. Copy or update `.env.example` to `.env` with your API keys:

   ```bash
   cp .env.example .env
   # edit .env
   ```

3. Spin up services via Docker Compose:

   ```bash
   docker-compose up --build -d
   ```

4. Verify endpoints:

   - Backend: http://<HOST>:42745/
   - Agent-server: http://<HOST>:5000/health

## Directory Structure

```
oh-deployment/
├── backend/
│   ├── Dockerfile
│   └── requirements.txt
├── agent-server/
│   └── Dockerfile (and related code)
├── config.toml        # Template configuration
├── docker-compose.yml
├── .env.example
└── README.md
```

## Configuration

Edit `config.toml` to adjust:

- server.host & port
- CORS settings
- cache (in-memory & Mongo)
- summarization limits
- agent-server URL

## Local Development

1. Backend:

   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload --host 0.0.0.0 --port 42745
   ```

2. Agent-server:

   ```bash
   cd agent-server
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt  # if exists
   uvicorn main:app --reload --host 0.0.0.0 --port 5000
   ```

## Docker Compose

`docker-compose.yml` orchestrates:

- `backend` service (FastAPI)
- `agent-server` service
- `mongo` service (if `MONGO_URL` points to it)

Run `docker-compose up -d --build` to start.



## Token Costs & Rate Limits

- Model: `gpt-3.5-turbo` @ $0.002/1k tokens
- Summarization reduces token burn by ~90%
- Rate limit: ~3500 tokens/minute (~3 calls/sec)

Happy deploying! 🚀
