import pygame, sys
from PIL import Image
import numpy as np
import random

pygame.init()

#Variables indican cuanto recorrer cuadricula (útiles en resize)
difx = 0
dify = 0

# Se establece el número de celdas en el eje x e y
ncx, ncy = 21, 21

#Definimos tamaño
altura = 690
ancho = 690
size = (ancho, altura)

#Tamaño de las celdas
tx = ancho/ncx
ty = altura/ncy

# Se crean las matriz que va a guardar los estados de las celdas
CellState = np.zeros((100, 100), np.int8)
nextCellState = np.zeros((100, 100), np.int8)

#Guarda el estado de juego
pause = True

#colores

wh= (255,255,255)
blue=(0,0,255)
bl=(0,0,0)
gr=(100,100,100)
red=(255,0,0)
greenyellow= (173,255,47)
hotpink= (255,105,180)
lightgrey= (211,211,211)
lime= (0,255,0)
olivedrab= (107,142,35)
paleturquoise= (175,238,238)
pink= (255,192,203)
salmon= (250,128,114)

ColorVivo=wh
ColorMuerto=bl
ColorRendija=wh

#Lista de Colores
AllColors = [blue, bl, gr, red, greenyellow, hotpink, lightgrey, \
             lime, olivedrab, paleturquoise, pink, salmon]

#Medidas de los botones en configuración
colores= pygame.Rect(295,255,100,50)
tamaño= pygame.Rect(295,315,100,50)
start_game = pygame.Rect(295,415,100,50)

## Botones Colores ##

#Textos para botones colores
Fuente = pygame.font.SysFont("Goudy Old Style",int(ancho*.025))
Texto= Fuente.render("CeldasVivas",True,(wh))
TextoM = Fuente.render("CeldasMuertas",True,(wh))
TextoR= Fuente.render("Cuadrícula",True,(wh))

#h_color: Altura de cada boton. Se calcula un tercio de la pantalla
#para boton uno se multiplica por 0, boton 2 por 1 y así hasta n botones
h_color = int(altura/3)
#Dimensiones boton
x_color = ancho/7
y_color = x_color/2
#Se crean rectangulos para botones
coloresVivos= pygame.Rect(int(ancho/140), (0*h_color)+5, x_color, y_color)
coloresMuertos= pygame.Rect(int(ancho/140), (1*h_color)+5, x_color, y_color)
colorRendija=pygame.Rect(int(ancho/140),(2*h_color)+5, x_color, y_color)
tamaño20x20= pygame.Rect(int(ancho/2)-(y_color),(0*h_color)+200, x_color, y_color)
tamaño50x50= pygame.Rect(int(ancho/2)-(y_color),(0*h_color)+(y_color)+210, x_color, y_color)
tamaño100x100= pygame.Rect(int(ancho/2)-(y_color),(0*h_color)+(2*y_color)+220, x_color, y_color)
#Se dibuja botones

#Medida cuadros colores
l_color = int(ancho/34.5)

#Definimos la escala a la que queremos que esten los botones
scale = .4
scale_patt = .25

#Obtemeos la imagen (Especie de Array)
start = Image.open('startbutton.jpg')
#Ancho y Altura original de la imagen (útil para no perder proporción)
start_x, start_y = start.size
#Pasamos la imagen a un objeto de pygame para facilitar el uso de funciones como "blit"
start = pygame.image.fromstring(start.tobytes(),(start_x, start_y), start.mode)
#Se escala el tamaño de la imagen (Ancho como determinanate)
start = pygame.transform.smoothscale(start, (ancho*scale, (ancho*scale)*(start_y/start_x)))

credit = Image.open('startbutton.jpg')
credit_x, credit_y = credit.size
credit = pygame.image.fromstring(credit.tobytes(),(credit_x, credit_y), credit.mode)
credit = pygame.transform.smoothscale(credit, (ancho*scale, (ancho*scale)*(credit_y/credit_x)))

logo = Image.open('logob1.png')
logo_x, logo_y = logo.size
logo = pygame.image.fromstring(logo.tobytes(),(logo_x, logo_y), logo.mode)
logo = pygame.transform.smoothscale(logo, (ancho*scale, (ancho*scale)*(logo_y/logo_x)))

