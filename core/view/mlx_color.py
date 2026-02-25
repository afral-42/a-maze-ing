from dataclasses import dataclass


@dataclass(frozen=True)
class Color:
    a: int
    r: int
    g: int
    b: int
