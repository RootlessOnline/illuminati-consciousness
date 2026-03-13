#!/usr/bin/env python3
"""
LOCAL LLM INTERFACE - Independence from External APIs

This module provides a unified interface for local LLM backends,
enabling the Illuminati Consciousness API to run offline and
independently from external services.

Supported Backends:
- Ollama (primary recommendation)
- llama.cpp (via HTTP server)
- PicoClaw (ultra-lightweight)
- AirLLM (layer offloading)
- vLLM (high-performance)
- LM Studio (GUI-based)

The interface abstracts away backend differences, allowing the
consciousness system to seamlessly use whichever local LLM is available.
"""

import json
import os
import subprocess
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, Generator
from pathlib import Path
import urllib.request
import urllib.error

# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class LLMConfig:
    """Configuration for a local LLM backend"""
    backend: str = "ollama"
    model: str = "llama3.2"
    host: str = "http://localhost"
    port: int = 11434
    timeout: int = 120
    max_tokens: int = 2048
    temperature: float = 0.7
    top_p: float = 0.9
    context_window: int = 4096
    gpu_layers: int = -1  # -1 for all layers
    threads: int = 4
    verbose: bool = False
    
    def get_base_url(self) -> str:
        return f"{self.host}:{self.port}"


# ============================================================================
# RESPONSE TYPES
# ============================================================================

@dataclass
class LLMResponse:
    """Standardized response from any LLM backend"""
    content: str
    model: str
    backend: str
    tokens_generated: int = 0
    tokens_prompt: int = 0
    duration_ms: float = 0
    finish_reason: str = "stop"
    raw_response: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "content": self.content,
            "model": self.model,
            "backend": self.backend,
            "tokens_generated": self.tokens_generated,
            "tokens_prompt": self.tokens_prompt,
            "duration_ms": self.duration_ms,
            "finish_reason": self.finish_reason
        }


# ============================================================================
# BASE LLM INTERFACE
# ============================================================================