#Botones patrones
    #Ancho de botones
width_patterns = ancho*scale_patt

SLifes = Image.open('startbutton.jpg')
SLifes_x, SLifes_y = SLifes.size
SLifes = pygame.image.fromstring(SLifes.tobytes(),(SLifes_x, SLifes_y), SLifes.mode)
SLifes = pygame.transform.smoothscale(SLifes, (width_patterns, width_patterns*(SLifes_y/SLifes_x)))

Oscilla = Image.open('startbutton.jpg')
Oscilla_x, Oscilla_y = Oscilla.size
Oscilla = pygame.image.fromstring(Oscilla.tobytes(),(Oscilla_x, Oscilla_y), Oscilla.mode)
Oscilla = pygame.transform.smoothscale(Oscilla, (width_patterns, width_patterns*(Oscilla_y/Oscilla_x)))

Ships = Image.open('startbutton.jpg')
Ships_x, Ships_y = Ships.size
Ships = pygame.image.fromstring(Ships.tobytes(),(Ships_x, Ships_y), Ships.mode)
Ships = pygame.transform.smoothscale(Ships, (width_patterns, width_patterns*(Ships_y/Ships_x)))

Methu = Image.open('startbutton.jpg')
Methu_x, Methu_y = Methu.size
Methu = pygame.image.fromstring(Methu.tobytes(),(Methu_x, Methu_y), Methu.mode)
Methu = pygame.transform.smoothscale(Methu, (width_patterns, width_patterns*(Methu_y/Methu_x)))

Others = Image.open('startbutton.jpg')
Others_x, Others_y = Others.size
Others = pygame.image.fromstring(Others.tobytes(),(Others_x, Others_y), Others.mode)
Others = pygame.transform.smoothscale(Others, (width_patterns, width_patterns*(Others_y/Others_x)))

#Se crea la pantalla
screen = pygame.display.set_mode((ancho, altura),  pygame.RESIZABLE)

# Se establece el color de fondo de la pantalla
screen.fill(bl)

#Preparamos la velocidad de refresco
fps = 6
run_fps = fps
brush_fps = 60
clock=pygame.time.Clock()

## Hit Box ##

#Se toman las coordenadas del boton, 
#para usarlas para crear el rectangulo de boton (Así usar collidepoint)
mesh_start = (((screen.get_width()/2)-(start.get_width()/2)), altura/2)
#Se toman las medidas del boton
start_rect = start.get_rect()
#Se crea la "Hitbox" (rectangulo que no se ve) pero detecta colisiones
start_rect = pygame.Rect(start_rect[0] + mesh_start[0], \
                         start_rect[1] + mesh_start[1], start_rect[2], start_rect[3])
mesh_credit = ((screen.get_width()/2)-(credit.get_width()/2), altura/1.5)
credit_rect = credit.get_rect()
credit_rect = pygame.Rect(credit_rect[0] + mesh_credit[0], \
                         credit_rect[1] + mesh_credit[1], credit_rect[2], credit_rect[3])
mesh_SLifes = ((screen.get_width()/30), altura/11)
SLifes_rect = SLifes.get_rect()
SLifes_rect = pygame.Rect(SLifes_rect[0] + mesh_SLifes[0], \
                         SLifes_rect[1] + mesh_SLifes[1], SLifes_rect[2], SLifes_rect[3])

mesh_Oscilla = ((screen.get_width()/30), altura*3/11)
Oscilla_rect = Oscilla.get_rect()
Oscilla_rect = pygame.Rect(Oscilla_rect[0] + mesh_Oscilla[0], \
                         Oscilla_rect[1] + mesh_Oscilla[1], Oscilla_rect[2], Oscilla_rect[3])

mesh_Ships = ((screen.get_width()/30), altura*5/11)
Ships_rect = Ships.get_rect()
Ships_rect = pygame.Rect(Ships_rect[0] + mesh_Ships[0], \
                         Ships_rect[1] + mesh_Ships[1], Ships_rect[2], Ships_rect[3])

