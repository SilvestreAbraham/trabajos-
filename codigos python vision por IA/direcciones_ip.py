def ip_valida(ip):
    ipo = ip.split('.')

    if len(ipo) != 4:
        return False

    for num in ipo:
        if not num.isdigit():
            return False
        n = int(num)
        if n < 0 or n > 255:
            return False

    return True


def obtener_mascara(ip):
    ipo = ip.split('.')
    primer_ipo = int(ipo[0])

    # IPs especiales
    if ip_especial(ip):
        if ipo[0] == '0':
            return "0.0.0.0", "Red por defecto"
        elif ipo[0] == '127':
            return "255.0.0.0", "Loopback"
        elif 224 <= primer_ipo <= 239:
            return "240.0.0.0", "Multicast"
        elif primer_ipo >= 240:
            return "240.0.0.0", "Experimental"

    # IPs privadas
    if ip_privada(ip):
        if ipo[0] == '10':
            return "255.0.0.0", "Red Privada Clase A (10.0.0.0/8)"
        elif ipo[0] == '172' and 16 <= int(ipo[1]) <= 31:
            return "255.240.0.0", "Red Privada Clase B (172.16.0.0/12)"
        elif ipo[0] == '192' and ipo[1] == '168':
            return "255.255.0.0", "Red Privada Clase C (192.168.0.0/16)"

    # IPs públicas
    if primer_ipo <= 126:
        return "255.0.0.0", "Red Publica Clase A"
    elif primer_ipo <= 191:
        return "255.255.0.0", "Red Publica Clase B"
    else:
        return "255.255.255.0", "Red Publica Clase C"


def ip_especial(ip):
    ipo = ip.split('.')
    primer_ipo = int(ipo[0])

    if ipo[0] == '0':
        return True
    if ipo[0] == '127':
        return True
    if 224 <= primer_ipo <= 239:
        return True
    if primer_ipo >= 240:
        return True

    # Otras IPs especiales
    if ipo[0] == '169' and ipo[1] == '254':
        return True
    if ipo[0] == '100' and 64 <= int(ipo[1]) <= 127:
        return True

    return False


def ip_privada(ip):
    ipo = ip.split('.')

    if ipo[0] == '10':
        return True
    if ipo[0] == '172' and 16 <= int(ipo[1]) <= 31:
        return True
    if ipo[0] == '192' and ipo[1] == '168':
        return True
    if ipo[0] == '100' and 64 <= int(ipo[1]) <= 127:
        return True

    return False


def evaluar_ip():
    while True:
        ip = input("\nIntroduce una direccion IP: ").strip()

        if ip_valida(ip):
            mascara, descripcion = obtener_mascara(ip)
            print(f"\nInformacion de la IP {ip}:")
            print(f"- Mascara de red: {mascara}")
            print(f"- Tipo de red: {descripcion}")

            if ip_especial(ip):
                if ip == "127.0.0.1":
                    print("- Uso de Localhost (loopback)")
                elif ip.startswith("169.254"):
                    print("- Uso de Direccion APIPA (asignacion automatica cuando DHCP falla)")
                elif ip.startswith("0."):
                    print("- Uso de Red por defecto")
                elif 224 <= int(ip.split('.')[0]) <= 239:
                    print("- Uso de Direccion multicast")
                else:
                    print("- Uso de Reservada/Experimental")
            elif ip_privada(ip):
                print("- Uso de Red privada interna")
            else:
                print("- Uso de Red publica (Internet)")

            break
        else:
            print("Error Formato incorrecto Deben ser 4 numeros (ej: 8.8.8.8)")


# Programa principal
print("Analaizer de Direcciones IP, Mascaras y Tipos de Red")
while True:
    evaluar_ip()

    while True:
        continuar = input("\n¿Quieres Ingresar otra IP? (s/n): ").strip().lower()
        if continuar in ['s', 'n', 'si', 'no']:
            break
        print("Por favor, ingresa 's' para sí o 'n' para no.")

    if continuar in ['n', 'no']:
        print("\nAdios Humano")
        break