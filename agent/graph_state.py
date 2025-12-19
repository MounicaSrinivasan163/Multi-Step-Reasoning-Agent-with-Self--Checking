from typing import Dict, Any, List
from dataclasses import dataclass, field

@dataclass
class GraphState:
    question: str
    plan: Dict[str, Any] = field(default_factory=dict)
    executor_output: Dict[str, Any] = field(default_factory=dict)
    verification: Dict[str, Any] = field(default_factory=dict)
    checks: List[Dict[str, Any]] = field(default_factory=list)
    retries: int = 0
    status: str = "running"
