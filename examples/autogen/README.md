# Autogen with MCP server

This example demonstrates how to use the MCP server with AutoGen agents.

> **NOTE**: There seems to be a bug in autogen-mcp that causes Pydantic types with refs to raise an error. To use this example, comment out the `search_subreddits` tool in `tools/__init__.py`.

## Running the example

Add your OpenAI API key to an `.env` file:

```bash
OPENAI_API_KEY=<your-openai-api-key>
```

Install the dependencies:

```bash
uv sync
```

Run the example:

```bash
uv run main.py
```

## Example output

> Here are some interesting Reddit posts about AI agents:
>
> 1. **[Moore's Law for AI Agents](https://i.redd.it/2zht3052qupe1.png)**  
>    _Score: 76 | Comments: 42_  
>    _(Posted on March 20, 2025)_
>
> 2. **[custom AI agents](https://www.reddit.com/r/BlackboxAI_/comments/1jfgzxu/custom_ai_agents/)**  
>    _Score: 5 | Comments: 2_  
>    _(Posted on March 20, 2025)_
>
> 3. **[Stop Calling AI Automation "AI Agents" – It’s Misleading!](https://i.redd.it/wg127obp2wpe1.gif)**  
>    _Score: 2 | Comments: 0_  
>    _(Posted on March 20, 2025)_
>
> 4. **[Building an AI Agent with Memory and Adaptability](https://www.reddit.com/r/PromptEngineering/comments/1jfs3mt/building_an_ai_agent_with_memory_and_adaptability/)**  
>    _Score: 85 | Comments: 6_  
>    _(Posted on March 20, 2025)_
>
> 5. **[AI Mailing Agent MVP](https://www.reddit.com/r/SaaS/comments/1jfqrhk/ai_mailing_agent_mvp/)**  
>    _Score: 3 | Comments: 0_  
>    _(Posted on March 20, 2025)_
>
> 6. **[Moore's Law for AI Agents: if the length of tasks AIs can do continues doubling every 7 months, then the singularity is near](https://i.redd.it/hua9inf9jupe1.png)**  
>    _Score: 14 | Comments: 7_  
>    _(Posted on March 20, 2025)_
>
> 7. **[Optimizing AI Agents with Open-source High-Performance RAG framework](https://www.reddit.com/r/AI_Agents/comments/1jexngk/optimizing_ai_agents_with_opensouce/)**  
>    _Score: 17 | Comments: 5_  
>    _(Posted on March 19, 2025)_
>
> 8. **[Built an AI Agent to find and apply to jobs automatically](https://www.reddit.com/r/RemoteJobs/comments/1jfxfj9/built_an_ai_agent_to_find_and_apply_to_jobs/)**  
>    _Score: 73 | Comments: 31_  
>    _(Posted on March 20, 2025)_
>
> Please let me know if you need further information or details on any specific post! TERMINATE
