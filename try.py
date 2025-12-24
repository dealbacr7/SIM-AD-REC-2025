import sys
import random
import math
import time
import matplotlib.pyplot as plt
import networkx as nx

# Constantes
MADERA = 0
PIEDRA = 1
DINERO = 2

# ==========================================
# 1. SISTEMA DE MAPA
# ==========================================
class MapaReino:
    def __init__(self, rango_x=100, rango_y=100):
        self.rango_x = rango_x
        self.rango_y = rango_y
        self.grafo = nx.Graph()
        self.posiciones = {} 
        self.contador_ids = 0
        
    def agregar_edificio(self, nombre_tipo):
        my_id = self.contador_ids
        self.contador_ids += 1
        x = round(random.uniform(0, self.rango_x), 1)
        y = round(random.uniform(0, self.rango_y), 1)
        
        self.posiciones[my_id] = (x, y)
        # Etiqueta más limpia
        etiqueta = f"{nombre_tipo[:3].upper()}-{my_id}"
        self.grafo.add_node(my_id, label=etiqueta, tipo=nombre_tipo)
        self._conectar_vecinos(my_id)
        return (x, y)

    def _conectar_vecinos(self, nuevo_id):
        pos_nueva = self.posiciones[nuevo_id]
        for otro_id, pos_otra in self.posiciones.items():
            if otro_id == nuevo_id: continue
            dist = math.sqrt((pos_otra[0]-pos_nueva[0])**2 + (pos_otra[1]-pos_nueva[1])**2)
            dist = round(dist, 1)
            if dist < 60:
                self.grafo.add_edge(nuevo_id, otro_id, weight=dist)

    def mostrar_ventana(self):
        if not self.posiciones:
            print(">> 🗺️ El mapa está vacío.")
            return

        plt.figure(figsize=(10, 8))
        plt.title(f"Reino Generado por IA - {self.contador_ids} Edificios")
        colores = []
        for n_id, datos in self.grafo.nodes(data=True):
            t = datos.get('tipo', '')
            if t == 'Castillo': colores.append('#FFD700')   # Dorado
            elif t == 'Hospital': colores.append('#FF6961') # Rojo
            elif t == 'Escuela': colores.append('#77DD77')  # Verde
            elif t == 'Granja': colores.append('#FDFD96')   # Amarillo pálido
            else: colores.append('#87CEEB')                 # Azul (Choza)

        nx.draw_networkx_nodes(self.grafo, self.posiciones, node_size=800, node_color=colores, edgecolors='black')
        labels = nx.get_node_attributes(self.grafo, 'label')
        nx.draw_networkx_labels(self.grafo, self.posiciones, labels, font_size=8)
        nx.draw_networkx_edges(self.grafo, self.posiciones, edge_color='gray', style='dashed', alpha=0.5)
        
        # Distancias
        edge_labels = nx.get_edge_attributes(self.grafo, 'weight')
        nx.draw_networkx_edge_labels(self.grafo, self.posiciones, edge_labels={k: f"{v}m" for k, v in edge_labels.items()}, font_size=7, font_color='red')

        plt.axis('on')
        plt.grid(True, linestyle=':', alpha=0.3)
        print(">> [SISTEMA] Mapa abierto. Cierra la ventana para continuar.")
        plt.show()

# ==========================================
# 2. LÓGICA DEL JUEGO
# ==========================================

class Edificio:
    def __init__(self, nombre, c_madera, c_piedra, c_dinero, utilidad, requisito=None):
        self.nombre = nombre
        self.costos = [c_madera, c_piedra, c_dinero]
        self.utilidad = utilidad
        self.requisito = requisito

