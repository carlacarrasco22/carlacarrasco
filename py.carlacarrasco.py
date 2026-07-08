def validar_texto(texto):
    return bool(texto and texto.strip())

def validar_clasificacion(clasificacion):
    return clasificacion in ['E', 'T', 'M']

def validar_multiplayer(opcion):
    return opcion.lower() in ['s', 'n']

def validar_precio(precio):
    return precio > 0

def validar_stock(stock):
    return stock >= 0


def leer_opcion():
    while True:
        try:
            opcion = int(input("Ingrese opción: "))
            if 1 <= opcion <= 6:
                return opcion
            else:
                print("Debe seleccionar una opción válida")
        except ValueError:
            print("Debe seleccionar una opción válida")


def buscar_codigo(codigo, juegos):
    for clave in juegos.keys():
        if clave.upper() == codigo.upper():
            return True
    return False


def obtener_clave_real(codigo, juegos):
    for clave in juegos.keys():
        if clave.upper() == codigo.upper():
            return clave
    return codigo


def stock_plataforma(plataforma, juegos, inventario):
    total_stock = 0
    for codigo, datos in juegos.items():
        plataforma_juego = datos[1]
        if plataforma_juego.lower() == plataforma.lower():
            if codigo in inventario:
                total_stock += inventario[codigo][1]
    
    print(f"El total de stock disponibles es: {total_stock}")


def busqueda_precio(p_min, p_max, juegos, inventario):
    resultados = []
    
    for codigo, datos_inv in inventario.items():
        precio = datos_inv[0]
        stock = datos_inv[1]
        
        if p_min <= precio <= p_max and stock > 0:
            if codigo in juegos:
                titulo = juegos[codigo][0]
                resultados.append(f"{titulo}--{codigo}")
    
    if resultados:
        resultados.sort()
        print(f"Los juegos encontrados son: {resultados}")
    else:
        print("No hay juegos en ese rango de precios.")


def actualizar_precio(codigo, nuevo_precio, juegos, inventario):
    if buscar_codigo(codigo, juegos):
        clave_real = obtener_clave_real(codigo, juegos)
        inventario[clave_real][0] = nuevo_precio
        return True
    return False


def agregar_juego(codigo, titulo, plataforma, genero, clasificacion, multiplayer, editor, precio, stock, juegos, inventario):
    if buscar_codigo(codigo, juegos):
        return False
    
    mp_bool = True if multiplayer.lower() == 's' else False
    
    juegos[codigo] = [titulo, plataforma, genero, clasificacion, mp_bool, editor]
    inventario[codigo] = [precio, stock]
    return True


def eliminar_juego(codigo, juegos, inventario):
    if buscar_codigo(codigo, juegos):
        clave_real = obtener_clave_real(codigo, juegos)
        juegos.pop(clave_real)
        inventario.pop(clave_real)
        return True
    return False


def main():
    juegos = {
        'G001': ['Eclipse Runner', 'PC', 'accion', 'T', True, 'NovaStudio'],
        'G002': ['Puzzle Atlas', 'Switch', 'puzzle', 'E', False, 'BrightWorks'],
        'G003': ['Sky Legends', 'PS5', 'aventura', 'T', True, 'OrionGames'],
        'G004': ['Racing Pulse', 'PC', 'carreras', 'E', True, 'VelocityLab'],
        'G005': ['Mystic Farm', 'Switch', 'simulacion', 'E', False, 'GreenSeed'],
        'G006': ['Shadow Tactics', 'Xbox', 'estrategia', 'M', False, 'IronGate']
    }

    inventario = {
        'G001': [9990, 7],
        'G002': [19990, 0],
        'G003': [42990, 3],
        'G004': [14990, 5],
        'G005': [17990, 9],
        'G006': [39990, 2]
    }

    continuar = True
    while continuar:
        print("\n========== MENÚ PRINCIPAL ==========")
        print("1. Stock por plataforma")
        print("2. Búsqueda de juegos por rango de precio")
        print("3. Actualizar precio de juego")
        print("4. Agregar juego")
        print("5. Eliminar juego")
        print("6. Salir")
        print("====================================")
        
        opcion = leer_opcion()
        
        if opcion == 1:
            plat = input("Ingrese plataforma a consultar: ")
            stock_plataforma(plat, juegos, inventario)
            
        elif opcion == 2:
            while True:
                try:
                    p_min = int(input("Ingrese precio mínimo: "))
                    p_max = int(input("Ingrese precio máximo: "))
                    break
                except ValueError:
                    print("Debe ingresar valores enteros")
            busqueda_precio(p_min, p_max, juegos, inventario)
            
        elif opcion == 3:
            resp = 's'
            while resp.lower() == 's':
                cod = input("Ingrese código del juego: ")
                try:
                    n_precio = int(input("Ingrese nuevo precio: "))
                    if n_precio > 0:
                        if actualizar_precio(cod, n_precio, juegos, inventario):
                            print("Precio actualizado")
                        else:
                            print("El código no existe")
                    else:
                        print("El precio debe ser mayor a cero.")
                except ValueError:
                    print("Debe ingresar un valor entero válido.")
                
                resp = input("¿Desea actualizar otro precio (s/n)?: ")
                
        elif opcion == 4:
            cod = input("Ingrese código del juego: ")
            tit = input("Ingrese título: ")
            plat = input("Ingrese plataforma: ")
            gen = input("Ingrese género: ")
            clas = input("Ingrese clasificación: ")
            mult = input("¿Es multiplayer? (s/n): ")
            edit = input("Ingrese editor: ")
        
            try:
                prec = int(input("Ingrese precio: "))
                stk = int(input("Ingrese stock: "))
            except ValueError:
                print("Error: El precio y el stock deben ser números enteros.")
                continue
            
            if not validar_texto(cod):
                print("Error: El código no puede estar vacío.")
            elif buscar_codigo(cod, juegos):
                print("El código ya existe")
            elif not validar_texto(tit):
                print("Error: El título no puede estar vacío.")
            elif not validar_texto(plat):
                print("Error: La plataforma no puede estar vacía.")
            elif not validar_texto(gen):
                print("Error: El género no puede estar vacío.")
            elif not validar_clasificacion(clas):
                print("Error: La clasificación debe ser 'E', 'T' o 'M'.")
            elif not validar_multiplayer(mult):
                print("Error: En multiplayer debe ingresar 's' o 'n'.")
            elif not validar_texto(edit):
                print("Error: El editor no puede estar vacío.")
            elif not validar_precio(prec):
                print("Error: El precio debe ser un número entero mayor que cero.")
            elif not validar_stock(stk):
                print("Error: El stock debe ser un número entero mayor o igual a cero.")
            else:
                if agregar_juego(cod, tit, plat, gen, clas, mult, edit, prec, stk, juegos, inventario):
                    print("Juego agregado")
                else:
                    print("El código ya existe")
                    
        elif opcion == 5:
            cod = input("Ingrese código del juego que desea eliminar: ")
            if eliminar_juego(cod, juegos, inventario):
                print("Juego eliminado")
            else:
                print("El código no existe")
                
        elif opcion == 6:
            print("Programa finalizado.")
            continuar = False

if __name__ == "__main__":
    main()