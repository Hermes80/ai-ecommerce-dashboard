#!/bin/bash
cd /home/ubuntu/ai-ecommerce-dashboard
source venv/bin/activate

# Start token refresher in background (auto-loop)
python3 token_refresh.py &

# Start main AI engine (never stops)
python3 ai_engine.py
