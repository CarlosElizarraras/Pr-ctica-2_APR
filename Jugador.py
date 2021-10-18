from time import time
import socket


def matrizP():
    filas = ["1", "2", "3"];
    columnas = ["A", "B", "C"];
    alto = len(filas) + 1
    largo = len(columnas) + 1;
    matriz = []
    for i in range(alto):
        matriz.append([])
        for j in range(largo):
            matriz[i].append(" ")
    return generarMatrizInicial(matriz, filas, columnas)


def matrizA():
    filas = ["1", "2", "3", "4", "5"];
    columnas = ["A", "B", "C", "D", "E"];
    alto = len(filas) + 1
    largo = len(columnas) + 1;
    matriz = []
    for i in range(alto):
        matriz.append([])
        for j in range(largo):
            matriz[i].append(" ")
    return generarMatrizInicial(matriz, filas, columnas)


def generarMatrizInicial(matriz, filas, columnas):

    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if i == 0:
                if j == 0:
                    matriz[i][j] = " "
                else:
                    matriz[i][j] = columnas[j - 1]
            else:
                if j == 0:
                    matriz[i][j] = filas[i - 1]
                else:
                    matriz[i][j] = "-"
    return matriz


def verMatriz(matriz):
    alto = len(matriz)
    largo = len(matriz[0])
    for i in range(alto):
        for j in range(largo):
            print(matriz[i][j], "\t", end=" ")
        print()


def Inicio(TCPClientSocket, case):
    if case == 1:
        matrizp = matrizP()
        verMatriz(matrizp)
        jugar(matrizp, TCPClientSocket)
    if case == 2:
        matriza = matrizA()
        verMatriz(matriza)
        jugar(matriza, TCPClientSocket)


def menuAux(TCPClientSocket):
    print("\tElige una dificultad\t")
    print("1. Principiante")
    print("2. Avanzado")
    case = int(input("Opcion: "))
    caseb = case.to_bytes(1, 'little')
    TCPClientSocket.sendall(caseb)


def colocar(matriz, sim, TCPClientSocket):
    pos = str(input("Ingrese una coordenada (Ej. 1A,2C): "))
    TCPClientSocket.sendall(pos.encode())
    cont = str(TCPClientSocket.recv(buffer_size), "ascii")
    print(cont)
    if cont == "Libre":
        fila = int(pos[0])
        col = ord(pos[1]) - 64
        matriz[int(fila)][int(col)] = sim

    elif cont == "Ocupado":
        print("Posicion Invalida")
        colocar(matriz, sim, TCPClientSocket)


def recibirAct(TCPClientSocket, sim, matriz):
    pos = str(TCPClientSocket.recv(buffer_size), "ascii")
    if len(pos) > 0:
        print(pos)
        fila = int(pos[0])
        col = ord(pos[1]) - 64
        matriz[int(fila)][int(col)] = sim


def juegoAuto(matriz, sim, TCPClientSocket):
    pos = str(TCPClientSocket.recv(buffer_size), "ascii")
    fila = int(pos[0])
    col = ord(pos[1]) - 64
    matriz[int(fila)][int(col)] = sim
    print(str(TCPClientSocket.recv(buffer_size),"ascii"))


def ganarH(matriz, sim):
    cont = 0
    for i in range(1, len(matriz)):
        cont = 0
        for j in range(1, len(matriz[0])):
            if matriz[i][j] == sim:
                cont += 1
                if cont is (len(matriz) - 1):
                    return 1
                    break;


def ganarV(matriz, sim):
    cont = 0
    for j in range(1, len(matriz[0])):
        cont = 0
        for i in range(1, len(matriz)):
            if matriz[i][j] == sim:
                cont += 1
                if cont is (len(matriz) - 1):
                    return 1
                    break;


def jugar(matriz, TCPClientSocket):
    simJ = "x"
    simS = "o"
    cont = 0
    print("El jugador tira con: ", simJ)
    print("La máquina tira con: ", simS)
    long = (len(matriz) - 1) * (len(matriz) - 1)
    inicio = time()
    while cont < long:
        print("Turno del jugador\n")
        colocar(matriz, simJ, TCPClientSocket)
        verMatriz(matriz)
        if ganarH(matriz, simJ) == 1:
            print("Ganó el jugador")
            break;
        if ganarV(matriz, simJ) == 1:
            print("Ganó el jugador")
            break;
        cont += 1;
        if cont >= long:
            print("Juego terminado: Es un empate")
            break
        if (str(TCPClientSocket.recv(buffer_size), "ascii") == "Turno de la máquina"):
            print("Turno de la máquina\n")
            juegoAuto(matriz, simS, TCPClientSocket)
            verMatriz(matriz)
            if ganarH(matriz, simS) == 1:
                print("Ganó la máquina")
                break;
            if ganarV(matriz, simS) == 1:
                print("Ganó la máquina")
                break;
            cont += 1
            if cont >= long:
                print("Juego terminado: Es un empate")
                break
        else:
            recibirAct(TCPClientSocket, simJ, matriz)

    final = time()
    print("Duración de la partida: %.2f segundos" % (final - inicio))



import socket

HOST = str(input("Introduzca la dirección IP del servidor: "))
PORT = int(input("Introduzca el número de puerto del servidor: "))
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print(str(TCPClientSocket.recv(buffer_size), "ascii"))
    print(str(TCPClientSocket.recv(buffer_size), "ascii"))
    cliente = int.from_bytes(TCPClientSocket.recv(buffer_size), 'little')

    if (cliente == 0):
        print("Cliente:", cliente + 1)
        menuAux(TCPClientSocket)
    else:
        print("Soy jugador ", cliente + 1, ". Esperando tablero de juego")
    case = int.from_bytes(TCPClientSocket.recv(buffer_size), 'little')
    Inicio(TCPClientSocket, case)
