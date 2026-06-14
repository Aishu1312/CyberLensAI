import networkx as nx
import matplotlib.pyplot as plt

def create_network(df):

    G = nx.Graph()

    for _, row in df.iterrows():
        G.add_edge(
            row["Sender"],
            row["Receiver"]
        )

    return G
