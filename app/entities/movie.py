from dataclasses import dataclass


@dataclass
class Movie:
    id: str
    title: str
    description: str
    release_year: int
    watched: bool = False
