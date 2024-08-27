from dataclasses import dataclass
from typing import List

@dataclass
class ComponentMessage:
    input: List[float]
    health_check: bool

@dataclass
class ComponentResponse:
    output: List[float]
    prediction: int
