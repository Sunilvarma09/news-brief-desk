from langgraph.graph import StateGraph, START, END
from news_desk.investigate import investigate, State
from news_desk.editor import editor
from news_desk.published import publish

graph_builder = StateGraph(State)

graph_builder.add_node("investigate", investigate)
graph_builder.add_node("editor", editor)
graph_builder.add_node("publish", publish)

graph_builder.add_edge(START, "investigate")
graph_builder.add_edge("investigate", "editor")
graph_builder.add_edge("editor", "publish")
graph_builder.add_edge("publish", END)

graph = graph_builder.compile()