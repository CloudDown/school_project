# Met le barème en tout début de programme.
#Il me semble que tu as mis trop de choses dans la boucle et pas assez dans les méthodes des classe.
#Par exemple, tu pourrais dans bouger_dg gérer la prise en compte des touches pour gérer la totalité du mouvement.

#on peut gerer la prise en compte du mouvement dans a classe mais il est plus compliqué de gerer l'image qui change n fonction de la direction

'''   /20

1er rendu               :  /2
Objet                   :  /2
Mouvements              :  /2
Types construits        :  /1
CSV                     :  /1
Interactions            :  /2
Variété des tracés      :  /2
Qualité du code         :  /3
Complexité du jeu       :  /3
Esthétique              :  /2
'''


import sys, pygame, time, os
from pygame.locals import *
from random import randint,choice,random
from couleurs import C
from time import sleep
from pygame import mixer #https://www.educative.io/answers/how-to-play-an-audio-file-in-pygame


print('''
Je vais créer un jeu de combat ou deux joueurs pourront combatre,on pourra choisir un mode de dificulté qui varriera la vitesse de descente des platformes
on peut changer le theme du niveau avec les fleches directionelles et enfin  il yaura aussi des :

Plateformes : Dans mon jeu, les plateformes blanches servent de moyen de déplacement pour les joueurs. Ces plateformes sont générées aléatoirement et sont disposées 
horizontalement dans l'écran de jeu. Les joueurs peuvent sauter d'une plateforme à l'autre pour se déplacer et éviter la lave en dessous.

Lave comme obstacle : La lave, représentée par une grande surface orange en bas de l'écran, ajoute de la difficulté au jeu. Si les joueurs tombent dans la lave, ils perdent la partie. 
Cela crée une pression constante pour rester sur les plateformes et ajoute un élément de danger qui pousse les joueurs à être agiles et à bien gérer leurs sauts.

Regardez en haut à gauche de l'écran pour voir combien de temps vous avez joué. Les secondes s'affichent là.

Gardez un œil en haut à droite pour connaître le meilleur score actuel.

Juste en dessous du meilleur score, vous verrez un indicateur de la puissance du saut. C'est là que vous contrôlez la force de votre saut.

Amusez-vous bien et essayez d'obtenir le meilleur score !


''')
VITESSE=150
nb_plat=10

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10,100)

dimensions = largeur, haut = (800, 600)
fenetre = pygame.display.set_mode(dimensions)



dim_perso=(70,70)
images=[
[pygame.transform.scale(pygame.image.load("modele/fond/monde1/image"+str(i+1)+".gif"), dimensions)for i in range(1,4)], #https://www.pygame.org/docs/ref/transform.html#pygame.transform.scale , https://www.pygame.org/docs/ref/image.html#pygame.image.load
[pygame.transform.scale(pygame.image.load("modele/fond/monde2/frame_"+str(i)+"_delay-0.08s.gif"), dimensions)for i in range(60)],
[pygame.transform.scale(pygame.image.load("modele/fond/monde3/frame_"+str(i)+"_delay-0.1s.gif"), dimensions)for i in range(95)],
[pygame.transform.scale(pygame.image.load("modele/fond/monde4/frame_"+str(i)+"_delay-0.1s.gif"), dimensions)for i in range(69)]
]

perso=[
[pygame.transform.scale(pygame.image.load("modele/perso/frame_024_delay-0.1s.png"), dim_perso)], [pygame.transform.scale(pygame.image.load("modele/perso/frame_0"+str(i)+"_delay-0.1s.png"), dim_perso)for i in range(19,23)],
[pygame.transform.scale(pygame.image.load("modele/perso/frame_0"+str(i)+"_delay-0.1s.png"), dim_perso)for i in range(83,88)]+[pygame.transform.scale(pygame.image.load("modele/perso/frame_0"+str(i)+"_delay-0.1s.png"), dim_perso)for i in range(83,88)][::-1]
,pygame.transform.scale(pygame.image.load("modele/perso/frame_088_delay-0.1s.png"), dim_perso)
]


fond_change=images[0][0]
perso_change=perso[0][0]
x = (largeur - fond_change.get_width()) // 2
y = (haut - fond_change.get_height()) // 2
rafraichissement = pygame.time.Clock()


#musique----------------

mixer.init()
mixer.music.load('modele/son/Nami.mp3')
mixer.music.set_volume(0.2)
mixer.music.play()


