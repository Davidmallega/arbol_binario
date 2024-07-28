import networkx as nx
from .models import trees, G_road, G_air, find_optimal_route_tree, find_optimal_route_graph

# Función que obtiene la ruta óptima entre origen y destino basado en un criterio de peso.
def get_optimal_route(origin, destination, weight):
    route_key = f"{origin}-{destination}"
    
    # Intentar obtener la ruta óptima usando árboles
    if route_key in trees:
        recommended_route, all_routes = find_optimal_route_tree(trees[route_key], weight)
    else:
        recommended_route, all_routes = None, None

    # Si no se encuentra una ruta recomendada en el árbol, usar grafos
    if recommended_route is None:
        graph_route, _ = find_optimal_route_graph(G_road, origin, destination, weight)
        if graph_route:
            recommended_route = f"Graph road route via {graph_route}"
            all_routes = [
                {"route": f"{graph_route[i]}-{graph_route[i+1]}", 
                 "tiempo": nx.get_edge_attributes(G_road, 'tiempo')[(graph_route[i], graph_route[i+1])],
                 "distancia": nx.get_edge_attributes(G_road, 'distancia')[(graph_route[i], graph_route[i+1])],
                 "costo": nx.get_edge_attributes(G_road, 'costo')[(graph_route[i], graph_route[i+1])]}
                for i in range(len(graph_route)-1)
            ]
        
        # Intentar encontrar la ruta usando grafos aéreos si la ruta por carretera no se encontró
        if recommended_route is None:
            graph_route, _ = find_optimal_route_graph(G_air, origin, destination, weight)
            if graph_route:
                recommended_route = f"Graph air route via {graph_route}"
                all_routes = [
                    {"route": f"{graph_route[i]}-{graph_route[i+1]}", 
                     "tiempo": nx.get_edge_attributes(G_air, 'tiempo')[(graph_route[i], graph_route[i+1])],
                     "distancia": nx.get_edge_attributes(G_air, 'distancia')[(graph_route[i], graph_route[i+1])],
                     "costo": nx.get_edge_attributes(G_air, 'costo')[(graph_route[i], graph_route[i+1])]}
                    for i in range(len(graph_route)-1)
                ]

    return recommended_route, all_routes
