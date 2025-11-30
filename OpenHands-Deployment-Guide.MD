# 📘 **OpenHands Deployment Guide (Universal Install)**

This guide walks you step-by-step through deploying OpenHands on:

- Windows 10/11 + WSL2  
- Linux  
- Cloud VMs  
- Bare metal workstations  

It installs:

- 🧠 Agent runtime  
- 🐳 Docker sandbox  
- 🌐 Web UI (localhost:3000)  
- 💾 Persistent workspace + conversations  

This guide is written based on a complete working setup.

---

# 🧩 **1. Requirements**

### ✔ Hardware  
- 16 GB RAM minimum  
- 50–150 GB disk  
- Stable internet  

### ✔ Software  
- Python 3.10–3.12  
- Git  
- Docker Engine / Docker Desktop  

---

# 🏗 **2. Windows WSL2 Setup**

```powershell
wsl --install
wsl --set-default-version 2
```

Install **Ubuntu** from Microsoft Store.

Install **Docker Desktop** and enable:

- ✓ Use WSL2 backend  
- ✓ Ubuntu integration  

Restart Docker Desktop.

---

# 📥 **3. Clone OpenHands**

```bash
git clone https://github.com/All-Hands-AI/OpenHands.git
cd OpenHands
```

---

# 🐍 **4. Create Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
```

---

# 📦 **5. Install OpenHands (Editable Mode)**

```bash
pip install -e .
```

Optional:

```bash
pip install -r requirements.txt
pip install -r requirements.dev.txt
```

---

# ⚙️ **6. Create Configuration**

Copy template:

```bash
cp config.template.toml config.toml
```

Edit:

```toml
[core]
debug = true
workspace_base = "/path/to/OpenHands/workspace"
cache_dir = "/path/to/OpenHands/cache"
file_store_path = "/path/to/OpenHands/data"

[sandbox]
type = "docker"
runtime_container_image = "ghcr.io/openhands/runtime:0.61-nikolaik"
user_id = 1000
timeout = 600
use_host_network = false

[agent]
agent_type = "CodeActAgent"
enable_browser = false
```

Browser disabled = fewer errors.

---

# 🐳 **7. Pull Required Docker Images**

```bash
docker pull ghcr.io/openhands/runtime:0.61-nikolaik
docker pull ghcr.io/openhands/agent-server:latest
```

Test Docker:

```bash
docker ps
docker info
```

---

# ▶️ **8. Start OpenHands Backend**

```bash
LLM_DROP_PARAMS=true python3 -m openhands.server --host 0.0.0.0 --port 3000
```

Expected logs:

```
Container started: openhands-runtime-xxxx
Waiting for client to become ready...
```

---

# 🌐 **9. Open the Web UI**

Open:

```
http://localhost:3000
```

You'll see:

- Chat  
- Workspace  
- Terminal  
- File explorer  
- Logs  

---

# 🧪 **10. Validate Runtime**

```bash
docker ps
```

Expected:

```
openhands-runtime-<session>
openhands-worker
```

Check heartbeat:

```bash
curl http://localhost:<PORT>
```

---

# 📁 Folder Structure

```
OpenHands/
├── openhands/              # Backend
├── openhands-ui/           # Frontend
├── workspace/              # AI output
├── cache/                  # Embeddings, LLM cache
├── data/                   # File storage
├── config.toml             # Your settings
└── venv/                   # Python env
```

---

# 🛡 **Troubleshooting**

### ❌ Docker containers not starting
```powershell
wsl --shutdown
Restart Docker Desktop
```

### ❌ JWT or python-jose import errors
```bash
pip install python-jose PyJWT jose
pip install base58
```

### ❌ BrowserGym mismatch  
Set:

```toml
enable_browser = false
```

### ❌ Runtime stuck  
```bash
docker rm -f $(docker ps -aq)
```

---

# 🎉 **Success — OpenHands Is Fully Installed**

You now have:

- Stable runtime sandbox  
- Persistent UI + conversations  
- Reproducible dev environment  
- All components running cleanly  

Feel free to copy this file into:

```
OpenHands/README-OH.md
```

