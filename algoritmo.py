from tablero import *

PROFUNDIDAD=2

class Nodo:
    def __init__(self, posicion, padre, tablero, turno):
        self.tablero = tablero
        self.posicion = posicion
        self.turno = turno
        self.valor = 0
        self.padre = padre
        self.hijos = []

    def getProfundidad(self):
        if self.padre == None:
            return 0
        else:
            return self.padre.getProfundidad() + 1
    
    def getPositionX(self):
        return self.posicion[0]

    def getPositionY(self):
        return self.posicion[1]
    
    def getValor(self):
        return self.valor
    
    def setValor(self, valor):
        self.valor = valor
    
    def dibujarHijos(self):
        for hijo in self.hijos:
            print (hijo.posicion)
            hijo.dibujarHijos()

def obtenerOpciones(tablero):
    opciones = []
    ancho = tablero.getAncho()
    alto = tablero.getAlto()

    for j in range(ancho):
        for i in range(alto):
            if tablero.getCelda(0,j) != 0:
                break
            if tablero.getCelda(i,j) != 0:
                opciones.append([i-1,j])
                break
            if i == alto-1 and tablero.getCelda(i,j) == 0:
                opciones.append([i,j])
                break

    return opciones

def busca(tablero, col):  
    if tablero.getCelda(0,col) != 0:
        i=-1
    i=0
    while i<tablero.getAlto() and tablero.getCelda(i,col)==0:          
        i=i+1      
    i=i-1
   
    return i

# Evaluamos el movimiento posicion con en tablero
def evaluar(nodo):
    tablero = nodo.tablero
    ancho = tablero.getAncho()
    alto = tablero.getAlto()
    posicion = nodo.posicion
    turno = nodo.turno
    
    # JEUGO DEL 4 EN RAYA
    # Con la posicion del nodo, evaluamos el tablero
    # Si hay 4 en seguidas, devuelve 100
    # Si hay 3 en seguidas y a los lados dos vacias, devuelve 90
    # Si hay 3 en seguidas y a los lados una vacia, devuelve 80
    # Si hay 2 en seguidas y a los lados dos vacias, devuelve 50
    # Si hay 2 en seguidas y a los lados una vacia, devuelve 40
    # Si hay 1 y a los lados dos vacias, devuelve 20
    # Si hay 1 y a los lados una vacia, devuelve 10
    # Todo lo demas 0

    # Obtenemos la vertical desde el tablero de alto por ancho
    vertical = []
    vertical_buscar = posicion[0]
    
    for i in range(alto):
        vertical.append(tablero.getCelda(i, posicion[1]))
        
    # Obtenemos la horizontal desde el tablero de alto por ancho
    horizontal = []
    horizontal_buscar = posicion[1]

    for i in range(ancho):
        horizontal.append(tablero.getCelda(posicion[0], i))

    puntuacion = 0
    
    # Recorrer vertical
    count = 0
    for i, v in enumerate(vertical):
        if v == turno:
            count += 1
        else:
            count = 0
        
        if (count == 4 and vertical_buscar in range(i-3, i+1)):
            puntuacion += 100
        
        if (count == 3 and vertical_buscar in range(i-2, i+1)):
            if (i-3 >= 0 and i+1 <= (alto - 1)):
                if (vertical[i-3] == 0 and vertical[i+1] == 0):
                    puntuacion += 90
            elif (i-3 >= 0 and i+1 > (alto - 1)):
                if (vertical[i-3] == 0):
                    puntuacion += 80
            elif (i-3 >= 0 and i+1 > (alto - 1)):    
                if (vertical[i+1] == 0):
                    puntuacion += 80
            
        if (count == 2 and vertical_buscar in range(i-1, i+1)):
            if (vertical[i-2] == 0 and vertical[i+1] == 0):
                puntuacion += 50
            elif (vertical[i-2] == 0 or vertical[i+1] == 0):
                puntuacion += 40
    
        if (count == 1 and vertical_buscar in range(i, i+1)):
            if (vertical[i-1] == 0 and vertical[i+1] == 0):
                puntuacion += 20
            elif (vertical[i-1] == 0 or vertical[i+1] == 0):
                puntuacion += 10
    
    # Recorrer horizontal
    for i, v in enumerate(horizontal):
        if v == turno:
            count += 1
        else:
            count = 0
        
        if (count == 4 and horizontal_buscar in range(i-3, i+1)):
            puntuacion += 100
        
        if (count == 3 and horizontal_buscar in range(i-2, i+1)):
            if (horizontal[i-3] == 0 and horizontal[i+1] == 0):
                puntuacion += 90
            elif (horizontal[i-3] == 0 or horizontal[i+1] == 0):
                puntuacion += 80
            
        if (count == 2 and horizontal_buscar in range(i-1, i+1)):
            if (horizontal[i-2] == 0 and horizontal[i+1] == 0):
                puntuacion += 50
            elif (horizontal[i-2] == 0 or horizontal[i+1] == 0):
                puntuacion += 40
    
        if (count == 1 and horizontal_buscar in range(i, i+1)):
            if (horizontal[i-1] == 0 and horizontal[i+1] == 0):
                puntuacion += 20
            elif (horizontal[i-1] == 0 or horizontal[i+1] == 0):
                puntuacion += 10
    
    return puntuacion

def minimax(nodo):
    # Obtenemos el turno
    turno = 2 if nodo.getProfundidad() % 2 == 0 else 1
    
    # Compruebo la profundidad del arbol
    if nodo.getProfundidad() == (PROFUNDIDAD):
        # Devuelvo el nodo con el valor mas alto o mas bajo, segun a quien le toque jugar
        nodo.setValor(evaluar(nodo))

        return nodo.getValor()
    
    else:
        # Genero los hijos
        for posicion in obtenerOpciones(nodo.tablero):
            tablero_base = Tablero(nodo.tablero)
            tablero_base.setCelda(posicion[0], posicion[1], turno)
            nodo.hijos.append(Nodo(posicion, nodo, tablero_base, 2 if nodo.turno == 1 else 1))

        # Llamo a minimax para cada hijo y obtengo el valor maximo o minimo
        valores = [minimax(hijo) for hijo in nodo.hijos]
        
        # Obtener el valor numerico mas alto o mas bajo, segun a quien le toque jugar
        if turno == 2:
            valores_ordenados = sorted(valores, reverse=True)
        else:
            valores_ordenados = sorted(valores)
        
        nodo.setValor(valores_ordenados[0])
        
        # Si el campo posicion esta vacio devuelve el nodo hijo que tenga mayor valor
        if nodo.posicion == []:
            for hijo in nodo.hijos:
                if hijo.getValor() == nodo.getValor():
                    return hijo
                
        return nodo.getValor()
        
# llama al algoritmo que decide la jugada
def juega(tablero_real, posicion):
    ####################################################
    ## sustituir este código por la llamada al algoritmo
    ####################################################
    tablero = Tablero(tablero_real)

    # Si el nodo no tiene posicion, devuelve el nodo hijo que tenga mayor valor
    nodo = minimax(Nodo([], None, tablero, 1))
    print(nodo.getPositionX(), nodo.getPositionY())

    posicion[0]=nodo.getPositionX()
    posicion[1]=nodo.getPositionY()
    
    # tablero.setCelda(6,0,2)
    # tablero.setCelda(5,0,1)
    # tablero.setCelda(4,0,2)
    # tablero.setCelda(3,0,1)
    # tablero.setCelda(2,0,2)
    # tablero.setCelda(1,0,1)
    # tablero.setCelda(0,0,2)
    
    # print(tablero)
    
    # print(obtenerOpciones(tablero))
    ####################################################  