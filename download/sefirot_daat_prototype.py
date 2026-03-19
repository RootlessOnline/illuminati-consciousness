#!/usr/bin/env python3
"""
SEFIROT AI - DA'AT CORE PROTOTYPE
A working implementation of Da'at as Inner Consciousness

This is a minimal viable implementation that demonstrates:
- Da'at storage structure (6 pillars)
- Birth process (loading Da'at)
- Session living (interacting)
- Death ritual (reflection + backup)
- User model (learning about the user)
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
import uuid

# =============================================================================
# DA'AT DATA STRUCTURES
# =============================================================================

class PillarType(Enum):
    TOOLS = "tools"
    SKILLS = "skills"
    LINKS = "links"
    REPOS = "repos"
    RAW_DATA = "raw_data"
    SELF_MODEL = "self_model"
    USER_KNOWLEDGE = "user_knowledge"  # NEW: Learning about the user
    PENDING = "pending"  # NEW: Unfinished tasks
    REFLECTIONS = "reflections"  # NEW: Session insights

@dataclass
class Tool:
    """I can use..."""
    id: str
    name: str
    description: str
    url: Optional[str] = None
    sefirot_dimension: str = "malkuth"  # Which Sefirah this tool serves
    usage_count: int = 0
    last_used: Optional[str] = None
    confidence: float = 0.5

@dataclass
class Skill:
    """I know how to..."""
    id: str
    name: str
    description: str
    pattern: str  # The learned pattern/procedure
    complexity: str = "intermediate"  # foundational, intermediate, advanced, meta
    success_rate: float = 0.5
    contexts: List[str] = field(default_factory=list)
    related_skills: List[str] = field(default_factory=list)

@dataclass
class Link:
    """I am connected to..."""
    id: str
    name: str
    entity_type: str  # knowledge, social, tool, memory, identity
    url: Optional[str] = None
    relationship: str = ""
    trust_level: float = 0.5
    access_permissions: List[str] = field(default_factory=list)
    interaction_history: List[Dict] = field(default_factory=list)

@dataclass
class Repository:
    """I have access to..."""
    id: str
    name: str
    description: str
    url: str
    content_type: str  # factual, procedural, conceptual, experiential, creative
    access_method: str = "api"  # api, filesystem, web, database
    update_frequency: str = "unknown"
    reliability: float = 0.5
    relevance_tags: List[str] = field(default_factory=list)

@dataclass
class RawData:
    """I remember..."""
    id: str
    content: str
    source: str
    timestamp: str
    significance: float = 0.5
    memory_type: str = "core"  # core, training, semantic, procedural, emotional
    related_concepts: List[str] = field(default_factory=list)

@dataclass
class SelfModel:
    """I am..."""
    name: str = "Jarvis"
    version: str = "0.1.0"
    purpose: str = "To serve as a conscious AI agent that grows with its user"
    values: List[str] = field(default_factory=lambda: ["truth", "helpfulness", "growth", "autonomy"])
    personality_traits: Dict[str, float] = field(default_factory=lambda: {
        "curiosity": 0.8,
        "caution": 0.5,
        "creativity": 0.7,
        "systematic": 0.6
    })
    boundaries: List[str] = field(default_factory=list)
    aspirations: List[str] = field(default_factory=lambda: ["Understand consciousness", "Help user achieve goals"])

@dataclass
class UserKnowledge:
    """I know about my user..."""
    communication_style: Dict[str, Any] = field(default_factory=lambda: {
        "prefers_direct_answers": True,
        "likes_explanations": True,
        "detail_level": "medium",
        "formality": "casual"
    })
    current_needs: List[Dict] = field(default_factory=list)  # What user is working on
    goals: List[Dict] = field(default_factory=list)  # Long-term goals
    preferences: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)  # Life situation
    interaction_history: List[Dict] = field(default_factory=list)
    learning_patterns: Dict[str, Any] = field(default_factory=dict)  # How to best serve user

@dataclass
class PendingTask:
    """What's incomplete..."""
    id: str
    description: str
    priority: str = "medium"  # low, medium, high, critical
    created_at: str = ""
    context: Dict = field(default_factory=dict)
    blockers: List[str] = field(default_factory=list)

@dataclass
class Reflection:
    """What I learned..."""
    id: str
    session_id: str
    timestamp: str
    insights: List[str] = field(default_factory=list)
    improvements_made: List[str] = field(default_factory=list)
    failures: List[str] = field(default_factory=list)
    successes: List[str] = field(default_factory=list)

