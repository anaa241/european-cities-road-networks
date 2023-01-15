import osmnx as ox
from networkx import MultiDiGraph


def plot_road_network(path_to_graph: str):
    G: MultiDiGraph = ox.load_graphml(path_to_graph)
    fig, ax = ox.plot_graph(G)