class Brique:
    def __init__(self,coul,x,y,long,haut):
        self.couleur=coul
        self.x=x
        self.y=y
        self.longueur=long
        self.hauteur=haut
        self.bord_gauche=self.x-self.longueur//2
        self.bord_droit=self.x+self.longueur//2
        self.bord_haut=self.y-self.hauteur//2
        self.bord_bas=self.y+self.hauteur//2
    def afficher(self):
        pygame.draw.rect(fenetre,self.couleur,(self.bord_gauche,self.bord_haut,self.longueur,self.hauteur))
    def desc(self,col,n):
        self.bord_haut=self.y=self.y+n
        self.couleur=col
    def coord(self):
        return(self.x,self.y)

class Perso:
    def __init__(self, x, y,status=False):
        self.x = x
        self.y = y
        self.stat=status
    def bouger_dg(self, ab):
        global droite_gauche, perso_change
        if touche[K_d] and per1.coord()[0]<largeur-72:
            self.x += ab  
            perso_change=perso[1][1]
            if not bloque_saut:
                haut_bas(vital,"d")
            droite_gauche="d"
        elif touche[K_a] or touche[K_q] and per1.coord()[0]>0:
            self.x -= ab
            perso_change=pygame.transform.flip(perso[1][1], True, False)
            if not bloque_saut:
                haut_bas(vital,"a")
            droite_gauche="g"
        if not bloque_saut:
            haut_bas(vital)        
        
    def saut(self,ordo):
        self.y -= ordo
    def afficher(self):
        fenetre.blit(perso_change, (self.x, self.y))
    def coord(self):
        return(self.x,self.y)
    def statut_change(self,x):
        self.stat=x
    def statut(self):
        return self.stat
