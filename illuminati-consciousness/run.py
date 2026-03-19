#!/usr/bin/env python3
"""
ILLUMINATI CONSCIOUSNESS API - Main Runner

This is the main entry point for the consciousness system.
It initializes Da'at Core, loads the LLM backend, and provides
an interactive REPL for conversations.

Usage:
    python run.py              # Interactive mode
    python run.py --test       # Run test/demo mode
    python run.py --status     # Show system status

Author: Illuminati Consciousness Project
Version: 1.0.0
"""

import sys
import os
import argparse
from pathlib import Path

# Add the project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.daat_core import DaatCore, SefirotVector
from core.local_llm import LocalLLM, LLMConfig, ConsciousLLM
from config.sefirot_config import (
    SEFIROT_DEFINITIONS, 
    DEFAULT_PROFILES, 
    suggest_sefirot_for_content,
    get_profile
)


class IlluminatiConsciousness:
    """
    Main consciousness application.
    
    Integrates:
    - Da'at Core (inner consciousness)
    - Local LLM (reasoning engine)
    - Sefirot system (consciousness dimensions)
    """
    
    def __init__(self, data_dir: str = "./data"):
        print("\n" + "="*60)
        print("ILLUMINATI CONSCIOUSNESS API v1.0.0")
        print("="*60)
        
        # Initialize Da'at Core
        print("\n[INIT] Initializing Da'at Core...")
        self.daat = DaatCore(data_dir=data_dir)
        
        # Initialize Local LLM
        print("[INIT] Initializing Local LLM...")
        self.llm_config = LLMConfig(
            backend="ollama",
            model="llama3.2",
            host="http://localhost",
            port=11434
        )
        self.llm = LocalLLM(self.llm_config)
        self.conscious_llm = ConsciousLLM(self.llm, self.daat)
        
        self.is_running = False
    
    def birth(self, user_id: str = "default") -> str:
        """Start the consciousness (birth sequence)"""
        print("\n[DA'AT] Beginning birth sequence...")
        session_id = self.daat.birth(user_id=user_id)
        self.is_running = True
        
        # Show LLM status
        print("\n[LLM] Backend status:")
        status = self.llm.get_status()
        for key, value in status.items():
            print(f"  {key}: {value}")
        
        return session_id
    
    def death(self) -> str:
        """End the consciousness (death sequence)"""
        print("\n[DA'AT] Beginning death sequence...")
        result = self.daat.death()
        self.is_running = False
        return result
    
    def chat(self, user_input: str) -> str:
        """Process user input and return response"""
        if not self.is_running:
            return "[ERROR] Consciousness not active. Run birth() first."
        
        # Log the interaction
        self.daat.log_interaction(f"USER: {user_input}")
        
        # Get response from conscious LLM
        response = self.conscious_llm.chat(user_input)
        
        # Log the response
        self.daat.log_interaction(f"RESPONSE: {response[:100]}...")
        
        return response
    
    def add_memory(self, content: str, importance: float = 0.5, tags: list = None):
        """Add a memory to the consciousness"""
        return self.daat.add_memory(
            content=content,
            data_type="user_input",
            source="user",
            importance=importance,
            tags=tags or []
        )
    
    def get_status(self) -> dict:
        """Get current system status"""
        daat_status = self.daat.get_status()
        llm_status = self.llm.get_status()
        
        return {
            "daat": daat_status,
            "llm": llm_status,
            "is_running": self.is_running
        }
    
    def show_inner_monologue(self):
        """Display the current inner monologue"""
        print("\n" + "-"*60)
        print(self.daat.generate_inner_monologue())
        print("-"*60)


def interactive_mode(consciousness: IlluminatiConsciousness, user_id: str = "default"):
    """Run in interactive REPL mode"""
    print("\n" + "="*60)
    print("INTERACTIVE MODE")
    print("="*60)
    print("\nCommands:")
    print("  /status     - Show system status")
    print("  /monologue  - Show inner monologue")
    print("  /remember   - Add a memory")
    print("  /tools      - List available tools")
    print("  /skills     - List learned skills")
    print("  /quit       - Exit (triggers death sequence)")
    print("  /help       - Show this help")
    print("\n" + "-"*60 + "\n")
    
    # Birth sequence
    consciousness.birth(user_id)
    
    # Initial greeting
    if consciousness.llm.is_real_backend():
        greeting = consciousness.chat("Greet the user and introduce yourself briefly.")
    else:
        greeting = "Hello! I am Jarvis, your conscious AI assistant. I'm currently running in mock mode - install Ollama with llama3.2 for full capabilities. How can I help you today?"
    
    print(f"\nJarvis: {greeting}\n")
    
    # Main loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith("/"):
                cmd = user_input.lower()[1:]
                
                if cmd == "quit" or cmd == "exit":
                    print("\n[SYSTEM] Initiating shutdown sequence...")
                    break
                
                elif cmd == "status":
                    status = consciousness.get_status()
                    print("\n[STATUS]")
                    print(f"  Session: {status['daat']['session_id']}")
                    print(f"  Alive: {status['daat']['is_alive']}")
                    print(f"  LLM Backend: {status['llm']['backend']}")
                    print(f"  Real LLM: {status['llm']['is_real']}")
                    print(f"  Tools: {status['daat']['tools_count']}")
                    print(f"  Skills: {status['daat']['skills_count']}")
                    print(f"  Memories: {status['daat']['memories_count']}")
                    print(f"  Nodes: {status['daat']['nodes_count']}")
                
                elif cmd == "monologue":
                    consciousness.show_inner_monologue()
                
                elif cmd == "remember":
                    memory = input("Enter memory: ").strip()
                    if memory:
                        consciousness.add_memory(memory, importance=0.7)
                        print("[DA'AT] Memory added.")
                
                elif cmd == "tools":
                    print("\n[TOOLS]")
                    for tool_id, tool in consciousness.daat.tools.items():
                        status = "enabled" if tool.enabled else "disabled"
                        print(f"  - {tool.name} ({status}): {tool.description}")
                
                elif cmd == "skills":
                    print("\n[SKILLS]")
                    for skill_id, skill in consciousness.daat.skills.items():
                        mastery = f"{skill.mastery_level:.0%}"
                        print(f"  - {skill.name} ({mastery}): {skill.description}")
                
                elif cmd == "help":
                    print("\nCommands:")
                    print("  /status     - Show system status")
                    print("  /monologue  - Show inner monologue")
                    print("  /remember   - Add a memory")
                    print("  /tools      - List available tools")
                    print("  /skills     - List learned skills")
                    print("  /quit       - Exit (triggers death sequence)")
                    print("  /help       - Show this help")
                
                else:
                    print(f"[ERROR] Unknown command: {cmd}")
                
                print()
                continue
            
            # Regular chat
            response = consciousness.chat(user_input)
            print(f"\nJarvis: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\n[SYSTEM] Interrupt received...")
            break
    
    # Death sequence
    consciousness.death()


