import json
from typing import List, Dict, Any
from .brain import Brain
from .personality import Personality

class StrategicPlanner:
    def __init__(self):
        self.brain = Brain(Personality())

    def plan(self, task: str, context: Dict, available_agents: Dict) -> List[Dict]:
        """Return a plan: list of steps, each with agent and instruction."""
        agent_descriptions = "\n".join([f"- {name}: {self._describe_agent(agent)}" for name, agent in available_agents.items()])
        prompt = f"""
        Task: {task}
        Context: {json.dumps(context)}
        Available agents:
        {agent_descriptions}

        Create a step‑by‑step plan using these agents. Output as JSON list of objects with keys: "agent", "instruction", "description".
        """
        response = self.brain.generate(prompt)
        try:
            plan = json.loads(response)
        except:
            # Fallback: single agent
            plan = [{"agent": "stormy", "instruction": task, "description": "Main agent handles it"}]
        return plan

    def _describe_agent(self, agent) -> str:
        # Use docstring or generate a description
        return getattr(agent, "description", "General purpose agent")