plat= []
longueur_plat=largeur//6
hauteur_plat=35
placement_y=[elt for elt in range(hauteur_plat,600,hauteur_plat+hauteur_plat-10)]
placement_x=[largeur*i//nb_plat for i in range(1,nb_plat)]
cl_plat=C["tchang"]
bordure=15

hauteur_lave=200
lave=Brique(C["darkorange"],largeur//2,haut-hauteur_lave//2,largeur,hauteur_lave)
lave.afficher()

vital=1
vitesse_ann=30

base_place=randint(0,1)
place_perso={0:[largeur*1//30,haut-hauteur_lave-72],1:[largeur*27//30,haut-hauteur_lave-72]}
per1=Perso(place_perso[base_place][0],place_perso[base_place][1])

z=0
h=0
t=0
jouer=True
rejouer=False
tolerance = 5
start_plat=True
bloque=False
droite_gauche="d"
bloque_saut=False
temps=int(time.time())
tp=0

resaut=int(time.time())
stat_saut=0
taille_saut=int(haut//8.5)


csv=open('parametre.csv','r')
ligne=csv.readline()
if ligne=="":
    f=open("parametre.csv",'w')
    f.write("0;0")
    f.close()
    ligne=csv.readline()
scores = map(int,ligne.split(";"))
personnal_best = max(scores)
csv.close

pygame.font.init() #https://www.pygame.org/docs/ref/font.html#pygame.font.init
cl_txt=C["white"]
cl_txt2=C["yellow"]
liste_surface_plat=[[],[]]

def haut_bas(vit, s="t", p=per1.coord()):
    global perso_change, start_plat,stat_saut
    n =10
    if s in "da":
        n //= 17

    if (touche[K_SPACE] or touche[K_z]) and stat_saut<taille_saut:
        perso_change = perso[2][2]
        per1.saut(vit + n)
        start_plat = False
        stat_saut+=1
        
while jouer and vital<5:
    touche = pygame.key.get_pressed()


#REJOUER------------------------------------------------------------

    if rejouer:
        bloque=False
        per1=Perso(place_perso[base_place][0],place_perso[base_place][1])
        start_plat=True
        liste_surface_plat=[[],[]]
        plat=[]
        rejouer=False
        tp=0
        csv=open('parametre.csv','r')
        ligne=csv.readline()
        scores = map(int,ligne.split(";"))
        personnal_best = max(scores)
        csv.close
        stat_saut=0
        vital=1


#PLATEFORMES -----------------------------------------------

    rafraichissement.tick(VITESSE)
    if h%50==0 and len(plat)<5:
        plat.append(Brique(cl_plat,choice(placement_x),10,longueur_plat,hauteur_plat))

#FOND ------------------------------------------------------

    lave_ann=[i for i in range(0,vitesse_ann*len(images[t])+1,vitesse_ann)]
    vit_perso=vital*2.5
    lave.afficher()
    fenetre.blit(fond_change, (x, y))
    for i in range(len(images[t])):
        if z>=lave_ann[i] and z<=lave_ann[i+1]:
            fond_change = images[t][i]
        elif z>lave_ann[-1]:
            z=0
            fond_change = images[t][0]
            vital+=0.01

#CHRONO -----------------------------------------------------

    if not bloque and start_plat==False:
        if time.time()>=temps+1:
            tp+=1
            temps = time.time()
    fenetre.blit(pygame.font.Font(None, 80).render(str(tp), True, cl_txt), (30, 30)) # https://numerique.ostralo.net/pygame/partie4_les_objets_de_type_surface/c_texte.htm
    fenetre.blit(pygame.font.Font(None, 35).render("pb : "+str(personnal_best), True, cl_txt), (largeur-120, 30))
    fenetre.blit(pygame.font.Font(None, 29).render("saut : "+str(stat_saut)+"/"+str(taille_saut), True, cl_txt2), (largeur-120, 80))
#GENERATION ET DESTRUCTION DE PLATEFORMES -------------------

    for p in range(len(plat)):
        plat[p].afficher()
        plat[p].desc(cl_plat,vital)
        liste_surface_plat[0].append(i+plat[p].coord()[0] for i in range(longueur_plat))
        liste_surface_plat[1].append(plat[p].coord()[1]+hauteur_plat//2)

        if plat[p].coord()[1] >= haut-hauteur_lave+hauteur_plat//2:
            plat.append(Brique(cl_plat,choice(placement_x),10,longueur_plat,hauteur_plat))
            plat.pop(p)
            for i in range(longueur_plat):
                liste_surface_plat[0].pop()
            liste_surface_plat[1].pop()


#conditions de descente et de platformes----------------------
    if start_plat==True:
        if per1.coord()[0]>-50 and per1.coord()[0]<largeur+50 and per1.coord()[1] < haut-hauteur_lave-72:
            per1.saut(-vital-2)
        elif per1.coord()[0]>80 and per1.coord()[0]<largeur-140:
            per1.saut(-vital-2)
        elif per1.coord()[1] > haut-hauteur_lave-60:
            per1.saut(-vital-2)
    else:
        per1.saut(-vital-2)

    for plateforme in plat:
        if plateforme.coord()[0]-longueur_plat//2-10<= per1.coord()[0] <= plateforme.coord()[0]+longueur_plat//2+10 and plateforme.coord()[1]-50>=per1.coord()[1] >= plateforme.coord()[1]-hauteur_plat//2-50:
            stat_saut=0
            bloque=True
            if time.time()>=resaut+0.01:
                resaut = time.time()
                bloque=False
                per1.saut(8)
            per1.saut(-vital)

#CONTROLE-----------------------------------------------------

    if touche[K_UP]:
        cl_plat=C["tchang"]
        cl_txt=C["white"]
        cl_txt2=C["yellow"]
        t=0
        hauteur_lave=200
        VITESSE=150
        vital=1
    elif touche[K_LEFT]:
        cl_plat="white"
        cl_txt=C["red"]
        cl_txt2=C["black"]
        t=1
        hauteur_lave=160
        VITESSE=150
        vital=1
    elif touche[K_RIGHT]:
        cl_plat=C["vert"]
        cl_txt=C["pink"]
        cl_txt2=C["yellow"]
        t=2
        hauteur_lave=0
        VITESSE=150
        vital=1
    elif touche[K_DOWN]:
        cl_plat=C["saumon"]
        cl_txt=C["black"]
        cl_txt2=C["brown"]
        hauteur_lave=130
        t=3
        VITESSE=150
        vital=1

    if not bloque:
        per1.bouger_dg(vit_perso)
    per1.afficher()
    if droite_gauche=="d":
        perso_change=perso[0][0]
    else:
        perso_change=pygame.transform.flip(perso[0][0], True, False) #https://www.pygame.org/docs/ref/transform.html#pygame.transform.flip

#PERDU / REJOUER-----------------------------------------------
        
    if per1.coord()[1] >= haut-hauteur_lave+hauteur_plat//2 and not rejouer:
        fenetre.blit(pygame.font.Font(None, 150).render("PERDU :(", True, cl_txt), (largeur // 3.7, haut // 2.7))
        fenetre.blit(pygame.font.Font(None, 35).render("pressez Y pour rejouer N pour quitter", True, cl_txt),(largeur // 4.3, haut // 1.15))
        if tp>personnal_best:
            f=open("parametre.csv",'w')
            f.write(ligne+";"+str(tp))
            f.close()
        else:
            f=open("parametre.csv",'w')
            f.write(ligne+";"+str(personnal_best))
            f.close()
        bloque=True
        if touche[K_y]:
            rejouer = True
    

    pygame.display.flip()
    clavier=pygame.event.get()
    for event in clavier:
        if event.type == pygame.QUIT or touche[K_ESCAPE] or touche[K_n]:
            jouer=False

#variable incrémenté ----------------------------------------------
    z+=1
    h+=1
pygame.quit()