import random
import math
import time
import matplotlib.pyplot as plt
import networkx as nx

# ---------------------------------------------------------
# CLASE 1: EL EDIFICIO
# Representa un nodo en nuestra ciudad
# ---------------------------------------------------------
class Edificio:
    def __init__(self, id_edificio, nombre, ubicacion):
        """
        id_edificio: Identificador único (int)
        nombre: Nombre del edificio (str)
        ubicacion: Tupla de coordenadas (x, y)
        """
        self.id = id_edificio
        self.nombre = nombre
        self.ubicacion = ubicacion # Tupla (x, y)
        self.recursos = 0

    def recibir_entrega(self, cantidad):
        self.recursos += cantidad
        print(f"   -> [{self.nombre}] recibió {cantidad} unidades. Total: {self.recursos}")

    def __repr__(self):
        return f"{self.nombre} en {self.ubicacion}"


# ---------------------------------------------------------
# CLASE 2: EL MAPA DE LA CIUDAD (Lógica Espacial)
# Maneja las coordenadas, distancias y el grafo visual
# ---------------------------------------------------------
class MapaCiudad:
    def __init__(self, rango_x=(0, 100), rango_y=(0, 100)):
        self.rango_x = rango_x
        self.rango_y = rango_y
        self.grafo = nx.Graph()
        self.posiciones = {} # Diccionario {id_nodo: (x, y)}

    def generar_ubicacion_aleatoria(self):
        """Genera una coordenada (x, y) aleatoria dentro del rango."""
        x = round(random.uniform(*self.rango_x), 1)
        y = round(random.uniform(*self.rango_y), 1)
        return (x, y)

    def registrar_edificio(self, edificio):
        """Agrega el edificio al grafo y guarda su posición."""
        self.posiciones[edificio.id] = edificio.ubicacion
        # Añadimos el nodo al grafo con sus metadatos
        self.grafo.add_node(edificio.id, label=edificio.nombre)

    def calcular_distancia(self, pos1, pos2):
        """Calcula distancia Euclidiana entre dos tuplas (x,y)."""
        return round(math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2), 2)

    def conectar_nodos_cercanos(self, distancia_maxima=60):
        """
        Crea 'calles' (aristas) visuales entre edificios que estén cerca.
        Esto es para que el mapa se vea como una red y no solo puntos sueltos.
        """
        ids = list(self.posiciones.keys())
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                id1, id2 = ids[i], ids[j]
                dist = self.calcular_distancia(self.posiciones[id1], self.posiciones[id2])
                
                # Conectamos si están cerca para simular calles
                if dist <= distancia_maxima:
                    self.grafo.add_edge(id1, id2, weight=dist)

    def visualizar(self, ruta_recorrida=None):
        """
        Dibuja el mapa usando Matplotlib.
        ruta_recorrida: Lista de IDs [0, 2, 5...] para resaltar el camino.
        """
        plt.figure(figsize=(10, 7))
        plt.title("Mapa de la Ciudad - Simulación Logística")

        # 1. Dibujar todos los nodos (Edificios)
        nx.draw_networkx_nodes(self.grafo, self.posiciones, node_size=800, node_color='skyblue', edgecolors='black')
        
        # 2. Dibujar etiquetas de los nombres
        labels = nx.get_node_attributes(self.grafo, 'label')
        nx.draw_networkx_labels(self.grafo, self.posiciones, labels, font_size=9)

        # 3. Dibujar las calles (aristas grises)
        nx.draw_networkx_edges(self.grafo, self.posiciones, edge_color='lightgray', style='dashed')
        
        # 4. Mostrar las distancias en las calles
        edge_labels = nx.get_edge_attributes(self.grafo, 'weight')
        edge_labels_fmt = {k: f"{v}km" for k, v in edge_labels.items()}
        nx.draw_networkx_edge_labels(self.grafo, self.posiciones, edge_labels=edge_labels_fmt, font_size=7)

        # 5. RESALTAR LA RUTA (Si existe)
        if ruta_recorrida and len(ruta_recorrida) > 1:
            ruta_edges = [(ruta_recorrida[i], ruta_recorrida[i+1]) for i in range(len(ruta_recorrida)-1)]
            
            # Dibujar lineas rojas para la ruta
            # Nota: Agregamos las aristas temporalmente si no existen para poder dibujarlas
            self.grafo.add_edges_from(ruta_edges) 
            nx.draw_networkx_edges(self.grafo, self.posiciones, edgelist=ruta_edges, edge_color='red', width=2.5)
            
            # Colorear los nodos de la ruta de otro color
            nx.draw_networkx_nodes(self.grafo, self.posiciones, nodelist=ruta_recorrida, node_color='#ff9999', node_size=850, edgecolors='red')

        plt.grid(True, linestyle=':', alpha=0.3)
        plt.axis('on')
        print("\n[SISTEMA] Abriendo visualización del mapa...")
        plt.show()


