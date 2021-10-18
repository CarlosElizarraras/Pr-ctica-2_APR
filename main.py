from random import randint
from time import time
import socket
import threading

def matrizP():
    filas=["1","2","3"];
    columnas=["A","B","C"];
    alto = len(filas) + 1
    largo=len(columnas)+1;
    matriz=[]
    for i in range(alto):
        matriz.append([])
        for j in range(largo):
            matriz[i].append(" ")
    return generarMatrizInicial(matriz,filas,columnas)


def matrizA():
    filas=["1","2","3","4","5"];
    columnas=["A","B","C","D","E"];
    alto = len(filas) + 1
    largo=len(columnas)+1;
    matriz=[]
    for i in range(alto):
        matriz.append([])
        for j in range(largo):
            matriz[i].append(" ")
    return generarMatrizInicial(matriz,filas,columnas)


def generarMatrizInicial(matriz,filas,columnas):

    for i in range(len(matriz)):  # ALTO
        for j in range(len(matriz[0])):  # LARGO
            if i == 0:
                if j == 0:
                    matriz[i][j]=" "
                else:
                    matriz[i][j] = columnas[j-1]
            else:
                if j == 0:
                    matriz[i][j]=filas[i-1]
                else:
                    matriz[i][j]="-"
    return matriz


def verMatriz(matriz):
    alto = len(matriz)
    largo = len(matriz[0])
    for i in range(alto):
        for j in range(largo):  # LARGO
            print(matriz[i][j], "\t", end=" ")
        print()


def ganarH(matriz,sim):
    cont=0
    for i in range (1,len(matriz)):
        cont=0
        for j in range(1,len(matriz[0])):
            if matriz[i][j]==sim:
                cont+=1
                if cont is (len(matriz)-1):
                    return 1
                    break;
def ganarV(matriz,sim):
    cont=0
    for j in range (1,len(matriz[0])):
        cont=0
        for i in range(1,len(matriz)):
            if matriz[i][j]==sim:
                cont+=1
                if cont is (len(matriz)-1):
                    return 1
                    break;

def menu(listaConexiones,matriz):

        matrizp=matrizP()
        verMatriz(matriz)
        jugar(matriz,listaJugadores)
        return False
        Client_conn.sendall(b"Juego Terminado.Adios")

def colocar(matriz,sim,Client_conn,listaConexiones,id):
    pos=str(Client_conn.recv(buffer_size),"ascii")
    print(pos)
    fila = int(pos[0])
    col = ord(pos[1]) - 64
    for i in range(len(matriz)):
            if i == fila:
                for j in range(len(matriz[0])):
                    if j == col:
                        if matriz[i][j] == "-":
                            matriz[i][j] = sim
                            cont = "Libre"
                            verMatriz(matriz)
                            Client_conn.sendall(cont.encode())
                            return pos
                        else:
                            cont="Ocupado"
                            Client_conn.sendall(cont.encode())
                            break
                    elif col <= 0 or col >= len(matriz[0]):
                        cont = "Ocupado"
                        Client_conn.sendall(cont.encode())
                        break
            elif fila <= 0 or fila >= len(matriz):
                cont = "Ocupado"
                Client_conn.sendall(cont.enconde())
                break


def enviarAct(pos,listaConexiones):
    for i in range(len(listaConexiones)):
        listaConexiones[i].sendall(pos.encode())


def juegoAuto(matriz,sim,Client_conn):
    cont=0
    while cont==0:
        fila = randint(1,len(matriz)-1)
        col = randint(65,65+(len(matriz)-2))-64#COdigo ascii desde A hasta el tamaño de la matriz

        for i in range (len(matriz)):
            if i==fila:
                for j in range (len(matriz[0])):
                    if j==col:
                        if matriz[i][j]=="-":
                            msg="Elegi Casilla: "+str(fila)+(chr(col+64))
                            matriz[i][j]=sim
                            cont+=1
                            verMatriz(matriz)


                    elif col<=0 or col>=len(matriz[0]):
                        break;
            elif fila <= 0 or fila >= len(matriz):
                break;
    pos=str(fila)+(chr(col+64))
    enviarAct(pos,listaConexiones)
    Client_conn.sendall(pos.encode())
    Client_conn.sendall(msg.encode())


