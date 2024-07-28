import networkx as nx

# Crear grafos para carretera y avión
G_road = nx.Graph()
G_air = nx.Graph()

# Datos de rutas entre ciudades
routes_data = {
    "Santiago-Valparaíso": {
        "Ruta 68": {"tiempo": 1.52, "distancia": 121, "costo": 12902},
        "Ruta 78": {"tiempo": 2.37, "distancia": 187, "costo": 19947},
        
    },
    "Santiago-Antofagasta": {
        "Ruta 5": {"tiempo": 15.35, "distancia": 1370, "costo": 145493},
        "Avión Latam": {"tiempo": 2.08, "distancia": 1364, "costo": 84582}
    },
    "Santiago-Iquique": {
        "Ruta 5": {"tiempo": 19.40, "distancia": 1780, "costo": 183680},
        "Avión Latam": {"tiempo": 2.37, "distancia": 1722, "costo": 58762}
    }
}

# Clase para representar un nodo en el árbol de rutas
class TreeNode:
    def __init__(self, route, tiempo, distancia, costo, left=None, right=None):
        self.route = route
        self.tiempo = tiempo
        self.distancia = distancia
        self.costo = costo
        self.left = left
        self.right = right

# Función para crear un árbol binario de rutas a partir de datos de rutas
def create_route_tree(route_data):
    root = None
    for route, data in route_data.items():
        node = TreeNode(route, data['tiempo'], data['distancia'], data['costo'])
        if root is None:
            root = node
        else:
            current = root
            while True:
                if data['costo'] < current.costo:
                    if current.left is None:
                        current.left = node
                        break
                    current = current.left
                else:
                    if current.right is None:
                        current.right = node
                        break
                    current = current.right
    return root

# Crear árboles binarios para cada ruta
trees = {route: create_route_tree(data) for route, data in routes_data.items()}

# Función para encontrar la ruta óptima en un árbol basado en un criterio de peso
def find_optimal_route_tree(tree, weight):
    if not tree:
        return None, None
    
    def compare(node1, node2):
        if weight == "tiempo":
            return node1.tiempo < node2.tiempo
        elif weight == "distancia":
            return node1.distancia < node2.distancia
        elif weight == "costo":
            return node1.costo < node2.costo

    best_node = tree
    stack = [tree]
    all_routes = []
    
    while stack:
        current = stack.pop()
        all_routes.append(current)
        if compare(current, best_node):
            best_node = current
        if current.left:
            stack.append(current.left)
        if current.right:
            stack.append(current.right)
    
    all_routes.sort(key=lambda x: getattr(x, weight))
    return best_node.route, [
        {"route": node.route, "tiempo": node.tiempo, "distancia": node.distancia, "costo": node.costo} 
        for node in all_routes
    ]

# Añadir nodos y aristas al grafo de carretera y avión
for ciudad_pair, routes in routes_data.items():
    cities = ciudad_pair.split('-')
    for route, data in routes.items():
        if 'Ruta' in route:
            G_road.add_edge(cities[0], cities[1], tiempo=data['tiempo'], distancia=data['distancia'], costo=data['costo'])
        else:
            G_air.add_edge(cities[0], cities[1], tiempo=data['tiempo'], distancia=data['distancia'], costo=data['costo'])

# Función para encontrar la ruta óptima en un grafo usando el algoritmo de Dijkstra
def find_optimal_route_graph(G, source, target, weight):
    try:
        path = nx.dijkstra_path(G, source, target, weight)
        total_weight = sum(nx.get_edge_attributes(G, weight)[(path[i], path[i+1])] for i in range(len(path)-1))
        return path, total_weight
    except nx.NetworkXNoPath:
        return None, None
