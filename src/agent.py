import random
from .environment import Environment, Room

class Agent:
    def __init__(self, env: Environment, position: int = 0):
        self.env = env
        self.position = position
        self.steps = 0
        self.cleaned = 0
        self.initial_energy = 2.5 * len(env.rooms)
        self.energy = self.initial_energy
        self.action_sequence = []

    def perceive(self):
        """Return complete percept information"""
        current_room = self.env.rooms[self.position]
        return {
            'room_index': self.position,
            'is_dirty': current_room.is_dirty(),
            'dirtiness_level': current_room.dirtiness,
            'remaining_energy': self.energy
        }

    def can_suck(self):
        """Check if agent has enough energy to clean current room"""
        return self.energy >= self.env.rooms[self.position].dirtiness

    def can_move(self):
        """Check if agent has enough energy to move"""
        return self.energy >= 2

    def suck(self):
        """Clean current room if possible"""
        room = self.env.rooms[self.position]
        if room.is_dirty() and self.can_suck():
            energy_cost = room.dirtiness
            room.clean()
            self.energy -= energy_cost
            self.cleaned += 1
            self.action_sequence.append(f"Suck (room {self.position}, cost: {energy_cost})")
            return True
        return False

    def move_right(self):
        """Move to next room if possible and not at boundary"""
        if self.can_move() and self.position < len(self.env.rooms) - 1:
            self.position += 1
            self.energy -= 2
            self.action_sequence.append(f"MoveRight to room {self.position}")
            return True
        return False

    def move_left(self):
        """Move to previous room if possible and not at boundary"""
        if self.can_move() and self.position > 0:
            self.position -= 1
            self.energy -= 2
            self.action_sequence.append(f"MoveLeft to room {self.position}")
            return True
        return False

    def act(self):
        raise NotImplementedError

class BaselineAgent(Agent):
    def act(self):
        """Baseline behavior: If dirty and can clean -> Suck, else move right (or left at boundary)"""
        percept = self.perceive()
        
        # If current room is dirty and we can afford to clean it
        if percept['is_dirty'] and self.can_suck():
            self.suck()
        else:
            # Try to move right first, then left at boundary
            if not self.move_right():
                self.move_left()
        
        self.steps += 1

class HeuristicAgent(Agent):
    def act(self):
        """Heuristic behavior with improved energy management"""
        percept = self.perceive()
        
        # If current room is dirty and we can afford to clean it
        if percept['is_dirty'] and self.can_suck():
            self.suck()
        else:
            # Randomly choose direction, but respect boundaries
            if random.random() < 0.5:
                if not self.move_right():
                    self.move_left()
            else:
                if not self.move_left():
                    self.move_right()
        
        self.steps += 1
