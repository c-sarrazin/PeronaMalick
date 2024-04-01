#### ATTENTION ! ####
# Pour que le programme s'exécute, le dossier projet doit être structuré comme suit :
# - un dossier d'où viennent les photos (notre /photos)
# un dossier vide 'resultats/' où seront automatiquement sauvegardés les fichiers résultats.

import numpy as np
from PIL import Image
import datetime, time
NOM_IMAGE = 'photos/lax.jpg'

# Encodage de l'image comme array Numpy

img = Image.open(NOM_IMAGE)
numpydata = np.asarray(img)
H, L = numpydata.shape[0],numpydata.shape[1]

# Paramètres

BRUITAGE_GAUSSIEN = False
BRUITAGE_POIVRESEL = True
LAMBDA = 1e-8
T = 1
N = 300
NU=0.4/((((H+2)**2)+((L+2)**2))*T/N)
NU1 = NU
NU2 = NU

## Calcul de la condition CFL pour le terme diffusif

cfl=(((H+2)**2)+((L+2)**2))*NU1*T/N
print(cfl)

# Modifications de l'array image
## Passage en noir et blanc

def gris(rgb):
    r, g, b = rgb[0], rgb[1], rgb[2]
    return(0.2989 * r + 0.5870 * g + 0.1140 * b)

## Bruitage

def bruitage_gaussien(pixel):
    if BRUITAGE_GAUSSIEN:
        perturb = np.random.default_rng().normal(loc=0, scale=10)
        return pixel+perturb
    else:
        return pixel

def fix(val): # astreint les valeurs après bruitage à l'intervalle [0, 255]
    if val < 0 :
        return 0
    elif val > 255:
        return 255
    else:
        return val

def bruitage_poivresel(im):
    if BRUITAGE_POIVRESEL:
        nombre_noir = np.random.randint(int((H*L)/30), int((H*L)/10))
        nombre_blanc = np.random.randint(int((H*L)/30), int((H*L)/10))
        for n in range(nombre_blanc):
            y=np.random.randint(0, H - 1)
            x=np.random.randint(0, L - 1)
            im[y][x] = 255
        for n in range(nombre_noir):
            y=np.random.randint(0, H - 1)
            x=np.random.randint(0, L - 1)
            im[y][x] = 0
    return im

## Création et affichage de l'image de départ

imagebw= np.array([[fix(bruitage_gaussien(gris(rgb))) for rgb in numpydata[i]] for i in range(len(numpydata))])
imagebw1 = bruitage_poivresel(imagebw)
imagebw2=Image.fromarray(imagebw1)
imagebw2.show()

# Schéma numérique

## Discrétisation spatiale : le maillage est dicté par la pixélisation.
dx = 1/L
dy = 1/H

## Discrétisation temporelle

dt = T/N

## Initialisation

u_0 = np.pad(imagebw, pad_width=1, mode='constant',constant_values=0) # On entoure l'image de bords noirs
u_n = [u_0]

## Boucle

sol = u_0
im = []
for n in range(N):
    print(int(n/(N/100)), "% fait!") # indicateur d'avancement utile pour les compilations longues
    imgsol = Image.fromarray(sol)
    im.append(imgsol)
    newsol = np.zeros(sol.shape)
    for i in range(1, H+1):
        for j in range(1, L+1):
            # Pour compactifier l'expression du schéma et gagner un peu de temps à la compilation on calcule d'abord les dérivées discrètes
            u_x = (sol[i+1,j]-sol[i,j])/dx
            u_y = (sol[i,j+1]-sol[i,j])/dy
            u_xx = (sol[i+1,j] - 2*sol[i,j] + sol[i-1,j])/(dx*dx)
            u_yy = (sol[i,j+1] - 2*sol[i,j] + sol[i,j-1])/(dy*dy)
            u_xy = (sol[i+1,j+1] - sol[i,j+1] - sol[i+1,j] + sol[i,j])/(dx*dy)
            newsol[i, j] = sol[i, j]+ dt*(  (NU1/(1+(u_x**2 + u_y**2)*LAMBDA))*(u_xx + u_yy) - (NU2*LAMBDA/(1+(u_x**2 + u_y**2)*LAMBDA)**2)*(u_xx*(u_x**2) + 2*u_x*u_y*u_xy + u_yy*(u_y**2))  )
    # La boucle ayant eu lieu partout sauf au bord, le bord est toujours nul
    u_n.append(newsol)
    sol = newsol

# Sauvegarde automatique du résultat comme GIF

## Création du nom unique

nomcourt = (NOM_IMAGE.split('/')[1]).split('.')[0] # 'dossier/photo.jpg' donne 'photo'
timestamp = datetime.datetime.fromtimestamp(time.time()).strftime("%d%m%H%M")
nom = 'resultats/PM'+'BG'*BRUITAGE_GAUSSIEN+'BPV'*BRUITAGE_POIVRESEL+nomcourt+timestamp+'.gif'

## Sauvegarde du GIF et logging des paramètres

im[0].save(nom,
               save_all=True, append_images=im[1:], optimize=False, duration=40, loop=0)

log = open('resultats/!log.txt', 'a')
log.writelines(['\n', nom+' : nu='+str(NU)+', lambda='+str(LAMBDA)+', T='+str(T)+', N='+str(N)+', ce qui donne CFL='+str(cfl)])