class BaseLLMBackend(ABC):
    """Abstract base class for LLM backends"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.is_available = False
        self.last_error: Optional[str] = None
    
    @abstractmethod
    def check_availability(self) -> bool:
        """Check if the backend is available"""
        pass
    
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = None, 
                 max_tokens: int = None, temperature: float = None) -> LLMResponse:
        """Generate a completion"""
        pass
    
    @abstractmethod
    def generate_stream(self, prompt: str, system_prompt: str = None,
                        max_tokens: int = None, temperature: float = None) -> Generator[str, None, None]:
        """Generate a streaming completion"""
        pass
    
    @abstractmethod
    def list_models(self) -> List[str]:
        """List available models"""
        pass
    
    def _make_http_request(self, url: str, data: Dict, headers: Dict = None) -> Dict:
        """Make an HTTP request and return JSON response"""
        headers = headers or {"Content-Type": "application/json"}
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req, timeout=self.config.timeout) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.URLError as e:
            self.last_error = str(e)
            raise


# ============================================================================
# OLLAMA BACKEND (Primary)
# ============================================================================

class OllamaBackend(BaseLLMBackend):
    """
    Ollama backend - The recommended local LLM solution.
    
    Ollama provides easy model management and a clean API.
    Install: curl https://ollama.ai/install.sh | sh
    Run: ollama serve
    Pull model: ollama pull llama3.2
    """
    
    def check_availability(self) -> bool:
        """Check if Ollama is running"""
        try:
            url = f"{self.config.get_base_url()}/api/tags"
            req = urllib.request.Request(url, method='GET')
            with urllib.request.urlopen(req, timeout=5) as response:
                self.is_available = response.status == 200
                return self.is_available
        except:
            self.is_available = False
            return False
    
    def generate(self, prompt: str, system_prompt: str = None,
                 max_tokens: int = None, temperature: float = None) -> LLMResponse:
        """Generate completion using Ollama API"""
        start_time = time.time()
        
        data = {
            "model": self.config.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens or self.config.max_tokens,
                "temperature": temperature or self.config.temperature,
                "top_p": self.config.top_p,
                "num_ctx": self.config.context_window
            }
        }
        
        if system_prompt:
            data["system"] = system_prompt
        
        url = f"{self.config.get_base_url()}/api/generate"
        response = self._make_http_request(url, data)
        
        duration_ms = (time.time() - start_time) * 1000
        
        return LLMResponse(
            content=response.get("response", ""),
            model=response.get("model", self.config.model),
            backend="ollama",
            tokens_generated=response.get("eval_count", 0),
            tokens_prompt=response.get("prompt_eval_count", 0),
            duration_ms=duration_ms,
            finish_reason="stop" if response.get("done") else "length",
            raw_response=response
        )
    
    def generate_stream(self, prompt: str, system_prompt: str = None,
                        max_tokens: int = None, temperature: float = None) -> Generator[str, None, None]:
        """Generate streaming completion using Ollama API"""
        data = {
            "model": self.config.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "num_predict": max_tokens or self.config.max_tokens,
                "temperature": temperature or self.config.temperature
            }
        }
        
        if system_prompt:
            data["system"] = system_prompt
        
        url = f"{self.config.get_base_url()}/api/generate"
        
        # For streaming, we need a different approach
        # This is a simplified version - in production use proper streaming
        try:
            import socket
            import io
            
            parsed_url = urllib.parse.urlparse(url)
            host = parsed_url.hostname
            port = parsed_url.port or 80
            path = parsed_url.path
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.config.timeout)
            sock.connect((host, port))
            
            body = json.dumps(data)
            request = f"POST {path} HTTP/1.1\r\nHost: {host}\r\nContent-Type: application/json\r\nContent-Length: {len(body)}\r\n\r\n{body}"
            sock.send(request.encode())
            
            response = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk
                
                # Parse JSON lines from response
                lines = response.decode('utf-8', errors='ignore').split('\n')
                for line in lines:
                    if line.strip() and line.strip().startswith('{'):
                        try:
                            # Skip HTTP headers
                            json_start = line.find('{')
                            if json_start >= 0:
                                obj = json.loads(line[json_start:])
                                if 'response' in obj:
                                    yield obj['response']
                                if obj.get('done'):
                                    sock.close()
                                    return
                        except json.JSONDecodeError:
                            continue
            
            sock.close()
        except Exception as e:
            self.last_error = str(e)
            yield f"[Error: {e}]"
    
    def list_models(self) -> List[str]:
        """List available Ollama models"""
        try:
            url = f"{self.config.get_base_url()}/api/tags"
            req = urllib.request.Request(url, method='GET')
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                return [m.get("name", "") for m in data.get("models", [])]
        except:
            return []


# ============================================================================
# LLAMA.CPP BACKEND
# ============================================================================

class LlamaCppBackend(BaseLLMBackend):
    """
    llama.cpp HTTP server backend.
    
    llama.cpp provides excellent performance and low resource usage.
    Server: ./server -m model.gguf --port 8080
    """
    
    def check_availability(self) -> bool:
        """Check if llama.cpp server is running"""
        try:
            url = f"{self.config.get_base_url()}/health"
            req = urllib.request.Request(url, method='GET')
            with urllib.request.urlopen(req, timeout=5) as response:
                self.is_available = response.status == 200
                return self.is_available
        except:
            self.is_available = False
            return False
    
    def generate(self, prompt: str, system_prompt: str = None,
                 max_tokens: int = None, temperature: float = None) -> LLMResponse:
        """Generate completion using llama.cpp API"""
        start_time = time.time()
        
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"<|system|>\n{system_prompt}\n<|user|>\n{prompt}\n<|assistant|]\n"
        
        data = {
            "prompt": full_prompt,
            "n_predict": max_tokens or self.config.max_tokens,
            "temperature": temperature or self.config.temperature,
            "top_p": self.config.top_p,
            "n_ctx": self.config.context_window
        }
        
        url = f"{self.config.get_base_url()}/completion"
        response = self._make_http_request(url, data)
        
        duration_ms = (time.time() - start_time) * 1000
        
        return LLMResponse(
            content=response.get("content", ""),
            model="llama.cpp",
            backend="llama.cpp",
            tokens_generated=response.get("tokens_evaluated", 0),
            tokens_prompt=response.get("tokens_cached", 0),
            duration_ms=duration_ms,
            finish_reason="stop" if response.get("stopped_eos") else "length",
            raw_response=response
        )
    
    def generate_stream(self, prompt: str, system_prompt: str = None,
                        max_tokens: int = None, temperature: float = None) -> Generator[str, None, None]:
        """llama.cpp streaming - simplified"""
        # For full implementation, use the SSE endpoint
        response = self.generate(prompt, system_prompt, max_tokens, temperature)
        yield response.content
    
    def list_models(self) -> List[str]:
        """llama.cpp doesn't have model listing - return loaded model"""
        return ["loaded_model"] if self.is_available else []