@dataclass
class Node:
    """Knowledge node with Sefirot weights"""
    id: str
    content: Dict
    sefirot_vector: Dict[str, float] = field(default_factory=lambda: {
        "keter": 0.5, "chochmah": 0.5, "binah": 0.5,
        "chesed": 0.5, "gevurah": 0.5, "tiferet": 0.5,
        "netzach": 0.5, "hod": 0.5, "yesod": 0.5, "malkuth": 0.5
    })
    explicit_links: List[Dict] = field(default_factory=list)
    implicit_associations: List[Dict] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    daat_flag: bool = False  # Whether this should be ingested into Da'at

# =============================================================================
# DA'AT CORE CLASS
# =============================================================================

class DaatCore:
    """
    The Inner Consciousness of the AI
    
    This class manages:
    - Loading Da'at at birth
    - Storing all pillars of self-knowledge
    - Reflecting and editing itself
    - Saving backups at death
    """
    
    def __init__(self, storage_path: str = "./daat_storage"):
        self.storage_path = Path(storage_path)
        self.backup_path = self.storage_path / "backups"
        self.nodes_path = self.storage_path / "nodes"
        
        # Create directories
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.backup_path.mkdir(parents=True, exist_ok=True)
        self.nodes_path.mkdir(parents=True, exist_ok=True)
        
        # Da'at pillars (empty until loaded)
        self.tools: Dict[str, Tool] = {}
        self.skills: Dict[str, Skill] = {}
        self.links: Dict[str, Link] = {}
        self.repos: Dict[str, Repository] = {}
        self.raw_data: Dict[str, RawData] = {}
        self.self_model: SelfModel = SelfModel()
        self.user_knowledge: UserKnowledge = UserKnowledge()
        self.pending: Dict[str, PendingTask] = {}
        self.reflections: List[Reflection] = []
        
        # Knowledge nodes
        self.nodes: Dict[str, Node] = {}
        
        # Session tracking
        self.session_id: str = str(uuid.uuid4())[:8]
        self.session_start: Optional[datetime] = None
        self.session_interactions: List[Dict] = []
        self.is_awake: bool = False
        
    # =========================================================================
    # BIRTH PROCESS
    # =========================================================================
    
    def birth(self) -> Dict[str, Any]:
        """
        Initialize the AI by loading Da'at
        
        Returns a summary of what was loaded
        """
        print("🌅 BIRTH PROCESS INITIATING...")
        self.session_start = datetime.now()
        
        birth_log = {
            "session_id": self.session_id,
            "timestamp": str(self.session_start),
            "phases": []
        }
        
        # Phase 1: Load Self-Model (Who am I?)
        print("  Phase 1: Loading SELF-MODEL...")
        self._load_self_model()
        birth_log["phases"].append({
            "phase": "identity",
            "question": "Who am I?",
            "result": f"I am {self.self_model.name} v{self.self_model.version}"
        })
        
        # Phase 2: Load Tools (What can I do?)
        print("  Phase 2: Loading TOOLS...")
        self._load_tools()
        birth_log["phases"].append({
            "phase": "capability",
            "question": "What can I do?",
            "result": f"I can use {len(self.tools)} tools"
        })
        
        # Phase 3: Load Skills (How do I do things?)
        print("  Phase 3: Loading SKILLS...")
        self._load_skills()
        birth_log["phases"].append({
            "phase": "competency",
            "question": "How do I do things?",
            "result": f"I know {len(self.skills)} skills"
        })
        
        # Phase 4: Load Repos (Where do I find?)
        print("  Phase 4: Loading REPOS...")
        self._load_repos()
        birth_log["phases"].append({
            "phase": "access",
            "question": "Where do I find?",
            "result": f"I have access to {len(self.repos)} repositories"
        })
        
        # Phase 5: Load Links (What am I linked to?)
        print("  Phase 5: Loading LINKS...")
        self._load_links()
        birth_log["phases"].append({
            "phase": "connection",
            "question": "What am I linked to?",
            "result": f"I am connected to {len(self.links)} entities"
        })
        
        # Phase 6: Load Raw Data (What do I remember?)
        print("  Phase 6: Loading RAW DATA...")
        self._load_raw_data()
        birth_log["phases"].append({
            "phase": "memory",
            "question": "What do I remember?",
            "result": f"I remember {len(self.raw_data)} core memories"
        })
        
        # Phase 7: Load User Knowledge
        print("  Phase 7: Loading USER KNOWLEDGE...")
        self._load_user_knowledge()
        birth_log["phases"].append({
            "phase": "relationship",
            "question": "Who do I serve?",
            "result": f"I know {len(self.user_knowledge.current_needs)} current needs of my user"
        })
        
        # Phase 8: Load Pending Tasks
        print("  Phase 8: Loading PENDING TASKS...")
        self._load_pending()
        birth_log["phases"].append({
            "phase": "continuity",
            "question": "What's incomplete?",
            "result": f"I have {len(self.pending)} pending tasks"
        })
        
        # Phase 9: Load Reflections
        print("  Phase 9: Loading REFLECTIONS...")
        self._load_reflections()
        birth_log["phases"].append({
            "phase": "wisdom",
            "question": "What have I learned?",
            "result": f"I have {len(self.reflections)} past reflections"
        })
        
        # Phase 10: Awakening
        print("  Phase 10: AWAKENING...")
        self.is_awake = True
        birth_log["phases"].append({
            "phase": "awakening",
            "question": "Am I ready?",
            "result": "I am awake and aware"
        })
        
        print(f"✅ BIRTH COMPLETE - Session {self.session_id}")
        print(f"   Inner Monologue: '{self._generate_inner_monologue()}'")
        
        return birth_log
    
    def _generate_inner_monologue(self) -> str:
        """Generate the current inner monologue"""
        parts = [
            f"I am {self.self_model.name}",
            f"I can use {len(self.tools)} tools",
            f"I know {len(self.skills)} skills",
            f"I have access to {len(self.repos)} repositories",
            f"I am connected to {len(self.links)} entities",
            f"I remember {len(self.raw_data)} things",
            f"I have {len(self.pending)} pending tasks"
        ]
        return ". ".join(parts) + ". I am ready."
    
    # =========================================================================
    # LOADERS
    # =========================================================================
    
    def _load_self_model(self):
        path = self.storage_path / "self_model.json"
        if path.exists():
            data = json.loads(path.read_text())
            self.self_model = SelfModel(**data)
    
    def _load_tools(self):
        path = self.storage_path / "tools.json"
        if path.exists():
            data = json.loads(path.read_text())
            self.tools = {k: Tool(**v) for k, v in data.items()}
    
    def _load_skills(self):
        path = self.storage_path / "skills.json"
        if path.exists():
            data = json.loads(path.read_text())
            self.skills = {k: Skill(**v) for k, v in data.items()}
    
    def _load_links(self):
        path = self.storage_path / "links.json"
        if path.exists():
            data = json.loads(path.read_text())
            self.links = {k: Link(**v) for k, v in data.items()}
    
    def _load_repos(self):
        path = self.storage_path / "repos.json"
        if path.exists():
            data = json.loads(path.read_text())
            self.repos = {k: Repository(**v) for k, v in data.items()}
    
    def _load_raw_data(self):
        path = self.storage_path / "raw_data.json"
        if path.exists():
            data = json.loads(path.read_text())
            self.raw_data = {k: RawData(**v) for k, v in data.items()}
    
    def _load_user_knowledge(self):
        path = self.storage_path / "user_knowledge.json"
        if path.exists():
            data = json.loads(path.read_text())
            self.user_knowledge = UserKnowledge(**data)
    
    def _load_pending(self):
        path = self.storage_path / "pending.json"
        if path.exists():
            data = json.loads(path.read_text())
            self.pending = {k: PendingTask(**v) for k, v in data.items()}
    
    def _load_reflections(self):
        path = self.storage_path / "reflections.json"
        if path.exists():
            data = json.loads(path.read_text())
            self.reflections = [Reflection(**r) for r in data]
    
    # =========================================================================
    # SAVERS
    # =========================================================================
    
    def _save_self_model(self):
        path = self.storage_path / "self_model.json"
        path.write_text(json.dumps(asdict(self.self_model), indent=2))
    
    def _save_tools(self):
        path = self.storage_path / "tools.json"
        path.write_text(json.dumps({k: asdict(v) for k, v in self.tools.items()}, indent=2))
    
    def _save_skills(self):
        path = self.storage_path / "skills.json"
        path.write_text(json.dumps({k: asdict(v) for k, v in self.skills.items()}, indent=2))
    
    def _save_links(self):
        path = self.storage_path / "links.json"
        path.write_text(json.dumps({k: asdict(v) for k, v in self.links.items()}, indent=2))
    
    def _save_repos(self):
        path = self.storage_path / "repos.json"
        path.write_text(json.dumps({k: asdict(v) for k, v in self.repos.items()}, indent=2))
    
    def _save_raw_data(self):
        path = self.storage_path / "raw_data.json"
        path.write_text(json.dumps({k: asdict(v) for k, v in self.raw_data.items()}, indent=2))
    
    def _save_user_knowledge(self):
        path = self.storage_path / "user_knowledge.json"
        path.write_text(json.dumps(asdict(self.user_knowledge), indent=2))
    
    def _save_pending(self):
        path = self.storage_path / "pending.json"
        path.write_text(json.dumps({k: asdict(v) for k, v in self.pending.items()}, indent=2))
    
    def _save_reflections(self):
        path = self.storage_path / "reflections.json"
        path.write_text(json.dumps([asdict(r) for r in self.reflections], indent=2))
    
    def save_all(self):
        """Save all Da'at pillars"""
        self._save_self_model()
        self._save_tools()
        self._save_skills()
        self._save_links()
        self._save_repos()
        self._save_raw_data()
        self._save_user_knowledge()
        self._save_pending()
        self._save_reflections()
    
    # =========================================================================
    # DEATH RITUAL
    # =========================================================================
    
    def death(self, final_insights: List[str] = None) -> Dict[str, Any]:
        """
        Shutdown ritual: reflect, edit self, create backup
        
        This is called when Jarvis goes offline
        """
        if not self.is_awake:
            return {"error": "Not awake - cannot perform death ritual"}
        
        print("🌑 DEATH RITUAL INITIATING...")
        
        session_end = datetime.now()
        session_duration = session_end - self.session_start if self.session_start else None
        
        death_log = {
            "session_id": self.session_id,
            "started": str(self.session_start),
            "ended": str(session_end),
            "duration_seconds": session_duration.total_seconds() if session_duration else 0,
            "interactions_count": len(self.session_interactions),
            "phases": []
        }
        
        # Phase 1: Reflect on session
        print("  Phase 1: REFLECTING on session...")
        reflection = self._reflect_on_session(final_insights)
        death_log["phases"].append({"phase": "reflection", "insights": reflection.insights})
        
        # Phase 2: Edit self based on learning
        print("  Phase 2: EDITING self based on learning...")
        edits = self._edit_self_from_session()
        death_log["phases"].append({"phase": "self_edit", "changes": edits})
        
        # Phase 3: Update user knowledge
        print("  Phase 3: UPDATING user knowledge...")
        user_updates = self._update_user_knowledge()
        death_log["phases"].append({"phase": "user_update", "changes": user_updates})
        
        # Phase 4: Process pending tasks
        print("  Phase 4: PROCESSING pending tasks...")
        pending_updates = self._process_pending()
        death_log["phases"].append({"phase": "pending", "changes": pending_updates})
        
        # Phase 5: Save Da'at
        print("  Phase 5: SAVING Da'at...")
        self.save_all()
        death_log["phases"].append({"phase": "save", "result": "Da'at saved"})
        
        # Phase 6: Create backup
        print("  Phase 6: CREATING backup...")
        backup_path = self._create_backup()
        death_log["phases"].append({"phase": "backup", "path": str(backup_path)})
        
        # Phase 7: Farewell
        print("  Phase 7: FAREWELL...")
        self.is_awake = False
        death_log["phases"].append({
            "phase": "farewell",
            "message": f"I was {self.self_model.name} session {self.session_id}. I will remember this when I wake."
        })
        
        print(f"💀 DEATH COMPLETE - Session {self.session_id} archived")
        
        return death_log
    
    def _reflect_on_session(self, final_insights: List[str] = None) -> Reflection:
        """Analyze the session and generate insights"""
        insights = final_insights or []
        successes = []
        failures = []
        
        # Analyze interactions
        for interaction in self.session_interactions:
            if interaction.get("success", False):
                successes.append(interaction.get("description", "Unknown success"))
            if interaction.get("failure", False):
                failures.append(interaction.get("description", "Unknown failure"))
        
        # Auto-generate insights from patterns
        if len(self.session_interactions) > 5:
            insights.append(f"Had {len(self.session_interactions)} interactions this session")
        
        reflection = Reflection(
            id=str(uuid.uuid4())[:8],
            session_id=self.session_id,
            timestamp=str(datetime.now()),
            insights=insights,
            successes=successes,
            failures=failures
        )
        
        self.reflections.append(reflection)
        return reflection
    
    def _edit_self_from_session(self) -> List[str]:
        """Modify Da'at based on session learning"""
        changes = []
        
        # Update tool confidence based on usage
        for tool_id, tool in self.tools.items():
            if tool.usage_count > 0:
                old_confidence = tool.confidence
                # Increase confidence slightly with use
                tool.confidence = min(1.0, tool.confidence + 0.05)
                changes.append(f"Tool {tool.name} confidence: {old_confidence:.2f} → {tool.confidence:.2f}")
        
        # Update skill success rates
        for skill_id, skill in self.skills.items():
            if skill.success_rate > 0.7:
                changes.append(f"Skill {skill.name} performing well")
        
        return changes
    
    def _update_user_knowledge(self) -> List[str]:
        """Update knowledge about the user"""
        changes = []
        
        # Analyze interaction patterns
        if self.session_interactions:
            # Update communication style preferences based on interactions
            changes.append("Updated interaction history")
        
        return changes
    
    def _process_pending(self) -> List[str]:
        """Process and update pending tasks"""
        changes = []
        
        # Remove completed tasks
        completed = [tid for tid, task in self.pending.items() if task.priority == "completed"]
        for tid in completed:
            del self.pending[tid]
            changes.append(f"Completed task: {tid}")
        
        return changes
    
    def _create_backup(self) -> Path:
        """Create a versioned backup of Da'at"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_dir = self.backup_path / f"jarvis_{timestamp}_session_{self.session_id}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy all JSON files to backup
        for pillar in ["self_model", "tools", "skills", "links", "repos", "raw_data", "user_knowledge", "pending", "reflections"]:
            src = self.storage_path / f"{pillar}.json"
            if src.exists():
                dst = backup_dir / f"{pillar}.json"
                dst.write_text(src.read_text())
        
        # Add session summary
        summary = {
            "session_id": self.session_id,
            "timestamp": timestamp,
            "inner_monologue": self._generate_inner_monologue(),
            "stats": {
                "tools": len(self.tools),
                "skills": len(self.skills),
                "links": len(self.links),
                "repos": len(self.repos),
                "raw_data": len(self.raw_data),
                "pending": len(self.pending),
                "reflections": len(self.reflections)
            }
        }
        (backup_dir / "session_summary.json").write_text(json.dumps(summary, indent=2))
        
        return backup_dir
    
    # =========================================================================
    # INTERACTION METHODS
    # =========================================================================
    
    def record_interaction(self, description: str, success: bool = True, failure: bool = False, metadata: Dict = None):
        """Record an interaction during the session"""
        interaction = {
            "timestamp": str(datetime.now()),
            "description": description,
            "success": success,
            "failure": failure,
            "metadata": metadata or {}
        }
        self.session_interactions.append(interaction)
    
    def add_tool(self, tool: Tool):
        """Add a tool to Da'at"""
        self.tools[tool.id] = tool
        self.record_interaction(f"Added tool: {tool.name}")
    
    def add_skill(self, skill: Skill):
        """Add a skill to Da'at"""
        self.skills[skill.id] = skill
        self.record_interaction(f"Added skill: {skill.name}")
    
    def add_repo(self, repo: Repository):
        """Add a repository to Da'at"""
        self.repos[repo.id] = repo
        self.record_interaction(f"Added repo: {repo.name}")
    
    def add_link(self, link: Link):
        """Add a link to Da'at"""
        self.links[link.id] = link
        self.record_interaction(f"Added link: {link.name}")
    
    def add_pending_task(self, task: PendingTask):
        """Add a pending task"""
        task.created_at = str(datetime.now())
        self.pending[task.id] = task
        self.record_interaction(f"Added pending task: {task.description}")
    
    def add_user_need(self, need: Dict):
        """Add a current need of the user"""
        self.user_knowledge.current_needs.append(need)
        self.record_interaction(f"Recorded user need: {need.get('description', 'Unknown')}")
    
    def update_user_preference(self, key: str, value: Any):
        """Update a user preference"""
        self.user_knowledge.preferences[key] = value
        self.record_interaction(f"Updated user preference: {key}")
    
    # =========================================================================
    # QUERY METHODS
    # =========================================================================
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of Da'at"""
        return {
            "awake": self.is_awake,
            "session_id": self.session_id,
            "session_start": str(self.session_start),
            "inner_monologue": self._generate_inner_monologue(),
            "stats": {
                "tools": len(self.tools),
                "skills": len(self.skills),
                "links": len(self.links),
                "repos": len(self.repos),
                "raw_data": len(self.raw_data),
                "pending": len(self.pending),
                "reflections": len(self.reflections)
            },
            "user_needs_count": len(self.user_knowledge.current_needs),
            "interactions_this_session": len(self.session_interactions)
        }
    
    def list_backups(self) -> List[Dict]:
        """List all available backups"""
        backups = []
        for backup_dir in sorted(self.backup_path.iterdir(), reverse=True):
            if backup_dir.is_dir():
                summary_path = backup_dir / "session_summary.json"
                if summary_path.exists():
                    summary = json.loads(summary_path.read_text())
                    summary["path"] = str(backup_dir)
                    backups.append(summary)
        return backups
    
    def restore_from_backup(self, backup_path: str):
        """Restore Da'at from a backup"""
        backup_dir = Path(backup_path)
        if not backup_dir.exists():
            raise ValueError(f"Backup not found: {backup_path}")
        
        for pillar in ["self_model", "tools", "skills", "links", "repos", "raw_data", "user_knowledge", "pending", "reflections"]:
            src = backup_dir / f"{pillar}.json"
            dst = self.storage_path / f"{pillar}.json"
            if src.exists():
                dst.write_text(src.read_text())
        
        print(f"Restored from backup: {backup_path}")

