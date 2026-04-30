import anthropic
import json
from typing import Optional


class BaseAgent:
    """Base class for all agents in the pipeline."""

    def __init__(self, name: str, system_prompt: str, model: str = "claude-opus-4-5"):
        self.name = name
        self.system_prompt = system_prompt
        self.model = model
        self.client = anthropic.Anthropic()

    def run(self, user_message: str, context: Optional[dict] = None) -> str:
        """Run the agent with optional context from previous agents."""
        messages = []

        if context:
            context_str = "\n\n=== Context from Previous Agents ===\n"
            for key, value in context.items():
                context_str += f"\n[{key}]\n{value}\n"
            user_message = context_str + "\n\n=== Your Task ===\n" + user_message

        messages.append({"role": "user", "content": user_message})

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=self.system_prompt,
            messages=messages,
        )

        return response.content[0].text

    def run_json(self, user_message: str, context: Optional[dict] = None) -> dict:
        """Run agent and parse JSON response."""
        result = self.run(user_message, context)
        # Strip markdown code fences if present
        clean = result.strip()
        if clean.startswith("```"):
            clean = clean.split("\n", 1)[1]
            clean = clean.rsplit("```", 1)[0]
        return json.loads(clean.strip())
