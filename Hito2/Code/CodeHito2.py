import sys

class Videogame:
    def __init__(self, id, name, platform, year, genre, publisher):
        self.id = id
        self.name = name
        self.platform = platform
        self.genre = genre
        self.year = year
        self.publisher = publisher

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getPlatform(self):
        return self.platform

    def getGenre(self):
        return self.genre

    def getYear(self):
        return self.year

    def getPublisher(self):
        return self.publisher

# Función para calcular el peso de una arista entre dos juegos
def compare_videogames(videogame1, videogame2):
    umbral_similitud = 0.2  # Umbral de similitud mínimo para crear una arista

    # Comparar el género
    if videogame1.getGenre() != videogame2.getGenre():
        return 0  # No hay similitud en el género, la arista no se crea

    similitud = 0

    # Comparar los demás atributos
    if videogame1.getPlatform() == videogame2.getPlatform():
        similitud += 0.3

    if abs(int(videogame1.getYear()) - int(videogame2.getYear())) <= 5:
        similitud += 0.2
    elif abs(int(videogame1.getYear()) - int(videogame2.getYear())) <= 15:
        similitud += 0.1

    if videogame1.getPublisher() == videogame2.getPublisher():
        similitud += 0.1

    if similitud < umbral_similitud:
        return 0  # No se supera el umbral de similitud, la arista no se crea


    return 1 - similitud

# Ejemplo de uso
videogame1 = Videogame(1,"Wii Sports","Wii",2006,"Sports","Nintendo")
videogame2 = Videogame(2,"Super Mario Bros.","NES",1985,"Platform","Nintendo")
videogame3 = Videogame(3,"Mario Kart Wii","Wii",2008,"Racing","Nintendo")
videogame4 = Videogame(4,"Wii Sports Resort","Wii",2009,"Sports","Nintendo")
videogame5 = Videogame(5,"Pokemon Red/Pokemon Blue","GB",1996,"Role-Playing","Nintendo")
videogame6= Videogame(6,"Tetris","GB","1989","Puzzle","Nintendo",)

import csv
import networkx as nx
import matplotlib.pyplot as plt

videogames = []

with open("vgsales.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        videogames.append(Videogame(len(videogames),row[1],row[2],row[3],row[4],row[5]))
    videogames.pop(0)

def create_graph(videogames):
    graph = {}
    for i, v1 in enumerate(videogames):
        if int(v1.id) not in graph:
            graph[int(v1.id)] = {}
        for j, v2 in enumerate(videogames):
            if i != j:
                weight = compare_videogames(v1, v2)
                if weight > 0:
                  graph[int(v1.id)][int(v2.id)] = weight

    return graph

graph = create_graph(videogames[:1500])

def prim_mst(graph, start_index):
    vertices = list(graph.keys())
    num_vertices = len(vertices)

    if num_vertices == 0:
        return []

    visited = [False] * num_vertices
    parent = [None] * num_vertices
    key = [sys.maxsize] * num_vertices

    key[start_index] = 0
    parent[start_index] = -1

    for _ in range(num_vertices - 1):
        min_key = sys.maxsize
        min_index = -1

        for i in range(num_vertices):
            if not visited[i] and key[i] < min_key:
                min_key = key[i]
                min_index = i

        visited[min_index] = True

        for vertex, weight in graph[vertices[min_index]].items():
            v_index = vertices.index(vertex)
            if not visited[v_index] and weight < key[v_index]:
                key[v_index] = weight
                parent[v_index] = min_index

    mst = []
    for i in range(num_vertices):
        if parent[i] is not None and parent[i] != -1:
          mst.append((vertices[parent[i]], vertices[i]))

    return mst

recomendations = []
start=2
mst = prim_mst(graph,start)
# Imprimir las aristas del MST
count = 0
for edge in mst:
    count += 1
    print(f"{count}. {edge[0]} - {edge[1]}")
    
    if videogames[start].genre==videogames[int(edge[1])-1].genre:
      recomendations.append(videogames[int(edge[1])-1])
      if count==5:
          break




def grafiqueGraph(recomendations):
    recomendations.append(videogames[start])
    graphRecomend = create_graph(recomendations)
    nx_graph = nx.Graph(graphRecomend)

    # Retrieve the weights from the graph dictionary
    edge_labels = {}
    for node1, edges in graphRecomend.items():
        for node2, weight in edges.items():
            edge_labels[(node1, node2)] = weight

    # Draw the graph
    pos = nx.spring_layout(nx_graph)
    nx.draw(nx_graph, pos, with_labels=True, node_color='#8b78a5', node_size=500, font_size=10, font_weight='bold', edge_color='gray', font_color='white')

    # Draw edge labels
    nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=edge_labels)

    plt.show()



grafiqueGraph(recomendations)