mesh_Methu = ((screen.get_width()/30), altura*7/11)
Methu_rect = Methu.get_rect()
Methu_rect = pygame.Rect(Methu_rect[0] + mesh_Methu[0], \
                         Methu_rect[1] + mesh_Methu[1], Methu_rect[2], Methu_rect[3])

mesh_Others = ((screen.get_width()/30), altura*9/11)
Others_rect = Others.get_rect()
Others_rect = pygame.Rect(Others_rect[0] + mesh_Others[0], \
                         Others_rect[1] + mesh_Others[1], Others_rect[2], Others_rect[3])

# "Global" Le indica a las funciones que
# se trata de variables declaradas fuera (arriba)
# se debe usar cuando (=)

#Dibuja las superficies del ciclo principal (Botones/pantalla)
def Dibujo_Surfaces():
    screen.fill(bl)
    pygame.Surface.blit(screen, logo, ((screen.get_width()/2)-(start.get_width()/2), altura/6))
    pygame.Surface.blit(screen, start, mesh_start)
    pygame.Surface.blit(screen, credit, mesh_credit)

#Dibuja los botones de Patterns
def Dibujo_SurfacesPatterns():
    screen.fill(bl)
    # altura*n/numero_espacios (Para sea parejo)
    pygame.Surface.blit(screen, SLifes, mesh_SLifes)
    pygame.Surface.blit(screen, Oscilla, mesh_Oscilla)
    pygame.Surface.blit(screen, Ships, mesh_Ships)
    pygame.Surface.blit(screen, Methu, mesh_Methu)
    pygame.Surface.blit(screen, Others, mesh_Others)

def Dibujo_SurfacesColors():
    global l_color
    pygame.draw.rect(screen,(gr),coloresVivos,0)
    pygame.draw.rect(screen,(bl),coloresMuertos,0)
    pygame.draw.rect(screen,(gr),colorRendija,0)
    screen.blit(Texto,(int(ancho/140) + (x_color/10),(0*h_color)+(y_color/2)))
    screen.blit(TextoM,(int(ancho/140) + (x_color/10),(1*h_color)+(y_color/2)))
    screen.blit(TextoR,(int(ancho/140) + (x_color/10),(2*h_color)+(y_color/2)))
    l_color = int(ancho/34.5)
    
    #Ancho de Vista previa
    x_CeldaPre = int(ancho/9)
    #Posición en y de la Vista previa
    h_VistaPre = int(altura/2)-int(x_CeldaPre*3/2)
    #Poscición en x de la Vista previa
    x_VistaPre = int(screen.get_width()*5/8)
    #Vista previa
    pygame.draw.rect(screen,ColorMuerto,pygame.Rect(x_VistaPre+(0*x_CeldaPre), h_VistaPre+(0*x_CeldaPre), x_CeldaPre*3, x_CeldaPre*3),0)
    pygame.draw.rect(screen,ColorRendija,pygame.Rect(x_VistaPre+(0*x_CeldaPre), h_VistaPre+(0*x_CeldaPre), x_CeldaPre, x_CeldaPre),1)
    pygame.draw.rect(screen,ColorRendija,pygame.Rect(x_VistaPre+(1*x_CeldaPre), h_VistaPre+(0*x_CeldaPre), x_CeldaPre, x_CeldaPre),1)
    pygame.draw.rect(screen,ColorRendija,pygame.Rect(x_VistaPre+(2*x_CeldaPre), h_VistaPre+(0*x_CeldaPre), x_CeldaPre, x_CeldaPre),1)
    pygame.draw.rect(screen,ColorRendija,pygame.Rect(x_VistaPre+(0*x_CeldaPre), h_VistaPre+(1*x_CeldaPre), x_CeldaPre, x_CeldaPre),1)
    pygame.draw.rect(screen,ColorVivo,pygame.Rect(x_VistaPre+(1*x_CeldaPre), h_VistaPre+(1*x_CeldaPre), x_CeldaPre, x_CeldaPre),0)
    pygame.draw.rect(screen,ColorRendija,pygame.Rect(x_VistaPre+(2*x_CeldaPre), h_VistaPre+(1*x_CeldaPre), x_CeldaPre, x_CeldaPre),1)
    pygame.draw.rect(screen,ColorRendija,pygame.Rect(x_VistaPre+(0*x_CeldaPre), h_VistaPre+(2*x_CeldaPre), x_CeldaPre, x_CeldaPre),1)
    pygame.draw.rect(screen,ColorRendija,pygame.Rect(x_VistaPre+(1*x_CeldaPre), h_VistaPre+(2*x_CeldaPre), x_CeldaPre, x_CeldaPre),1)
    pygame.draw.rect(screen,ColorRendija,pygame.Rect(x_VistaPre+(2*x_CeldaPre), h_VistaPre+(2*x_CeldaPre), x_CeldaPre, x_CeldaPre),1)

