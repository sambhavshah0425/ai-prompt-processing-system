import asyncio
from config import Config

class AIService:

    @staticmethod
    async def call_ai_async(prompt):
        """
        Mock async AI response
        """

        await asyncio.sleep(1)

        return f"Mocked AI response for: '{prompt}'"

    @staticmethod
    def call_ai_sync(prompt):
        """
        Mock sync AI response
        """

        return asyncio.run(
            AIService.call_ai_async(prompt)
        )