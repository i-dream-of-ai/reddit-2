import asyncio
from typing import Sequence
from autogen_core import CancellationToken
from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import TextMessage, ChatMessage
from autogen_agentchat.base import Response


class CountingAgent(BaseChatAgent):
    """An agent that returns a new number by adding 1 to the last number in the input messages."""

    async def on_messages(
        self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken
    ) -> Response:
        if len(messages) == 0:
            last_number = 0  # Start from 0 if no messages are given.
        else:
            assert isinstance(messages[-1], TextMessage)
            last_number = int(
                messages[-1].content
            )  # Otherwise, start from the last number.
        return Response(
            chat_message=TextMessage(content=str(last_number + 1), source=self.name)
        )

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        pass

    @property
    def produced_message_types(self) -> Sequence[type[ChatMessage]]:
        return (TextMessage,)


class NestedCountingAgent(BaseChatAgent):
    """An agent that increments the last number in the input messages
    multiple times using a nested counting team."""

    def __init__(self, name: str, counting_team: RoundRobinGroupChat) -> None:
        super().__init__(name, description="An agent that counts numbers.")
        self._counting_team = counting_team

    async def on_messages(
        self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken
    ) -> Response:
        # Run the inner team with the given messages and returns the last message produced by the team.
        result = await self._counting_team.run(
            task=messages, cancellation_token=cancellation_token
        )
        # To stream the inner messages, implement `on_messages_stream` and use that to implement `on_messages`.
        assert isinstance(result.messages[-1], TextMessage)
        return Response(
            chat_message=result.messages[-1],
            inner_messages=result.messages[len(messages) : -1],
        )

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        # Reset the inner team.
        await self._counting_team.reset()

    @property
    def produced_message_types(self) -> Sequence[type[ChatMessage]]:
        return (TextMessage,)


async def main() -> None:
    # Create a team of two counting agents as the inner team.
    counting_agent_1 = CountingAgent(
        "counting_agent_1", description="An agent that counts numbers."
    )
    counting_agent_2 = CountingAgent(
        "counting_agent_2", description="An agent that counts numbers."
    )
    counting_team = RoundRobinGroupChat(
        [counting_agent_1, counting_agent_2], max_turns=5
    )
    # Create a nested counting agent that takes the inner team as a parameter.
    nested_counting_agent = NestedCountingAgent("nested_counting_agent", counting_team)
    # Run the nested counting agent with a message starting from 1.
    response = await nested_counting_agent.on_messages(
        [TextMessage(content="1", source="user")], CancellationToken()
    )
    assert response.inner_messages is not None
    for message in response.inner_messages:
        print(message)
    print(response.chat_message)


asyncio.run(main())