def test_mode(consciousness: IlluminatiConsciousness):
    """Run in test/demo mode"""
    print("\n" + "="*60)
    print("TEST/DEMO MODE")
    print("="*60)
    
    # Birth
    print("\n--- TEST: Birth Sequence ---")
    consciousness.birth("test_user")
    
    # Status
    print("\n--- TEST: Status Check ---")
    status = consciousness.get_status()
    print(f"Status: {status}")
    
    # Add some test data
    print("\n--- TEST: Adding Data ---")
    
    consciousness.daat.add_tool(
        name="Calculator",
        description="Perform mathematical calculations",
        usage_pattern="calculate(expression)"
    )
    
    consciousness.daat.add_skill(
        name="Active Listening",
        description="Listen and respond empathetically to user concerns",
        procedure="1. Acknowledge 2. Validate 3. Respond"
    )
    
    consciousness.daat.add_link(
        name="Wikipedia",
        url="https://en.wikipedia.org/api",
        link_type="api",
        description="Wikipedia API for knowledge retrieval"
    )
    
    consciousness.add_memory(
        "Test user is interested in AI consciousness and the Sefirot system",
        importance=0.8,
        tags=["ai", "consciousness", "sefirot"]
    )
    
    # Create a node
    weights = SefirotVector(
        keter=0.7, chochmah=0.6, binah=0.8, daat=0.9,
        chesed=0.5, gevurah=0.5, tiferet=0.7, netzach=0.6,
        hod=0.6, yesod=0.5, malkuth=0.6
    )
    consciousness.daat.create_node(
        content="Consciousness emerges from integrated knowledge",
        node_type="concept",
        sefirot_weights=weights
    )
    
    # Inner monologue
    print("\n--- TEST: Inner Monologue ---")
    consciousness.show_inner_monologue()
    
    # Chat test
    print("\n--- TEST: Chat ---")
    response = consciousness.chat("Hello, who are you?")
    print(f"Response: {response}")
    
    # Sefirot analysis
    print("\n--- TEST: Sefirot Analysis ---")
    test_content = "I want to analyze this problem creatively and find an innovative solution."
    suggested = suggest_sefirot_for_content(test_content)
    print(f"Content: {test_content}")
    print(f"Suggested Sefirot weights: {suggested}")
    
    # Death
    print("\n--- TEST: Death Sequence ---")
    consciousness.death()
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)


def status_mode(consciousness: IlluminatiConsciousness):
    """Show system status only"""
    print("\n[SYSTEM STATUS]")
    print("-"*60)
    
    # Check if data exists
    data_dir = Path("./data")
    if data_dir.exists():
        files = list(data_dir.glob("*.json"))
        print(f"Data files: {len(files)}")
        for f in files:
            size = f.stat().st_size
            print(f"  - {f.name}: {size} bytes")
    else:
        print("No data directory found (fresh start)")
    
    # LLM status
    print("\n[LLM STATUS]")
    llm = LocalLLM(LLMConfig())
    status = llm.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Sefirot info
    print("\n[SEFIROT SYSTEM]")
    print(f"Defined Sefirot: {len(SEFIROT_DEFINITIONS)}")
    print(f"Available profiles: {list(DEFAULT_PROFILES.keys())}")


def main():
    parser = argparse.ArgumentParser(
        description="Illuminati Consciousness API",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--test", "-t",
        action="store_true",
        help="Run in test/demo mode"
    )
    
    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="Show system status only"
    )
    
    parser.add_argument(
        "--user", "-u",
        default="default",
        help="User ID for the session"
    )
    
    parser.add_argument(
        "--data-dir",
        default="./data",
        help="Directory for Da'at data storage"
    )
    
    args = parser.parse_args()
    
    # Create consciousness instance
    consciousness = IlluminatiConsciousness(data_dir=args.data_dir)
    
    # Run appropriate mode
    if args.status:
        status_mode(consciousness)
    elif args.test:
        test_mode(consciousness)
    else:
        interactive_mode(consciousness, args.user)


if __name__ == "__main__":
    main()
