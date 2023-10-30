import os

class APIKeys:
    def get_keys(self):

        self.openai_api_key = os.getenv("OpenAI_API")
        self.elevenlabs_api_key = os.getenv("ElevenLabs_API")