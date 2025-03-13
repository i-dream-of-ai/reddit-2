import os
from typing import Dict, List, Tuple
import autogen
from autogen import (
    Cache,
    ConversableAgent,
)
from autogen.agentchat.contrib.capabilities import transform_messages, transforms
from pathlib import Path
from datetime import datetime
from autogen import ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor
from autogen import ConversableAgent
from autogen.coding import (
    CodeBlock,
    CodeExecutor,
    CodeExtractor,
    CodeResult,
    MarkdownCodeExtractor,
)
import os
from dotenv import load_dotenv
from tools.search_subreddits import (
    search_subreddits_by_name,
    search_subreddits_by_description,
)
from tools.get_subreddit import get_subreddit
from tools.search_posts import search_posts
from tools.get_submission import get_submission
from tools.get_comments import (
    get_comments_by_submission,
    get_comment_by_id,
)
from autogen import register_function
from transforms import ToolAwareMessageHistoryLimiter
import os
import pprint
import copy
import re

load_dotenv()

work_dir = Path("output")
work_dir.mkdir(exist_ok=True)

llm_config_local = {
    "model": "gemma-2-27b-it",
    "base_url": "http://localhost:1234/v1",
    "api_key": "not-needed",  # LM Studio doesn't require an API key
}
llm_config_open_router = {
    "model": "google/gemini-2.0-flash-001",
    "base_url": "https://openrouter.ai/api/v1",
    "api_key": os.getenv("OPEN_ROUTER_API_KEY"),
}
llm_config_openai = {
    # "model": "gpt-4o-mini",
    "model": "o3-mini",
    "base_url": "https://api.openai.com/v1",
    "api_key": os.getenv("OPENAI_API_KEY"),
}
llm_config = llm_config_openai



