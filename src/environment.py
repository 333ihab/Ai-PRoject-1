import random

class Room:
    def __init__(self, index: int, dirtiness: int = 0):
        self.index = index
        self.dirtiness = dirtiness  # 0 = clean, 1–5 = dirt level

    def is_dirty(self) -> bool:
        return self.dirtiness > 0

    def clean(self):
        self.dirtiness = 0

    def maybe_get_dirty(self, prob: float = 0.1):
        if self.dirtiness == 0 and random.random() < prob:
            self.dirtiness = random.randint(1, 5)


class Environment:
    def __init__(self, n_rooms: int, dirt_prob: float = 0.5):
        self.rooms = []
        for i in range(n_rooms):
            dirt = random.randint(1, 5) if random.random() < dirt_prob else 0
            self.rooms.append(Room(i, dirt))

    def all_clean(self) -> bool:
        return all(not r.is_dirty() for r in self.rooms)

    def step_dirt_reappearance(self):
        for r in self.rooms:
            r.maybe_get_dirty(prob=0.1)
