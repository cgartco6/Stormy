import importlib
from .brain import Brain
from .personality import Personality
from .agent_factory import AgentFactory

class HarnessEngineer:
    def __init__(self):
        self.brain = Brain(Personality())
        self.factory = AgentFactory()

    def improve_agent(self, agent) -> object:
        """Analyze agent's performance and generate an improved version."""
        # Get agent's code (if it's a module, read source)
        try:
            source = inspect.getsource(agent.__class__)
        except:
            return None
        prompt = f"""
        Here is the code of an AI agent:
        {source}

        Suggest improvements to make it faster, more accurate, or handle edge cases better.
        Return the full improved code.
        """
        new_code = self.brain.generate(prompt)
        # Write new code to a temporary file, then import and instantiate
        # For simplicity, we'll just use the factory to create a new agent with the description of its purpose
        # In production, you'd diff and test before replacing.
        return self.factory.create_agent(agent.__doc__ or "General agent")