# ---------------------------------------------------------
# CLASE 3: EL CONTROLADOR DE LA SIMULACIÓN
# Orquesta todo
# ---------------------------------------------------------
class Simulacion:
    def __init__(self, num_edificios):
        self.mapa = MapaCiudad(rango_x=(0, 100), rango_y=(0, 100))
        self.edificios = []
        self.num_edificios = num_edificios

    def inicializar_entorno(self):
        print("--- GENERANDO CIUDAD ---")
        nombres = ["Torre A", "Plaza Central", "Hospital", "Estación", "Escuela", "Mercado", "Cine", "Parque", "Oficinas", "Fábrica"]
        
        for i in range(self.num_edificios):
            # 1. Obtener ubicación aleatoria del mapa
            ubicacion = self.mapa.generar_ubicacion_aleatoria()
            
            # 2. Crear nombre (usar lista o genérico)
            nombre = nombres[i] if i < len(nombres) else f"Edificio {i}"
            
            # 3. Crear objeto Edificio
            nuevo_edificio = Edificio(i, nombre, ubicacion)
            self.edificios.append(nuevo_edificio)
            
            # 4. Registrarlo en el mapa visual
            self.mapa.registrar_edificio(nuevo_edificio)
            print(f"Construido: {nuevo_edificio}")

        # Crear conexiones visuales (calles)
        self.mapa.conectar_nodos_cercanos()
        print("------------------------\n")

    def ejecutar_ruta_logistica(self, ids_ruta):
        """Simula un vehículo viajando por una lista de IDs de edificios."""
        print(f"--- INICIANDO RUTA DE REPARTO: {ids_ruta} ---")
        tiempo_total = 0
        distancia_total = 0

        for i in range(len(ids_ruta) - 1):
            origen = self.edificios[ids_ruta[i]]
            destino = self.edificios[ids_ruta[i+1]]

            distancia = self.mapa.calcular_distancia(origen.ubicacion, destino.ubicacion)
            
            # Simulamos velocidad: 1 unidad de distancia = 0.1 segundos de espera
            tiempo_viaje = distancia * 0.05 
            
            print(f"Viajando de '{origen.nombre}' a '{destino.nombre}'...")
            print(f"   Distancia: {distancia} km")
            time.sleep(0.5) # Pausa dramática para consola
            
            destino.recibir_entrega(10) # Entregamos algo
            distancia_total += distancia

        print(f"\n--- RUTA FINALIZADA ---")
        print(f"Distancia total recorrida: {round(distancia_total, 2)} km")
        
        # Finalmente, mostramos el mapa con la ruta pintada
        self.mapa.visualizar(ruta_recorrida=ids_ruta)


# ---------------------------------------------------------
# EJECUCIÓN PRINCIPAL
# ---------------------------------------------------------
if __name__ == "__main__":
    # 1. Configurar simulación con 8 edificios
    sim = Simulacion(num_edificios=8)
    
    # 2. Crear los edificios y el mapa
    sim.inicializar_entorno()
    
    # 3. Definir una ruta (IDs de los edificios a visitar)
    # Hacemos una ruta aleatoria de 4 paradas
    ruta = random.sample(range(8), 4)
    
    # 4. Correr simulación
    sim.ejecutar_ruta_logistica(ruta)