class JuegoGestion:
    def __init__(self):
        self.recursos = [50, 30, 100] # Mad, Pie, Din
        self.obreros = 2
        self.salario_obrero = 5
        self.tiempo_base = 3
        self.paso = 1
        self.construidos = {} 
        self.mapa = MapaReino() 
        self.cola_construccion = []
        
        # He ajustado un poco las utilidades para que no haya diferencias abismales
        self.catalogo = {
            "Choza":    Edificio("Choza",    10, 5,  20,  utilidad=15),
            "Granja":   Edificio("Granja",   8,  4,  15,  utilidad=20),
            "Escuela":  Edificio("Escuela",  15, 10, 40,  utilidad=50, requisito="Choza"),
            "Hospital": Edificio("Hospital", 20, 15, 60,  utilidad=80, requisito="Escuela"),
            "Castillo": Edificio("Castillo", 50, 50, 200, utilidad=200, requisito="Hospital")
        }

    def verificar_requisitos(self, edificio):
        if edificio.requisito is None: return True
        return self.construidos.get(edificio.requisito, 0) > 0

    # --- CEREBRO INTELIGENTE Y DIVERSIFICADO DE LA IA ---
    def ejecutar_turno_ia(self):
        print(f"--- DÍA {self.paso} (IA) ---")
        
        # 1. SEGURIDAD FINANCIERA (Anti-Quiebra)
        gasto_salarios = self.obreros * self.salario_obrero
        margen_seguridad = gasto_salarios * 4 

        if self.recursos[DINERO] < margen_seguridad:
            if self.recursos[DINERO] < gasto_salarios and self.obreros > 1:
                 print("🤖 IA: ¡CRISIS! Despidiendo obrero.")
                 self.obreros -= 1
            else:
                print(f"🤖 IA: Ahorrando (Caja: {self.recursos[DINERO]}). Impuestos.")
                self.recursos[DINERO] += 15 
            self.actualizar_estado()
            time.sleep(0.1)
            return

        # 2. SELECCIÓN PONDERADA (Aquí está la magia de la variedad)
        posibles = [e for e in self.catalogo.values() if self.verificar_requisitos(e)]
        
        candidatos = []
        for edif in posibles:
            # Cuántos tenemos ya de este tipo?
            cantidad_actual = self.construidos.get(edif.nombre, 0)
            
            # --- LEY DE RENDIMIENTOS DECRECIENTES ---
            # Dividimos la utilidad por la cantidad que ya tenemos.
            # Si tienes 0 Granjas, valor = 20 / 1 = 20
            # Si tienes 4 Granjas, valor = 20 / 5 = 4
            score_base = edif.utilidad / (1 + cantidad_actual)
            
            # --- FACTOR ALEATORIO (CAOS) ---
            # Multiplicamos por un número entre 0.8 y 1.4 para que a veces
            # la IA se "encapriche" con algo que no es estrictamente lo mejor.
            factor_suerte = random.uniform(0.8, 1.4)
            
            score_final = score_base * factor_suerte
            candidatos.append((edif, score_final))
        
        # Ordenamos por el score modificado
        candidatos.sort(key=lambda x: x[1], reverse=True)
        objetivo = candidatos[0][0] # El ganador del concurso de popularidad de hoy

        # 3. EJECUCIÓN
        costo_total_dinero = objetivo.costos[DINERO]
        dinero_tras_compra = self.recursos[DINERO] - costo_total_dinero
        
        # Solo compra si mantiene el margen de seguridad
        puede_pagar_seguro = (
            self.recursos[MADERA] >= objetivo.costos[MADERA] and
            self.recursos[PIEDRA] >= objetivo.costos[PIEDRA] and
            dinero_tras_compra >= margen_seguridad
        )

        if puede_pagar_seguro:
            print(f"🤖 IA: Decide construir {objetivo.nombre} (Tiene {self.construidos.get(objetivo.nombre,0)}).")
            self.recursos[MADERA] -= objetivo.costos[MADERA]
            self.recursos[PIEDRA] -= objetivo.costos[PIEDRA]
            self.recursos[DINERO] -= objetivo.costos[DINERO]
            tiempo = max(1, self.tiempo_base - self.obreros + 1)
            self.cola_construccion.append([objetivo, tiempo])
        
        else:
            # GESTIÓN DE RECURSOS (Si no puede construir, recolecta lo que falta)
            if dinero_tras_compra < margen_seguridad:
                print(f"🤖 IA: Ahorrando para {objetivo.nombre}. Impuestos.")
                self.recursos[DINERO] += 15
            elif self.recursos[MADERA] < objetivo.costos[MADERA]:
                print(f"🤖 IA: Falta madera para {objetivo.nombre}. Talando.")
                self.recursos[MADERA] += 10
            elif self.recursos[PIEDRA] < objetivo.costos[PIEDRA]:
                print(f"🤖 IA: Falta piedra para {objetivo.nombre}. Picando.")
                self.recursos[PIEDRA] += 6
            else:
                self.recursos[DINERO] += 15 # Fallback

        self.actualizar_estado()
        time.sleep(0.1)

    def bucle_ia(self):
        try:
            dias = int(input("\n🤖 ¿Días de simulación?: "))
        except: return
        print(f"\n>>> IA DIVERSIFICADA ACTIVADA ({dias} días) <<<")
        for _ in range(dias):
            self.ejecutar_turno_ia()
            # Resumen en una línea
            resumen_edif = ", ".join([f"{k}:{v}" for k,v in self.construidos.items()])
            print(f"    [Mad:{self.recursos[MADERA]} Pie:{self.recursos[PIEDRA]} Oro:{self.recursos[DINERO]}] | Ciud: {{{resumen_edif}}}")
            if self.recursos[DINERO] < 0:
                print("💀 GAME OVER")
                break

    # --- MANUAL ---
    def construir_manual(self):
        print("\n--- Catálogo ---")
        opciones = list(self.catalogo.values())
        for i, edif in enumerate(opciones, start=1):
            estado = "DISPONIBLE" if self.verificar_requisitos(edif) else "BLOQUEADO"
            print(f"{i}. {edif.nombre} (Costos: {edif.costos}) | {estado}")
        try:
            sel = int(input("Elige: ")) - 1
            if 0 <= sel < len(opciones):
                obj = opciones[sel]
                if not self.verificar_requisitos(obj):
                    print("¡Requisito no cumplido!")
                    return
                if all(self.recursos[i] >= obj.costos[i] for i in range(3)):
                    for i in range(3): self.recursos[i] -= obj.costos[i]
                    t = max(1, self.tiempo_base - self.obreros + 1)
                    self.cola_construccion.append([obj, t])
                    print(f"¡Iniciando {obj.nombre}!")
                else: print("Recursos insuficientes.")
        except: pass

    def gestionar_manual(self):
        print("\n1. Talar (+20) | 2. Picar (+15) | 3. Impuestos (+25) | 4. Contratar (-5 oro) | 5. Despedir")
        op = input("Acción: ")
        if op == "1": self.recursos[MADERA] += 20
        elif op == "2": self.recursos[PIEDRA] += 15
        elif op == "3": self.recursos[DINERO] += 25
        elif op == "4": 
            if self.recursos[DINERO]>=5: self.obreros+=1; self.recursos[DINERO]-=5
        elif op == "5": 
            if self.obreros>0: self.obreros-=1
        self.actualizar_estado()

    def actualizar_estado(self):
        costo = self.obreros * self.salario_obrero
        self.recursos[DINERO] -= costo
        
        nuevas_colas = []
        for obra in self.cola_construccion:
            edif, tiempo = obra
            tiempo -= 1
            if tiempo <= 0:
                self.construidos[edif.nombre] = self.construidos.get(edif.nombre, 0) + 1
                coords = self.mapa.agregar_edificio(edif.nombre)
                print(f"✅ ¡{edif.nombre} TERMINADO! -> Mapa: {coords}")
            else:
                nuevas_colas.append([edif, tiempo])
        self.cola_construccion = nuevas_colas
        self.paso += 1

    def ejecutar(self):
        while True:
            print(f"\n=== DÍA {self.paso} | Obreros: {self.obreros} ===")
            print("[1] Construir  [2] Trabajar  [3] 🤖 IA Auto-Play  [4] 🗺️ Ver Mapa  [5] Salir")
            op = input(">>> ")
            if op == "1": self.construir_manual(); self.actualizar_estado()
            elif op == "2": self.gestionar_manual()
            elif op == "3": self.bucle_ia()
            elif op == "4": self.mapa.mostrar_ventana()
            elif op == "5": break

if __name__ == "__main__":
    juego = JuegoGestion()
    juego.ejecutar()