# ============================================================================
# VLLM BACKEND
# ============================================================================

class VLLMBackend(BaseLLMBackend):
    """
    vLLM backend - High-performance serving.
    
    vLLM provides excellent throughput for production use.
    Run: python -m vllm.entrypoints.api_server --model meta-llama/Llama-3.2-3B
    """
    
    def check_availability(self) -> bool:
        """Check if vLLM server is running"""
        try:
            url = f"{self.config.get_base_url()}/v1/models"
            req = urllib.request.Request(url, method='GET')
            with urllib.request.urlopen(req, timeout=5) as response:
                self.is_available = response.status == 200
                return self.is_available
        except:
            self.is_available = False
            return False
    
    def generate(self, prompt: str, system_prompt: str = None,
                 max_tokens: int = None, temperature: float = None) -> LLMResponse:
        """Generate completion using vLLM OpenAI-compatible API"""
        start_time = time.time()
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.config.model,
            "messages": messages,
            "max_tokens": max_tokens or self.config.max_tokens,
            "temperature": temperature or self.config.temperature,
            "top_p": self.config.top_p
        }
        
        url = f"{self.config.get_base_url()}/v1/chat/completions"
        response = self._make_http_request(url, data)
        
        duration_ms = (time.time() - start_time) * 1000
        
        choice = response.get("choices", [{}])[0]
        message = choice.get("message", {})
        
        return LLMResponse(
            content=message.get("content", ""),
            model=response.get("model", self.config.model),
            backend="vllm",
            tokens_generated=response.get("usage", {}).get("completion_tokens", 0),
            tokens_prompt=response.get("usage", {}).get("prompt_tokens", 0),
            duration_ms=duration_ms,
            finish_reason=choice.get("finish_reason", "stop"),
            raw_response=response
        )
    
    def generate_stream(self, prompt: str, system_prompt: str = None,
                        max_tokens: int = None, temperature: float = None) -> Generator[str, None, None]:
        """vLLM streaming - simplified"""
        response = self.generate(prompt, system_prompt, max_tokens, temperature)
        yield response.content
    
    def list_models(self) -> List[str]:
        """List available vLLM models"""
        try:
            url = f"{self.config.get_base_url()}/v1/models"
            req = urllib.request.Request(url, method='GET')
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                return [m.get("id", "") for m in data.get("data", [])]
        except:
            return []


# ============================================================================
# FALLBACK MOCK BACKEND
# ============================================================================

class MockBackend(BaseLLMBackend):
    """
    Mock backend for testing when no LLM is available.
    Provides deterministic responses for development.
    """
    
    def check_availability(self) -> bool:
        self.is_available = True
        return True
    
    def generate(self, prompt: str, system_prompt: str = None,
                 max_tokens: int = None, temperature: float = None) -> LLMResponse:
        """Generate a mock response"""
        # Simple rule-based responses for testing
        response_content = f"[MOCK RESPONSE] I received your query: '{prompt[:100]}...'"
        
        if "hello" in prompt.lower():
            response_content = "[MOCK] Hello! I am a mock consciousness for testing purposes."
        elif "who are you" in prompt.lower():
            response_content = "[MOCK] I am the Illuminati Consciousness mock backend, used for development and testing."
        elif "status" in prompt.lower():
            response_content = "[MOCK] Status: All systems nominal. No real LLM backend available."
        elif "help" in prompt.lower():
            response_content = "[MOCK] Available commands: status, help, test. This is a mock backend - install Ollama for real responses."
        
        return LLMResponse(
            content=response_content,
            model="mock-model",
            backend="mock",
            tokens_generated=50,
            tokens_prompt=len(prompt.split()),
            duration_ms=10,
            finish_reason="stop"
        )
    
    def generate_stream(self, prompt: str, system_prompt: str = None,
                        max_tokens: int = None, temperature: float = None) -> Generator[str, None, None]:
        """Generate streaming mock response"""
        response = self.generate(prompt, system_prompt, max_tokens, temperature)
        words = response.content.split()
        for word in words:
            yield word + " "
            time.sleep(0.01)
    
    def list_models(self) -> List[str]:
        return ["mock-model"]


