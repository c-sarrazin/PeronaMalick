# Ce programme est un essai de généralisation naïve à des images RGB. Il n'a pas abouti pour des raisons techniques. 

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from PIL import Image

## encodage de l'image comme array

img = Image.open('photos/gattodefi.png')
numpydata = np.asarray(img)

H, L = numpydata.shape[0],numpydata.shape[1]
print(H, L)

def rgb2gray(rgb):

    r, g, b = rgb[0], rgb[1], rgb[2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

## discrétisation spatiale ; LE MAILLAGE EST DONNÉ PAR LA PIXÉLISATION : carré de 1 par 1, coupé en 1600*1200
dx = 1/L
dy = 1/H

## discrétisation temporelle

T = 1
N = 900 #gérer la consistance
dt = T/N

nu=0.0001

ims = []

for c in range(3):
    imagebw= np.array([[rgb[c] for rgb in numpydata[i]] for i in range(len(numpydata))])
    imagebw1=Image.fromarray(imagebw)
# imagebw1.show()

## initialisation

    u_0 = np.pad(imagebw, pad_width=1, mode='constant',constant_values=0)
    u_t = [u_0]


## boucle

    sol = u_0
    im = []
    for n in range(N):
        imgsol = Image.fromarray(sol)
        im.append(imgsol)
        newsol = np.zeros(sol.shape)
        for j in range(1, H+1):
            for k in range(1, L+1):
                newsol[j, k] = sol[j,k] + dt*nu*((1/(dx*dx))*(sol[j-1,k] - 2*sol[j,k] + sol[j+1,k]) + (1/(dy*dy))*(sol[j,k-1] - 2*sol[j,k] + sol[j,k+1]))
        u_t.append(newsol)
        sol = newsol
    
    ims.append(im)

ims[0][0].save('roujouj.gif',
               save_all=True, append_images=ims[0][1:], optimize=False, duration=40, loop=0)
ims[1][0].save('verrer.gif',
               save_all=True, append_images=ims[1][1:], optimize=False, duration=40, loop=0)
ims[2][0].save('bleuleul.gif',
               save_all=True, append_images=ims[2][1:], optimize=False, duration=40, loop=0)
# rgb_t = [np.dstack((ims[0][t],ims[1][t],ims[2][t])) for t in range(len(ims[0]))]
# im = [Image.fromarray(rgb_t[t]) for t in range(len(rgb_t))]

# imjaaj[1].save('test.jpeg')
# ims[1][0].save('verrer.gif',
#               save_all=True, append_images=ims[1][1:], optimize=False, duration=40, loop=0)
# imjaaj[0].save('anicolor.gif',
#               save_all=True, append_images=imjaaj[1:], optimize=False, duration=40, loop=1)