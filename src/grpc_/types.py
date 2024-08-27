class ComponentMessage:
    input: list[float]
    health_check: bool

class ComponentResponse:
    output: list[float]
    prediction: int