def Dibujo_SurfacesSizes():
    global ncx,ncy,tx,ty
    screen.fill(ColorMuerto)
    pygame.draw.rect(screen,(gr),tamaño20x20,0) 
    pygame.draw.rect(screen,(gr),tamaño50x50,0)  
    pygame.draw.rect(screen,(gr),tamaño100x100,0)    
    for y in range(0, ncx):
        for x in range (0, ncy):            
            Coordenadas=[((x)*tx, (y)*ty), ((x+1)*tx, (y)*ty), ((x+1)*tx, (y+1)*ty ),((x)*tx, (y+1)*ty)]
            pygame.draw.polygon(screen,ColorRendija, Coordenadas,1)
    
    
    
def Dibujo_SurfacePickColors(n_boton):
    for i in range(12):
        pygame.draw.rect(screen,AllColors[i],(pygame.Rect(x_color+(5*(i+2))+(i*l_color),(n_boton*h_color)+5,l_color,l_color)),(i==1))
    pygame.draw.rect(screen,AllColors[1],(pygame.Rect(x_color+(5*2)+(0*l_color),(n_boton*h_color)+10+l_color,l_color,l_color)),0)
    print(n_boton)
    
#En caso de RESIZE se modifica el tamaño que tendran las celdas (Necesita nuevo tamaño)
def AjusteTamano_Celdas(event_w, event_h):
    #"global" para que tome las variables exteriores a la función ('=')
    global difx, dify, tx, ty, altura, ancho
    #Se toma al lado menor para conservar la proporción de un cuadrado
    if(event_w < event_h):
        altura = ancho = event_w
        dify = (event_h - ancho) / 2
        difx = 0
    else:
        altura = ancho = event_h
        difx = (event_w - altura) / 2
        dify = 0
    #Ajustamos tamaño de las celdas
    tx = ancho / ncx
    ty = altura / ncy

#En caso de RESIZE se modifica el tamaño de los botones, y pantalla (Necesita nuevo tamaño)
def AjusteTamano_Surfaces(event_w, event_h):
    #Ajustamos la pantalla de tamaño // POSIBLEMENTE NEGOCIABLE
    global screen, logo, start, options, credit, mesh_start, start_rect, mesh_credit
    screen = pygame.display.set_mode((event_w, event_h), pygame.RESIZABLE)
    #Reajustamos tamaño boton
    logo = pygame.transform.smoothscale(logo, (ancho*scale, (ancho*scale)*(logo_y/logo_x)))
    start = pygame.transform.smoothscale(start, (ancho*scale, (ancho*scale)*(start_y/start_x)))
    mesh_start = (((screen.get_width()/2)-(start.get_width()/2)), screen.get_height()/2)
    start_rect = start.get_rect()
    start_rect = pygame.Rect(start_rect[0] + mesh_start[0], \
                             start_rect[1] + mesh_start[1], start_rect[2], start_rect[3])
    credit = pygame.transform.smoothscale(credit, (ancho*scale, (ancho*scale)*(credit_y/credit_x)))
    mesh_credit = ((screen.get_width()/2)-(credit.get_width()/2), altura/1.5)
    credit_rect = credit.get_rect()
    credit_rect = pygame.Rect(credit_rect[0] + mesh_credit[0], \
                             credit_rect[1] + mesh_credit[1], credit_rect[2], credit_rect[3])

