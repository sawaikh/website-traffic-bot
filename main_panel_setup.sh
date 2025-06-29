#!/bin/bash

# GitHub repo
REPO_URL="https://github.com/sawaikh/yt-smart-bot.git"

echo "📁 Cloning panel backend..."
git clone "$REPO_URL" panel

cd panel/server || exit

echo "📦 Installing dependencies..."
sudo apt update
sudo apt install -y python3-pip git curl

# Fix for externally-managed error
python3 -m pip install --break-system-packages -r requirements.txt
python3 -m pip install --break-system-packages fastapi uvicorn

# Open port 8000
echo "🛡️ Setting firewall rule to allow port 8000..."
gcloud compute firewall-rules create allow-8000 --allow tcp:8000 --target-tags=http-server --quiet || echo "⚠️ Firewall rule may already exist."

# Start backend
echo "🟢 Starting backend server on port 8000..."
nohup python3 main.py > server.log 2>&1 &

echo "✅ Panel backend started!"
