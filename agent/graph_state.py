from typing import Dict, Any
from dataclasses import dataclass, field

@dataclass
class GraphState:
    question: str
    plan: Dict[str, Any] = field(default_factory=dict)
    executor_output: Dict[str, Any] = field(default_factory=dict)
    verification: Dict[str, Any] = field(default_factory=dict)
    retries: int = 0
    status: str = "running"