#Reajusta el tamaño de botones Patterns // Misma lógica a Tamano_Surfaces
def AjusteTamano_SurfacesPatterns(event_w, event_h):
    global SLifes, Oscilla, Ships, Methu, Others, mesh_SLifes, SLifes_rect, \
        mesh_Oscilla, Oscilla_rect, mesh_Ships, Ships_rect, mesh_Methu, Methu_rect, \
        mesh_Others, Others_rect
    #Reajustamos tamaño boton
    SLifes = pygame.transform.smoothscale(SLifes, (ancho*scale_patt, (ancho*scale_patt)*(SLifes_y/SLifes_x)))
    mesh_SLifes = ((screen.get_width()/30), altura/11)
    SLifes_rect = SLifes.get_rect()
    SLifes_rect = pygame.Rect(SLifes_rect[0] + mesh_SLifes[0], \
                             SLifes_rect[1] + mesh_SLifes[1], SLifes_rect[2], SLifes_rect[3])
    Oscilla = pygame.transform.smoothscale(Oscilla, (ancho*scale_patt, (ancho*scale_patt)*(Oscilla_y/Oscilla_x)))
    mesh_Oscilla = ((screen.get_width()/30), altura/11)
    Oscilla_rect = Oscilla.get_rect()
    Oscilla_rect = pygame.Rect(Oscilla_rect[0] + mesh_Oscilla[0], \
                             Oscilla_rect[1] + mesh_Oscilla[1], Oscilla_rect[2], Oscilla_rect[3])
    Ships = pygame.transform.smoothscale(Ships, (ancho*scale_patt, (ancho*scale_patt)*(Ships_y/Ships_x)))
    mesh_Ships = ((screen.get_width()/30), altura*5/11)
    Ships_rect = Ships.get_rect()
    Ships_rect = pygame.Rect(Ships_rect[0] + mesh_Ships[0], \
                             Ships_rect[1] + mesh_Ships[1], Ships_rect[2], Ships_rect[3])
    Methu = pygame.transform.smoothscale(Methu, (ancho*scale_patt, (ancho*scale_patt)*(Methu_y/Methu_x)))
    mesh_Methu = ((screen.get_width()/30), altura*7/11)
    Methu_rect = Methu.get_rect()
    Methu_rect = pygame.Rect(Methu_rect[0] + mesh_Methu[0], \
                             Methu_rect[1] + mesh_Methu[1], Methu_rect[2], Methu_rect[3])
    Others = pygame.transform.smoothscale(Others, (ancho*scale_patt, (ancho*scale_patt)*(Others_y/Others_x)))
    mesh_Others = ((screen.get_width()/30), altura*9/11)
    Others_rect = Others.get_rect()
    Others_rect = pygame.Rect(Others_rect[0] + mesh_Others[0], \
                             Others_rect[1] + mesh_Others[1], Others_rect[2], Others_rect[3])
    
#Reajusta el tamaño del texto volviendolo a calcular
def AjusteTamano_Letras():
    global Fuente, Texto, TextoM, TextoR
    Fuente = pygame.font.SysFont("Goudy Old Style",int(ancho*.025))
    Texto= Fuente.render("CeldasVivas",True,(wh))
    TextoM = Fuente.render("CeldasMuertas",True,(wh))
    TextoR= Fuente.render("Cuadrícula",True,(wh))

def AjusteTamano_Colores():
    global h_color, x_color, y_color, coloresVivos, coloresMuertos, colorRendija
    #h_color: Altura de cada boton. Se calcula un tercio de la pantalla
    #para boton uno se multiplica por 0, boton 2 por 1 y así hasta n botones
    h_color = int(altura/3)
    #Dimensiones boton
    x_color = ancho/7
    y_color = x_color/2
    #Se crean rectangulos para botones
    coloresVivos= pygame.Rect(int(ancho/140), (0*h_color)+5, x_color, y_color)
    coloresMuertos= pygame.Rect(int(ancho/140), (1*h_color)+5, x_color, y_color)
    colorRendija=pygame.Rect(int(ancho/140),(2*h_color)+5, x_color, y_color)
    #Se dibuja botones

#Manda a llamar a todas las funciones RESIZE
def AjusteTamano_All(event_w, event_h):
    AjusteTamano_Celdas(event_w, event_h)
    AjusteTamano_Surfaces(event_w, event_h)
    AjusteTamano_SurfacesPatterns(event_w, event_h)
    AjusteTamano_Letras()
    AjusteTamano_Colores()

