import argparse
from simulation import simulate
from agent import BaselineAgent, HeuristicAgent

def main():
    parser = argparse.ArgumentParser(description="Vacuum Agent Simulation")
    parser.add_argument("--agent", choices=["baseline", "heuristic"], default="baseline")
    parser.add_argument("--rooms", type=int, default=5)
    parser.add_argument("--steps", type=int, default=100)
    args = parser.parse_args()

    agent_class = BaselineAgent if args.agent == "baseline" else HeuristicAgent
    history, agent = simulate(agent_class, args.rooms, args.steps)
    
    # Print beautiful header
    print("\n" + "=" * 60)
    print(f"   {args.agent.upper()} AGENT SIMULATION")
    print("=" * 60)
    print(f"  Environment:     {args.rooms} rooms")
    print(f"  Max Steps:       {args.steps}")
    print(f"  Initial Energy:  {agent.initial_energy:.1f} units")
    print("-" * 60)
    
    # Print step-by-step history with better formatting
    print("\n   SIMULATION PROGRESS:")
    print("-" * 60)
    
    for step, state in enumerate(history):
        # Format room states with visual indicators
        room_display = []
        for i, dirt in enumerate(state):
            if dirt == 0:
                room_display.append("CLEAN")  # Clean room
            elif dirt <= 2:
                room_display.append(f"D{dirt}")  # Light dirt
            elif dirt <= 4:
                room_display.append(f"D{dirt}")  # Medium dirt
            else:
                room_display.append(f"D{dirt}")  # Heavy dirt
        
        print(f"  Step {step + 1:2d}: [{'  '.join(room_display)}]")
    
    # Beautiful results summary
    print("\n" + "=" * 60)
    print("   SIMULATION RESULTS")
    print("=" * 60)
    
    # Final room visualization
    final_states = [room.dirtiness for room in agent.env.rooms]
    room_viz = []
    for i, dirt in enumerate(final_states):
        if i == agent.position:
            if dirt == 0:
                room_viz.append("AGENT")  # Agent in clean room
            else:
                room_viz.append(f"AGENT-D{dirt}")  # Agent in dirty room
        else:
            if dirt == 0:
                room_viz.append("CLEAN")
            else:
                room_viz.append(f"D{dirt}")
    
    print(f"  Final Layout:    [{'  '.join(room_viz)}]")
    print(f"  Agent Position:  Room {agent.position}")
    print()
    print(f"  Rooms Cleaned:     {agent.cleaned}")
    print(f"  Energy Consumed:    {agent.initial_energy - agent.energy:.1f} / {agent.initial_energy:.1f}")
    print(f"  Energy Remaining:   {agent.energy:.1f}")
    print(f"  Steps Taken:       {agent.steps}")
    print(f"  Simulation Steps:   {len(history)}")
    
    # Action sequence with better formatting
    print("\n" + "=" * 60)
    print("   ACTION SEQUENCE")
    print("=" * 60)
    
    if agent.action_sequence:
        for i, action in enumerate(agent.action_sequence, 1):
            # Add text indicators for different actions
            if "Suck" in action:
                prefix = "[CLEAN]"
            elif "MoveRight" in action:
                prefix = "[RIGHT]"
            elif "MoveLeft" in action:
                prefix = "[LEFT] "
            else:
                prefix = "[ACTION]"
            
            print(f"  {i:2d}. {prefix} {action}")
    else:
        print("  No actions taken")
    
    # Termination reason with status indicators
    print("\n" + "=" * 60)
    print("   TERMINATION REASON")
    print("=" * 60)
    
    all_clean = agent.env.all_clean()
    can_act = (agent.can_suck() and agent.env.rooms[agent.position].is_dirty()) or agent.can_move()
    
    if all_clean:
        print("  STATUS: SUCCESS - All rooms are clean!")
        print("  RESULT: Mission accomplished!")
    elif not can_act:
        print("  STATUS: ENERGY DEPLETED - Agent ran out of energy")
        print(f"  REASON: Remaining energy ({agent.energy:.1f}) insufficient for any action")
    elif len(history) >= args.steps:
        print("  STATUS: TIME LIMIT - Maximum steps reached")
        print("  ADVICE: Consider increasing step limit for better performance")
    else:
        print("  STATUS: UNKNOWN - Unexpected termination")
    
    print("=" * 60)
    print("   SIMULATION COMPLETE")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