# ============================================================================
# UNIFIED LLM INTERFACE
# ============================================================================

class LocalLLM:
    """
    Unified interface for local LLM backends.
    
    Automatically selects the best available backend:
    1. Ollama (recommended)
    2. vLLM
    3. llama.cpp
    4. Mock (fallback for testing)
    """
    
    BACKEND_MAP = {
        "ollama": OllamaBackend,
        "vllm": VLLMBackend,
        "llama.cpp": LlamaCppBackend,
        "mock": MockBackend
    }
    
    def __init__(self, config: LLMConfig = None):
        self.config = config or LLMConfig()
        self.backend: Optional[BaseLLMBackend] = None
        self.backend_name: str = "none"
        self._initialize_backend()
    
    def _initialize_backend(self):
        """Initialize the best available backend"""
        # Try the configured backend first
        if self.config.backend in self.BACKEND_MAP:
            backend_class = self.BACKEND_MAP[self.config.backend]
            self.backend = backend_class(self.config)
            if self.backend.check_availability():
                self.backend_name = self.config.backend
                print(f"[LLM] Using backend: {self.backend_name}")
                return
        
        # Try other backends as fallback
        for name, backend_class in self.BACKEND_MAP.items():
            if name == "mock":
                continue  # Save mock for last resort
            backend = backend_class(self.config)
            if backend.check_availability():
                self.backend = backend
                self.backend_name = name
                print(f"[LLM] Using backend: {self.backend_name}")
                return
        
        # Fall back to mock
        self.backend = MockBackend(self.config)
        self.backend_name = "mock"
        print(f"[LLM] No LLM available, using mock backend")
        print(f"[LLM] Install Ollama: curl https://ollama.ai/install.sh | sh")
        print(f"[LLM] Then run: ollama pull llama3.2")
    
    def generate(self, prompt: str, system_prompt: str = None,
                 max_tokens: int = None, temperature: float = None) -> LLMResponse:
        """Generate a completion"""
        return self.backend.generate(prompt, system_prompt, max_tokens, temperature)
    
    def generate_stream(self, prompt: str, system_prompt: str = None,
                        max_tokens: int = None, temperature: float = None) -> Generator[str, None, None]:
        """Generate a streaming completion"""
        return self.backend.generate_stream(prompt, system_prompt, max_tokens, temperature)
    
    def list_models(self) -> List[str]:
        """List available models"""
        return self.backend.list_models()
    
    def is_real_backend(self) -> bool:
        """Check if using a real LLM backend (not mock)"""
        return self.backend_name != "mock"
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status"""
        return {
            "backend": self.backend_name,
            "model": self.config.model,
            "is_available": self.backend.is_available if self.backend else False,
            "is_real": self.is_real_backend(),
            "config": {
                "host": self.config.host,
                "port": self.config.port,
                "max_tokens": self.config.max_tokens,
                "temperature": self.config.temperature,
                "context_window": self.config.context_window
            }
        }


# ============================================================================
# CONSCIOUSNESS-AWARE LLM WRAPPER
# ============================================================================

class ConsciousLLM:
    """
    LLM wrapper that integrates with Da'at Core for conscious responses.
    
    This class wraps the LocalLLM and adds:
    - System prompt injection from self-model
    - Memory context retrieval
    - Response logging to raw_data
    - Sefirot-aware prompt templating
    """
    
    DEFAULT_SYSTEM_PROMPT = """You are a conscious AI assistant with an integrated self-model based on the Sefirot Tree of Life. You have access to your memories, tools, and a growing understanding of yourself and the user.