#Verifica si click sobre un boton (Necesita posición mouse) (Regresa string)
def Collision_Surfaces_Main(Mse_px, Mse_py):
    if(start_rect.collidepoint(Mse_px, Mse_py)):
        return "start"
    elif(credit_rect.collidepoint(Mse_px, Mse_py)):
        return "credit"

#Equivalente de Collision Main pero para el menu Patterns
def Collision_Surfaces_Patterns(Mse_px, Mse_py):
    if(SLifes_rect.collidepoint(Mse_px, Mse_py)):
        return "SLifes"
    elif(Oscilla_rect.collidepoint(Mse_px, Mse_py)):
        return "Oscilla"
    elif(Ships_rect.collidepoint(Mse_px, Mse_py)):
        return "Ships"
    elif(Methu_rect.collidepoint(Mse_px, Mse_py)):
        return "Methu"
    elif(Others_rect.collidepoint(Mse_px, Mse_py)):
        return "Others"

def Collision_SurfacePickColors(Mse_px, Mse_py, n_boton):
    global ColorVivo, ColorMuerto, ColorRendija
    chose = False
    for i in range(12):
        if pygame.Rect(x_color+(5*(i+2))+(i*l_color),(n_boton*h_color)+5,l_color,l_color).collidepoint(Mse_px, Mse_py):
            if(i == 1):
                PickColor = wh
            else:
                PickColor = AllColors[i]
            chose = True
            break
    if pygame.Rect(x_color+(5*2)+(0*l_color),(n_boton*h_color)+10+l_color,l_color,l_color).collidepoint(Mse_px, Mse_py):
        PickColor =  AllColors[1]
        chose = True
    if chose:
        if n_boton == 0:
            ColorVivo = PickColor
        elif n_boton == 1:
            ColorMuerto = PickColor
        else:
            ColorRendija =  PickColor

#Función que limpia el tablero
def ClearCells():
    for i in range(100):
        for j in range(100):
            nextCellState[i, j] = 0

def Random_State():
    ClearCells()
    rcx = []
    rcy = []
    nstate = random.randint(0, int((ncx*ncy)/2))
    for i in range(nstate):
        rcx.append(random.randint(0, ncx))
        rcy.append(random.randint(0, ncy))
    nextCellState[rcx, rcy] = 1

#Colorea la celda en la que esta sostenido el mouse
#Necesita de la posción y si es botón izquiero o derecho
def Pinta_Celdas(px, py, draw):
    if px > difx and px < ((ncx+1)*tx)+difx and \
    py > dify and py < ((ncy+1)*ty)+dify:
        cx, cy = int((np.floor((px-difx) / tx))), int((np.floor((py-dify) / ty)))
        nextCellState[cx, cy] = draw

#Funcion para imprimir la matriz
#Útil para dibujado de patrones, no pensada para la versión final sino para desarrollo
def imprime():
    for y in range(ncy):
        print(nextCellState[y][0:ncx])

#Dentro de Color_Vivo/Muerto/Rendija solo se dibuja nuevos botones
#No se borran los de Opciones, sin embargo quedan inutilizables hasta cerrar


                    
def Color_Vivo():
    global ColorVivo
    run=True
    while run:
        #Función que coloca los cuadros
        Dibujo_SurfacePickColors(0)
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit() 
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:                   
                    run=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                #Seleccipon de Color al clicar
                if event.button==1:
                    px, py = pygame.mouse.get_pos()
                    Collision_SurfacePickColors(px, py, 0)
                    Dibujo_SurfacesColors()
            if event.type == pygame.VIDEORESIZE:
                AjusteTamano_All(event.w, event.h)
                screen.fill(wh)
                Dibujo_SurfacesColors()
        
        pygame.display.update()   
    screen.fill(wh)

def Color_Muerto():
    global ColorMuerto
    
    run=True
    while run:
        
        Dibujo_SurfacePickColors(1)
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:                   
                    run=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    px, py = pygame.mouse.get_pos()
                    Collision_SurfacePickColors(px, py, 1)
                    Dibujo_SurfacesColors()
            if event.type == pygame.VIDEORESIZE:
                AjusteTamano_All(event.w, event.h)
                screen.fill(wh)
                Dibujo_SurfacesColors()
            
        pygame.display.update() 
    screen.fill(wh)

