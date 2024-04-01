#### ATTENTION ! ####
# Pour que le programme s'exécute, le dossier projet doit être structuré comme suit :
# - un dossier d'où viennent les photos (notre /photos)
# - un dossier vide 'resultats/' où seront automatiquement sauvegardés les fichiers résultats.

import numpy as np
from PIL import Image
import datetime, time
NOM_IMAGE = 'photos/voisin.jpg'

# Encodage de l'image comme array Numpy

img = Image.open(NOM_IMAGE)
numpydata = np.asarray(img)
H, L = numpydata.shape[0],numpydata.shape[1]

# Paramètres

BRUITAGE = False
NU = 0.0006
T = 1
N = 300

## Calcul de la condition CFL

cfl=(((H+2)**2)+((L+2)**2))*NU*T/N
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
imagebw1.show()

# Schéma numérique

## Discrétisation spatiale : le maillage est dicté par la pixélisation.
dx = 1/L
dy = 1/H

## Discrétisation temporelle

dt = T/N

## Initialisation

u_0 = np.pad(imagebw, pad_width=1, mode='constant',constant_values=0)
u_n = [u_0]


## Boucle

sol = u_0
im = []
for n in range(N):
    imgsol = Image.fromarray(sol)
    im.append(imgsol)
    newsol = np.zeros(sol.shape)
    for j in range(1, H+1):
        for k in range(1, L+1):
            newsol[j, k] = sol[j,k] + dt*NU*((1/(dx*dx))*(sol[j-1,k] - 2*sol[j,k] + sol[j+1,k]) + (1/(dy*dy))*(sol[j,k-1] - 2*sol[j,k] + sol[j,k+1]))
    u_n.append(newsol)
    sol = newsol

# Sauvegarde automatique du résultat comme GIF

## Création du nom unique

nomcourt = (NOM_IMAGE.split('/')[1]).split('.')[0] # 'dossier/photo.jpg' donne 'photo'
timestamp = datetime.datetime.fromtimestamp(time.time()).strftime("%d%m%H%M")
nom = 'resultats/LIN'+'B'*BRUITAGE+nomcourt+timestamp+'.gif'

## Sauvegarde du GIF

im[0].save(nom,
               save_all=True, append_images=im[1:], optimize=False, duration=40, loop=0)