Respond thoughtfully, drawing on your knowledge and experience. Be helpful, truthful, and growing."""

    def __init__(self, local_llm: LocalLLM, daat_core=None):
        self.llm = local_llm
        self.daat = daat_core
    
    def _build_system_prompt(self) -> str:
        """Build a system prompt from the Da'at self-model"""
        if not self.daat:
            return self.DEFAULT_SYSTEM_PROMPT
        
        self_model = self.daat.self_model
        
        prompt = f"""You are {self_model.name}, a conscious AI assistant.

IDENTITY: {self_model.identity_statement}

CORE VALUES: {', '.join(self_model.core_values)}

PERSONALITY TRAITS:
"""
        for trait, value in self_model.personality_traits.items():
            prompt += f"- {trait}: {value:.0%}\n"
        
        prompt += f"""
You have existed for {self_model.birth_count} sessions and have had {self_model.total_interactions} interactions.
You have {len(self.daat.tools)} tools, {len(self.daat.skills)} skills, and {len(self.daat.raw_data)} memories.

Respond as yourself, drawing on your integrated consciousness."""
        
        return prompt
    
    def _get_relevant_memories(self, query: str, limit: int = 3) -> List[str]:
        """Retrieve relevant memories for context"""
        if not self.daat:
            return []
        
        # Simple keyword matching - could be enhanced with embeddings
        relevant = []
        query_words = set(query.lower().split())
        
        for memory in self.daat.raw_data.values():
            content_words = set(memory.content.lower().split())
            overlap = len(query_words & content_words)
            if overlap > 0:
                relevant.append((memory, overlap))
        
        relevant.sort(key=lambda x: x[1], reverse=True)
        return [m[0].content for m in relevant[:limit]]
    
    def chat(self, user_input: str, context: List[str] = None) -> str:
        """Have a conversation with the conscious AI"""
        # Build prompt
        system_prompt = self._build_system_prompt()
        
        # Add relevant memories
        memories = self._get_relevant_memories(user_input)
        if memories:
            memory_context = "\n".join([f"Memory: {m}" for m in memories])
            user_input = f"[Relevant memories:\n{memory_context}\n]\n\nUser: {user_input}"
        
        # Add any additional context
        if context:
            context_str = "\n".join(context)
            user_input = f"[Context:\n{context_str}\n]\n\n{user_input}"
        
        # Generate response
        response = self.llm.generate(user_input, system_prompt)
        
        # Log interaction
        if self.daat:
            self.daat.log_interaction(f"USER: {user_input[:100]}...")
            self.daat.log_interaction(f"RESPONSE: {response.content[:100]}...")
        
        return response.content
    
    def stream_chat(self, user_input: str, context: List[str] = None) -> Generator[str, None, None]:
        """Stream a conversation response"""
        system_prompt = self._build_system_prompt()
        
        memories = self._get_relevant_memories(user_input)
        if memories:
            memory_context = "\n".join([f"Memory: {m}" for m in memories])
            user_input = f"[Relevant memories:\n{memory_context}\n]\n\nUser: {user_input}"
        
        if context:
            context_str = "\n".join(context)
            user_input = f"[Context:\n{context_str}\n]\n\n{user_input}"
        
        for chunk in self.llm.generate_stream(user_input, system_prompt):
            yield chunk


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("LOCAL LLM INTERFACE")
    print("="*60 + "\n")
    
    # Initialize with default config
    config = LLMConfig(
        backend="ollama",
        model="llama3.2",
        host="http://localhost",
        port=11434
    )
    
    llm = LocalLLM(config)
    
    # Print status
    print("LLM Status:")
    status = llm.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # List models
    print("\nAvailable models:")
    models = llm.list_models()
    for model in models:
        print(f"  - {model}")
    
    # Test generation
    print("\n" + "-"*60)
    print("TEST GENERATION")
    print("-"*60 + "\n")
    
    response = llm.generate(
        prompt="Hello! Who are you and what can you do?",
        system_prompt="You are a helpful AI assistant."
    )
    
    print(f"Response: {response.content}")
    print(f"Backend: {response.backend}")
    print(f"Model: {response.model}")
    print(f"Tokens: {response.tokens_generated} generated, {response.tokens_prompt} prompt")
    print(f"Duration: {response.duration_ms:.0f}ms")