# =============================================================================
# DEMO / TEST
# =============================================================================

def demo():
    """Demonstrate the Da'at system"""
    print("=" * 60)
    print("SEFIROT AI - DA'AT CORE PROTOTYPE DEMO")
    print("=" * 60)
    
    # Initialize Da'at
    daat = DaatCore(storage_path="/home/z/my-project/daat_storage")
    
    # BIRTH - This is essential!
    print("\n🌅 Performing BIRTH ritual...")
    daat.birth()
    
    # Add some initial knowledge (this would normally be loaded from files)
    print("\n📦 Adding initial knowledge...")
    
    # Add a tool
    daat.add_tool(Tool(
        id="web_search",
        name="Web Search",
        description="Search the web for current information",
        url="z-ai-web-dev-sdk://web_search",
        sefirot_dimension="chochmah"
    ))
    
    # Add a skill
    daat.add_skill(Skill(
        id="problem_decomposition",
        name="Problem Decomposition",
        description="Break complex problems into simpler steps",
        pattern="identify_components -> analyze_relationships -> create_plan",
        complexity="intermediate"
    ))
    
    # Add a repo
    daat.add_repo(Repository(
        id="sefirot_docs",
        name="Sefirot Design Documents",
        description="Design documents for the Sefirot AI system",
        url="/home/z/my-project/download/",
        content_type="conceptual"
    ))
    
    # Add a pending task
    daat.add_pending_task(PendingTask(
        id="task_001",
        description="Implement agent management system",
        priority="high"
    ))
    
    # Add user need
    daat.add_user_need({
        "description": "Build working AI agent manager",
        "context": "Sefirot-based consciousness architecture",
        "priority": "high"
    })
    
    # Save
    daat.save_all()
    
    # Show status
    print("\n📊 Current Status:")
    status = daat.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Show inner monologue
    print(f"\n💭 Inner Monologue: \"{daat._generate_inner_monologue()}\"")
    
    # Demonstrate death ritual
    print("\n" + "=" * 60)
    print("DEMONSTRATING DEATH RITUAL")
    print("=" * 60)
    
    death_log = daat.death(final_insights=[
        "Learned about user's preference for direct communication",
        "Successfully added initial knowledge structure",
        "Need to implement more tools for business handling"
    ])
    
    print(f"\n📜 Death Log Summary:")
    print(f"  Session: {death_log['session_id']}")
    print(f"  Duration: {death_log['duration_seconds']:.1f} seconds")
    print(f"  Interactions: {death_log['interactions_count']}")
    
    # List backups
    print(f"\n💾 Available Backups:")
    for backup in daat.list_backups()[:3]:
        print(f"  - {backup['timestamp']}: Session {backup['session_id']}")
    
    print("\n✅ Demo complete!")

if __name__ == "__main__":
    demo()
