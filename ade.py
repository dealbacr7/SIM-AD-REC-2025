def construir_edificio(recursos, costos, obreros, edificios_en_construccion):
    print("Opciones de construcción:")
    for nombre, costo in costos.items():
        print(f"- {nombre} (madera={costo[0]}, piedra={costo[1]}, dinero={costo[2]})")
    eleccion = input("¿Qué quieres construir? ").strip().lower()

    if eleccion not in costos:
        print("Opción inválida.")
        return 0

    costo = costos[eleccion]
    puede = all(recursos[i] >= costo[i] for i in range(len(recursos)))

    if puede:
        for i in range(len(recursos)):
            recursos[i] -= costo[i]
        tiempo_base = 3  # pasos base para construir
        tiempo_real = max(1, tiempo_base - obreros + 1)  # cada obrero reduce 1 paso
        edificios_en_construccion.append([eleccion, tiempo_real])
        print(f"Comenzaste a construir un(a) {eleccion}, tardará {tiempo_real} paso(s).")
        return 1
    else:
        print(f"No tienes suficientes recursos para construir un(a) {eleccion}.")
        return 0


def simular_juego(recursos, costos, obreros):
    paso = 1
    edificios_en_construccion = []

    while True:
        print(f"\n--- Paso {paso} ---")
        print(f"Recursos actuales: madera={recursos[0]}, piedra={recursos[1]}, dinero={recursos[2]}")
        if edificios_en_construccion:
            print("Edificios en construcción:")
            for e, t in edificios_en_construccion:
                print(f"- {e}, pasos restantes: {t}")

        print("\nMenú:")
        print("- construir")
        print("- recursos")
        print("- salir")

        opcion = input("Elige una opción: ").strip().lower()

        if opcion == "salir":
            print("Fin de la simulación.")
            break

        elif opcion == "construir":
            construir_edificio(recursos, costos, obreros, edificios_en_construccion)

        elif opcion == "recursos":
            print("Opciones de recursos:")
            print("- talar arboles")
            print("- picar piedra")
            print("- cobrar impuestos")
            eleccion = input("¿Qué quieres hacer? ").strip().lower()

            if eleccion == "talar arboles":
                recursos[0] += 10
                print("Talaste árboles y conseguiste 10 de madera.")
            elif eleccion == "picar piedra":
                recursos[1] += 6
                print("Picaste piedra y conseguiste 6 de piedra.")
            elif eleccion == "cobrar impuestos":
                recursos[2] += 15
                print("Recaudaste impuestos y conseguiste 15 de dinero.")
            else:
                print("Opción inválida.")

        else:
            print("Opción inválida.")

        # Reducir tiempo de construcción
        for e in edificios_en_construccion:
            e[1] -= 1
        terminados = [e for e in edificios_en_construccion if e[1] <= 0]
        for e in terminados:
            print(f"✅ Se terminó de construir un(a) {e[0]}.")
            edificios_en_construccion.remove(e)

        paso += 1

    return recursos


def main():
    recursos = [50, 30, 100]
    obreros = 2  # cantidad de obreros disponibles

    costos = {
        "casa":     [10, 5, 20],
        "escuela":  [15, 10, 40],
        "hospital": [20, 15, 60],
        "granja":   [8,  4, 15]
    }

    recursos_finales = simular_juego(recursos, costos, obreros)
    print(f"\nRecursos restantes al final: madera={recursos_finales[0]}, piedra={recursos_finales[1]}, dinero={recursos_finales[2]}")


main()
