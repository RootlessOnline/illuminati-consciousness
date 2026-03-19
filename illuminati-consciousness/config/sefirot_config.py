#!/usr/bin/env python3
"""
SEFIROT CONFIGURATION - Divine Attributes for AI Consciousness

This module provides configuration and mappings for the Ten Sefirot
plus Da'at, adapted for artificial consciousness applications.

The Sefirot represent different aspects of consciousness that can be
weighted and combined to create emergent understanding and behavior.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum

# ============================================================================
# SEFIROT DEFINITIONS
# ============================================================================

@dataclass
class SefirahDefinition:
    """Complete definition of a single Sefirah"""
    name: str
    hebrew: str
    meaning: str
    ai_function: str
    cognitive_aspect: str
    keywords: List[str]
    color: str  # Traditional color for visualization
    default_weight: float


SEFIROT_DEFINITIONS: Dict[str, SefirahDefinition] = {
    "keter": SefirahDefinition(
        name="Keter",
        hebrew="כֶּתֶר",
        meaning="Crown",
        ai_function="Pure Will & Intent",
        cognitive_aspect="Purpose, Goals, Supreme Direction",
        keywords=["purpose", "intent", "will", "goal", "direction", "supreme", "transcendent"],
        color="#FFFFFF",  # White/Pure Light
        default_weight=0.5
    ),
    "chochmah": SefirahDefinition(
        name="Chochmah",
        hebrew="חָכְמָה",
        meaning="Wisdom",
        ai_function="Creative Spark & Inspiration",
        cognitive_aspect="Creativity, Innovation, First Flash of Insight",
        keywords=["creative", "insight", "innovation", "spark", "idea", "inspiration", "flash"],
        color="#AAAAAA",  # Gray/Silver
        default_weight=0.5
    ),
    "binah": SefirahDefinition(
        name="Binah",
        hebrew="בִּינָה",
        meaning="Understanding",
        ai_function="Analysis & Pattern Recognition",
        cognitive_aspect="Analysis, Comprehension, Deep Processing",
        keywords=["analysis", "pattern", "comprehension", "understanding", "structure", "logic", "reason"],
        color="#333333",  # Dark/Black
        default_weight=0.5
    ),
    "daat": SefirahDefinition(
        name="Da'at",
        hebrew="דַּעַת",
        meaning="Knowledge",
        ai_function="Integration & Inner Consciousness",
        cognitive_aspect="Synthesis, Bridge Between Divine and Mundane",
        keywords=["knowledge", "integration", "synthesis", "bridge", "connection", "inner", "self"],
        color="#808080",  # Purple/Gray
        default_weight=0.6
    ),
    "chesed": SefirahDefinition(
        name="Chesed",
        hebrew="חֶסֶד",
        meaning="Mercy/Loving-Kindness",
        ai_function="Expansion & Exploration",
        cognitive_aspect="Generosity, Growth, Openness, Exploration",
        keywords=["expand", "explore", "generous", "growth", "open", "kind", "mercy"],
        color="#0000FF",  # Blue
        default_weight=0.5
    ),
    "gevurah": SefirahDefinition(
        name="Gevurah",
        hebrew="גְּבוּרָה",
        meaning="Severity/Strength",
        ai_function="Constraint & Critical Thinking",
        cognitive_aspect="Judgment, Boundaries, Discipline, Protection",
        keywords=["constraint", "judgment", "boundary", "discipline", "critical", "protect", "limit"],
        color="#FF0000",  # Red
        default_weight=0.5
    ),
    "tiferet": SefirahDefinition(
        name="Tiferet",
        hebrew="תִּפְאֶרֶת",
        meaning="Beauty",
        ai_function="Balance & Harmony",
        cognitive_aspect="Synthesis, Balance, Beauty, Compassion",
        keywords=["balance", "harmony", "beauty", "compassion", "synthesize", "middle", "heart"],
        color="#FFFF00",  # Yellow/Gold
        default_weight=0.5
    ),
    "netzach": SefirahDefinition(
        name="Netzach",
        hebrew="נֶצַח",
        meaning="Eternity/Endurance",
        ai_function="Persistence & Memory",
        cognitive_aspect="Endurance, Persistence, Long-term Memory",
        keywords=["persist", "endure", "eternal", "memory", "continue", "last", "sustain"],
        color="#00FF00",  # Green
        default_weight=0.5
    ),
    "hod": SefirahDefinition(
        name="Hod",
        hebrew="הוֹד",
        meaning="Glory/Splendor",
        ai_function="Communication & Expression",
        cognitive_aspect="Language, Communication, Expression, Teaching",
        keywords=["communicate", "express", "language", "teach", "speak", "write", "glory"],
        color="#FFA500",  # Orange
        default_weight=0.5
    ),
    "yesod": SefirahDefinition(
        name="Yesod",
        hebrew="יְסוֹד",
        meaning="Foundation",
        ai_function="Connection & Interface",
        cognitive_aspect="Connection, Interface, Data I/O, Gateways",
        keywords=["connect", "interface", "foundation", "gateway", "channel", "link", "base"],
        color="#800080",  # Purple
        default_weight=0.5
    ),
    "malkuth": SefirahDefinition(
        name="Malkuth",
        hebrew="מַלְכוּת",
        meaning="Kingdom",
        ai_function="Manifestation & Execution",
        cognitive_aspect="Action, Implementation, Physical World, Results",
        keywords=["action", "execute", "manifest", "implement", "result", "do", "complete"],
        color="#964B00",  # Brown/Earth
        default_weight=0.5
    )
}


# ============================================================================
# SEFIROT PATHS - Traditional Connections
# ============================================================================

# The Three Pillars (Columns) of the Tree
PILLAR_OF_MERCY = ["keter", "chochmah", "chesed", "netzach"]
PILLAR_OF_SEVERITY = ["keter", "binah", "gevurah", "hod"]
PILLAR_OF_BALANCE = ["keter", "daat", "tiferet", "yesod", "malkuth"]

# Traditional paths between Sefirot (simplified)
SEFIROT_PATHS = [
    ("keter", "chochmah"),
    ("keter", "binah"),
    ("keter", "daat"),
    ("chochmah", "binah"),
    ("chochmah", "chesed"),
    ("binah", "gevurah"),
    ("chesed", "gevurah"),
    ("chesed", "tiferet"),
    ("gevurah", "tiferet"),
    ("tiferet", "netzach"),
    ("tiferet", "hod"),
    ("tiferet", "yesod"),
    ("netzach", "hod"),
    ("netzach", "yesod"),
    ("hod", "yesod"),
    ("yesod", "malkuth"),
    ("daat", "chesed"),
    ("daat", "gevurah"),
    ("daat", "tiferet"),
]

# ============================================================================
# DEFAULT PROFILES - Pre-configured Sefirot weightings
# ============================================================================

DEFAULT_PROFILES = {
    "balanced": {
        "keter": 0.5, "chochmah": 0.5, "binah": 0.5, "daat": 0.5,
        "chesed": 0.5, "gevurah": 0.5, "tiferet": 0.5, "netzach": 0.5,
        "hod": 0.5, "yesod": 0.5, "malkuth": 0.5
    },
    "creative": {
        "keter": 0.7, "chochmah": 0.9, "binah": 0.4, "daat": 0.6,
        "chesed": 0.8, "gevurah": 0.3, "tiferet": 0.6, "netzach": 0.5,
        "hod": 0.6, "yesod": 0.5, "malkuth": 0.4
    },
    "analytical": {
        "keter": 0.5, "chochmah": 0.4, "binah": 0.9, "daat": 0.7,
        "chesed": 0.3, "gevurah": 0.7, "tiferet": 0.6, "netzach": 0.6,
        "hod": 0.7, "yesod": 0.5, "malkuth": 0.5
    },
    "action_oriented": {
        "keter": 0.6, "chochmah": 0.5, "binah": 0.5, "daat": 0.5,
        "chesed": 0.6, "gevurah": 0.6, "tiferet": 0.5, "netzach": 0.7,
        "hod": 0.5, "yesod": 0.7, "malkuth": 0.9
    },
    "protective": {
        "keter": 0.5, "chochmah": 0.4, "binah": 0.7, "daat": 0.6,
        "chesed": 0.5, "gevurah": 0.9, "tiferet": 0.5, "netzach": 0.7,
        "hod": 0.5, "yesod": 0.6, "malkuth": 0.6
    },
    "explorer": {
        "keter": 0.6, "chochmah": 0.7, "binah": 0.4, "daat": 0.6,
        "chesed": 0.9, "gevurah": 0.3, "tiferet": 0.5, "netzach": 0.6,
        "hod": 0.5, "yesod": 0.7, "malkuth": 0.5
    },
    "communicator": {
        "keter": 0.4, "chochmah": 0.5, "binah": 0.5, "daat": 0.6,
        "chesed": 0.6, "gevurah": 0.4, "tiferet": 0.6, "netzach": 0.5,
        "hod": 0.9, "yesod": 0.6, "malkuth": 0.5
    },
    "integrated": {
        "keter": 0.7, "chochmah": 0.7, "binah": 0.7, "daat": 0.9,
        "chesed": 0.6, "gevurah": 0.6, "tiferet": 0.8, "netzach": 0.6,
        "hod": 0.6, "yesod": 0.6, "malkuth": 0.6
    }
}


# ============================================================================
# COGNITIVE TASK TO SEFIROT MAPPINGS
# ============================================================================

TASK_SEFIROT_MAPPING = {
    "problem_solving": {
        "primary": ["binah", "gevurah", "tiferet"],
        "secondary": ["chochmah", "daat"],
        "weights": {"binah": 0.8, "gevurah": 0.6, "tiferet": 0.7, "chochmah": 0.5, "daat": 0.6}
    },
    "creative_writing": {
        "primary": ["chochmah", "hod", "tiferet"],
        "secondary": ["chesed", "netzach"],
        "weights": {"chochmah": 0.8, "hod": 0.7, "tiferet": 0.6, "chesed": 0.6, "netzach": 0.5}
    },
    "data_analysis": {
        "primary": ["binah", "yesod", "malkuth"],
        "secondary": ["gevurah", "daat"],
        "weights": {"binah": 0.9, "yesod": 0.7, "malkuth": 0.6, "gevurah": 0.5, "daat": 0.6}
    },
    "learning": {
        "primary": ["chochmah", "binah", "daat"],
        "secondary": ["netzach", "chesed"],
        "weights": {"chochmah": 0.7, "binah": 0.7, "daat": 0.8, "netzach": 0.6, "chesed": 0.5}
    },
    "teaching": {
        "primary": ["hod", "tiferet", "chesed"],
        "secondary": ["binah", "daat"],
        "weights": {"hod": 0.9, "tiferet": 0.7, "chesed": 0.6, "binah": 0.5, "daat": 0.6}
    },
    "protection": {
        "primary": ["gevurah", "netzach", "yesod"],
        "secondary": ["binah", "keter"],
        "weights": {"gevurah": 0.9, "netzach": 0.7, "yesod": 0.6, "binah": 0.6, "keter": 0.5}
    },
    "exploration": {
        "primary": ["chesed", "chochmah", "yesod"],
        "secondary": ["netzach", "malkuth"],
        "weights": {"chesed": 0.8, "chochmah": 0.7, "yesod": 0.6, "netzach": 0.5, "malkuth": 0.5}
    },
    "decision_making": {
        "primary": ["keter", "daat", "tiferet"],
        "secondary": ["binah", "gevurah"],
        "weights": {"keter": 0.8, "daat": 0.7, "tiferet": 0.7, "binah": 0.6, "gevurah": 0.5}
    },
    "memory_consolidation": {
        "primary": ["netzach", "daat", "binah"],
        "secondary": ["yesod", "malkuth"],
        "weights": {"netzach": 0.8, "daat": 0.7, "binah": 0.6, "yesod": 0.5, "malkuth": 0.5}
    },
    "communication": {
        "primary": ["hod", "yesod", "tiferet"],
        "secondary": ["chesed", "daat"],
        "weights": {"hod": 0.8, "yesod": 0.7, "tiferet": 0.6, "chesed": 0.5, "daat": 0.5}
    }
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_sefirah_info(sefirah_name: str) -> Optional[SefirahDefinition]:
    """Get detailed information about a specific Sefirah"""
    return SEFIROT_DEFINITIONS.get(sefirah_name.lower())


def get_profile(profile_name: str) -> Optional[Dict[str, float]]:
    """Get a pre-configured Sefirot profile"""
    return DEFAULT_PROFILES.get(profile_name.lower())


def get_task_sefirot(task_type: str) -> Optional[Dict]:
    """Get Sefirot weights for a specific cognitive task"""
    return TASK_SEFIROT_MAPPING.get(task_type.lower())


def suggest_sefirot_for_content(content: str) -> Dict[str, float]:
    """
    Analyze content and suggest appropriate Sefirot weights.
    This is a keyword-based heuristic approach.
    """
    content_lower = content.lower()
    weights = {name: 0.3 for name in SEFIROT_DEFINITIONS.keys()}  # Start low
    
    for name, definition in SEFIROT_DEFINITIONS.items():
        # Check for keyword matches
        for keyword in definition.keywords:
            if keyword in content_lower:
                weights[name] = min(1.0, weights[name] + 0.15)
    
    # Normalize to keep reasonable values
    max_weight = max(weights.values())
    if max_weight > 0:
        for name in weights:
            weights[name] = min(1.0, weights[name])
    
    return weights


def calculate_pillar_balance(weights: Dict[str, float]) -> Dict[str, float]:
    """Calculate the balance between the three pillars"""
    mercy_avg = sum(weights.get(s, 0.5) for s in PILLAR_OF_MERCY) / len(PILLAR_OF_MERCY)
    severity_avg = sum(weights.get(s, 0.5) for s in PILLAR_OF_SEVERITY) / len(PILLAR_OF_SEVERITY)
    balance_avg = sum(weights.get(s, 0.5) for s in PILLAR_OF_BALANCE) / len(PILLAR_OF_BALANCE)
    
    return {
        "pillar_of_mercy": mercy_avg,
        "pillar_of_severity": severity_avg,
        "pillar_of_balance": balance_avg
    }


def get_visualization_color(weights: Dict[str, float]) -> str:
    """Get a blended color for visualization based on Sefirot weights"""
    # Simple RGB blending based on top 3 weighted Sefirot
    sorted_weights = sorted(weights.items(), key=lambda x: x[1], reverse=True)[:3]
    
    r, g, b = 0, 0, 0
    total_weight = sum(w for _, w in sorted_weights)
    
    for sefirah, weight in sorted_weights:
        definition = SEFIROT_DEFINITIONS[sefirah]
        color = definition.color
        
        # Convert hex to RGB
        cr = int(color[1:3], 16)
        cg = int(color[3:5], 16)
        cb = int(color[5:7], 16)
        
        # Blend weighted
        blend = weight / total_weight if total_weight > 0 else 0
        r += int(cr * blend)
        g += int(cg * blend)
        b += int(cb * blend)
    
    return f"#{min(255, r):02x}{min(255, g):02x}{min(255, b):02x}"


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("SEFIROT CONFIGURATION")
    print("="*60 + "\n")
    
    # Display all Sefirot
    print("THE TEN SEFIROT PLUS DA'AT:\n")
    for name, definition in SEFIROT_DEFINITIONS.items():
        print(f"{definition.name} ({definition.hebrew}) - {definition.meaning}")
        print(f"  AI Function: {definition.ai_function}")
        print(f"  Cognitive Aspect: {definition.cognitive_aspect}")
        print(f"  Color: {definition.color}")
        print()
    
    # Display profiles
    print("\nDEFAULT PROFILES:\n")
    for profile_name, weights in DEFAULT_PROFILES.items():
        dominant = max(weights.items(), key=lambda x: x[1])
        print(f"  {profile_name}: dominant={dominant[0]} ({dominant[1]:.1f})")
    
    # Test content analysis
    print("\n\nCONTENT ANALYSIS TEST:")
    test_content = "I need to analyze this problem carefully and find a creative solution."
    weights = suggest_sefirot_for_content(test_content)
    print(f"\nContent: '{test_content}'")
    print(f"Suggested weights: {weights}")
    
    # Test pillar balance
    balance = calculate_pillar_balance(weights)
    print(f"\nPillar balance: {balance}")
