# LangGraph Examples

These examples are designed to give you a clear understanding of why and when we need LangGraph.

The same AI workflow is implemented in two ways:

1. Without LangGraph
2. With LangGraph

By comparing both implementations, you can clearly understand:

- What problem LangGraph solves
- Why workflow management becomes difficult as complexity grows
- How LangGraph manages state, branching, loops, and execution
- When using LangGraph actually makes sense

The goal is not just to learn the syntax, but to build a clear mental model of LangGraph.

Added MongoDB checkpointing
  -I have added mongodb check pointing in new commit
  -Added a conditional route which first search from the same thread from mongodb if it finds then     give result from there if not it does the web search and  stores in mongodb.
  -This example has running both web searching and storing data in database and then in the next part of string it is fetching the data from database and shows findings from the mongodb instead of web searching.


# Mem0 orchestration example
Mem0 + Qdrant AI Memory

A simple AI chatbot project exploring long-term memory using Mem0, Qdrant, embeddings, and LLMs.

What Problem Does Mem0 Solve?

A vector database like Qdrant can store embeddings and search for similar information, but it doesn't decide:

What information is worth remembering?
Should a memory be added or updated?
Should an old memory be deleted?
Is the information already stored?

Without Mem0, we would need to build this memory-management logic ourselves.

Mem0 provides the memory-management layer on top of the vector database.

Architecture
                 User Message
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
       Groq LLM                 Mem0
     Chat Response          Memory Management
                                  │
                                  ▼
                          Mem0 Internal LLM
                          Memory Reasoning
                                  │
                                  ▼
                         ADD / UPDATE /
                         DELETE / NONE
                                  │
                                  ▼
                              Embedder
                                  │
                                  ▼
                              Qdrant
                           Vector Database
Technologies
Python — Application
Groq — Conversational LLM
Mem0 — Long-term memory management
Nex N2.5 Pro — Mem0's internal LLM
OpenAI text-embedding-3-small — Embeddings
Qdrant — Vector database
OpenRouter — LLM/embedding API access
Example
User: I am a backend developer.

User: I have started working with Python.

User: I mainly work with Node.js now.

The memory system needs to understand whether new information should be added, updated, deleted, or ignored instead of simply storing every message.

That's the main concept explored in this project.

Setup

Create a .env file:

OPENROUTER_API_KEY=your_openrouter_api_key
QDRANT_API_KEY=your_qdrant_api_key
GROQ_API_KEY=your_groq_api_key

Install dependencies:

pip install mem0ai qdrant-client openai groq python-dotenv pydantic

Run:

python -m Memory.main

Note: Never commit your .env file or API keys to GitHub.

What I Learned

This project helped me understand the difference between:

Groq     → Talks to the user
Mem0     → Manages long-term memory
Embedder → Converts text into vectors
Qdrant   → Stores and searches vectors

The key takeaway:

Qdrant provides vector storage and search.
Mem0 adds the memory-management layer around it.

🚧 Learning & Experimentation Project

Feel free to explore the code and experiment with different memory scenarios.