def jugar(matriz,Client_conn,listaConexiones,id):
    simJ="x"
    simS="o"
    cont=0
    print("Jugador es: ", simJ)
    print("Maquina es: ", simS)
    long=(len(matriz)-1)*(len(matriz)-1)
    inicio=time()
    verMatriz(matriz)
    while cont<long:
        print("Turno del jugador\n")
        pos=colocar(matriz,simJ,Client_conn,listaConexiones,id)
        verMatriz(matriz)
        if ganarH(matriz,simJ) == 1:
            print("Ganó el jugador")
            break;
        if ganarV(matriz, simJ) == 1:
             print("Ganó el jugador")
             break;
        cont+=1;
        if cont>=long:
            print("Juego terminado: Es un empate")
            break;
        if (numeroDeJuga(simJ,matriz,listaConexiones)%len(listaConexiones))==0:
            Client_conn.sendall(b"Turno Maquina")
            print("Turno de la máquina\n")
            juegoAuto(matriz,simS, Client_conn)
            if ganarH(matriz,simS) == 1:
                print("Ganó la máquina")
                break;
            if ganarV(matriz, simS) == 1:
                print("Ganó la máquina")
                break;
            cont+=1
            if cont>=long:
                print("Juego terminado: Es un empate")
                break

    final=time()
    print("Duración de la partida: %.2f segundos" %(final-inicio))


def numeroDeJuga(sim,matriz,listaConexiones):
    alto = len(matriz)
    largo = len(matriz[0])
    cont=0
    for i in range(alto):
        for j in range(largo):
            if matriz[i][j]==sim:
                cont+=1
    return cont

def IniciarHilos(listaConexiones,case):
    thread_jugador=[None]*len(listaConexiones)
    if case==1:
        matriz=matrizP()
    if case==2:
        matriz=matrizA()
    for i in range (len(listaConexiones)):
        thread_jugador[i] = threading.Thread(target=jugar, args=(matriz,listaConexiones[i],listaConexiones,i))
        thread_jugador[i].start()

def gestionHilos(Client_addr):
    print("Conectado a", Client_addr)
    print("Se agrego Conexion {} a hilo : {}\n".format(Client_addr,threading.current_thread().ident))

def servirPorSiempre(TCPServerSocket, listaconexiones):
    try:
        while True:
            Client_conn, Client_addr = TCPServerSocket.accept()
            print("Conectado a", Client_addr)
            listaconexiones.append(Client_conn)
            if len(listaconexiones)<numConn:
                Client_conn.sendall(b"Esperando la conexion de los demas jugadores")
            else:
                Client_conn.sendall(b"Eres el jugador que faltaba")
                for i in range (len(listaConexiones)):
                    listaConexiones[i].sendall(b"Todos los jugadores se han conectado")
            if len(listaConexiones)==numConn:
                print("Esperando inicio de juego")
                for i in range(len(listaConexiones)):
                    cliente=i.to_bytes(1, 'little')
                    listaConexiones[i].sendall(cliente)
                case = int.from_bytes(listaConexiones[0].recv(buffer_size), 'little')
                print("Recibido modo de juego: ", case)
                caseb = case.to_bytes(1, 'little')
                for i in range(len(listaConexiones)):
                    listaConexiones[i].sendall(caseb)
                IniciarHilos(listaConexiones,case)
    except Exception as e:
        print(e)

HOST = "192.168.0.103"
PORT = 9755
buffer_size = 1024
listaConexiones = []
numConn=int(input("Introduzca el número de conexiones a aceptar: "))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen(int(numConn))
    print("El servidor TCP está disponible y en espera de solicitudes")
    servirPorSiempre(TCPServerSocket, listaConexiones)

