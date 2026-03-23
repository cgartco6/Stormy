import asyncio
from core.brain import Brain
from core.personality import Personality
from core.memory import Memory
from modules.music import MusicPlayer
from modules.region import RegionManager
from modules.compliance import ComplianceManager
from interfaces.voice.stt import STT
from interfaces.voice.tts import TTS

class Stormy:
    def __init__(self):
        self.personality = Personality()
        self.brain = Brain(self.personality)
        self.memory = Memory()
        self.music = MusicPlayer()
        self.region = RegionManager()
        self.compliance = ComplianceManager(self.region)
        self.stt = STT()
        self.tts = TTS()

    async def handle_command(self, text):
        # Route to appropriate module
        if "play bok radio" in text.lower():
            self.music.play_bok_radio()
            return "Playing Bok Radio, hotstuff!"
        elif "play my station" in text.lower():
            # parse station name
            pass
        elif "navigate" in text.lower():
            # navigation stub
            pass
        else:
            # Use LLM for general conversation
            response = self.brain.generate(text, context=self.memory.search(text))
            return response

    async def run_voice(self):
        print("Stormy is ready. Say 'Stormy' to wake me.")
        while True:
            # Wake word detection
            text = await self.stt.listen()
            if text:
                resp = await self.handle_command(text)
                self.tts.speak(resp)

    def run_cli(self):
        print("Stormy CLI. Type 'exit' to quit.")
        while True:
            user = input("You: ")
            if user.lower() == "exit":
                break
            resp = asyncio.run(self.handle_command(user))
            print(f"Stormy: {resp}")

if __name__ == "__main__":
    stormy = Stormy()
    # Choose mode: 'voice' or 'cli'
    stormy.run_cli()
