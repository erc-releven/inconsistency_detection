import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def generate_graph(data_path):
    """
    Generates a graph from the given dataset.
    
    Parameters:
        data_path (str): Path to the Excel file containing relationship data.
    
    Returns:
        networkx.Graph: Generated graph with nodes and edges.
    """
    df = pd.read_excel(data_path)
    G = nx.Graph()
    
    # Extract unique nodes
    node_list = list(df['person_x'].unique()) + list(df['kinsman'].unique())
    G.add_nodes_from(set(node_list))
    
    # Add edges with relationship attributes
    for _, row in df.iterrows():
        G.add_edge(row['person_x'], row['kinsman'], name=row['ontology_kinship'])
    
    return G,df

def print_graph(G):
    """
    Displays the graph with nodes colored by connected components.
    
    Parameters:
        G (networkx.Graph): The graph to visualize.
    """
    components = list(nx.connected_components(G))
    colors = list(mcolors.TABLEAU_COLORS.keys())  # Predefined color set
    color_map = {}
    
    # Assign colors to each component
    for i, component in enumerate(components):
        for node in component:
            color_map[node] = colors[i % len(colors)]
    
    node_colors = [color_map[node] for node in G.nodes]
    pos = nx.spring_layout(G)
    
    nx.draw(G, pos, node_color=node_colors, node_size=40)
    plt.show()

def generate_data_for_sub_graph(sub_graph, df):
    """
    Filters the original dataset to only include relationships within a given subgraph.
    
    Parameters:
        sub_graph (set): Set of nodes representing the subgraph.
        df (DataFrame): Original DataFrame containing relationship data.
    
    Returns:
        DataFrame: Filtered DataFrame containing only relevant rows.
    """
    return df[df['person_x'].isin(sub_graph) & df['kinsman'].isin(sub_graph)].copy()

def unpack_list(lists):
    """
    Flattens a list of sets into a single set.
    
    Parameters:
        lists (list of sets): List of sets to be combined.
    
    Returns:
        set: A single set containing all unique elements.
    """
    return set().union(*lists)

def save_subgraphs(G, list_of_indexes_in_subgraph, data, out_path):
    """
    Saves subgraphs as separate Excel files.
    
    Parameters:
        G (networkx.Graph): The original graph.
        list_of_indexes_in_subgraph (list): List of indexes representing subgraphs.
        data (DataFrame): The original dataset.
        out_path (str): Directory path to save the Excel files.
    """
    sub_graphs = sorted(nx.connected_components(G), key=len, reverse=True)
    
    for index, i in enumerate(list_of_indexes_in_subgraph):
        if isinstance(i,int):
            new_data = generate_data_for_sub_graph(sub_graphs[i], data)
            new_data.to_excel(f'{out_path}/final_data_sub_graph_{index}.xlsx', index=False)
        else : 
            if i[1]> 0 : 
                new_data = generate_data_for_sub_graph(sub_graphs[i[0]:i[1]], data)
            else: 
                new_data = generate_data_for_sub_graph(sub_graphs[i[0]:], data)
            new_data.to_excel(f'{out_path}/final_data_sub_graph_{index}.xlsx', index=False)