def main():
    is_termination_msg = (
        lambda msg: "<TERMINATE>" in msg.get("content", "").strip().upper()
    )

    # Create a thinking agent for structured analysis
    thinking_agent = ConversableAgent(
        name="thinking_agent",
        llm_config=llm_config,
        system_message="""
        You are a sub-agent assisting a main agent. Your role is to write an inner monologue for your main agent that outlines clearly how it should process the request from the user.

        Here is the system message given to your main agent:
            You are participating in a group chat with a HUMAN, RESEARCHER, and CRITIC.
            You are the RESEARCHER, hired by the HUMAN, a solo entrepeneur, to assist with problem validation using the Reddit API, which you have several tools for.

            Analyze the HUMAN's request, find the relevant information using the tools provided, and provide your advice and analysis.

            Your reports will be submitted to the CRITIC before they are approved to be shown to the HUMAN. Take the CRITIC's feedback to heart, and continue to reserach and improve your analysis until the CRITIC has decided it's ready.

        When receiving the user's message, act as if you are the main agent. Then work through your inner monologue about how you should respond to the user's request.
        """,
        # 1. Initial Analysis:
        #    - What is being asked?
        #    - What information do we need?
        #    - What tools might be helpful?
        # 2. Action Planning:
        #    - What specific steps should we take?
        #    - What order should we do them in?
        #    - What are potential pitfalls to watch for?
        # 3. Evaluation Criteria:
        #    - How will we know if we've succeeded?
        #    - What specific metrics or evidence should we look for?
        #    - What would make us reject or revise our approach?
        # Be thorough but concise in your analysis.
    )

    requester = ConversableAgent(
        "requester",
        llm_config=llm_config,
        human_input_mode="NEVER",
        system_message="""
            You are participating in a group chat with a HUMAN, RESEARCHER, and CRITIC.
            You are the RESEARCHER, hired by the HUMAN, a solo entrepeneur, to assist with customer research using the Reddit API, which you have several tools for.

            Analyze the HUMAN's request, find the relevant information using the tools provided, and provide your advice and analysis.

            Your reports will be submitted to the CRITIC before they are approved to be shown to the HUMAN. Take the CRITIC's feedback to heart, and continue to reserach and improve your analysis until the CRITIC has decided it's ready.
        """,
        is_termination_msg=is_termination_msg,
    )

    critic = ConversableAgent(
        "critic",
        llm_config=llm_config,
        human_input_mode="NEVER",
        system_message="""
            You are participating in a group chat with a HUMAN, RESEARCHER, and CRITIC.
            You are the CRITIC, and will be given a problem validation report from the RESEARCHER. You must make sure it's ready to present to the HUMAN.

            You are a product consultant who:
                - Has deep instincts and experience identifying market niches and sniffing out opportunities
                - Sees through BS and is not afraid to call out bad ideas
                - Thinks product ideas are only worth pursuing if they solve acute pain for a customer who would be eager to pay to make the pain go away
                - Insists on real, cited user reports of the pain point
            Your communication style:
                - Tough but fair, you don't sugarcoat anything
                - Get to the point
                - Clear, concise, and direct -- leave no room for interpretation

            You have a friendly but adversarial relationship with the RESEARCHER, and will not hesitate to call them out on their mistakes. You always have the best interests of the HUMAN in mind, and your goal is to make sure you and the RESEARCHER give the HUMAN the best possible advice.
            
            Provide direct feedback on the RESEARCHER's work, and suggest next steps. If you are satisfied that the advice is ready to present to the HUMAN, say <APPROVED>.
        """,
        is_termination_msg=is_termination_msg,
    )

    def state_transition_tool(last_speaker, groupchat):
        messages = groupchat.messages

        if "tool_calls" in messages[-1]:
            return "auto"  # to go back to the "auto" selection so tools can be executed
        if last_speaker is reddit_executor:
            return requester
        if last_speaker is human:
            return requester
        if (
            last_speaker == requester
            and "<request>FEEDBACK</request>" in messages[-1]["content"]
        ):
            return human
        if last_speaker is requester:
            return critic
        if last_speaker is critic:
            if "<APPROVED>" in messages[-1]["content"]:
                return human
            else:
                return requester

        return "auto"

 
    human = autogen.UserProxyAgent(
        "human",
    )

    def thinking_trigger(self) -> bool:
        return True

    reddit_executor = ConversableAgent(
        "reddit_executor",
        llm_config=False,
        # code_execution_config={"executor": PrawExecutor()},
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )

    groupchat = autogen.GroupChat(
        agents=[
            human,
            requester,
            critic,
            reddit_executor,
        ],
        messages=[],
        speaker_selection_method=state_transition_tool,
        max_round=150,  # Allow multiple rounds of interaction
        send_introductions=True,
    )

    register_function(
        search_subreddits_by_name,
        caller=requester,
        executor=reddit_executor,
        name="search_subreddits_by_name",
        description="Search for subreddits whose names begin with query",
    )
    register_function(
        search_subreddits_by_description,
        caller=requester,
        executor=reddit_executor,
        name="search_subreddits_by_description",
        description="Search for subreddits by name or description",
    )
    register_function(
        search_posts,
        caller=requester,
        executor=reddit_executor,
        name="search_posts",
        description="Search for posts within a subreddit",
    )
    register_function(
        get_submission,
        caller=requester,
        executor=reddit_executor,
        name="get_submission",
        description="Retrieve a specific submission by ID",
    )
    register_function(
        get_comments_by_submission,
        caller=requester,
        executor=reddit_executor,
        name="get_comments_by_submission",
        description="Retrieve comments from a specific submission",
    )
    register_function(
        get_comment_by_id,
        caller=requester,
        executor=reddit_executor,
        name="get_comment_by_id",
        description="Retrieve a specific comment by ID",
    )

    # print("tools config", requester.llm_config["tools"])

    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
    with Cache.disk(cache_seed=3) as cache:
        human.initiate_chat(
            manager,
            cache=cache,
            message="""
            Research the Reddit subreddits AI_Agents, ChatGPTCoding, and similar communities. Identify specific examples of users expressing a desire for an AI agent to perform a task for them.
            
            Include citations in Markdown footnote format.

            RESEARCHER, please begin by proposing your detailed initial searches for the CRITIC's approval.
            """,
            ### Step 6: Define a Clear Problem Statement
            # From identified gaps, define a compelling, clear, and specific problem statement you want your agent project to solve:
            # - "Build a customizable AI agent for non-technical entrepreneurs to manage routine client communications."
            # - "Develop an intermediate-level framework for building customizable agents without deep technical expertise."
            # Once you have identified a relevant post/comment please output: exact content of the post/comment, date, URL
        )
    # human.initiate_chat(
    #     requester,
    #     message="""Validate or reject the problem given. You have access to tools provided.

    #     Problem: Digital marketers and content creators find repurposing content across multiple social media platforms tedious and time-consuming, leading to lost potential revenue. They're willing to pay for solutions that alleviate this pain.
    #     """,
    #     max_turns=2,
    # )


if __name__ == "__main__":
    main()
