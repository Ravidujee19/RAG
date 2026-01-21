export const sections = [
  {
    title: "Local + Cloud RAG",
    body: "Vector search and memory stay local. Gemini is used only for planning and final responses.",
  },
  {
    title: "Multi-Agent Orchestration",
    body: "Aggregator selects agents for retrieval, tools, and offline web search.",
  },
  {
    title: "Privacy-First Design",
    body: "No external data movement except the prompt passed to the LLM adapter.",
  },
];

export const flow = [
  "User Query",
  "Aggregator Agent",
  "Agent Actions",
  "Local Retrieval",
  "RAG Synthesis",
  "Final Response",
];