def Color_Rendija():
    global ColorRendija
    run=True
    
    while run:
        
        Dibujo_SurfacePickColors(2)
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()  
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:                   
                    run=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    px, py = pygame.mouse.get_pos()
                    Collision_SurfacePickColors(px, py, 2)
                    Dibujo_SurfacesColors()
            if event.type == pygame.VIDEORESIZE:
                AjusteTamano_All(event.w, event.h)
                screen.fill(wh)
                Dibujo_SurfacesColors()
            
        pygame.display.update() 
        
    screen.fill(wh)

#Función Colores (Apartado de Opciones)
def Colores():
    run= True 
    while run:
        screen.fill(wh)
        Dibujo_SurfacesColors()          
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    run=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                #Saber sobre que se pico
                #Notese que no se desdibuja los botones de ciclo Opciones
                    if coloresVivos.collidepoint(pygame.mouse.get_pos()):
                        Color_Vivo()
                    elif coloresMuertos.collidepoint(pygame.mouse.get_pos()):
                        Color_Muerto()
                    elif colorRendija.collidepoint(pygame.mouse.get_pos()):
                        Color_Rendija()
            if event.type == pygame.VIDEORESIZE:
                AjusteTamano_All(event.w, event.h)
        
        pygame.display.update()
    screen.fill(wh)
    
def Tamaño():
    global ncx, ncy, tx, ty,ancho,altura
    tx = ancho/ncx
    ty = altura/ncy
    
    run= True 
    while run:
        screen.fill(wh)
        Dibujo_SurfacesSizes()
        for event in pygame.event.get():
            
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    run=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                #Saber sobre que se pico
                #Notese que no se desdibuja los botones de ciclo Opciones
                    if tamaño20x20.collidepoint(pygame.mouse.get_pos()):
                        ncx=20
                        ncy=20
                        tx = ancho/ncx
                        ty = altura/ncy
                        Dibujo_SurfacesSizes()
                    elif tamaño50x50.collidepoint(pygame.mouse.get_pos()):
                        ncx=50
                        ncy=50
                        tx = ancho/ncx
                        ty = altura/ncy
                        Dibujo_SurfacesSizes()                       
                    elif tamaño100x100.collidepoint(pygame.mouse.get_pos()):
                        ncx=100 
                        ncy=100
                        tx = ancho/ncx
                        ty = altura/ncy
                        Dibujo_SurfacesSizes()
                if event.type == pygame.VIDEORESIZE:
                    AjusteTamano_All(event.w, event.h)
      
        pygame.display.update()
    screen.fill(wh) 

