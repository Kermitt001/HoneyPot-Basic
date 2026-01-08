#!/bin/bash

echo "[*] Building and starting SSH Honeypot..."
docker-compose up -d --build

echo ""
echo "[*] Honeypot is running on port 2222."
echo "[*] Connection example (from another terminal/VM):"
echo "    ssh root@localhost -p 2222"
echo ""
echo "[*] Logs are located at:"
echo "    - JSONL: ./events.jsonl"
echo "    - SQLite: ./honeypot.db"
echo ""
echo "[*] To view logs in real-time:"
echo "    tail -f events.jsonl"
