#!/bin/bash

# GitHub repo URL
REPO_URL="https://github.com/sawaikh/website-traffic-bot.git"

# Get latest PANEL_IP from GitHub
PANEL_IP=$(curl -s https://raw.githubusercontent.com/sawaikh/website-traffic-bot/main/client/config.py | grep PANEL_IP | cut -d '"' -f2)

echo "🌐 Panel IP detected: $PANEL_IP"

# USA Zones to use
ZONES=("us-central1-a" "us-west1-b" "us-east1-c" "us-west2-a" "us-central1-b" "us-east4-a" "us-west1-a" "us-west4-a")

# Create 8 VPS
for i in {1..8}; do
  NAME="bot-vps-$RANDOM"
  ZONE=${ZONES[$((i-1))]}
  echo "🛠️ Creating VPS $NAME in $ZONE..."

  gcloud compute instances create "$NAME" \
    --zone="$ZONE" \
    --machine-type=e2-micro \
    --image-project=ubuntu-os-cloud \
    --image-family=ubuntu-2204-lts \
    --boot-disk-size=15GB \
    --tags=http-server,https-server \
    --metadata=startup-script='
      sudo apt update
      sudo apt install -y git python3-pip curl
      git clone '"$REPO_URL"' /home/bot
      cd /home/bot/bot
      pip install --break-system-packages -r ../server/requirements.txt
      pip install --break-system-packages playwright requests
      playwright install
      echo "PANEL_IP=\"$PANEL_IP\"" > /home/bot/bot/config.py
      nohup python3 bot_agent.py > bot.log 2>&1 &
    '

  sleep 3
done

echo "✅ All VPS setup initiated!"