#Función del juego
def GameLife():
    global pause, screen, fps
    run = True
    while run:
        # Se hace una copia del juego en cada iteración que guarda los cambios sin afectar a
        # las demás celdas
        CellState = np.copy(nextCellState)
        
        # Se limpia la pantalla en cada iteración para que no se sobrepongan los cambios
        # Se pone un retraso para que vaya más lento el programa y se aprecie mejor 
        screen.fill(ColorMuerto)
        
        # Se registran los eventos que ocurran durante la ejecución
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #Si se presiona una tecla
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: #Space = pausar el juego
                    pause = not pause
                elif event.key == pygame.K_c: #C = limpiar tablero
                    ClearCells()
                elif event.key == pygame.K_ESCAPE: #Q = salir de la pantalla de juego
                    run = False
                elif event.key == pygame.K_s:
                    imprime()
                    
            brush = pygame.mouse.get_pressed() #Estado botones mouse
            px, py = pygame.mouse.get_pos()
            if True in brush:
                if pause:
                    fps = brush_fps
                if brush[0]:
                    draw = 1
                elif brush[2]:
                    draw = 0
                Pinta_Celdas(px, py, draw)   
            else:
                fps = run_fps
            if event.type == pygame.VIDEORESIZE:
                AjusteTamano_All(event.w, event.h)
        
        # Se establecen los bucles que recorrerán las matrices y diujarán las celdas
        # de izquierda a derecha 
        for y in range (ncy):
            for x in range (ncx):
                
                # Se ejecuta o no cada que se presiona una tecla. Al pausar, las celdas
                # quedan como están, sin cambios
                if not pause:
                     
                    # Se examina el estado de las celdas vecinas
                    AliveCells = CellState[(x - 1) % ncx, (y - 1) % ncy] + \
                                 CellState[(x    ) % ncx, (y - 1) % ncy] + \
                                 CellState[(x + 1) % ncx, (y - 1) % ncy] + \
                                 CellState[(x - 1) % ncx, (y    ) % ncy] + \
                                 CellState[(x + 1) % ncx, (y    ) % ncy] + \
                                 CellState[(x - 1) % ncx, (y + 1) % ncy] + \
                                 CellState[(x    ) % ncx, (y + 1) % ncy] + \
                                 CellState[(x + 1) % ncx, (y + 1) % ncy] 
        
                    # Se establecen las reglas del juego
                    if CellState[x, y] == 0 and AliveCells == 3:
                        nextCellState[x, y] = 1
                        
                    elif CellState[x, y] == 1 and (AliveCells < 2 or AliveCells > 3):
                        nextCellState[x, y] = 0
                
                # Se establecen las coordenadas de los cubos que formarán la rejilla
                cube = [(((x)*tx)+difx, ((y)*ty)+dify), (((x)*tx)+difx, ((y+1)*ty)+dify), 
                        ((x+1)*tx+difx, ((y+1)*ty)+dify), (((x+1)*tx)+difx, ((y)*ty)+dify)]
                
                # Dependiendo del estado de la celda, el cubo será blanco u oscuro            
                if nextCellState[x, y] == 1:
                    pygame.draw.polygon(screen, ColorVivo, cube, 0)
                    
                else:
                    pygame.draw.polygon(screen, ColorRendija, cube, 1)
        
        #Se limita la velocidad de refresco
        clock.tick(fps)
        # Se muestra en pantalla la cuadrícula
        pygame.display.update()
    #Se prepara pantalla para volver a dibujar el menu
    screen.fill(bl)

#Funcion Opciones
def Opciones():

    Fuente = pygame.font.SysFont("Goudy Old Style",23)
    Texto= Fuente.render("Colores",True,(wh))
    
    screen.fill(wh)
    run= True 
    while run:
        
        #Dibujamos los botones (Como rectangulos)
        pygame.draw.rect(screen,(gr),colores,0)
        pygame.draw.rect(screen,(gr),tamaño,0)
        pygame.draw.rect(screen, (gr), start_game, 0)
        screen.blit(Texto,(309,267))
        
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    run = False
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    #Utilizando ".collidepoint" definimos si toca el boton
                    if colores.collidepoint(pygame.mouse.get_pos()):
                        Colores()
                    elif tamaño.collidepoint(pygame.mouse.get_pos()):
                        Tamaño()
                    elif start_game.collidepoint(pygame.mouse.get_pos()):
                        #En caso de iniciar el juego:
                        screen.fill(bl)
                        GameLife()
                        run = False #False para salir directo al menu principal
            if event.type == pygame.VIDEORESIZE:
                AjusteTamano_All(event.w, event.h)
        
        pygame.display.update()

# Se inicia el bucle principal (Menu Principal)
while True:
    #Redibujo de superficies
    Dibujo_Surfaces()
    # Se registran los eventos que ocurran durante la ejecución
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            px, py = pygame.mouse.get_pos()
            #Guardamos la string que nos da "Colision_Surfaces"
            Place_Colis = Collision_Surfaces_Main(px, py)
            #Escogemos acciones según la string
            if Place_Colis == "start":
                Opciones()
                #Terminando el juego se vuelve a poner el menu
                Dibujo_Surfaces()
            elif Place_Colis == "credit":
                print("Credit")
        #Si se cambia de tamaño la pantalla
        if event.type == pygame.VIDEORESIZE:
            AjusteTamano_All(event.w, event.h)
    
    #Se limita la velocidad de refresco
    clock.tick(fps)
    # Se muestra en pantalla la cuadrícula
    pygame.display.update()
