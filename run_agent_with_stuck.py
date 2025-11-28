"""
Example: Run a Conversation with stuck detection enabled.
"""
import os
import asyncio
from pydantic import SecretStr

from openhands.sdk import LLM, Conversation, Agent
from sdk.conversation.stuck_detector import StuckDetector
from openhands.sdk import Agent


def main():
    # Configure the LLM
    api_key = os.getenv("LLM_API_KEY")
    assert api_key, "LLM_API_KEY must be set"
    model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    base_url = os.getenv("LLM_BASE_URL")

    llm = LLM(
        usage_id="agent",
        model=model,
        base_url=base_url,
        api_key=SecretStr(api_key),
    )

    # Instantiate default agent
    agent = Agent(llm=llm)

    # Create conversation with stuck detection (default-on)
    conversation = Conversation(
        agent=agent,
        callbacks=[],
        workspace=os.getcwd(),
        stuck_detection=True,
    )

    # Attach the stuck detector
    conversation.stuck_detector = StuckDetector(conversation.state)

    # Send a starter prompt
    conversation.send_message("Please start your task.")

    # Run the conversation
    conversation.run()

    # Check for stuck condition
    if conversation.stuck_detector.is_stuck():
        print("⚠️ Agent got stuck. Halting execution.")
    else:
        print("✅ Conversation completed without being stuck.")


if __name__ == "__main__":
    main()
