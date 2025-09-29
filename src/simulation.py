import random
from .agent import BaselineAgent, HeuristicAgent
from .environment import Environment

def simulate(agent_class, n_rooms=5, max_steps=100):
    """
    Run simulation with proper termination conditions:
    1. All rooms clean and no meaningful actions left
    2. Agent out of energy for any action
    3. Maximum steps reached
    """
    env = Environment(n_rooms)
    agent = agent_class(env)

    history = []
    step = 0
    
    while step < max_steps:
        # Check if agent can take any action
        can_act = (agent.can_suck() and env.rooms[agent.position].is_dirty()) or agent.can_move()
        
        if not can_act:
            # Agent is out of usable energy
            break
            
        # Agent acts
        agent.act()
        
        # Environment step: dirt reappearance
        env.step_dirt_reappearance()
        
        # Record state
        history.append([room.dirtiness for room in env.rooms])
        step += 1
        
        # Check if all rooms are clean and agent has no reason to move
        if env.all_clean():
            # If all clean, check if agent should continue (energy conservation)
            # For baseline: stop when all clean
            break
    
    return history, agent

if __name__ == "__main__":
    print("Baseline Agent Simulation:")
    history, agent = simulate(BaselineAgent)
    print(f"Steps: {len(history)}, Cleaned: {agent.cleaned}, Energy: {agent.energy:.1f}")

    print("\nHeuristic Agent Simulation:")
    history, agent = simulate(HeuristicAgent)
    print(f"Steps: {len(history)}, Cleaned: {agent.cleaned}, Energy: {agent.energy:.1f}")
