def cifrado_cesar(texto, desplazamiento):
    
    resultado = []
    tabla = []
    
    for caracter in texto:
        original = caracter
        codigo = ord(caracter)
        
        if 'A' <= caracter <= 'Z':
            nuevo_codigo = ord('A') + (codigo - ord('A') + desplazamiento) % 26
            nuevo_caracter = chr(nuevo_codigo)

        elif 'a' <= caracter <= 'z':
            nuevo_codigo = ord('a') + (codigo - ord('a') + desplazamiento) % 26
            nuevo_caracter = chr(nuevo_codigo)

        elif '0' <= caracter <= '9':
            nuevo_codigo = ord('0') + (codigo - ord('0') + desplazamiento) % 10
            nuevo_caracter = chr(nuevo_codigo)

        else:
            nuevo_caracter = caracter
        
        resultado.append(nuevo_caracter)
        tabla.append((original, nuevo_caracter, desplazamiento))
    
    return ''.join(resultado), tabla

def mostrar_tabla(tabla):
    print("\n╔══════════╦══════════╦══════════════╗")
    print("║ Original ║ Cifrado  ║ Desplazamiento ║")
    print("╠══════════╬══════════╬══════════════╣")
    
    for original, cifrado, desplazamiento in tabla:
        print(f"║    {original:<5} ║    {cifrado:<5} ║      {desplazamiento:>3}      ║")
    
    print("╚══════════╩══════════╩══════════════╝")

def obtener_desplazamiento():

    while True:
        try:
            desplazamiento = int(input("Ingresa el numero de desplazamiento para el cifrado (entero): "))
            return desplazamiento
        except ValueError:
            print("Por favor ingrese un numero entero valido.")

def main():
    print("""
     ██████╗██╗███████╗██████╗  █████╗ ██████╗      ██████╗███████╗███████╗ █████╗ ██████╗ 
    ██╔════╝██║██╔════╝██╔══██╗██╔══██╗██╔══██╗    ██╔════╝██╔════╝██╔════╝██╔══██╗██╔══██╗
    ██║     ██║█████╗  ██████╔╝███████║██████╔╝    ██║     █████╗  ███████╗███████║██████╔╝
    ██║     ██║██╔══╝  ██╔══██╗██╔══██║██╔══██╗    ██║     ██╔══╝  ╚════██║██╔══██║██╔══██╗
    ╚██████╗██║██      ██║  ██║██║  ██║██║  ██║    ╚██████╗███████╗███████║██║  ██║██║  ██║
     ╚═════╝╚═╝╚═      ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝      ╚═════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
    """)
    
    while True:
        texto = input("\nIngresa el texto a cifrar o escribe 'salir' para terminar: ")
        
        if texto.lower() == 'salir':
            print("\nAdios Humano Programa terminado.")
            break
        
        desplazamiento = obtener_desplazamiento()
        
        texto_cifrado, tabla = cifrado_cesar(texto, desplazamiento)
        
        print("\n" + "="*50)
        print(f"Texto original: {texto}")
        mostrar_tabla(tabla)
        print(f"\nTexto cifrado: {texto_cifrado}")
        print("="*50 + "\n")
        
        continuar = input("¿Quieres cifrar otro texto? (s/n): ").lower()
        if continuar != 's':
            print("\nAdios Humano Programa terminado.")
            break

if __name__ == "__main__":
    main()