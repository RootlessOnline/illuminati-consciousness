#!/bin/bash
# Setup script for Illuminati Consciousness API

echo "============================================================"
echo "ILLUMINATI CONSCIOUSNESS API - Setup"
echo "============================================================"

# Create necessary directories
echo "[SETUP] Creating directories..."
mkdir -p data logs backups tools

# Check Python version
echo "[SETUP] Checking Python version..."
python3 --version

# Install dependencies (minimal - using only stdlib)
echo "[SETUP] Checking dependencies..."
python3 -c "import json, os, time, uuid, hashlib, datetime" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "[SETUP] Core dependencies available (stdlib)"
else
    echo "[SETUP] ERROR: Missing core dependencies"
    exit 1
fi

# Check for Ollama
echo "[SETUP] Checking for Ollama..."
if command -v ollama &> /dev/null; then
    echo "[SETUP] Ollama found: $(ollama --version 2>/dev/null || echo 'version unknown')"
    
    # Check if ollama is running
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "[SETUP] Ollama server is running"
        
        # List available models
        echo "[SETUP] Available models:"
        ollama list 2>/dev/null || echo "  (unable to list models)"
    else
        echo "[SETUP] Ollama server not running. Start with: ollama serve"
        echo "[SETUP] Pull a model with: ollama pull llama3.2"
    fi
else
    echo "[SETUP] Ollama not found."
    echo "[SETUP] Install Ollama for full LLM capabilities:"
    echo "[SETUP]   curl https://ollama.ai/install.sh | sh"
    echo "[SETUP]   ollama pull llama3.2"
    echo "[SETUP] System will run in mock mode without Ollama."
fi

# Test basic functionality
echo ""
echo "[SETUP] Testing basic functionality..."
python3 -c "
import sys
sys.path.insert(0, '.')
from core.daat_core import DaatCore, SefirotVector
from core.local_llm import LocalLLM, LLMConfig

# Quick test
daat = DaatCore('./data')
weights = SefirotVector()
print('Da\\'at Core: OK')
print('Sefirot Vector: OK')

llm = LocalLLM(LLMConfig())
print('Local LLM: OK')
print(f'Backend: {llm.backend_name}')
" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "[SETUP] All core components working!"
else
    echo "[SETUP] WARNING: Some components may have issues"
fi

echo ""
echo "============================================================"
echo "SETUP COMPLETE"
echo "============================================================"
echo ""
echo "Usage:"
echo "  python3 run.py              # Interactive mode"
echo "  python3 run.py --test       # Test/demo mode"
echo "  python3 run.py --status     # Show status"
echo ""
echo "For full LLM capabilities, install Ollama:"
echo "  curl https://ollama.ai/install.sh | sh"
echo "  ollama pull llama3.2"
echo ""
