# Ce programme s'exécute depuis la ligne de commande en lui passant un argument i. Il a été conçu pour tester automatiquement la stabilité de Perona-Malik pour un grand nombre de valeurs de la "condition CFL" grâce au script Bash nus.sh

import numpy as np
from PIL import Image
import datetime, time
import sys
I = int(sys.argv[1])
NOM_IMAGE = 'photos/lax.jpg'

cfltest = 0.1 + I*0.01

# Encodage de l'image comme array Numpy

img = Image.open(NOM_IMAGE)
numpydata = np.asarray(img)
H, L = numpydata.shape[0],numpydata.shape[1]

# Paramètres

BRUITAGE = True
LAMBDA = 1e-6
T = 1
N = 300
NU=cfltest/((((H+2)**2)+((L+2)**2))*T/N)
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
    if BRUITAGE:
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

## Création et affichage de l'image de départ

imagebw= np.array([[fix(bruitage_gaussien(gris(rgb))) for rgb in numpydata[i]] for i in range(len(numpydata))])
imagebw1=Image.fromarray(imagebw)
#imagebw1.show()

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


nom = 'auto_run_nu/resultats/lax_cfl'+str(0.1 + I*0.01)+'.gif'

## Sauvegarde du GIF et logging des paramètres

im[0].save(nom,
               save_all=True, append_images=im[1:], optimize=False, duration=40, loop=0)
