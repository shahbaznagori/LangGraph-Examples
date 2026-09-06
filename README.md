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