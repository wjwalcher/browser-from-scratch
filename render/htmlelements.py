from dataclasses import dataclass, field
from typing import List

@dataclass
class Text:
    text: str
    parent: any
    children: List = field(default_factory=lambda: [])

    def __repr__(self):
        return repr(self.text)

@dataclass
class Element:
    tag: str
    parent: any
    attributes: dict()
    children: List = field(default_factory=lambda: [])

    def __repr__(self):
        return "<" + self.tag + ">"