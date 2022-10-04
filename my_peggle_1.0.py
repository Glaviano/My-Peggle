import pygame
import time
import os
from math import dist
from numpy import linspace
from numpy import arcsin
from numpy import arctan
from math import pi, sin, cos
from random import randint 
from pandas import read_csv
import numpy as np
from menu import Selezione_mappa, Menu_principale, Impostazioni, Menu_pausa
from pygame import mixer
import tkinter as tk
def aggiorna():
    pygame.display.update()
    #pygame.time.Clock().tick(30)
    #clock.tick(60)
    #print(clock.get_fps())



def angolo(a,b,Y,x0):
    x1=((Y-a[1])/(b[1]-a[1]))*(b[0]-a[0])+a[0]
    ipotenusa=(x1-a[0])**2+(Y-a[1])**2
    ipotenusa=pow(ipotenusa,0.5)
    seno=(x1-a[0])/ipotenusa
    coseno=(Y-a[1])/ipotenusa
    #print(b[1]-a[1])
    #print(b[1])
    #print(a[1])
    if b[0]>x0:
        seno=abs(seno)
    if b[0]<x0:
        seno=(-1)*abs(seno)
    #print(seno,coseno)
    return seno, coseno


def angolo_verticale(a,b,Y,x0):
    x1=((Y-a[1])/(b[1]-a[1]))*(b[0]-a[0])+a[0]
    ipotenusa=(x1-a[0])**2+(Y-a[1])**2
    ipotenusa=pow(ipotenusa,0.5)
    seno=(x1-a[0])/ipotenusa
    coseno=(Y-a[1])/ipotenusa
    gamma=arcsin(seno)
    teta=pi-pi/2-gamma
    seno=sin(teta)
    coseno=cos(teta)
    #print(b[1]-a[1])
    #print(b[1])
    #print(a[1])
    '''if b[0]>x0:
        seno=abs(seno)
    if b[0]<x0:
        seno=(-1)*abs(seno)'''
    #print(seno,coseno)
    return seno, coseno


def rot_center(image, angle, x, y):
    
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect

def coordinate_vertici(cx,cy,x1,y1,Phi):
    
    x = cx+ (x1-cx) * cos(Phi) + (y1-cy) * sin(Phi)
    y = cy+(y1-cy) * cos(Phi) - (x1-cx) * sin(Phi)

    return x,y
    
def eq_retta(a,b,x0):
    m=(b[1]-a[1])/(b[0]-a[0])
    y=m*x0-m*a[0]+a[1]
    return y

def eq_retta2(a,b):
    #if b[0]-a[0]!=0:
    m=(b[1]-a[1])/(b[0]-a[0])
    #else:
    #    m=100000
    q=-m*a[0]+a[1]
    return m,q

def eq_retta3(a,b):
    if b[0]-a[0]!=0:
        m=(b[1]-a[1])/(b[0]-a[0])
    else:
        m=100000
    q=-m*a[0]+a[1]
    return m,q

def punti_di_intersezione(m0,q0,m1,q1):
    x=(q0-q1)/(m1-m0)
    y=m0*x+q0
    return [x,y]

def retta(m,x0,p):
    y=m*x0-m*p[0]+p[1]
    return y
    
def Hitbox(xc,yc,r,hitbox,hitbox0):
       
        hitbox0.clear()
        for i in hitbox:
            hitbox0.append(i)
        hitbox.clear()
        
        for teta in range(0,360,14):
            teta=teta*pi/180
            x1=xc+r*cos(teta)
            y1=yc+r*sin(teta)
            hitbox.append([x1,y1])
        #print(self.hitbox)
        return hitbox,hitbox0
    
def verde_viola(blocchi,sfere, cont_verde,max_verdi):
    blocchi_blu=[]
    sfere_blu=[]
    for i in range(len(blocchi)):
        if blocchi[i].tipo=="verde" or blocchi[i].tipo=="viola" or blocchi[i].tipo=="giallo":
            blocchi[i].tipo="blu"
    for i in range(len(sfere)):
        if sfere[i].tipo=="verde" or sfere[i].tipo=="viola" or sfere[i].tipo=="giallo":
            sfere[i].tipo="blu"
            
    for i in range(len(blocchi)):
        if blocchi[i].tipo=="blu" and blocchi[i].mov!=1:
            blocchi_blu.append(i)
    for i in range(len(sfere)):
        if sfere[i].tipo=="blu":
            sfere_blu.append(i)


    
    eseguito=False
    rand1=np.random.random()
    if cont_verde!=max_verdi:
        if rand1>=0.5 and len(blocchi_blu)>0 and len(sfere_blu)!=0:
            rand2=np.random.randint(0,len(blocchi_blu))
            a=("blocchi",blocchi_blu[rand2])
            blocchi_blu.pop(rand2)
            eseguito=True
        if rand1<0.5 and len(sfere_blu)>0 and eseguito==False and len(blocchi_blu)!=0:
            rand2=np.random.randint(0,len(sfere_blu))
            a=("sfere",sfere_blu[rand2])
            sfere_blu.pop(rand2)
            eseguito=True
        if len(blocchi_blu)>0 and len(sfere_blu)==0 and eseguito==False:
            rand2=np.random.randint(0,len(blocchi_blu))
            a=("blocchi",blocchi_blu[rand2])
            blocchi_blu.pop(rand2)
            eseguito=True
        if len(sfere_blu)>0 and len(blocchi_blu)==0 and eseguito==False:
            rand2=np.random.randint(0,len(sfere_blu))
            a=("sfere",sfere_blu[rand2])
            sfere_blu.pop(rand2)
            eseguito=True
        if eseguito==True:
            if a[0]=="blocchi":
                blocchi[a[1]].tipo="verde"
            if a[0]=="sfere":
                sfere[a[1]].tipo="verde"
    #print(a)
    
    rand1=np.random.random()
    #rand1=0.7
    eseguito=False
    if rand1>=0.5 and len(blocchi_blu)>0 and len(sfere_blu)!=0:
        rand2=np.random.randint(0,len(blocchi_blu))
        a=("blocchi",blocchi_blu[rand2])
        blocchi_blu.pop(rand2)
        eseguito=True
    if rand1<0.5 and len(sfere_blu)>0 and eseguito==False and len(blocchi_blu)!=0:
        rand2=np.random.randint(0,len(sfere_blu))
        a=("sfere",sfere_blu[rand2])
        sfere_blu.pop(rand2)
        eseguito=True
    if len(blocchi_blu)>0 and len(sfere_blu)==0 and eseguito==False:
        rand2=np.random.randint(0,len(blocchi_blu))
        a=("blocchi",blocchi_blu[rand2])
        blocchi_blu.pop(rand2)
        eseguito=True
    if len(sfere_blu)>0 and len(blocchi_blu)==0 and eseguito==False:
        rand2=np.random.randint(0,len(sfere_blu))
        a=("sfere",sfere_blu[rand2])
        sfere_blu.pop(rand2)
        eseguito=True
    if eseguito==True:
        if a[0]=="blocchi":
            blocchi[a[1]].tipo="viola"
        if a[0]=="sfere":
            sfere[a[1]].tipo="viola"
    #print(a)   

def aggiornamento_potere(turno,pg1,pg2,potere1,potere2):
    if turno==1:
        if pg1=="Ufo" or pg1=="Tiger" or pg1=="Alien" or pg1=="Rocket" or pg1=="Steroid":
            
            potere1=potere1+2
        if pg1=="Horse":
            potere1=potere1+4
        if pg1=="Pot" or pg1=="Crack-color" or pg1=="Painter":
            potere1=potere1+3
    if turno==2:
        if  pg2=="Ufo" or pg2=="Tiger" or pg2=="Alien" or pg2=="Rocket" or pg1=="Steroid":
            potere2=potere2+2
        if pg2=="Horse":
            potere2=potere2+4
        if pg2=="Pot" or pg2=="Crack-color" or pg2=="Painter":
            potere2=potere2+3
    return potere1,potere2

def conteggio_punti(peg_c, blocco_c,sfere,oggetti,somma,molt,n_rossi,rosso_colpito,cont_verde,turno,potere1,potere2,verde_colpito):
    tipo=0
    lista=[]
    var=False
    if peg_c!=0:
       ind= sfere.index(peg_c)
       if sfere[ind].hit==0:
           if sfere[ind].festa==0:
               sfere[ind].hit=1
           tipo=sfere[ind].tipo
           x=sfere[ind].x-10
           y=sfere[ind].y-5
       if peg_c.festa==1:
           var=True
       #print("sfera colpita")
    
    if blocco_c!=0:
        ind=oggetti.index(blocco_c)
        if oggetti[ind].hit==0:
            if oggetti[ind].mov!=1:
                oggetti[ind].hit=1
            if oggetti[ind].mov==1:
                var=True
                bol=False
                if oggetti[ind].colpito==False:
                    oggetti[ind].colpito=True
                    bol=True
                if oggetti[ind].colpito==True and bol==False:
                    oggetti[ind].colpito=False
                    oggetti[ind].phi_r=oggetti[ind].w1*oggetti[ind].t1+oggetti[ind].phi_r
                    oggetti[ind].t=0
            tipo=oggetti[ind].tipo
            x=oggetti[ind].centro[0]-10
            y=oggetti[ind].centro[1]-10
        #print("blocco colpito")
    if tipo!=0:
        if tipo=="blu":
           if n_rossi!=0: 
               punti=molt*punti_blu 
               somma=somma+molt*punti_blu
           if n_rossi==0:
               punti=1000
               somma=somma+punti
        if tipo=="rosso":
            punti=molt*punti_rosso
            somma=somma+molt*punti_rosso
            n_rossi=n_rossi-1
            rosso_colpito=True
            if n_rossi==0:
                for i in range(0,6,1):
                    
                    sfere.append(Peg(xb1+i*((xb2-xb1)/5),Y,"s",1,mov=0))
        if tipo=="viola":
            if n_rossi!=0:
                
                punti=molt*punti_viola
                somma=somma+molt*punti_viola
            if n_rossi==0:
                punti=10000
                somma=somma+punti
        if tipo=="verde":
            punti=0
            cont_verde=cont_verde+1
            potere1,potere2=aggiornamento_potere(turno, pg1, pg2, potere1, potere2)
            verde_colpito=True
        
            
        if tipo=="giallo":
            if n_rossi!=0:
                
                punti=molt*punti_giallo
                somma=somma+molt*punti_giallo
            if n_rossi==0:
                punti=13000
                somma=somma+punti
        #print(somma)
        #print(molt,n_rossi)
        if 15<=n_rossi<25:
            molt=1
        if 10<=n_rossi<15:
            molt=2
        if 6<=n_rossi<10:
            molt=3
        if 3<=n_rossi<6:
            molt=5
        if 1<=n_rossi<3:
            molt=10
        if var==False:
            lista=[x,y,punti]
        
    return somma, molt, n_rossi, lista, rosso_colpito,cont_verde, potere1,potere2, verde_colpito
        
def eliminazione(sfere, oggetti):
    i=0
    while i<len(sfere):
        if sfere[i].hit==1:
            sfere.pop(i)
            i=-1
        i=i+1
    
    i=0
    while i<len(oggetti):
        if oggetti[i].hit==1:
            oggetti.pop(i)
            i=-1
        i=i+1
              
def blit_punti(numeri,insieme_numeri, n_colpiti,somma,note,cont_note,t1,volume2):
    
    if numeri!=[]:
        numeri.append(time.time())
        insieme_numeri.append(numeri)
        n_colpiti=n_colpiti+1
        punti=n_colpiti*somma
        t2=time.time()
        if t2-t1<0.3:
            if cont_note<len(note)-1:
                cont_note=cont_note-1
        note[cont_note].set_volume(volume2/10)
        note[cont_note].play()
        if cont_note<len(note)-1:
            cont_note=cont_note+1
        
        t1=t2
    t=time.time()
    k=0
    while k<len(insieme_numeri):
        if abs(t-insieme_numeri[k][3])>0.8:
            insieme_numeri.pop(k)
            k=-1
        k=k+1
    for k in insieme_numeri:
        text = font5.render(str(k[2]), True, giallo)
        schermo.blit(text, (k[0],k[1]))
    
    return insieme_numeri, n_colpiti, cont_note, t1
    

def blit_fe(n_rossi, lista,numeri):
    if n_rossi==0:
        cont=0
        for k in lista:
            text = font2.render(str(numeri[cont]), True, giallo)
            schermo.blit(text,k)
            cont=cont+1
 
def punti_fe(n_rossi,palla,sfere):
    lista=[]
    punti=0
    for k in sfere:
        if k.festa==1:
            r=k.r
            lista.append(k.x)
    if n_rossi==0:
        if xb1<=palla.centro[0]<lista[1]-r:
            punti=10000
        if lista[1]+r<=palla.centro[0]<lista[2]-r:
            punti=25000
        if lista[2]+r<=palla.centro[0]<lista[3]-r:
            punti=50000
        if lista[3]+r<=palla.centro[0]<lista[4]-r:
            punti=25000
        if lista[4]+r<=palla.centro[0]<=xb2:
            punti=10000
    #print(punti)        
    return punti        


def blit_nome(turno, nome1,nome2,h,bol_potere,pg1,pg2,potere1,potere2):
    text1 = font2.render(nome1, True, giallo)
    text2 = font2.render(nome2, True, giallo)
    text3=font2.render("left click to use your power",True,giallo)
    text4=font2.render("hold left click to use your power",True,giallo)
    text5=font2.render("horse's power is active",True,giallo)
    if turno==1:
        schermo.blit(text1,(xb1+5,h+5))
        if bol_potere==True:
            if pg1=="Alien" or pg1=="Ufo":
                schermo.blit(text3,(xb1+5,h+35))
            if pg1=="Rocket":
                schermo.blit(text4,(xb1+5,h+35))
            if pg1 =="Horse" and potere1>0:
                schermo.blit(text5,(xb1+5,h+35))
               
    if turno==2:
        schermo.blit(text2,(xb1+5,h+5))
        if bol_potere==True:
            if pg2=="Alien" or pg2=="Ufo":
                schermo.blit(text3,(xb1+5,h+35))
            if pg2=="Rocket":
                schermo.blit(text4,(xb1+5,h+35))
            if pg2 =="Horse" and potere2>0:
                schermo.blit(text5,(xb1+5,h+35))
                #print(potere2)
        
def blit_punti_centro(somma,n_colpiti,bonus,bonus2,tempo,parz, rosso_colpito,punti1,punti2,turno):
    mostra_punti=False
    t=time.time()
    sec=2
    if rosso_colpito==True:
        bonus=bonus+bonus2
        punti=somma*n_colpiti+bonus
        intervallo=punti/(60*sec)
        parz=parz+intervallo
        #print(punti)
        #bonus=10000
        
        if bonus!=0:
            a=" (blocks hit)+ "
        if bonus==0:
            a=" (blocks hit)= "
        riga1=str(somma)+" x "+str(n_colpiti)+ a
        riga2=str(bonus)+" (bonus) ="
        if parz<punti:
            riga3=str(int(parz))
        if parz>=punti:
            riga3=str(punti)
        #testo="ciao"
        text1 = font6.render(riga1, True, giallo)
        text2 = font6.render(riga2, True, verde)
        text3 = font6.render(riga3, True, rosso)
        pannello_punti.blit()
        schermo.blit(text1,(470,250))
        if bonus==0:
            schermo.blit(text3,(595,320))
        #schermo.blit(text,(300,300))
        if bonus!=0:
            schermo.blit(text2,(515,320))
            schermo.blit(text3,(595,420))
    
    if rosso_colpito==False:
        if turno==1:
            punti=punti1
        if turno==2:
            punti=punti2
        punti_tolti=punti*0.25
        intervallo=punti_tolti/(sec*60)
        parz=parz+intervallo
        riga1="No red block hit -25%"
        if parz<punti_tolti:
            riga2=str(int(-parz))
        if parz>=punti_tolti:
            riga2=str(int(-punti_tolti))
        text1 = font6.render(riga1, True, giallo)
        text2 = font6.render(riga2, True, rosso)
        pannello_punti.blit()
        schermo.blit(text1,(470,250))
        schermo.blit(text2,(595,320))
    if abs(tempo-t)>sec+0.5:
        mostra_punti=True
    return mostra_punti, parz

def check_rossi(oggetti, sfere):
    n=0
    for i in sfere:
        if i.tipo=="rosso":
            n=n+1
    for i in oggetti:
        if i.tipo=="rosso":
            n=n+1
    return n
    
def potere_viola(blocchi,sfere):
    blocchi_blu=[]
    sfere_blu=[]
    ritorno=[]
    #print("sono qui")
    for i in range(len(blocchi)):
        if blocchi[i].tipo=="blu" and blocchi[i].hit==0 and blocchi[i].mov!=1:
            blocchi_blu.append(blocchi[i])
    for i in range(len(sfere)):
        if sfere[i].tipo=="blu" and sfere[i].hit==0 :
            sfere_blu.append(sfere[i])
    #finale=zip(blocchi_blu,sfere_blu)
    finale=blocchi_blu+sfere_blu
    #print(finale)
    if len(finale)>=2:
        n=2
    if len(finale)==1:
        n=1
    if len(finale)==0:
        n=0
    for i in range(n):
        a=np.random.randint(0,len(finale))
        ritorno.append(finale[a])
        finale.remove(finale[a])
        '''scelto=finale[a]
        if scelto in sfere:
            pos=sfere.index(scelto)
            sfere[pos].tipo="viola"
        if scelto in blocchi:
            pos=blocchi.index(scelto)
            blocchi[pos].tipo="viola"'''
    return ritorno

def colorazione(sfere,oggetti):
    i=0
    if len(sfere)+len(oggetti)>=35:
        soglia=len(sfere)/(len(sfere)+len(oggetti))
        while i<25:
            k=np.random.random()
            if k<soglia and len(sfere)>0:
                a=np.random.randint(0,len(sfere))
                if sfere[a].tipo=="blu":
                    sfere[a].tipo="rosso"
                    i=i+1
                    continue
            if k>1-soglia and len(oggetti)>0:
                a=np.random.randint(0,len(oggetti))
                if oggetti[a].tipo=="blu" and oggetti[a].mov!=1:
                    oggetti[a].tipo="rosso"
                    i=i+1


def musica_festa(n_rossi,bol_musica,volume1):
    if n_rossi==0 and bol_musica==False:
        mixer.music.load("musica/fever.mp3")
        mixer.music.play()
        mixer.music.set_volume(volume1/10)
        bol_musica=True
        
    return bol_musica


def blit_rossi(oggetti,sfere):
    lista=[]
    for i in sfere:
        if i.tipo=="rosso":
            lista.append(i.rect.center)
    for i in oggetti:
        if i.tipo=="rosso":
            lista.append(i.centro)
    print(lista)
    return lista
class Palla():
    def __init__(self,h,acc):
        self.dim_x=20
        self.dim_y=20
        self.r=self.dim_x/2
        self.x=(xb2-xb1)/2
        self.y=h+5
        self.bol=0
        self.v=700
        self.acc=0
        self.accx=0
        self.accy=0
        self.coef=0.87
        self.vx=0
        self.vy=0
        self.hitbox=[[self.x+self.dim_x/2,self.y],[self.x+self.dim_x,self.y+self.dim_y/2],[self.x+self.dim_x/2,self.y+self.dim_y],[self.x,self.y+self.dim_y/2]]
        self.hitbox0=[]
        self.traiettoria=[]
        self.centro=[self.x+self.dim_x/2,self.y+self.dim_y/2]
        self.centro0=[]
        self.ball=pygame.image.load('immagini/sphere-19.png')
        self.ball=pygame.transform.scale(self.ball, (self.dim_x, self.dim_y))
        self.t0=time.time()
        self.colpito=[]
        self.bol_cesto=0
        


    def rotazione(self,cannone):
        if self.bol==0:

            self.centro=[cannone.centro_r[0],cannone.centro_r[1]]
            #print(self.centro)
            self.x=self.centro[0]-self.dim_x/2
            self.y=self.centro[1]-self.dim_y/2
        
    def tiro(self,b,Y):
        if self.bol==0:
            self.t0=time.time()
            self.bol=1
            seno, coseno=angolo(self.centro,b,Y,self.centro[0])
            self.vx=self.v*seno
            self.vy=self.v*coseno
            
    def movimento(self, animazione):
        if self.bol==1:
            tf=time.time()
            if animazione==False or animazione==True:
                if self.accx==0:
                    self.x=self.x+self.vx*(tf-self.t0)
                    self.y=self.y+self.vy*(tf-self.t0)+self.acc*pow((tf-self.t0),2)
                    self.vy=self.vy+self.acc*(tf-self.t0)
                if self.accx!=0:
                    self.x=self.x+self.vx*(tf-self.t0)+self.accx*pow((tf-self.t0),2)
                    self.y=self.y+self.vy*(tf-self.t0)+self.accy*pow((tf-self.t0),2)
                    self.vy=self.vy+self.accy*(tf-self.t0)
                    self.vx=self.vx+self.accx*(tf-self.t0)
            self.t0=tf
            self.centro0=[self.centro[0],self.centro[1]]
            self.centro=[self.x+self.dim_x/2,self.y+self.dim_y/2]
            self.hitbox=[[self.x+self.dim_x/2,self.y],[self.x+self.dim_x,self.y+self.dim_y/2],[self.x+self.dim_x/2,self.y+self.dim_y],[self.x,self.y+self.dim_y/2]]
            self.traiettoria.append(self.centro)
            self.v=pow(self.vx**2+self.vy**2,0.5)
        '''for punto in self.hitbox:
            schermo.fill((0,0,0),(punto,(4,4)))'''
    
    def urto(self,oggetti):
        bol=0
        cont=0
        temp=False
        punti=[[],[],[],[]]
        traccia=[]
        oggetti2=[]
        t1=time.time()
        colpito=0
        for oggetto in oggetti:
            if dist(oggetto.centro,self.centro)<1000*self.r:
                oggetti2.append(oggetto)
        for oggetto in oggetti2:
            if bol==1 or temp==True:
                break
            for i in range(len(oggetto.hitbox)):
                if bol==1:
                    break
                hitbox=oggetto.hitbox[i]
                for punto in hitbox:
                    distanza=dist(self.centro,punto)
                    
                    #if distanza>4*self.r:
                        #bol=1
                        #continue
                    if distanza<=self.r:
                        if i not in traccia:
                            traccia.append(i)
                        punti[cont].append(punto)
                        colpito=oggetto
                        #print("sono qui")

                        temp=True
                if temp==True:
                    cont=cont+1
        if colpito in oggetti:
            colpito.n=colpito.n+1
        t2=time.time()
        #print(t2-t1)
        #print(traccia)
        #if temp==True:             
            #print(punti)
        for i in range(4):
            if [] in punti:
                punti.remove([])
        #print(punti)
        minima=1000
        temp=False
        for i in range(len(punti)):
            insieme=punti[i]
            for j in insieme:
                d=dist(j,self.centro)
                if d<minima:
                    minima=d
                    indice=i
                    temp=True
                    punto=j
        if temp==True:
            if self.acc==0:
                self.acc=accelerazione
            bol=0
            indice=traccia[indice]
            #print("eccomi")
            hitbox=colpito.hitbox[indice]
                    

            if hitbox[0][0]-hitbox[1][0]!=0:
                m=(hitbox[0][1]-hitbox[1][1])/(hitbox[0][0]-hitbox[1][0])*(-1)
                teta_b=arctan(m)
            if hitbox[0][0]-hitbox[1][0]==0:
                teta_b=pi/2
                m=0
            teta_b_g=teta_b*180/pi
            if self.centro0[0]-self.centro[0]!=0:
                m2=(self.centro0[1]-self.centro[1])/(self.centro0[0]-self.centro[0])*(-1)
            if self.centro0[0]-self.centro[0]==0:
                m2=1000
            teta=arctan(abs((m-m2)/(1+m*m2)))
            #print(arctan(m2)*180/pi)
            teta_g=teta*180/pi
            alfa=abs(pi-(2*pi-abs(teta_b))/2-teta)
            
            alfa_g=alfa*180/pi
            #print(teta_g)
            #print(indice)
            #print(indice,hitbox.index(punto))
            #print(teta_b_g)
            #print(teta_g)
            sinistra=0
            destra=0
            sotto=0
            sopra=0
            retta_c=[]
            if teta_b_g!=90:
                for punto1 in hitbox:
                    y1=retta(-m,punto1[0],[colpito.x,colpito.y])
                    retta_c.append([punto1[0],y1])
            if teta_b_g==90:
                for punto1 in hitbox:
                    retta_c.append([colpito.x,punto1[1]])
            #print(hitbox)
            #print(retta_c)
            for i in range(len(hitbox)):
                if 0<=colpito.teta<90:
                    if hitbox[i][1]<=retta_c[i][1] and 0<teta_b_g<90:
                        sinistra=sinistra+1
                    if hitbox[i][1]>=retta_c[i][1] and 0<teta_b_g<90:
                        destra=destra+1
                    if hitbox[i][1]>=retta_c[i][1] and teta_b<=0:
                        sotto=sotto+1
                    if hitbox[i][1]<=retta_c[i][1] and teta_b<=0:
                        sopra=sopra+1
                
                if 90<=colpito.teta<180:
                    if hitbox[i][1]>retta_c[i][1] and teta_b<0:
                        sinistra=sinistra+1
                    if hitbox[i][1]<retta_c[i][1] and teta_b<0:
                        destra=destra+1
                    if hitbox[i][1]>=retta_c[i][1] and 0<=teta_b_g<90:
                        sotto=sotto+1
                    if hitbox[i][1]<=retta_c[i][1] and 0<=teta_b_g<90:
                        sopra=sopra+1
                if hitbox[i][0]<retta_c[i][0] and teta_b_g==90:
                    sinistra=sinistra+1
                if hitbox[i][0]>retta_c[i][0] and teta_b_g==90:
                    destra=destra+1
            #print(sinistra)
            if sinistra==len(hitbox):
                #print("sono qui sinistra")
                var="sinistra"
            if destra==len(hitbox):
                #print("sono qui destra")
                var="destra"
            if sotto==len(hitbox):
                #print("sono qui sotto")
                var="sotto"
            if sopra==len(hitbox):
                #print("sono qui sopra")
                var="sopra"
            #print(var)
            if self.centro0[0]>self.centro[0]:
                temp='sinistra'
            if self.centro0[0]<self.centro[0]:
                temp='destra'
            if self.centro0[1]<self.centro[1]:
                temp2="sopra"
            if self.centro0[1]>self.centro[1]:
                temp2="sotto"
            if var=="sinistra":
                while True:
                    cont=0
                    #print("primo")
                    if teta_b_g<=0:
                        self.x=self.x-abs(sin(teta_b))
                        self.y=self.y+abs(cos(teta_b))
                    if teta_b_g>0:
                        self.x=self.x-abs(sin(teta_b))
                        self.y=self.y-abs(cos(teta_b))
                    self.centro=[self.x+self.dim_x/2,self.y+self.dim_y/2]
                    for k in hitbox:
                        if dist(self.centro,k)>self.r:
                            cont=cont+1
                    if cont==len(hitbox):
                        self.v=self.v*self.coef
                        v0=self.vx
                        v1=self.v
                        self.vx=cos(teta)*self.v
                        if v0*self.vx<0:
                            self.vx=self.vx*(-1)
                        self.vy=sin(teta)*self.v*(-1)
                        #print(teta_b_g)
                        #print(teta_g)
                        if teta_b_g>0:
                            if temp2=="sopra" and temp=="destra" and abs(teta_b_g)<=45:
                                self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,teta_b )
                            if temp2=="sopra" and temp=="destra" and abs(teta_b_g)>45:
                                self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,-teta_b )
                                self.vx=-self.vx
                            if temp2=="sopra" and temp=="sinistra":
                                self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,teta_b )
                                #self.vx=(-1)*self.vx
                            if temp2=="sotto" and temp=="destra":
                                self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,teta_b )
                        if teta_b_g<0:
                            if temp2=="sopra":
                                self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,-pi-teta_b )
                                #self.vy=-self.vy
                                self.vx=-self.vx
                            if temp2=="sotto" and temp=="destra" and abs(teta_b_g)>=45:
                                self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,-(-pi-teta_b) )
                            if temp2=="sotto" and temp=="destra" and abs(teta_b_g)<45:
                                self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,-(-pi-teta_b) )   
                                self.vx=-self.vx
                                #self.vx=-self.vx
                                #print(self.vx,self.vy)
                            if temp2=="sotto" and temp=="sinistra":
                                self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy, (-pi-teta_b) )  
                                self.vx=-self.vx
                                

                        break
            
            if var=="destra":
                while True:
                    cont=0
                    #print("primo")
                    if teta_b_g<=0:
                        self.x=self.x+abs(sin(teta_b))
                        self.y=self.y-abs(cos(teta_b))
                    if teta_b_g>0:
                        self.x=self.x+abs(sin(teta_b))
                        self.y=self.y+abs(cos(teta_b))
                    self.centro=[self.x+self.dim_x/2,self.y+self.dim_y/2]
                    for k in hitbox:
                        if dist(self.centro,k)>self.r:
                            cont=cont+1
                    if cont==len(hitbox):
                        #print(alfa_g)
                        #print(teta_g)
                        #print(teta_b_g)
                        self.v=self.v*self.coef
                        v0=self.vx
                        v1=self.v
                        self.vx=cos(teta)*self.v
                        if v0*self.vx<0:
                            self.vx=self.vx*(-1)
                        self.vy=sin(teta)*self.v*(-1)

                        if teta_b_g<0:
                             if temp2=="sopra" and temp=="destra":
                                 self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,teta_b )
                                 #print("eccomi")
                             if temp2=="sopra" and temp=="sinistra" and abs(teta_b_g)>=45:
                                 self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,-teta_b )         #destaaaaaaaaaa
                                 self.vx=self.vx*(-1)
                             if temp2=="sopra" and temp=="sinistra" and abs(teta_b_g)<45:
                                 self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,teta_b )
                                 #print("eccomi")
                             if temp2=="sotto":
                                 self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,teta_b )
                        if teta_b_g>0:
                            if temp2=="sopra":
                                self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,pi/2+teta_b )
                            if temp2=="sotto" and temp=="sinistra" and abs(teta_b_g)<45:
                                self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,pi/2+teta_b )
                                #print("sono qui")
                            if temp2=="sotto" and temp=="sinistra" and abs(teta_b_g)>=45:
                                self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,-teta_b )
                                #self.vx=self.vx*(-1)
                            if temp2=="sotto" and temp=="destra":
                                #print(self.vx, self.vy)
                                self.vx, self.vy =coordinate_vertici(0, 0, -self.vx, self.vy,(pi-abs(teta_b)))
                                
                                #print((pi-abs(teta_b))*(180/pi))
                                #self.vx=self.vx*(-1)
                                
                                #print(self.vx,self.vy)
                                

                                
                                
                        break
            if var=="sopra":
                while True:
                    cont=0
                    #print("primo")
                    if teta_b_g<=0:
                        self.x=self.x+abs(sin(teta_b))
                        self.y=self.y-abs(cos(teta_b))
                    if teta_b_g>0:
                        self.x=self.x-abs(sin(teta_b))
                        self.y=self.y-abs(cos(teta_b))
                    self.centro=[self.x+self.dim_x/2,self.y+self.dim_y/2]
                    for k in hitbox:
                        if dist(self.centro,k)>self.r:
                            cont=cont+1
                    if cont==len(hitbox):
                        bol=1
                        #print(alfa_g)
                        #print(teta_g)
                        #print(teta_b_g)
                        self.v=self.v*self.coef
                        v0=self.vx
                        v1=self.v
                        self.vx=cos(teta)*self.v
                        if v0*self.vx<0:
                            self.vx=self.vx*(-1)
                        self.vy=sin(teta)*self.v*(-1)
                        if teta_b_g<0:
                            if temp2=="sopra":
                                if temp=='destra':
                                    self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,teta_b )
                                if temp=='sinistra' and abs(teta_b_g)<45:
                                    #print("sono qui")
                                    self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,teta_b )
                                    #self.vx=(-1)*self.vx
                                if temp=='sinistra' and abs(teta_b_g)>=45:
                                    self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,-teta_b )
                                    self.vx=(-1)*self.vx
                                    #self.vy=(-1)*self.vyù
                            if temp2=="sotto":
                                self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,teta_b )
                                
                        if teta_b_g>0:
                            if temp2=="sopra":
                                if temp=="sinistra":
                                    self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,teta_b )
                                if temp=="destra" and abs(teta_b_g)<45:
                                    self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,teta_b )
                                if temp=="destra" and abs(teta_b_g)>=45:
                                    self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,-teta_b )
                                    self.vx=(-1)*self.vx
                            if temp2=="sotto":
                                self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,teta_b )
                                #print("sono qui")
                        
                        '''self.vx=0
                        self.vy=0
                        self.acc=0'''
                        v2=pow(self.vx**2+self.vy**2,0.5)
                        #print(self.vx,self.vy)
                        break
                     
            if var=="sotto":
                while True:
                    cont=0
                    #print("primo")
                    if teta_b_g<=0:
                        self.x=self.x-abs(sin(teta_b))
                        self.y=self.y+abs(cos(teta_b))
                    if teta_b_g>0:
                        self.x=self.x+abs(sin(teta_b))
                        self.y=self.y+abs(cos(teta_b))
                    self.centro=[self.x+self.dim_x/2,self.y+self.dim_y/2]
                    for k in hitbox:
                        if dist(self.centro,k)>self.r:
                            cont=cont+1
                    if cont==len(hitbox):
                        self.v=self.v*self.coef
                        v0=self.vx
                        v1=self.v
                        self.vx=cos(teta)*self.v
                        if v0*self.vx<0:
                            self.vx=self.vx*(-1)
                        self.vy=sin(teta)*self.v*(-1)
                        self.vy=-self.vy
                        #print(teta_g)
                        if teta_b_g<0:
                            if temp2=="sotto" and temp=="sinistra":
                                self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,teta_b )
                            if temp2=="sotto" and temp=="destra" and abs(teta_b_g)>=45:
                                self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,-teta_b )
                                self.vx=-self.vx
                            
                            if temp2=="sotto" and temp=="destra" and abs(teta_b_g)<45:
                                self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,teta_b )
                                #self.vx=-self.vx
                            if temp2=="sopra":
                                self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,teta_b )
                        if teta_b_g>0:
                            if temp2=="sotto" and temp=="destra":
                                self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,teta_b )
                                #print(self.vx,self.vy)
                            if temp2=="sotto" and temp=="sinistra" and abs(teta_b_g)<45:
                                self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,teta_b )
                            if temp2=="sotto" and temp=="sinistra" and abs(teta_b_g)>=45:
                                self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,-teta_b )
                                self.vx=-self.vx
                            if temp2=="sopra":
                                self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,teta_b )
                                #print("sono qui")
                        break
            self.vx=self.vx+colpito.vx
            self.vy=self.vy+colpito.vy
            self.v=pow(self.vx**2+self.vy**2,0.5)
        return colpito
               
    def urto_palle(self,sfere):
        hit=False
        oggetto=0
        for peg in sfere:
            if dist(peg.rect.center,self.centro)<=self.r+peg.r:
                oggetto=peg
                oggetto.n=oggetto.n+1
                hit=True
                break
        if hit==True and animazione_horse.sto_tirando==False:
            if self.acc==0:
                self.acc=accelerazione
            centro=self.centro
            m,q=eq_retta2(oggetto.rect.center,self.centro)
            if m>200:
                m=100
            if m<-200:
                m=-100
            #print(m)
            p=(self.x,self.y)
            while dist(oggetto.rect.center,self.centro)<=self.r+oggetto.r:
                if oggetto.rect.centerx<=self.centro[0]:
                    self.x=self.x+0.05
                    self.y=retta(m,self.x,p)
                    self.centro=[self.x+self.dim_x/2,self.y+self.dim_y/2]
                if oggetto.rect.centerx>self.centro[0]:
                    self.x=self.x-0.05
                    self.y=retta(m,self.x,p)
                    self.centro=[self.x+self.dim_x/2,self.y+self.dim_y/2]
            minima=100000
            for punto in oggetto.hitbox:
                if dist(punto,self.centro)<minima:
                    scelto=punto
                    minima=dist(punto,self.centro)
            m,q=eq_retta3(scelto, oggetto.rect.center)
            if m==0:
                m_tan=100000
            if m!=0:    
                m_tan=(1/m)*(-1)
            m_tan=(-1)*m_tan
            m_p,q=eq_retta3(centro, self.centro0)
            m_p=m_p*(-1)
            teta=arctan(abs((m_tan-m_p)/(1+m_tan*m_p)))
            teta_g=180*teta/pi
            alfa=arctan(m_tan)
            alfa_g=180*alfa/pi
            #print(alfa_g,teta_g)
            if self.centro0[0]>centro[0]:
                temp='sinistra'
            if self.centro0[0]<centro[0]:
                temp='destra'
            if self.centro0[1]<centro[1]:
                temp2="sopra"
            if self.centro0[1]>centro[1]:
                temp2="sotto"
            self.colpito.append(scelto)
            self.v=self.v*self.coef
            v0=self.vx
            v1=self.v
            self.vx=cos(teta)*self.v
            if v0*self.vx<0:
                self.vx=self.vx*(-1)
            self.vy=sin(teta)*self.v*(-1)
            if temp2=="sopra" and temp=="destra":
                
                if self.centro[0]<=oggetto.x:
                    if 45<=alfa_g<90:
                        self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,-alfa)
                        self.vx=-self.vx
                    if 0<alfa_g<45:
                        self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,alfa)
                    if -89<alfa_g<0:
                        #print("sono qui")
                        self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,-pi-alfa)
                    if alfa_g<-89:
                        self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,alfa)
                        self.vx=-self.vx
                if self.centro[0]>oggetto.x:
                    #print("sono qui")
                    self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,alfa)
                    
            if temp2=="sopra" and temp=="sinistra":
                
                if self.centro[0]>=oggetto.x:
                    if -45<=alfa_g<0:
                        #print("sono qui")
                        self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,alfa)
                        #self.vx=-self.vx
                    if -90<alfa_g<-45:
                        #print("sono qui")
                        self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,-alfa)
                        self.vx=-self.vx
                    if alfa_g>0:
                        self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,pi/2+alfa)
                        #self.vx=-self.vx
                if self.centro[0]<oggetto.x:
                    self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,alfa)
                
            if temp2=="sotto" and temp=="destra":
                if self.centro[1]>=oggetto.y:
                    if -90<=alfa_g<=-45:
                        #print("sono qui")
                        self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,-((3/2)*pi+abs(alfa)))
                        self.vx=-self.vx
                        #self.vy=-self.vy
                    if -45<alfa_g<=0:
                        #print("sono qui")
                        self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,-(pi+abs(alfa)))
                        self.vx=-self.vx
                        #self.vy=-self.vy
                    if alfa_g>0:
                        self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,pi-alfa)
                        self.vx=-self.vx
                if self.centro[1]<oggetto.y:
                    self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,alfa)
                    
            if temp2=="sotto" and temp=="sinistra":
                if self.centro[1]>=oggetto.y:
                    if 45<=alfa_g<=90:
                        self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,alfa)
                        #self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,-(pi/2+alfa))
                        self.vx=-self.vx
                
                    if 0<=alfa_g<45:
                        #print("sono qui")
                        self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,(pi/2+alfa))
                        #self.vx=-self.vx
                        #self.vx=-self.vx
                    if alfa_g<0:
                        self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,-(pi+alfa))
                        self.vx=-self.vx
                if self.centro[1]<oggetto.y:
                        self.vx, self.vy =coordinate_vertici(0, 0, self.vx, self.vy,alfa)
            self.vx=self.vx+oggetto.vx
            self.vy=self.vy+oggetto.vy            
        return oggetto                        
    def urto_cesto(self,cesto):
        bol=0
        for punto in cesto.hitbox:
            if dist(punto,self.centro)<=self.r:
                if self.centro[1]>=cesto.hitbox[2][1]:
                #print("eccomi")
                    if cesto.hitbox[2][0]<self.centro[0]<cesto.hitbox[3][0]:
                        if cesto.vero==0:
                            self.bol_cesto=1
                        else:
                            if self.bol_cesto==0:
                                self.x=np.random.randint(xb1+2*self.r+10,xb2-2*self.r-10)
                                self.y=50+self.r+1
                        bol=0
                        break
                else:
                    #punto1=punto
                    bol=1
                    
                    break
        if bol==0:
            if self.centro[1]>=cesto.hitbox[2][1]:
                #print("eccomi")
                if cesto.hitbox[2][0]<self.centro[0]<cesto.hitbox[3][0]:
                    if cesto.vero==0:
                        self.bol_cesto=1
                    else:
                        if self.bol_cesto==0:
                           self.x=np.random.randint(xb1+2*self.r+10,xb2-2*self.r-10)
                           self.y=50+self.r+1 
                    bol=0
                    #print("sono qui")
        if bol==1:
            m2=(self.centro0[1]-self.centro[1])/(self.centro0[0]-self.centro[0])*(-1)
            teta=arctan(m2)
            while True:
                cont=0
                #print("primo")
                if self.centro[0]>=self.centro0[0]:
                    self.x=self.x-1
                    self.y=self.y-1
                if self.centro[0]<self.centro0[0]:
                    self.x=self.x+1
                    self.y=self.y-1
                self.centro=[self.x+self.dim_x/2,self.y+self.dim_y/2]
                for k in cesto.hitbox:
                    if dist(self.centro,k)>self.r:
                        cont=cont+1
                if cont==len(cesto.hitbox):
                    teta_g=180*teta/pi
                    #print(teta_g)
                    #self.vx=self.vy=self.v=self.acc=0
                    self.v=self.v*self.coef
                    v0=self.vx
                    v1=self.v
                    self.vx=cos(teta)*self.v+cesto.vx
                    if v0*self.vx<0:
                        self.vx=self.vx*(-1)+cesto.vx
                        
                    self.vy=-abs(sin(teta)*self.v*(-1))
                    #print(self.vx,self.vy)
                    break
    def urto_cesto(self,cesto):
        bol=0
        for punto in cesto.hitbox:
            if dist(punto,self.centro)<=self.r:
                if self.centro[1]>=cesto.hitbox[2][1]:
                #print("eccomi")
                    if cesto.hitbox[2][0]<self.centro[0]<cesto.hitbox[3][0]:
                        if cesto.vero==0:
                            self.bol_cesto=1
                        else:
                            if self.bol_cesto==0:
                                self.x=np.random.randint(xb1+2*self.r+10,xb2-2*self.r-10)
                                self.y=50+self.r+1
                        bol=0
                        break
                else:
                    #punto1=punto
                    bol=1
                    
                    break
        if bol==0:
            if self.centro[1]>=cesto.hitbox[2][1]:
                #print("eccomi")
                if cesto.hitbox[2][0]<self.centro[0]<cesto.hitbox[3][0]:
                    if cesto.vero==0:
                        self.bol_cesto=1
                    else:
                        if self.bol_cesto==0:
                           self.x=np.random.randint(xb1+2*self.r+10,xb2-2*self.r-10)
                           self.y=50+self.r+1 
                    bol=0
                    #print("sono qui")
        if bol==1:
            m2=(self.centro0[1]-self.centro[1])/(self.centro0[0]-self.centro[0])*(-1)
            teta=arctan(m2)
            if self.acc==0:
                self.acc=accelerazione
            while True:
                cont=0
                #print("primo")
                if self.centro[0]>=self.centro0[0]:
                    self.x=self.x-1
                    self.y=self.y-1
                if self.centro[0]<self.centro0[0]:
                    self.x=self.x+1
                    self.y=self.y-1
                self.centro=[self.x+self.dim_x/2,self.y+self.dim_y/2]
                for k in cesto.hitbox:
                    if dist(self.centro,k)>self.r:
                        cont=cont+1
                if cont==len(cesto.hitbox):
                    teta_g=180*teta/pi
                    #print(teta_g)
                    #self.vx=self.vy=self.v=self.acc=0
                    self.v=self.v*self.coef
                    v0=self.vx
                    v1=self.v
                    self.vx=cos(teta)*self.v+cesto.vx
                    if v0*self.vx<0:
                        self.vx=self.vx*(-1)+cesto.vx
                        
                    self.vy=-abs(sin(teta)*self.v*(-1))
                    self.v=pow(self.vx**2+self.vy**2,0.5)
                    #print(self.vx,self.vy)
                    break

    def urto_laterale(self,h):
        if self.centro[0]+self.r>=xb2:
            if self.acc==0:
                self.acc=accelerazione
            seno, coseno=angolo_verticale(self.centro0,self.centro,Y,self.centro0[0])
            teta=arcsin(seno)
            #print(teta*180/pi)
            self.v=self.v*self.coef
            if self.centro0[1]>=self.centro[1]:
                self.vy=sin(teta)*self.v*(1)
            if self.centro0[1]<self.centro[1]:

                self.vy=sin(teta)*self.v
            self.vx=cos(teta)*self.v*(-1)
            if self.centro[1]<self.centro0[1]:
                self.vy=-self.vy
            while self.centro[0]+self.r>=xb2:
                self.x=self.x-1
                self.centro=[self.x+self.dim_x/2,self.y+self.dim_y/2]
                
                #self.v=self.vx=self.vy=self.acc=0
        if self.centro[0]-self.r<=xb1:
            if self.acc==0:
                self.acc=accelerazione
            seno, coseno=angolo_verticale(self.centro0,self.centro,Y,self.centro0[0])
            teta=arcsin(seno)
            #print(teta*180/pi)
            self.v=self.v*self.coef
            if self.centro0[1]>=self.centro[1]:
                self.vy=sin(teta)*self.v*(-1)
            if self.centro0[1]<self.centro[1]:
                self.vy=sin(teta)*self.v
            self.vx=cos(teta)*self.v
            while self.centro[0]+self.r>=xb2:
                self.x=self.x+1
                self.centro=[self.x+self.dim_x/2,self.y+self.dim_y/2]
        
        if self.centro[1]-self.r<=h and self.bol==1:
            #self.y=oggetto.y+2*self.r+1
            if self.acc==0:
                self.acc=accelerazione
            seno, coseno=angolo(self.centro0,self.centro,Y,self.centro0[0])
            teta=arcsin(seno)
            #print(teta*180/pi)
            self.v=self.v*self.coef
            self.vx=sin(teta)*self.v
            self.vy=cos(teta)*self.v
            while self.centro[1]+self.r<=h:
                self.y=self.y+1
                self.centro=[self.x+self.dim_x/2,self.y+self.dim_y/2]
                        
    
    def blit(self):
        if self.bol==1:
            schermo.blit(self.ball,(self.x,self.y))
        #for k in self.colpito:
            #schermo.fill(rosso,(k,(4,4)))
        #for k in self.traiettoria:
            #schermo.fill(nero,(k,(4,4)))


class Cannone():
    def __init__(self):
        self.dim_x=60
        self.dim_y=100
        self.x=(xb2+xb1)/2
        self.y=55
        self.teta=180
        self.rad=(self.teta*pi/180)
        self.cannon=pygame.image.load('immagini/Missile_Launcher3.png')
        self.cannon=pygame.transform.scale(self.cannon, (self.dim_x, self.dim_y))
        self.centro=[self.x,16]
        self.cannon,self.rect=rot_center(self.cannon, self.teta, self.x, self.y)
        self.teta1=0
        
        a,b=coordinate_vertici(self.x, self.y, self.centro[0], self.centro[1],self.rad)
        self.centro_r=[a,b]
        #self.centro=[a,b]
        
    def movimento(self,x,y,palla):
        
        if palla.bol==0 and y>self.y+1:
            centro=[self.x,self.y]
            b=[x,y]
            seno,coseno=angolo(centro, b, Y, centro[0])
            ang=arcsin(seno)
            rad=self.rad+ang
            teta=180*rad/pi
            self.teta1=teta
            #print(teta)
            if 104<teta<253:
                self.cannon=pygame.image.load('immagini/Missile_Launcher3.png')
                self.cannon=pygame.transform.scale(self.cannon, (self.dim_x, self.dim_y))
                self.cannon,self.rect=rot_center(self.cannon, teta, self.x, self.y)
                a,b=coordinate_vertici(self.x, self.y, self.centro[0], self.centro[1],rad)
                self.centro_r=[a,b]
            
            if teta<104:
                teta=105
                rad=pi*teta/180
                self.cannon=pygame.image.load('immagini/Missile_Launcher3.png')
                self.cannon=pygame.transform.scale(self.cannon, (self.dim_x, self.dim_y))
                self.cannon,self.rect=rot_center(self.cannon, teta, self.x, self.y)
                a,b=coordinate_vertici(self.x, self.y, self.centro[0], self.centro[1],rad)
                self.centro_r=[a,b]
            if teta>253:
                teta=252
                rad=pi*teta/180
                self.cannon=pygame.image.load('immagini/Missile_Launcher3.png')
                self.cannon=pygame.transform.scale(self.cannon, (self.dim_x, self.dim_y))
                self.cannon,self.rect=rot_center(self.cannon, teta, self.x, self.y)
                a,b=coordinate_vertici(self.x, self.y, self.centro[0], self.centro[1],rad)
                self.centro_r=[a,b]
                
        if palla.bol==1:
            
            rad1=pi*self.teta1/180
            self.cannon=pygame.image.load('immagini/Missile_Launcher.png')
            self.cannon=pygame.transform.scale(self.cannon, (self.dim_x, self.dim_y))
            self.cannon,self.rect=rot_center(self.cannon, self.teta1, self.x, self.y)
            a,b=coordinate_vertici(self.x, self.y, self.centro[0], self.centro[1],rad1)
            self.centro_r=[a,b]
        
        
    def blit(self):
        
        schermo.blit(self.cannon,self.rect)
        #schermo.fill(nero,(self.centro_r,(4,4)))
        #schermo.fill(rosso,((self.x,self.y),(4,4)))


class Blocco():
    def __init__(self,pos_x,pos_y,rotazione,tipo,mov):
        self.dim_x=40
        self.dim_y=20
        self.x=pos_x
        self.y=pos_y
        self.teta=rotazione
        self.tipo=tipo
        self.hit=0
        self.rad=(self.teta*pi/180)
        self.hitbox=[[],[],[],[]]
        self.n=0
        self.mov=mov
        self.vx=0
        self.vy=0
        self.v=0
        self.block_blu=pygame.image.load('immagini/blocchi/block_blue.png')
        self.block1_blu=pygame.image.load('immagini/blocchi/element_blue_rectangle.png')
        self.block_rosso=pygame.image.load('immagini/blocchi/block_red.png')
        self.block1_rosso=pygame.image.load('immagini/blocchi/element_red_rectangle.png')
        self.block_viola=pygame.image.load('immagini/blocchi/block_purple.png')
        self.block1_viola=pygame.image.load('immagini/blocchi/element_purple_rectangle.png')
        self.block_verde=pygame.image.load('immagini/blocchi/block_green.png')
        self.block1_verde=pygame.image.load('immagini/blocchi/element_green_rectangle.png')
        self.block_giallo=pygame.image.load('immagini/blocchi/block_brown.png')
        self.block1_giallo=pygame.image.load('immagini/blocchi/element_yellow_rectangle.png')
        
        
        self.block_blu=pygame.transform.scale(self.block_blu, (self.dim_x, self.dim_y))
        self.block_blu,self.rect=rot_center(self.block_blu, self.teta, self.x, self.y)
        self.block1_blu=pygame.transform.scale(self.block1_blu, (self.dim_x, self.dim_y))
        self.block1_blu,self.rect=rot_center(self.block1_blu, self.teta, self.x, self.y)
        
        self.block_rosso=pygame.transform.scale(self.block_rosso, (self.dim_x, self.dim_y))
        self.block_rosso,self.rect=rot_center(self.block_rosso, self.teta, self.x, self.y)
        self.block1_rosso=pygame.transform.scale(self.block1_rosso, (self.dim_x, self.dim_y))
        self.block1_rosso,self.rect=rot_center(self.block1_rosso, self.teta, self.x, self.y)
        
        self.block_viola=pygame.transform.scale(self.block_viola, (self.dim_x, self.dim_y))
        self.block_viola,self.rect=rot_center(self.block_viola, self.teta, self.x, self.y)
        self.block1_viola=pygame.transform.scale(self.block1_viola, (self.dim_x, self.dim_y))
        self.block1_viola,self.rect=rot_center(self.block1_viola, self.teta, self.x, self.y)
        
        self.block_verde=pygame.transform.scale(self.block_verde, (self.dim_x, self.dim_y))
        self.block_verde,self.rect=rot_center(self.block_verde, self.teta, self.x, self.y)
        self.block1_verde=pygame.transform.scale(self.block1_verde, (self.dim_x, self.dim_y))
        self.block1_verde,self.rect=rot_center(self.block1_verde, self.teta, self.x, self.y)
        
        self.block_giallo=pygame.transform.scale(self.block_giallo, (self.dim_x, self.dim_y))
        self.block_giallo,self.rect=rot_center(self.block_giallo, self.teta, self.x, self.y)
        self.block1_giallo=pygame.transform.scale(self.block1_giallo, (self.dim_x, self.dim_y))
        self.block1_giallo,self.rect=rot_center(self.block1_giallo, self.teta, self.x, self.y)
        
        if self.tipo=="blu":
            self.block=self.block_blu
            self.block1=self.block1_blu
        if self.tipo=="rosso":
            self.block=self.block_rosso
            self.block1=self.block1_rosso
        if self.tipo=="viola":
            self.block=self.block_viola
            self.block1=self.block1_viola
        if self.tipo=="verde":
            self.block=self.block_verde
            self.block1=self.block1_verde

        
        
        #self.block1=pygame.transform.scale(self.block1, (self.dim_x, self.dim_y))
        #self.block1,self.rect1=rot_center(self.block1, self.teta, self.x, self.y)
        self.centro=[self.x,self.y]
        a,b=coordinate_vertici(self.centro[0], self.centro[1], self.x-self.dim_x/2, self.y-self.dim_y/2, self.rad)
        self.vertici=[[a,b]]
        a,b=coordinate_vertici(self.centro[0], self.centro[1], self.x+self.dim_x/2, self.y-self.dim_y/2, self.rad)
        self.vertici.append([a,b])
        a,b=coordinate_vertici(self.centro[0], self.centro[1], self.x-self.dim_x/2, self.y+self.dim_y/2, self.rad)
        self.vertici.append([a,b])
        a,b=coordinate_vertici(self.centro[0], self.centro[1], self.x+self.dim_x/2, self.y+self.dim_y/2, self.rad)
        self.vertici.append([a,b])
        self.base=8
        self.altezza=6
        #creazione hitbox base alta
        if self.teta!=90:
            punti_x=linspace(self.vertici[0][0],self.vertici[1][0],self.base)
            np.sort(punti_x)
            #print(punti_x)
            for x0 in punti_x:
                y0=eq_retta(self.vertici[0], self.vertici[1], x0)
                self.hitbox[0].append([x0,y0])
        if self.teta==90:
            punti_y=linspace(self.vertici[0][1],self.vertici[1][1],self.base)
            np.sort(punti_y)
            for y0 in punti_y:
                self.hitbox[0].append([self.vertici[0][0],y0])
        
        #creazione hitbox altezza destra
        if self.teta==0:
            punti_y=linspace(self.vertici[1][1],self.vertici[3][1],self.altezza)
            np.sort(punti_x)
            for y0 in punti_y:
                self.hitbox[1].append([self.vertici[1][0],y0])
        if self.teta!=0:
            punti_x=linspace(self.vertici[1][0],self.vertici[3][0],self.altezza)
            np.sort(punti_x)
            for x0 in punti_x:
                y0=eq_retta(self.vertici[1], self.vertici[3], x0)
                self.hitbox[1].append([x0,y0])
        
        #creazione hitbox base bassa
        if self.teta!=90:
            punti_x=linspace(self.vertici[2][0],self.vertici[3][0],self.base)
            np.sort(punti_x)
            for x0 in punti_x:
                y0=eq_retta(self.vertici[2], self.vertici[3], x0)
                self.hitbox[2].append([x0,y0])
        if self.teta==90:
            punti_y=linspace(self.vertici[2][1],self.vertici[3][1],self.base)
            np.sort(punti_y)
            for y0 in punti_y:
                self.hitbox[2].append([self.vertici[2][0],y0])
        
        #creazione hitbox lato sinistra
        if self.teta==0:
            punti_y=linspace(self.vertici[0][1],self.vertici[2][1],self.altezza)
            np.sort(punti_x)
            for y0 in punti_y:
                self.hitbox[3].append([self.vertici[0][0],y0])
        if self.teta!=0:
            punti_x=linspace(self.vertici[0][0],self.vertici[2][0],self.altezza)
            np.sort(punti_x)
            for x0 in punti_x:
                y0=eq_retta(self.vertici[0], self.vertici[2], x0)
                self.hitbox[3].append([x0,y0])
        
        #print(self.rect)
        #print(self.vertice)
    #hitbox[0]=lato alto, hitbox[1] lato a destra, hitbox[2] base bassa, hitboxe[3] lato sinistra
    
    def colore(self):
        if self.tipo=="blu":
            self.block=self.block_blu
            self.block1=self.block1_blu
        if self.tipo=="rosso":
            self.block=self.block_rosso
            self.block1=self.block1_rosso
        if self.tipo=="viola":
            self.block=self.block_viola
            self.block1=self.block1_viola
        if self.tipo=="verde":
            self.block=self.block_verde
            self.block1=self.block1_verde
    
    def blit(self):
        if self.hit==0:
            schermo.blit(self.block, self.rect)
        if self.hit==1:
            schermo.blit(self.block1, self.rect)
        #schermo.fill((0,0,0),(self.rect.center,(4,4)))
        #for vertice in self.vertici:
            #schermo.fill((0,0,0),(vertice,(4,4)))
        '''for i in range(len(self.hitbox)):
            
            for punto in self.hitbox[i]:
                schermo.fill(nero,(punto,(4,4)))'''
        #schermo.fill((0,0,0),([470,100],(4,4)))

class Blocco_ostacolo():
    def __init__(self,pos_x,pos_y,rotazione,tipo,mov,A,w,phi,alfa):
        self.dim_x=250
        self.dim_y=40
        self.x=pos_x
        self.y=pos_y
        self.centro0=[pos_x,pos_y]
        self.teta=rotazione
        self.tipo=tipo
        self.hit=0
        self.rad=(self.teta*pi/180)
        self.hitbox=[[],[],[],[]]
        self.n=0
        self.mov=mov
        self.A=A
        self.w=w
        self.phi=phi
        self.vx=0
        self.vy=0
        self.v=0
        self.t=0
        self.t1=0
        self.alfa=alfa
        self.colpito=True
        self.w1=w
        self.alfa_r=-pi*self.alfa/180
        self.phi_r=-pi*self.phi/180
        self.block_blu=pygame.image.load('immagini/orange_button.png')
        self.block1_blu=pygame.image.load('immagini/blocchi/element_blue_rectangle.png')
        self.block_rosso=pygame.image.load('immagini/blocchi/block_red.png')
        self.block1_rosso=pygame.image.load('immagini/blocchi/element_red_rectangle.png')
        self.block_viola=pygame.image.load('immagini/blocchi/block_purple.png')
        self.block1_viola=pygame.image.load('immagini/blocchi/element_purple_rectangle.png')
        self.block_verde=pygame.image.load('immagini/blocchi/block_green.png')
        self.block1_verde=pygame.image.load('immagini/blocchi/element_green_rectangle.png')
        self.block_giallo=pygame.image.load('immagini/blocchi/block_brown.png')
        self.block1_giallo=pygame.image.load('immagini/blocchi/element_yellow_rectangle.png')
        
        
        self.block_blu=pygame.transform.scale(self.block_blu, (self.dim_x, self.dim_y))
        self.block_blu,self.rect=rot_center(self.block_blu, self.teta, self.x, self.y)
        self.block1_blu=pygame.transform.scale(self.block1_blu, (self.dim_x, self.dim_y))
        self.block1_blu,self.rect=rot_center(self.block1_blu, self.teta, self.x, self.y)
        
        self.block_rosso=pygame.transform.scale(self.block_rosso, (self.dim_x, self.dim_y))
        self.block_rosso,self.rect=rot_center(self.block_rosso, self.teta, self.x, self.y)
        self.block1_rosso=pygame.transform.scale(self.block1_rosso, (self.dim_x, self.dim_y))
        self.block1_rosso,self.rect=rot_center(self.block1_rosso, self.teta, self.x, self.y)
        
        self.block_viola=pygame.transform.scale(self.block_viola, (self.dim_x, self.dim_y))
        self.block_viola,self.rect=rot_center(self.block_viola, self.teta, self.x, self.y)
        self.block1_viola=pygame.transform.scale(self.block1_viola, (self.dim_x, self.dim_y))
        self.block1_viola,self.rect=rot_center(self.block1_viola, self.teta, self.x, self.y)
        
        self.block_verde=pygame.transform.scale(self.block_verde, (self.dim_x, self.dim_y))
        self.block_verde,self.rect=rot_center(self.block_verde, self.teta, self.x, self.y)
        self.block1_verde=pygame.transform.scale(self.block1_verde, (self.dim_x, self.dim_y))
        self.block1_verde,self.rect=rot_center(self.block1_verde, self.teta, self.x, self.y)
        
        self.block_giallo=pygame.transform.scale(self.block_giallo, (self.dim_x, self.dim_y))
        self.block_giallo,self.rect=rot_center(self.block_giallo, self.teta, self.x, self.y)
        self.block1_giallo=pygame.transform.scale(self.block1_giallo, (self.dim_x, self.dim_y))
        self.block1_giallo,self.rect=rot_center(self.block1_giallo, self.teta, self.x, self.y)
        
        if self.tipo=="blu":
            self.block=self.block_blu
            self.block1=self.block1_blu
        if self.tipo=="rosso":
            self.block=self.block_rosso
            self.block1=self.block1_rosso
        if self.tipo=="viola":
            self.block=self.block_viola
            self.block1=self.block1_viola
        if self.tipo=="verde":
            self.block=self.block_verde
            self.block1=self.block1_verde

        
        
        
    def colore(self):
        if self.tipo=="blu":
            self.block=self.block_blu
            self.block1=self.block1_blu
        if self.tipo=="rosso":
            self.block=self.block_rosso
            self.block1=self.block1_rosso
        if self.tipo=="viola":
            self.block=self.block_viola
            self.block1=self.block1_viola
        if self.tipo=="verde":
            self.block=self.block_verde
            self.block1=self.block1_verde
    
    def movimento_armonico(self):
        if self.colpito==True:
            self.w=self.w1
        if self.colpito==False:
            self.w=0
        if self.t==0 and self.colpito==True:
            self.t=time.time()
        self.t1=abs(self.t-time.time())

        #t=0
        x=(self.A*cos(self.w*self.t1+self.phi_r))*cos(self.alfa_r)+self.centro0[0]
        y=(self.A*cos(self.w*self.t1+self.phi_r))*sin(self.alfa_r)+self.centro0[1]
        self.vx=-self.A*self.w*sin(self.w*self.t1)*cos(self.alfa_r)
        self.vy=-self.A*self.w*sin(self.w*self.t1)*sin(self.alfa_r)
        #x,y=coordinate_vertici(self.x,self.y,x,self.y,teta)
        self.rect.centerx=x
        self.rect.centery=y
        self.x=x
        self.y=y
        #print(self.x)
        self.centro=[x,y]
        self.hitbox=[[],[],[],[]]
        self.vertici=[]

        a,b=coordinate_vertici(self.centro[0], self.centro[1], self.x-self.dim_x/2, self.y-self.dim_y/2, self.rad)
        self.vertici=[[a,b]]
        a,b=coordinate_vertici(self.centro[0], self.centro[1], self.x+self.dim_x/2, self.y-self.dim_y/2, self.rad)
        self.vertici.append([a,b])
        a,b=coordinate_vertici(self.centro[0], self.centro[1], self.x-self.dim_x/2, self.y+self.dim_y/2, self.rad)
        self.vertici.append([a,b])
        a,b=coordinate_vertici(self.centro[0], self.centro[1], self.x+self.dim_x/2, self.y+self.dim_y/2, self.rad)
        self.vertici.append([a,b])
        self.base=22
        self.altezza=10
        #creazione hitbox base alta
        if self.teta!=90:
            punti_x=linspace(self.vertici[0][0],self.vertici[1][0],self.base)
            np.sort(punti_x)
            #print(punti_x)
            for x0 in punti_x:
                y0=eq_retta(self.vertici[0], self.vertici[1], x0)
                self.hitbox[0].append([x0,y0])
        if self.teta==90:
            punti_y=linspace(self.vertici[0][1],self.vertici[1][1],self.base)
            np.sort(punti_y)
            for y0 in punti_y:
                self.hitbox[0].append([self.vertici[0][0],y0])
        
        #creazione hitbox altezza destra
        if self.teta==0:
            punti_y=linspace(self.vertici[1][1],self.vertici[3][1],self.altezza)
            np.sort(punti_x)
            for y0 in punti_y:
                self.hitbox[1].append([self.vertici[1][0],y0])
        if self.teta!=0:
            punti_x=linspace(self.vertici[1][0],self.vertici[3][0],self.altezza)
            np.sort(punti_x)
            for x0 in punti_x:
                y0=eq_retta(self.vertici[1], self.vertici[3], x0)
                self.hitbox[1].append([x0,y0])
        
        #creazione hitbox base bassa
        if self.teta!=90:
            punti_x=linspace(self.vertici[2][0],self.vertici[3][0],self.base)
            np.sort(punti_x)
            for x0 in punti_x:
                y0=eq_retta(self.vertici[2], self.vertici[3], x0)
                self.hitbox[2].append([x0,y0])
        if self.teta==90:
            punti_y=linspace(self.vertici[2][1],self.vertici[3][1],self.base)
            np.sort(punti_y)
            for y0 in punti_y:
                self.hitbox[2].append([self.vertici[2][0],y0])
        
        #creazione hitbox lato sinistra
        if self.teta==0:
            punti_y=linspace(self.vertici[0][1],self.vertici[2][1],self.altezza)
            np.sort(punti_x)
            for y0 in punti_y:
                self.hitbox[3].append([self.vertici[0][0],y0])
        if self.teta!=0:
            punti_x=linspace(self.vertici[0][0],self.vertici[2][0],self.altezza)
            np.sort(punti_x)
            for x0 in punti_x:
                y0=eq_retta(self.vertici[0], self.vertici[2], x0)
                self.hitbox[3].append([x0,y0])

    def blit(self):
        if self.hit==0:
            schermo.blit(self.block, self.rect)
        if self.hit==1:
            schermo.blit(self.block1, self.rect)
        '''for i in range(len(self.hitbox)):
            for punto in self.hitbox[i]:
                schermo.fill(nero,(punto,(4,4)))'''
        
class Blocco_armonico():
    def __init__(self,pos_x,pos_y,rotazione,tipo,mov,A,w,phi,alfa):
        self.dim_x=40
        self.dim_y=20
        self.x=pos_x
        self.y=pos_y
        self.centro0=[pos_x,pos_y]
        self.teta=rotazione
        self.tipo=tipo
        self.hit=0
        self.rad=(self.teta*pi/180)
        self.hitbox=[[],[],[],[]]
        self.n=0
        self.mov=mov
        self.A=A
        self.w=w
        self.phi=phi
        self.vx=0
        self.vy=0
        self.v=0
        self.t=0
        self.t1=0
        self.alfa=alfa
        self.colpito=True
        self.w1=w
        self.alfa_r=-pi*self.alfa/180
        self.phi_r=-pi*self.phi/180
        self.block_blu=pygame.image.load('immagini/blocchi/block_blue.png')
        self.block1_blu=pygame.image.load('immagini/blocchi/element_blue_rectangle.png')
        self.block_rosso=pygame.image.load('immagini/blocchi/block_red.png')
        self.block1_rosso=pygame.image.load('immagini/blocchi/element_red_rectangle.png')
        self.block_viola=pygame.image.load('immagini/blocchi/block_purple.png')
        self.block1_viola=pygame.image.load('immagini/blocchi/element_purple_rectangle.png')
        self.block_verde=pygame.image.load('immagini/blocchi/block_green.png')
        self.block1_verde=pygame.image.load('immagini/blocchi/element_green_rectangle.png')
        self.block_giallo=pygame.image.load('immagini/blocchi/block_brown.png')
        self.block1_giallo=pygame.image.load('immagini/blocchi/element_yellow_rectangle.png')
        
        
        self.block_blu=pygame.transform.scale(self.block_blu, (self.dim_x, self.dim_y))
        self.block_blu,self.rect=rot_center(self.block_blu, self.teta, self.x, self.y)
        self.block1_blu=pygame.transform.scale(self.block1_blu, (self.dim_x, self.dim_y))
        self.block1_blu,self.rect=rot_center(self.block1_blu, self.teta, self.x, self.y)
        
        self.block_rosso=pygame.transform.scale(self.block_rosso, (self.dim_x, self.dim_y))
        self.block_rosso,self.rect=rot_center(self.block_rosso, self.teta, self.x, self.y)
        self.block1_rosso=pygame.transform.scale(self.block1_rosso, (self.dim_x, self.dim_y))
        self.block1_rosso,self.rect=rot_center(self.block1_rosso, self.teta, self.x, self.y)
        
        self.block_viola=pygame.transform.scale(self.block_viola, (self.dim_x, self.dim_y))
        self.block_viola,self.rect=rot_center(self.block_viola, self.teta, self.x, self.y)
        self.block1_viola=pygame.transform.scale(self.block1_viola, (self.dim_x, self.dim_y))
        self.block1_viola,self.rect=rot_center(self.block1_viola, self.teta, self.x, self.y)
        
        self.block_verde=pygame.transform.scale(self.block_verde, (self.dim_x, self.dim_y))
        self.block_verde,self.rect=rot_center(self.block_verde, self.teta, self.x, self.y)
        self.block1_verde=pygame.transform.scale(self.block1_verde, (self.dim_x, self.dim_y))
        self.block1_verde,self.rect=rot_center(self.block1_verde, self.teta, self.x, self.y)
        
        self.block_giallo=pygame.transform.scale(self.block_giallo, (self.dim_x, self.dim_y))
        self.block_giallo,self.rect=rot_center(self.block_giallo, self.teta, self.x, self.y)
        self.block1_giallo=pygame.transform.scale(self.block1_giallo, (self.dim_x, self.dim_y))
        self.block1_giallo,self.rect=rot_center(self.block1_giallo, self.teta, self.x, self.y)
        
        if self.tipo=="blu":
            self.block=self.block_blu
            self.block1=self.block1_blu
        if self.tipo=="rosso":
            self.block=self.block_rosso
            self.block1=self.block1_rosso
        if self.tipo=="viola":
            self.block=self.block_viola
            self.block1=self.block1_viola
        if self.tipo=="verde":
            self.block=self.block_verde
            self.block1=self.block1_verde
        self.centro=[self.x,self.y]
        
        
        
    def colore(self):
        if self.tipo=="blu":
            self.block=self.block_blu
            self.block1=self.block1_blu
        if self.tipo=="rosso":
            self.block=self.block_rosso
            self.block1=self.block1_rosso
        if self.tipo=="viola":
            self.block=self.block_viola
            self.block1=self.block1_viola
        if self.tipo=="verde":
            self.block=self.block_verde
            self.block1=self.block1_verde
    
    def movimento_armonico(self):
        if self.colpito==True:
            self.w=self.w1
        if self.colpito==False:
            self.w=0
        if self.t==0 and self.colpito==True:
            self.t=time.time()
        self.t1=abs(self.t-time.time())

        #t=0
        x=(self.A*cos(self.w*self.t1+self.phi_r))*cos(self.alfa_r)+self.centro0[0]
        y=(self.A*cos(self.w*self.t1+self.phi_r))*sin(self.alfa_r)+self.centro0[1]
        self.vx=-self.A*self.w*sin(self.w*self.t1)*cos(self.alfa_r)
        self.vy=-self.A*self.w*sin(self.w*self.t1)*sin(self.alfa_r)
        #x,y=coordinate_vertici(self.x,self.y,x,self.y,teta)
        self.rect.centerx=x
        self.rect.centery=y
        self.x=x
        self.y=y
        #print(self.x)
        self.centro=[x,y]
        self.hitbox=[[],[],[],[]]
        self.vertici=[]

        a,b=coordinate_vertici(self.centro[0], self.centro[1], self.x-self.dim_x/2, self.y-self.dim_y/2, self.rad)
        self.vertici=[[a,b]]
        a,b=coordinate_vertici(self.centro[0], self.centro[1], self.x+self.dim_x/2, self.y-self.dim_y/2, self.rad)
        self.vertici.append([a,b])
        a,b=coordinate_vertici(self.centro[0], self.centro[1], self.x-self.dim_x/2, self.y+self.dim_y/2, self.rad)
        self.vertici.append([a,b])
        a,b=coordinate_vertici(self.centro[0], self.centro[1], self.x+self.dim_x/2, self.y+self.dim_y/2, self.rad)
        self.vertici.append([a,b])
        self.base=22
        self.altezza=10
        #creazione hitbox base alta
        if self.teta!=90:
            punti_x=linspace(self.vertici[0][0],self.vertici[1][0],self.base)
            np.sort(punti_x)
            #print(punti_x)
            for x0 in punti_x:
                y0=eq_retta(self.vertici[0], self.vertici[1], x0)
                self.hitbox[0].append([x0,y0])
        if self.teta==90:
            punti_y=linspace(self.vertici[0][1],self.vertici[1][1],self.base)
            np.sort(punti_y)
            for y0 in punti_y:
                self.hitbox[0].append([self.vertici[0][0],y0])
        
        #creazione hitbox altezza destra
        if self.teta==0:
            punti_y=linspace(self.vertici[1][1],self.vertici[3][1],self.altezza)
            np.sort(punti_x)
            for y0 in punti_y:
                self.hitbox[1].append([self.vertici[1][0],y0])
        if self.teta!=0:
            punti_x=linspace(self.vertici[1][0],self.vertici[3][0],self.altezza)
            np.sort(punti_x)
            for x0 in punti_x:
                y0=eq_retta(self.vertici[1], self.vertici[3], x0)
                self.hitbox[1].append([x0,y0])
        
        #creazione hitbox base bassa
        if self.teta!=90:
            punti_x=linspace(self.vertici[2][0],self.vertici[3][0],self.base)
            np.sort(punti_x)
            for x0 in punti_x:
                y0=eq_retta(self.vertici[2], self.vertici[3], x0)
                self.hitbox[2].append([x0,y0])
        if self.teta==90:
            punti_y=linspace(self.vertici[2][1],self.vertici[3][1],self.base)
            np.sort(punti_y)
            for y0 in punti_y:
                self.hitbox[2].append([self.vertici[2][0],y0])
        
        #creazione hitbox lato sinistra
        if self.teta==0:
            punti_y=linspace(self.vertici[0][1],self.vertici[2][1],self.altezza)
            np.sort(punti_x)
            for y0 in punti_y:
                self.hitbox[3].append([self.vertici[0][0],y0])
        if self.teta!=0:
            punti_x=linspace(self.vertici[0][0],self.vertici[2][0],self.altezza)
            np.sort(punti_x)
            for x0 in punti_x:
                y0=eq_retta(self.vertici[0], self.vertici[2], x0)
                self.hitbox[3].append([x0,y0])

    def blit(self):
        if self.hit==0:
            schermo.blit(self.block, self.rect)
        if self.hit==1:
            schermo.blit(self.block1, self.rect)   


class Blocco_circolare():
    def __init__(self,pos_x,pos_y,rotazione,tipo,mov,ra,phi,w):
        self.dim_x=40
        self.dim_y=20
        self.x=pos_x
        self.y=pos_y
        self.cx=pos_x
        self.cy=pos_y
        self.centro0=[pos_x,pos_y]
        self.teta=rotazione
        self.tipo=tipo
        self.hit=0
        self.rad=(self.teta*pi/180)
        self.hitbox=[[],[],[],[]]
        self.n=0
        self.mov=mov
        self.ra=ra
        self.w=w
        self.phi=phi
        self.vx=0
        self.vy=0
        self.v=0
        self.t=0
        self.t1=0
        self.phi_r=-pi*self.phi/180
        self.block_blu=pygame.image.load('immagini/blocchi/block_blue.png')
        self.block1_blu=pygame.image.load('immagini/blocchi/element_blue_rectangle.png')
        self.block_rosso=pygame.image.load('immagini/blocchi/block_red.png')
        self.block1_rosso=pygame.image.load('immagini/blocchi/element_red_rectangle.png')
        self.block_viola=pygame.image.load('immagini/blocchi/block_purple.png')
        self.block1_viola=pygame.image.load('immagini/blocchi/element_purple_rectangle.png')
        self.block_verde=pygame.image.load('immagini/blocchi/block_green.png')
        self.block1_verde=pygame.image.load('immagini/blocchi/element_green_rectangle.png')
        self.block_giallo=pygame.image.load('immagini/blocchi/block_brown.png')
        self.block1_giallo=pygame.image.load('immagini/blocchi/element_yellow_rectangle.png')
        
        
        self.block_blu=pygame.transform.scale(self.block_blu, (self.dim_x, self.dim_y))
        self.block_blu,self.rect=rot_center(self.block_blu, self.teta, self.x, self.y)
        self.block1_blu=pygame.transform.scale(self.block1_blu, (self.dim_x, self.dim_y))
        self.block1_blu,self.rect=rot_center(self.block1_blu, self.teta, self.x, self.y)
        
        self.block_rosso=pygame.transform.scale(self.block_rosso, (self.dim_x, self.dim_y))
        self.block_rosso,self.rect=rot_center(self.block_rosso, self.teta, self.x, self.y)
        self.block1_rosso=pygame.transform.scale(self.block1_rosso, (self.dim_x, self.dim_y))
        self.block1_rosso,self.rect=rot_center(self.block1_rosso, self.teta, self.x, self.y)
        
        self.block_viola=pygame.transform.scale(self.block_viola, (self.dim_x, self.dim_y))
        self.block_viola,self.rect=rot_center(self.block_viola, self.teta, self.x, self.y)
        self.block1_viola=pygame.transform.scale(self.block1_viola, (self.dim_x, self.dim_y))
        self.block1_viola,self.rect=rot_center(self.block1_viola, self.teta, self.x, self.y)
        
        self.block_verde=pygame.transform.scale(self.block_verde, (self.dim_x, self.dim_y))
        self.block_verde,self.rect=rot_center(self.block_verde, self.teta, self.x, self.y)
        self.block1_verde=pygame.transform.scale(self.block1_verde, (self.dim_x, self.dim_y))
        self.block1_verde,self.rect=rot_center(self.block1_verde, self.teta, self.x, self.y)
        
        self.block_giallo=pygame.transform.scale(self.block_giallo, (self.dim_x, self.dim_y))
        self.block_giallo,self.rect=rot_center(self.block_giallo, self.teta, self.x, self.y)
        self.block1_giallo=pygame.transform.scale(self.block1_giallo, (self.dim_x, self.dim_y))
        self.block1_giallo,self.rect=rot_center(self.block1_giallo, self.teta, self.x, self.y)
        
        if self.tipo=="blu":
            self.block=self.block_blu
            self.block1=self.block1_blu
        if self.tipo=="rosso":
            self.block=self.block_rosso
            self.block1=self.block1_rosso
        if self.tipo=="viola":
            self.block=self.block_viola
            self.block1=self.block1_viola
        if self.tipo=="verde":
            self.block=self.block_verde
            self.block1=self.block1_verde
        self.centro=[self.x,self.y]
        
        
        
    def colore(self):
        if self.tipo=="blu":
            self.block=self.block_blu
            self.block1=self.block1_blu
        if self.tipo=="rosso":
            self.block=self.block_rosso
            self.block1=self.block1_rosso
        if self.tipo=="viola":
            self.block=self.block_viola
            self.block1=self.block1_viola
        if self.tipo=="verde":
            self.block=self.block_verde
            self.block1=self.block1_verde
    
    def movimento_circolare(self):
        #print(self.w)
        if self.t==0:
            self.t=time.time()
        #self.t1=abs(self.t-time.time())

        #t=0
        t=time.time()
        self.phi_r=self.phi_r+self.w*abs(self.t-t)
        if self.phi_r>2*pi:
            self.phi_r=self.phi_r-2*pi
        x=self.cx+self.ra*cos(self.phi_r)
        y=self.cy+self.ra*sin(self.phi_r)
    
        self.v=self.w*self.ra
        self.vx=-self.v*sin(self.phi_r)
        self.vy=self.v*cos(self.phi_r)
        #x,y=coordinate_vertici(self.x,self.y,x,self.y,teta)
        self.rect.centerx=x
        self.rect.centery=y
        self.x=x
        self.y=y
        self.t=t
        #print(self.x)
        self.centro=[x,y]
        self.hitbox=[[],[],[],[]]
        self.vertici=[]

        a,b=coordinate_vertici(self.centro[0], self.centro[1], self.x-self.dim_x/2, self.y-self.dim_y/2, self.rad)
        self.vertici=[[a,b]]
        a,b=coordinate_vertici(self.centro[0], self.centro[1], self.x+self.dim_x/2, self.y-self.dim_y/2, self.rad)
        self.vertici.append([a,b])
        a,b=coordinate_vertici(self.centro[0], self.centro[1], self.x-self.dim_x/2, self.y+self.dim_y/2, self.rad)
        self.vertici.append([a,b])
        a,b=coordinate_vertici(self.centro[0], self.centro[1], self.x+self.dim_x/2, self.y+self.dim_y/2, self.rad)
        self.vertici.append([a,b])
        self.base=22
        self.altezza=10
        #creazione hitbox base alta
        if self.teta!=90:
            punti_x=linspace(self.vertici[0][0],self.vertici[1][0],self.base)
            np.sort(punti_x)
            #print(punti_x)
            for x0 in punti_x:
                y0=eq_retta(self.vertici[0], self.vertici[1], x0)
                self.hitbox[0].append([x0,y0])
        if self.teta==90:
            punti_y=linspace(self.vertici[0][1],self.vertici[1][1],self.base)
            np.sort(punti_y)
            for y0 in punti_y:
                self.hitbox[0].append([self.vertici[0][0],y0])
        
        #creazione hitbox altezza destra
        if self.teta==0:
            punti_y=linspace(self.vertici[1][1],self.vertici[3][1],self.altezza)
            np.sort(punti_x)
            for y0 in punti_y:
                self.hitbox[1].append([self.vertici[1][0],y0])
        if self.teta!=0:
            punti_x=linspace(self.vertici[1][0],self.vertici[3][0],self.altezza)
            np.sort(punti_x)
            for x0 in punti_x:
                y0=eq_retta(self.vertici[1], self.vertici[3], x0)
                self.hitbox[1].append([x0,y0])
        
        #creazione hitbox base bassa
        if self.teta!=90:
            punti_x=linspace(self.vertici[2][0],self.vertici[3][0],self.base)
            np.sort(punti_x)
            for x0 in punti_x:
                y0=eq_retta(self.vertici[2], self.vertici[3], x0)
                self.hitbox[2].append([x0,y0])
        if self.teta==90:
            punti_y=linspace(self.vertici[2][1],self.vertici[3][1],self.base)
            np.sort(punti_y)
            for y0 in punti_y:
                self.hitbox[2].append([self.vertici[2][0],y0])
        
        #creazione hitbox lato sinistra
        if self.teta==0:
            punti_y=linspace(self.vertici[0][1],self.vertici[2][1],self.altezza)
            np.sort(punti_x)
            for y0 in punti_y:
                self.hitbox[3].append([self.vertici[0][0],y0])
        if self.teta!=0:
            punti_x=linspace(self.vertici[0][0],self.vertici[2][0],self.altezza)
            np.sort(punti_x)
            for x0 in punti_x:
                y0=eq_retta(self.vertici[0], self.vertici[2], x0)
                self.hitbox[3].append([x0,y0])

    def blit(self):
        if self.hit==0:
            schermo.blit(self.block, self.rect)
        if self.hit==1:
            schermo.blit(self.block1, self.rect)


class Peg():
    def __init__(self,pos_x,pos_y, tipo, festa, mov):
        self.dim_x=25
        self.dim_y=25
        self.x=pos_x
        self.y=pos_y
        self.tipo=tipo
        self.festa=festa
        self.hitbox0=[]
        self.hitbox=[]
        self.r=self.dim_x/2
        self.hit=0
        self.n=0
        self.mov=mov
        self.t=0
        self.vx=0
        self.vy=0
        
        if self.festa==0:
            self.sfera_blu=pygame.image.load('immagini/sfere/lit_blue_peg.png')
            self.sfera1_blu=pygame.image.load('immagini/sfere/glowing_blue_peg.png')
            self.sfera_rossa=pygame.image.load('immagini/sfere/lit_red_peg.png')
            self.sfera1_rossa=pygame.image.load('immagini/sfere/glowing_red_peg.png')
            self.sfera_viola=pygame.image.load('immagini/sfere/14.png')
            self.sfera1_viola=pygame.image.load('immagini/sfere/13.png')
            self.sfera_verde=pygame.image.load('immagini/sfere/lit_green_peg.png')
            self.sfera1_verde=pygame.image.load('immagini/sfere/glowing_green_peg.png')
            self.sfera_gialla=pygame.image.load('immagini/sfere/lit_yellow_peg.png')
            self.sfera1_gialla=pygame.image.load('immagini/sfere/glowing_yellow_peg.png')
            
            
            self.sfera_blu=pygame.transform.scale(self.sfera_blu, (self.dim_x, self.dim_y))
            self.sfera1_blu=pygame.transform.scale(self.sfera1_blu, (self.dim_x, self.dim_y))
            self.sfera_rossa=pygame.transform.scale(self.sfera_rossa, (self.dim_x, self.dim_y))
            self.sfera1_rossa=pygame.transform.scale(self.sfera1_rossa, (self.dim_x, self.dim_y))
            self.sfera_verde=pygame.transform.scale(self.sfera_verde, (self.dim_x, self.dim_y))
            self.sfera1_verde=pygame.transform.scale(self.sfera1_verde, (self.dim_x, self.dim_y))
            self.sfera_viola=pygame.transform.scale(self.sfera_viola, (self.dim_x, self.dim_y))
            self.sfera1_viola=pygame.transform.scale(self.sfera1_viola, (self.dim_x, self.dim_y))
            self.sfera_gialla=pygame.transform.scale(self.sfera_gialla, (self.dim_x, self.dim_y))
            self.sfera1_gialla=pygame.transform.scale(self.sfera1_gialla, (self.dim_x, self.dim_y))
            
            if self.tipo=="blu":
                self.sfera=self.sfera_blu
                self.sfera1=self.sfera1_blu
            if self.tipo=="rosso":
                self.sfera=self.sfera_rossa
                self.sfera1=self.sfera1_rossa
            if self.tipo=="viola":
                self.sfera=self.sfera_viola
                self.sfera1=self.sfera1_viola
            if self.tipo=="verde":
                self.sfera=self.sfera_verde
                self.sfera1=self.sfera1_verde
            self.rect = self.sfera.get_rect()
            self.rect.center=(self.x,self.y)
            self.hitbox, self.hitbox0=Hitbox(self.x,self.y,self.r,self.hitbox,self.hitbox0)
        if self.festa==1:
            self.x=pos_x
            self.y=pos_y
            self.dim_x=100
            self.dim_y=100
            self.r=self.dim_x/2
            self.sfera=pygame.image.load("immagini/color_circle.png")
            self.sfera=pygame.transform.scale(self.sfera,(self.dim_x,self.dim_y))
            self.sfera1=pygame.image.load("immagini/color_circle.png")
            self.sfera1=pygame.transform.scale(self.sfera1,(self.dim_x,self.dim_y))
            self.rect = self.sfera.get_rect()
            self.rect.center=(self.x,self.y)
            self.hitbox, self.hitbox0=Hitbox(self.x,self.y,self.r,self.hitbox,self.hitbox0)
    def colore(self):
        if self.festa==0:
            if self.tipo=="blu":
                self.sfera=self.sfera_blu
                self.sfera1=self.sfera1_blu
            if self.tipo=="rosso":
                self.sfera=self.sfera_rossa
                self.sfera1=self.sfera1_rossa
            if self.tipo=="viola":
                self.sfera=self.sfera_viola
                self.sfera1=self.sfera1_viola
            if self.tipo=="verde":
                self.sfera=self.sfera_verde
                self.sfera1=self.sfera1_verde

    def movimento_armonico(self,A,w,phi,teta):
        if self.mov==True:
            if self.t==0:
                self.t=time.time()
            t=abs(self.t-time.time())
            teta_r=-pi*teta/180
            phi_r=-pi*phi/180
            #t=0
            x=(A*cos(w*t+phi_r))*cos(teta_r)+self.x
            y=(A*cos(w*t+phi_r))*sin(teta_r)+self.y
            #x,y=coordinate_vertici(self.x,self.y,x,self.y,teta)
            self.rect.centerx=x
            self.rect.centery=y
            self.hitbox, self.hitbox0=Hitbox(self.rect.centerx,self.rect.centery,self.r,self.hitbox,self.hitbox0)
            self.vx=-A*w*sin(w*self.t)


    def blit(self):

        if self.hit==0:
            schermo.blit(self.sfera, self.rect)
        if self.hit==1:
            schermo.blit(self.sfera1, self.rect)
    
        
        #for punto in self.hitbox:
            #schermo.fill(rosso,(punto,(4,4)))
        #schermo.fill((255,0,0),((self.x,self.y),(4,4)))

class Peg_Armonico():
    def __init__(self,pos_x,pos_y, tipo, festa, mov,A,w,phi,teta):
        self.dim_x=25
        self.dim_y=25
        self.x=pos_x
        self.y=pos_y
        self.tipo=tipo
        self.festa=festa
        self.hitbox0=[]
        self.hitbox=[]
        self.r=self.dim_x/2
        self.hit=0
        self.n=0
        self.mov=mov
        self.t=0
        self.vx=0
        self.vy=0
        self.A=A
        self.w=w
        self.phi=phi
        self.teta=teta
        if self.festa==0:
            self.sfera_blu=pygame.image.load('immagini/sfere/lit_blue_peg.png')
            self.sfera1_blu=pygame.image.load('immagini/sfere/glowing_blue_peg.png')
            self.sfera_rossa=pygame.image.load('immagini/sfere/lit_red_peg.png')
            self.sfera1_rossa=pygame.image.load('immagini/sfere/glowing_red_peg.png')
            self.sfera_viola=pygame.image.load('immagini/sfere/14.png')
            self.sfera1_viola=pygame.image.load('immagini/sfere/13.png')
            self.sfera_verde=pygame.image.load('immagini/sfere/lit_green_peg.png')
            self.sfera1_verde=pygame.image.load('immagini/sfere/glowing_green_peg.png')
            self.sfera_gialla=pygame.image.load('immagini/sfere/lit_yellow_peg.png')
            self.sfera1_gialla=pygame.image.load('immagini/sfere/glowing_yellow_peg.png')
            
            
            self.sfera_blu=pygame.transform.scale(self.sfera_blu, (self.dim_x, self.dim_y))
            self.sfera1_blu=pygame.transform.scale(self.sfera1_blu, (self.dim_x, self.dim_y))
            self.sfera_rossa=pygame.transform.scale(self.sfera_rossa, (self.dim_x, self.dim_y))
            self.sfera1_rossa=pygame.transform.scale(self.sfera1_rossa, (self.dim_x, self.dim_y))
            self.sfera_verde=pygame.transform.scale(self.sfera_verde, (self.dim_x, self.dim_y))
            self.sfera1_verde=pygame.transform.scale(self.sfera1_verde, (self.dim_x, self.dim_y))
            self.sfera_viola=pygame.transform.scale(self.sfera_viola, (self.dim_x, self.dim_y))
            self.sfera1_viola=pygame.transform.scale(self.sfera1_viola, (self.dim_x, self.dim_y))
            self.sfera_gialla=pygame.transform.scale(self.sfera_gialla, (self.dim_x, self.dim_y))
            self.sfera1_gialla=pygame.transform.scale(self.sfera1_gialla, (self.dim_x, self.dim_y))
            
            if self.tipo=="blu":
                self.sfera=self.sfera_blu
                self.sfera1=self.sfera1_blu
            if self.tipo=="rosso":
                self.sfera=self.sfera_rossa
                self.sfera1=self.sfera1_rossa
            if self.tipo=="viola":
                self.sfera=self.sfera_viola
                self.sfera1=self.sfera1_viola
            if self.tipo=="verde":
                self.sfera=self.sfera_verde
                self.sfera1=self.sfera1_verde
            self.rect = self.sfera.get_rect()
            self.rect.center=(self.x,self.y)
            self.hitbox, self.hitbox0=Hitbox(self.x,self.y,self.r,self.hitbox,self.hitbox0)
        if self.festa==1:
            self.x=pos_x
            self.y=pos_y
            self.dim_x=100
            self.dim_y=100
            self.r=self.dim_x/2
            self.sfera=pygame.image.load("immagini/color_circle.png")
            self.sfera=pygame.transform.scale(self.sfera,(self.dim_x,self.dim_y))
            self.sfera1=pygame.image.load("immagini/color_circle.png")
            self.sfera1=pygame.transform.scale(self.sfera1,(self.dim_x,self.dim_y))
            self.rect = self.sfera.get_rect()
            self.rect.center=(self.x,self.y)
            self.hitbox, self.hitbox0=Hitbox(self.x,self.y,self.r,self.hitbox,self.hitbox0)
    def colore(self):
        if self.festa==0:
            if self.tipo=="blu":
                self.sfera=self.sfera_blu
                self.sfera1=self.sfera1_blu
            if self.tipo=="rosso":
                self.sfera=self.sfera_rossa
                self.sfera1=self.sfera1_rossa
            if self.tipo=="viola":
                self.sfera=self.sfera_viola
                self.sfera1=self.sfera1_viola
            if self.tipo=="verde":
                self.sfera=self.sfera_verde
                self.sfera1=self.sfera1_verde

    def movimento_armonico(self):
        
        if self.t==0:
            self.t=time.time()
        t=abs(self.t-time.time())
        teta_r=-pi*self.teta/180
        phi_r=-pi*self.phi/180
        #t=0
        x=(self.A*cos(self.w*t+phi_r))*cos(teta_r)+self.x
        y=(self.A*cos(self.w*t+phi_r))*sin(teta_r)+self.y
        self.vx=-self.A*self.w*sin(self.w*t)*cos(teta_r)
        self.vy=-self.A*self.w*sin(self.w*t)*sin(teta_r)
        #x,y=coordinate_vertici(self.x,self.y,x,self.y,teta)
        self.rect.centerx=x
        self.rect.centery=y
        self.hitbox, self.hitbox0=Hitbox(self.rect.centerx,self.rect.centery,self.r,self.hitbox,self.hitbox0)
        


    def blit(self):

        if self.hit==0:
            schermo.blit(self.sfera, self.rect)
        if self.hit==1:
            schermo.blit(self.sfera1, self.rect)


class Peg_Circolare():
    def __init__(self,pos_x,pos_y, tipo, festa, mov,ra,teta,w):
        self.dim_x=25
        self.dim_y=25
        self.x=pos_x
        self.y=pos_y
        self.cx=pos_x
        self.cy=pos_y
        self.tipo=tipo
        self.festa=festa
        self.hitbox0=[]
        self.hitbox=[]
        self.r=self.dim_x/2
        self.ra=ra
        self.teta=teta
        self.teta_r=teta*pi/180
        self.w=w
        self.hit=0
        self.n=0
        self.mov=mov
        self.t=0
        self.v=0
        self.vx=0
        self.vy=0
        if self.festa==0:
            self.sfera_blu=pygame.image.load('immagini/sfere/lit_blue_peg.png')
            self.sfera1_blu=pygame.image.load('immagini/sfere/glowing_blue_peg.png')
            self.sfera_rossa=pygame.image.load('immagini/sfere/lit_red_peg.png')
            self.sfera1_rossa=pygame.image.load('immagini/sfere/glowing_red_peg.png')
            self.sfera_viola=pygame.image.load('immagini/sfere/14.png')
            self.sfera1_viola=pygame.image.load('immagini/sfere/13.png')
            self.sfera_verde=pygame.image.load('immagini/sfere/lit_green_peg.png')
            self.sfera1_verde=pygame.image.load('immagini/sfere/glowing_green_peg.png')
            self.sfera_gialla=pygame.image.load('immagini/sfere/lit_yellow_peg.png')
            self.sfera1_gialla=pygame.image.load('immagini/sfere/glowing_yellow_peg.png')
            
            
            self.sfera_blu=pygame.transform.scale(self.sfera_blu, (self.dim_x, self.dim_y))
            self.sfera1_blu=pygame.transform.scale(self.sfera1_blu, (self.dim_x, self.dim_y))
            self.sfera_rossa=pygame.transform.scale(self.sfera_rossa, (self.dim_x, self.dim_y))
            self.sfera1_rossa=pygame.transform.scale(self.sfera1_rossa, (self.dim_x, self.dim_y))
            self.sfera_verde=pygame.transform.scale(self.sfera_verde, (self.dim_x, self.dim_y))
            self.sfera1_verde=pygame.transform.scale(self.sfera1_verde, (self.dim_x, self.dim_y))
            self.sfera_viola=pygame.transform.scale(self.sfera_viola, (self.dim_x, self.dim_y))
            self.sfera1_viola=pygame.transform.scale(self.sfera1_viola, (self.dim_x, self.dim_y))
            self.sfera_gialla=pygame.transform.scale(self.sfera_gialla, (self.dim_x, self.dim_y))
            self.sfera1_gialla=pygame.transform.scale(self.sfera1_gialla, (self.dim_x, self.dim_y))
            
            if self.tipo=="blu":
                self.sfera=self.sfera_blu
                self.sfera1=self.sfera1_blu
            if self.tipo=="rosso":
                self.sfera=self.sfera_rossa
                self.sfera1=self.sfera1_rossa
            if self.tipo=="viola":
                self.sfera=self.sfera_viola
                self.sfera1=self.sfera1_viola
            if self.tipo=="verde":
                self.sfera=self.sfera_verde
                self.sfera1=self.sfera1_verde
            self.rect = self.sfera.get_rect()
            self.rect.center=(self.x,self.y)
            self.hitbox, self.hitbox0=Hitbox(self.x,self.y,self.r,self.hitbox,self.hitbox0)
        if self.festa==1:
            self.x=pos_x
            self.y=pos_y
            self.dim_x=100
            self.dim_y=100
            self.r=self.dim_x/2
            self.sfera=pygame.image.load("immagini/color_circle.png")
            self.sfera=pygame.transform.scale(self.sfera,(self.dim_x,self.dim_y))
            self.sfera1=pygame.image.load("immagini/color_circle.png")
            self.sfera1=pygame.transform.scale(self.sfera1,(self.dim_x,self.dim_y))
            self.rect = self.sfera.get_rect()
            self.rect.center=(self.x,self.y)
            self.hitbox, self.hitbox0=Hitbox(self.x,self.y,self.r,self.hitbox,self.hitbox0)
    def colore(self):
        if self.festa==0:
            if self.tipo=="blu":
                self.sfera=self.sfera_blu
                self.sfera1=self.sfera1_blu
            if self.tipo=="rosso":
                self.sfera=self.sfera_rossa
                self.sfera1=self.sfera1_rossa
            if self.tipo=="viola":
                self.sfera=self.sfera_viola
                self.sfera1=self.sfera1_viola
            if self.tipo=="verde":
                self.sfera=self.sfera_verde
                self.sfera1=self.sfera1_verde

    def movimento_circolare(self):
        t=time.time()
        #teta_r=self.teta*pi/180
        #self.w=0
        self.teta_r=self.teta_r+self.w*abs(self.t-t)
        if self.teta_r>2*pi:
            self.teta_r=self.teta_r-2*pi
        self.rect.centerx=self.cx+self.ra*cos(self.teta_r)
        self.rect.centery=self.cy+self.ra*sin(self.teta_r)
        self.x=self.rect.centerx
        self.y=self.rect.centery
        self.v=self.w*self.ra
        self.vx=-self.v*sin(self.teta_r)
        self.vy=self.v*cos(self.teta_r)
        self.hitbox, self.hitbox0=Hitbox(self.x,self.y,self.r,self.hitbox,self.hitbox0)
        #print(self.x)
        self.t=t

    def blit(self):

        if self.hit==0:
            schermo.blit(self.sfera, self.rect)
        if self.hit==1:
            schermo.blit(self.sfera1, self.rect)


class Cesto():
    def __init__(self,pos_y,vero):
        self.dim_x=120
        self.dim_y=40
        self.vero=vero
        if vero==0:
            self.x=(xb2-xb1)/2-(self.dim_x/2)
            self.y=pos_y
        if vero==1:
            self.x=xb1
            self.y=pos_y
        if vero==2:
            self.x=xb2-self.dim_x
            self.y=pos_y
        self.cesto=pygame.image.load('immagini/cesto3.png')
        self.cesto=pygame.transform.scale(self.cesto, (self.dim_x, self.dim_y))
        c=17
        c1=7
        self.hitbox=[[self.x,self.y+c],[self.x+self.dim_x,self.y+c],[self.x+c1,self.y+c],[self.x+self.dim_x-c1,self.y+c]]
        self.t=0
        self.vx=0
        
    def movimento(self):
        c=17
        c1=7
        A=((xb2-xb1)/2-(self.dim_x/2))
        w=1
        self.t=time.time()
        self.x=A*cos(w*self.t)+A+40
        self.hitbox=[[self.x,self.y+c],[self.x+self.dim_x,self.y+c],[self.x+c1,self.y+c],[self.x+self.dim_x-c1,self.y+c]]
        self.vx=-A*w*sin(w*self.t)
    def blit(self):
        schermo.blit(self.cesto,(self.x,self.y))
        #for k in self.hitbox:
            #schermo.fill(rosso,(k,(4,4)))


class Bordo():
    def __init__(self,pos_x):
        self.x=pos_x
    def blit(self,h):
        pygame.draw.line(schermo, rosso, (self.x,0), (self.x,Y))
        pygame.draw.line(schermo,rosso,(xb1,h),(xb2,h))
        #pygame.draw.line(schermo,rosso,((xb2+xb1)/2,15),((xb2+xb1)/2,720))
    
class Pannello():
    def __init__(self):
        self.x=xb2
        self.y=0
        self.dim_x=100
        self.dim_y=720
        self.panel=pygame.image.load('immagini/panel.png')
        self.panel=pygame.transform.scale(self.panel, (self.dim_x, self.dim_y))
        self.dim_x2=42
        self.dim_y2=22
        self.x2=xb2+25
        self.y2=670
        self.blocco2=pygame.image.load('immagini/blocchi/rosso2.png')
        self.blocco2=pygame.transform.scale(self.blocco2, (self.dim_x2, self.dim_y2))
        self.lista2=[]
        self.blocco1=pygame.image.load('immagini/blocchi/rosso1.png')
        self.blocco1=pygame.transform.scale(self.blocco1, (self.dim_x2, self.dim_y2))
        for i in range(25):
           b=self.y2-self.dim_y2*i
           self.lista2.append((self.x2,b))
    def blit(self,n_rossi,molt):
        schermo.blit(self.panel,(self.x,self.y))
        for k in self.lista2:
            schermo.blit(self.blocco2,k)
        for i in range (n_rossi_max-n_rossi):
            schermo.blit(self.blocco1,(self.lista2[i][0],self.lista2[i][1]))
        molt= font3.render("x"+str(molt), True, bianco)
        schermo.blit(molt,(1210,60))

class Traga():
    def __init__(self, nome1, nome2):
        self.x=305
        self.y=25
        self.dim_x=50
        self.dim_y=525
        self.targa=pygame.image.load('immagini/panel.png')
        self.targa=pygame.transform.scale(self.targa, (self.dim_x, self.dim_y))
        #self.targa,self.rect=rot_center(self.targa, 0, self.x, self.y)
        self.targa,self.rect=rot_center(self.targa, 90, self.x, self.y)
        self.x2=920
        self.y2=25
        self.dim_x2=50
        self.dim_y2=525
        self.targa2=pygame.image.load('immagini/panel.png')
        self.targa2=pygame.transform.scale(self.targa2, (self.dim_x2, self.dim_y2))
        #self.targa,self.rect=rot_center(self.targa, 0, self.x, self.y)
        self.targa2,self.rect2=rot_center(self.targa2, 90, self.x2, self.y2)
        self.nome1= font.render(nome1, True, blu)
        self.nome2= font.render(nome2, True, blu)
        
        
    def blit(self, palle1,palle2,punti1,punti2):
        schermo.blit(self.targa,self.rect)
        schermo.blit(self.targa2,self.rect2)
        schermo.blit(self.nome1, (70,5))
        schermo.blit(self.nome2,(685,5))
        if palle1>1:
            a="balls "
        if palle1<=1:
            a="ball "
        if palle2>1:
            b= "balls "
        if palle2<=1:
            b="ball "
        palle1= font.render(a+str(palle1), True, blu)
        palle2= font.render(b+str(palle2), True, blu)
        punti1= font2.render(str(punti1), True, rosso)
        punti2=font2.render(str(punti2), True, rosso)
        schermo.blit(palle1,(80,30))
        schermo.blit(palle2,(695,30))
        schermo.blit(punti1,(300,15))
        schermo.blit(punti2,(900,15))


class Pannello_Punti():    
    def __init__(self):
        self.x=420
        self.y=200
        self.dim_x=500
        self.dim_y=300
        self.image=pygame.image.load('immagini/panel 3.png')
        self.image=pygame.transform.scale(self.image, (self.dim_x,self.dim_y ))
    def blit(self):
        schermo.blit(self.image,(self.x,self.y))


class Selezione_pg():
    def __init__(self):
        self.var=-1
        self.var2=-1
        self.dim_x_p=220
        self.dim_y_p=720
        self.x1=450
        self.y1=0
        self.x2=self.x1+self.dim_x_p
        self.y2=self.y1
        self.pannello=pygame.image.load("immagini/bottoni/Panel 18.png")
        self.pannello=pygame.transform.scale(self.pannello, (self.dim_x_p, self.dim_y_p))


        self.dim_x=100
        self.dim_y=100
        self.button1=pygame.image.load("immagini/bottoni/blue_panel.png")
        self.butotn1=pygame.transform.scale(self.button1, (self.dim_x, self.dim_y))
        self.button2=pygame.image.load("immagini/bottoni/green_panel.png")
        self.button2=pygame.transform.scale(self.button2, (self.dim_x, self.dim_y))
        self.lista_b1=[]
        self.lista_b2=[]
        for i in range(9):
            self.lista_b1.append(self.button1)
            self.lista_b2.append(self.button1)
        self.cord1=[]
        self.cord2=[]
        for i in range(4):
            for j in range(2):
                self.cord1.append([self.x1+j*self.dim_y+10,self.y1+i*self.dim_x+10])
                self.cord2.append([self.x2+j*self.dim_y+10,self.y2+i*self.dim_x+10])
        self.cord1.append([self.x1+int(self.dim_x/2)+10,self.y1+4*self.dim_y+10])
        self.cord2.append([self.x2+int(self.dim_x/2)+10,self.y2+4*self.dim_y+10])
        self.dim_x_pg=80
        self.dim_y_pg=80
        self.url="immagini/poteri/"
        self.png=".png"
        self.nomi=["girl","imbianchino","ufo","tiger","alieno","cavallo","razzo","cesto"]
        self.nomi_r=["Crack-color","Painter","Ufo","Tiger","Alien","Horse","Rocket","Pot"]
        self.immagini_pg=[]
        for i in self.nomi:
            im=pygame.image.load(self.url+i+self.png)
            im=pygame.transform.scale(im, (self.dim_x_pg, self.dim_y_pg))
            self.immagini_pg.append(im)
        font5=pygame.font.Font("freesansbold.ttf", 24)
        self.text=font5.render("Random", True, giallo)


        self.x_play=self.x1+7
        self.y_play=self.cord1[-1][1]+130
        self.dim_x_play=80
        self.dim_y_play=80
        self.play1=pygame.image.load("immagini/bottoni/play_blu.png")
        self.play1=pygame.transform.scale(self.play1, (self.dim_x_play, self.dim_y_play))
        self.play2=pygame.image.load("immagini/bottoni/play_green.png")
        self.play2=pygame.transform.scale(self.play2, (self.dim_x_play, self.dim_y_play))
        self.play=self.play1

        
    def selezione(self,x,y):
        #self.var=-1
        #self.var2=-1
        for i in range(len(self.cord1)):
            if self.cord1[i][0]<x<self.cord1[i][0]+self.dim_x and self.cord1[i][1]<y<self.cord1[i][1]+self.dim_y:
                self.var=i
            if self.cord2[i][0]<x<self.cord2[i][0]+self.dim_x and self.cord2[i][1]<y<self.cord2[i][1]+self.dim_y:
                self.var2=i
        if self.var!=-1:
            if self.button2 in self.lista_b1:
                indice=self.lista_b1.index(self.button2)
                self.lista_b1[indice]=self.button1
            self.lista_b1[self.var]=self.button2
        if self.var2!=-1:
            if self.button2 in self.lista_b2:
                indice=self.lista_b2.index(self.button2)
                self.lista_b2[indice]=self.button1
            self.lista_b2[self.var2]=self.button2
            #print("eccomi")

    def cambio_colore(self,x,y):
        if self.play==self.play2:
            self.play=self.play1
        if self.x_play<x<self.x_play+self.dim_x_play and self.y_play<y<self.y_play+self.dim_y_play:
            self.play=self.play2

    def click_play(self,x,y,scegliendo_pg,pg1,pg2):
        image1=0
        image2=0
        #print(self.var, self.var2)
        if self.x_play<x<self.x_play+self.dim_x_play and self.y_play<y<self.y_play+self.dim_y_play and self.var!=-1 and self.var2!=-1:
            #print("sono qui")
            scegliendo_pg=False
            if 0<=self.var<8:
                pg1=self.nomi_r[self.var]
            if self.var==8:
                a=np.random.randint(0,8)
                pg1=self.nomi_r[a]
            
            if 0<=self.var2<8:
                pg2=self.nomi_r[self.var2]
            if self.var2==8:
                a=np.random.randint(0,8)
                pg2=self.nomi_r[a]

            if pg1=="Crack-color":
                image1=pygame.image.load('immagini/poteri/girl.png')
            if pg2=="Crack-color":
                image2=pygame.image.load('immagini/poteri/girl.png')
            if pg1=="Painter":
                image1=pygame.image.load('immagini/poteri/imbianchino.png')
            if pg2=="Painter":
                image2=pygame.image.load('immagini/poteri/imbianchino.png')
            if pg1=="Ufo":
                image1=pygame.image.load('immagini/poteri/ufo.png')
            if pg2=="Ufo":
                image2=pygame.image.load('immagini/poteri/ufo.png')
            if pg1=="Tiger":
                image1=pygame.image.load('immagini/poteri/tiger.png')
            if pg2=="Tiger":
                image2=pygame.image.load('immagini/poteri/tiger.png')
            if pg1=="Alien":
                image1=pygame.image.load('immagini/poteri/alieno.png')
            if pg2=="Alien":
                image2=pygame.image.load('immagini/poteri/alieno.png')   
            if pg1=="Horse":
                image1=pygame.image.load('immagini/poteri/cavallo.png')
            if pg2=="Horse":
                image2=pygame.image.load('immagini/poteri/cavallo.png')
            if pg1=="Rocket":
                image1=pygame.image.load('immagini/poteri/razzo.png')
            if pg2=="Rocket":
                image2=pygame.image.load('immagini/poteri/razzo.png')
            if pg1=="Steroid":
                image1=pygame.image.load('immagini/poteri/pillole.png')
            if pg2=="Steroid":
                image2=pygame.image.load('immagini/poteri/pillole.png')
            if pg1=="Pot":
                image1=pygame.image.load('immagini/poteri/cesto.png')
            if pg2=="Pot":
                image2=pygame.image.load('immagini/poteri/cesto.png')
        return scegliendo_pg,pg1,pg2, image1,image2
            



    def blit(self):
        schermo.blit(self.pannello,(self.x1,self.y1))
        schermo.blit(self.pannello,(self.x2,self.y2))
        for i in range(len(self.cord1)):
            schermo.blit(self.lista_b1[i],self.cord1[i])
            schermo.blit(self.lista_b2[i],self.cord2[i])
        for i in range(len(self.immagini_pg)):
            schermo.blit(self.immagini_pg[i],self.cord1[i])
            schermo.blit(self.immagini_pg[i],self.cord2[i])
        x=self.cord1[-1][0]
        y=self.cord1[-1][1]+35
        x2=self.cord2[-1][0]
        y2=self.cord2[-1][1]+35
        schermo.blit(self.text,(x,y))
        schermo.blit(self.text,(x2,y2))
        schermo.blit(self.play,(self.x_play,self.y_play))


class Bottone_pausa():
    def __init__(self):
        self.x=0
        self.y=0
        self.dim_x=40
        self.dim_y=720
        self.im1=pygame.image.load("immagini/blue_button00.png")
        self.im1=pygame.transform.scale(self.im1, (self.dim_x, self.dim_y))
        self.im2=pygame.image.load("immagini/green_button00.png")
        self.im2=pygame.transform.scale(self.im2, (self.dim_x, self.dim_y))
        self.im=self.im1

    def passaggio(self,x,y):
        self.im=self.im1
        if self.x<x<self.x+self.dim_x and self.y<y<self.y+self.dim_y:
            self.im=self.im2

    def click(self,x,y,pausa):
        if self.x<x<self.x+self.dim_x and self.y<y<self.y+self.dim_y:
            pausa=True
        return pausa

    def blit(self):
        schermo.blit(self.im,(self.y,self.x))


class Fine_partita():
    def __init__(self,nome1,nome2,punti1,punti2):
        self.x=260
        self.y=180
        self.dim_x=700
        self.dim_y=400
        self.image=pygame.image.load('immagini/panel 7.png')
        self.image=pygame.transform.scale(self.image, (self.dim_x,self.dim_y ))
        self.p1=(610,235)
        self.p2=(610,570)
        self.nome1=nome1
        self.nome2=nome2
        self.x1=self.x+40
        self.y1=510
        self.dim_x1=140
        self.dim_y1=55
        self.x2=self.x1+self.dim_x1
        self.y2=self.y1
        self.bottone1=pygame.image.load('immagini/bottoni/bottone_rosso.png')
        self.bottone1=pygame.transform.scale(self.bottone1, (self.dim_x1,self.dim_y1 ))
        self.bottone2=pygame.image.load('immagini/bottoni/bottone_verde.png')
        self.bottone2=pygame.transform.scale(self.bottone2, (self.dim_x1,self.dim_y1 ))
        self.main=self.bottone1
        self.next=self.bottone1
        font6=pygame.font.Font("freesansbold.ttf", 36)
        self.text1=font6.render("Quit", True, giallo)
        self.text2=font6.render("Next", True, giallo)



    def passagio(self,x,y):
        self.main=self.bottone1
        if self.x1<x<self.x1+self.dim_x1 and self.y1<y<self.y1+self.dim_y1:
            self.main=self.bottone2
        self.next=self.bottone1
        if self.x2<x<self.x2+self.dim_x1 and self.y2<y<self.y2+self.dim_y1:
            self.next=self.bottone2

    def click_next(self,x,y,cont_round,livello,n_round,punti_tot1,punti_tot2,punti1,punti2):
        if self.x2<x<self.x2+self.dim_x1 and self.y2<y<self.y2+self.dim_y1 and cont_round<n_round:
            cont_round=cont_round+1
            livello=livello-1
            punti_tot1=punti_tot1+punti1
            punti_tot2=punti_tot2+punti2
        return cont_round,livello, punti_tot1,punti_tot2

    
    def click_quit(self,x,y,livello):
        if self.x1<x<self.x1+self.dim_x1 and self.y1<y<self.y1+self.dim_y1:
            livello=1
        return livello

    def blit(self,punti1,punti2,punti_tot1,punti_tot2,n_round,cont_round):
        schermo.blit(self.image,(self.x,self.y))
        pygame.draw.line(schermo,rosso,self.p1,self.p2)
        text1 = font3.render("Round "+str(cont_round)+"/"+str(n_round), True, giallo)
        schermo.blit(text1,(510,190))
        
        nome1=font7.render(self.nome1, True, rosso)
        schermo.blit(nome1,(310,240))
        
        nome2=font7.render(self.nome2, True, rosso)
        schermo.blit(nome2,(630,240))
        
        text2_1="This round you made"
        blit_punti1=font7.render(str(punti1), True, giallo)
        text2_1=font7.render(text2_1, True, rosso)
        schermo.blit(text2_1,(310,290))
        schermo.blit(blit_punti1,(400,330))
        
        text2_2="This round you made"
        blit_punti2=font7.render(str(punti2), True, giallo)
        text2_2=font7.render(text2_2, True, rosso)
        schermo.blit(text2_2,(630,290))
        schermo.blit(blit_punti2,(720,330))
        
        text3_1="Total point in this game"
        blit_punti_tot1=font7.render(str(punti_tot1+punti1), True, giallo)
        text3_1=font7.render(text3_1, True, rosso)
        schermo.blit(text3_1,(310,380))
        schermo.blit(blit_punti_tot1,(400,430))
        
        text3_2="Total point in this game"
        blit_punti_tot2=font7.render(str(punti_tot2+punti2), True, giallo)
        text3_2=font7.render(text3_2, True, rosso)
        schermo.blit(text3_2,(630,380))
        schermo.blit(blit_punti_tot2,(720,430))

        schermo.blit(self.main,(self.x1,self.y1))
        schermo.blit(self.text1,(self.x1+35,self.y1+12))
        if cont_round<n_round:
            schermo.blit(self.next,(self.x2,self.y2))
            schermo.blit(self.text2,(self.x2+35,self.y2+12))

class Personaggio():
    def __init__(self,image1,image2,pg1,pg2):
        self.pg1=pg1
        self.pg2=pg2
        self.dim_x=75
        self.dim_y=45
        self.image1=image1
        self.image1=pygame.transform.scale(self.image1, (self.dim_x, self.dim_y))
        self.image2=image2
        self.image2=pygame.transform.scale(self.image2, (self.dim_x, self.dim_y))
    
    def re_color(self,potere1,potere2, bol_potere, blocchi,sfere, animazione):
        #print(potere1,turno,pg1,bol_potere)
        peg_colpiti=[]
        if potere1>0 and turno==1 and self.pg1=="Crack-color" and bol_potere==False:
            bol_potere=True
            animazione=True
            potere1=potere1-1
            #print("eccomi")
            peg_colpiti=potere_viola(blocchi,sfere)
            
        if potere2>0 and turno==2 and self.pg2=="Crack-color" and bol_potere==False:
            #print(potere2)
            animazione=True
            bol_potere=True
            potere2=potere2-1
            peg_colpiti=potere_viola(blocchi,sfere)
        return potere1, potere2, bol_potere, peg_colpiti, animazione
    
    '''def poteri(self,potere1,potere2, bol_potere, animazione):
        if potere1>0 and turno==1 and self.pg1=="Painter" and bol_potere==False:
            bol_potere=True
            animazione=True
            potere1=potere1-1
            #print("eccomi")

            
        if potere2>0 and turno==2 and self.pg2=="Painter" and bol_potere==False:
            #print(potere2)
            animazione=True
            bol_potere=True
            potere2=potere2-1
    
        return potere1, potere2, bol_potere, animazione'''
    def poteri(self,potere1,potere2, bol_potere, animazione):
        if self.pg1!="Crack-color" and self.pg1!="Ufo" and self.pg1!="Tiger" and self.pg1!="Alien" and self.pg1!="Horse" and self.pg1!="Rocket" and self.pg1!="Steroid" and self.pg1!="Pot":
            if potere1>0 and turno==1 and bol_potere==False:
                bol_potere=True
                animazione=True
                potere1=potere1-1
                #print("eccomi")

        if self.pg2!="Crack-color" and self.pg2!="Ufo" and self.pg2!="Tiger" and self.pg2!="Alien" and self.pg2!="Horse" and self.pg2!="Rocket" and self.pg2!="Steroid" and self.pg2!="Pot":
            if potere2>0 and turno==2 and bol_potere==False:
                #print(potere2)
                animazione=True
                bol_potere=True
                potere2=potere2-1
        return potere1, potere2, bol_potere, animazione
    def potere_ufo(self,potere1,potere2,bol_potere,verde_colpito):
        #print(potere1,turno,pg1,bol_potere)
        if potere1>0 and turno==1 and self.pg1=="Ufo" and bol_potere==False:
            bol_potere=True
            potere1=potere1-1
            #print("eccomi")

        if potere2>0 and turno==2 and self.pg2=="Ufo" and bol_potere==False:
            #print("eccomi")
            #print(potere2)
            bol_potere=True
            potere2=potere2-1
            
            
        if potere1>0 and turno==1 and self.pg1=="Tiger" and bol_potere==False:
            bol_potere=True
            potere1=potere1-1
            #print("eccomi")
            
        if potere2>0 and turno==2 and self.pg2=="Tiger" and bol_potere==False:
            #print("eccomi")
            #print(potere2)
            bol_potere=True
            potere2=potere2-1
        
        
        if potere1>0 and turno==1 and self.pg1=="Alien" and bol_potere==False:
            bol_potere=True
            potere1=potere1-1
            #print("eccomi")

        if potere2>0 and turno==2 and self.pg2=="Alien" and bol_potere==False:
            #print("eccomi")
            #print(potere2)
            bol_potere=True
            potere2=potere2-1
        if potere1>0 and turno==1 and self.pg1=="Horse" and bol_potere==False:
            bol_potere=True
            potere1=potere1-1
            #print("eccomi")

        if potere2>0 and turno==2 and self.pg2=="Horse" and bol_potere==False:
            #print("eccomi")
            #print(potere2)
            bol_potere=True
            potere2=potere2-1
        if potere1>0 and turno==1 and self.pg1=="Rocket" and bol_potere==False:
            bol_potere=True
            potere1=potere1-1

        if potere2>0 and turno==2 and self.pg2=="Rocket" and bol_potere==False:
            bol_potere=True
            potere2=potere2-1
            
        if potere1>0 and turno==1 and self.pg1=="Steroid" and bol_potere==False and verde_colpito==False:
            bol_potere=True
            potere1=potere1-1

        if potere2>0 and turno==2 and self.pg2=="Steroid" and bol_potere==False and verde_colpito==False:
            bol_potere=True
            potere2=potere2-1
            
        if potere1>0 and turno==1 and self.pg1=="Pot" and bol_potere==False:
            bol_potere=True
            potere1=potere1-1

        if potere2>0 and turno==2 and self.pg2=="Pot" and bol_potere==False:
            bol_potere=True
            potere2=potere2-1
        return potere1, potere2, bol_potere
            
    
    def blit(self):
        schermo.blit(self.image1,(450,3))
        schermo.blit(self.image2,(1050,3))
        

class Animazione_re_color():
    def __init__(self):
        self.x1=1200
        self.x2=1200
        self.v=-500
        self.t0=time.time()
        self.dim_x1=120
        self.dim_y1=80
        self.pistola=pygame.image.load('immagini/pistallx4.png')
        self.pistola=pygame.transform.scale(self.pistola, (self.dim_x1, self.dim_y1))
        self.bullet=pygame.image.load('immagini/schizzo.png')
 
        self.bullet=pygame.transform.scale(self.bullet, (60, 60))
        self.colpo_partito=False
        self.peg_colpiti=[]
        self.cord=[]
    def blit(self, peg_colpiti,oggetti,sfere,animazione, turno,pg1,pg2):
        #print("sono qui")
        #schermo.blit(self.pistola,(xb2+self.dim_x1,200))
        vero=False
        if peg_colpiti!=[]:
            self.t0=time.time()
            self.peg_colpiti=peg_colpiti
        if animazione==True and turno==1 and pg1=="Crack-color":
            vero=True
                
        if animazione==True and turno==2 and pg2=="Crack-color":
            vero=True
        #print(vero,animazione)
        if vero==True:
            if self.colpo_partito==False:
                self.cord=[]
                for i in self.peg_colpiti:
                    if i in sfere:  
                        self.cord.append((i.x,i.y))
                        self.colpo_partito=True
                    if i in oggetti:
                        self.cord.append((i.x,i.y))
                        self.colpo_partito=True
            x=1170
            x_p=1200
            tf=time.time()
            if len(self.cord)==2:
                y1=self.cord[0][1]-20
                y2=self.cord[1][1]-20
                y_p1=y1
                y_p2=y2
                
                self.x1=self.x1+self.v*(tf-self.t0)
                self.x2=self.x2+self.v*(tf-self.t0)
                self.t0=tf
                if self.x1<=self.peg_colpiti[0].x and self.x1>0:
                    if self.peg_colpiti[0] in sfere:
                        sfere[sfere.index(self.peg_colpiti[0])].tipo="viola"
                        self.x1=-100
                    if self.peg_colpiti[0] in oggetti:
                        oggetti[oggetti.index(self.peg_colpiti[0])].tipo="viola"
                        self.x1=-100

                if self.x2<=self.peg_colpiti[1].x and self.x2>0:
                    if self.peg_colpiti[1] in sfere:
                        sfere[sfere.index(self.peg_colpiti[1])].tipo="viola"
                        self.x2=-100
                    if self.peg_colpiti[1] in oggetti:
                        oggetti[oggetti.index(self.peg_colpiti[1])].tipo="viola"
                        self.x2=-100
                schermo.blit(self.bullet,(self.x1,y_p1))
                schermo.blit(self.bullet,(self.x2,y_p2))
                schermo.blit(self.pistola,(x,y1))
                schermo.blit(self.pistola,(x,y2))
                if self.x1<0 and self.x2<0:
                    animazione=False
                    self.x1=1200
                    self.x2=1200
                    self.peg_colpiti=[]
                    self.cord=[]
                    self.colpo_partito=False
            if len(self.cord)==1:
                y1=self.cord[0][1]-20
                y_p1=y1
                
                self.x1=self.x1+self.v*(tf-self.t0)
                self.t0=tf
                if self.x1<=self.peg_colpiti[0].x and self.x1>0:
                    if self.peg_colpiti[0] in sfere:
                        sfere[sfere.index(self.peg_colpiti[0])].tipo="viola"
                        self.x1=-100
                        animazione=False
                    if self.peg_colpiti[0] in oggetti:
                        oggetti[oggetti.index(self.peg_colpiti[0])].tipo="viola"
                        self.x1=-100
                        animazione=False
                        
                schermo.blit(self.bullet,(self.x1,y_p1))      
                schermo.blit(self.pistola,(x,y1))
                if self.x1<0:
                    animazione=False
                    self.x1=1200
                    self.x2=1200
                    self.peg_colpiti=[]
                    self.cord=[]
                    self.colpo_partito=False
            if len(self.cord)==0:
                animazione=False
                self.x1=1200
                self.x2=1200
                self.peg_colpiti=[]
                self.cord=[]
                self.colpo_partito=False
        return animazione

class Animazione_painter():
    def __init__(self):
        self.dim_x=70
        self.dim_y=60
        self.roller=pygame.image.load('immagini/paint roller.png')
        self.roller=pygame.transform.scale(self.roller, (self.dim_x, self.dim_y))
        self.cord=[]
        self.oggetti=[]
        self.centro=[]
        self.tf=0
        self.ti=0
    def blit(self,animazione,sfere,blocchi,turno,pg1,pg2):
        vero=False
        if animazione==True and turno==1 and pg1=="Painter":
            vero=True
                
        if animazione==True and turno==2 and pg2=="Painter":
            vero=True
        
        if vero==True:
            if self.cord==[]:
                self.ti=time.time()
                for i in blocchi:
                    if i.tipo=="blu" and i.hit==0 and i.mov!=1:
                        self.cord.append([i.x,i.y])
                        self.oggetti.append(i)
                        self.centro.append([i.x-25,i.y-20])
                for i in sfere:
                    if i.tipo=="blu" and i.hit==0:
                        self.cord.append([i.x,i.y])
                        self.oggetti.append(i)
                        self.centro.append([i.x-25,i.y-20])
            if self.cord==[]:
                self.cord=[]
                self.oggetti=[]
                self.centro=[]
                self.tf=0
                self.ti=0
                animazione=False
            if self.cord!=[]:
                self.tf=time.time()
                if abs(self.ti-self.tf)<1.5:
                    for i in range (len(self.cord)):
                        A=25
                        w=15
                        t=time.time()
                        self.cord[i][1]=self.centro[i][1]+A*cos(w*t)
                    for i in self.cord:
                        schermo.blit(self.roller,(i[0]-25,i[1]))
                if abs(self.ti-self.tf)>1.5:
                    for i in sfere:
                        if i.tipo=="blu" and i.hit==0:
                            i.tipo="giallo"
                            i.sfera=i.sfera_gialla
                            i.sfera1=i.sfera1_gialla
                    for i in blocchi:
                        if i.tipo=="blu" and i.hit==0:
                            i.tipo="giallo"
                            i.block=i.block_giallo
                            i.block1=i.block1_giallo
                            
                    self.cord=[]
                    self.oggetti=[]
                    self.centro=[]
                    self.tf=0
                    self.ti=0
                    animazione=False
        return animazione
        

class Animazione_ufo():
    
    def __init__(self):
        self.image=pygame.image.load('immagini/arrow.png')
        self.image=pygame.transform.scale(self.image, (42, 180))
        self.utilizzato=False
        self.animazione=False
        self.prima=False
        self.ti=0
        self.tf=0
        
    def blit(self, palla):
        
        if self.animazione==True:
            if self.prima==False:
                self.ti=time.time()
                self.prima=True
            palla.acc=-470
            self.tf=time.time()
            if abs(self.tf-self.ti)>5:
                palla.acc=accelerazione
                #self.utilizzato=False
                self.animazione=False
                self.ti=0
                self.tf=0
                self.animazione=False
                self.prima=False
            for i in range(0,250*4,250):
                #print(i)
                schermo.blit(self.image,(200+i,200))
            
    def attivazione(self,pg1,pg2, turno, bol_potere):

        if self.utilizzato==False and turno==1 and pg1=="Ufo" and bol_potere==True:
            self.animazione=True
            self.utilizzato=True
        if self.utilizzato==False and turno==2 and pg2=="Ufo" and bol_potere==True:
            #print("eccomi")
            self.animazione=True
            self.utilizzato=True

class Animmazione_tiger():
    def __init__(self):
        self.attivo=False
    
    def blit(self,sfere, bol_potere,pg1,pg2,turno, lista,n_rossi):
        vero=False
        if bol_potere==True and turno==1 and pg1=="Tiger" and n_rossi!=0:
            vero=True
        if bol_potere==True and turno==2 and pg2=="Tiger" and n_rossi!=0:
            vero=True
        if vero==True:
            
            if self.attivo==False:
                self.attivo=True
                
                for i in range(0,6,1):
                    sfere.append(Peg(xb1+i*((xb2-xb1)/5),Y,"s",1,mov=0))
                
            cont=0
            numeri=[2500,5000,10000,5000,2500]
            for k in lista:
                text = font2.render(str(numeri[cont]), True, giallo)
                schermo.blit(text,k)
                cont=cont+1
    def punti_t(self,sfere,palla,turno,pg1,pg2,n_rossi):
        lista=[]
        punti=0
        vero=False
        for k in sfere:
            if k.festa==1:
                r=k.r
                lista.append(k.x)
        if n_rossi!=0 and turno==1 and pg1=="Tiger" and bol_potere==True:
            vero=True
        if n_rossi!=0 and turno==2 and pg2=="Tiger" and bol_potere==True:
            vero=True
        if vero==True:
            if xb1<=palla.centro[0]<lista[1]-r:
                punti=2500
            if lista[1]+r<=palla.centro[0]<lista[2]-r:
                punti=5000
            if lista[2]+r<=palla.centro[0]<lista[3]-r:
                punti=10000
            if lista[3]+r<=palla.centro[0]<lista[4]-r:
                punti=5000
            if lista[4]+r<=palla.centro[0]<=xb2:
                punti=2500
    #print(punti)        
        return punti
    def rimozione(self,sfere):
        bol=False
        i=0
        while i<len(sfere):

            if sfere[i].tipo=="s":
                sfere.remove(sfere[i])
                i=-1
            i=i+1
        self.attivo=False
        

class Animazione_Alien():
    def __init__(self):
        self.image=pygame.image.load('immagini/corona.png')
        self.x1=10
        self.image1=pygame.transform.scale(self.image, (self.x1, self.x1))
        self.utilizzato=False
        self.animazione=False
        self.centro=[]
        self.ti=0
        self.r=130
    def blit(self,palla,sfere,blocchi,molt,n_colpiti,n_rossi,somma, rosso_colpito,verde_colpito,cont_verde,potere1,potere2,pg1,pg2,turno):
        if self.animazione==True:
            if self.centro==[]:
                self.centro.append(palla.centro[0])
                self.centro.append(palla.centro[1])
                self.ti=time.time()
                colpiti=[]
                for i in sfere:
                    if i.hit==1:
                        continue
                    for punto in i.hitbox:
                        if dist(punto,self.centro)<=self.r:
                            k=sfere.index(i)
                            sfere[k].hit=1
                            colpiti.append(i)
                            break
                        
                for i in blocchi:
                    if i.hit==1 or i.mov==1:
                        continue
                    k=blocchi.index(i)
                    for j in i.hitbox:
                        if blocchi[k].hit==1:
                            break
                        for punto in j:
                            if dist(punto,self.centro)<=self.r:
                                
                                blocchi[k].hit=1
                                colpiti.append(i)
                                break
                            
                for i in colpiti:
                    if i.tipo=="blu":
                        punti=molt*punti_blu
                        somma=somma+punti
                        
                    if i.tipo=="rosso":
                        n_rossi=n_rossi-1
                        punti=molt*punti_rosso
                        somma=somma+punti
                        rosso_colpito=True
                    if i.tipo=="viola":
                        punti=molt*punti_viola
                        somma=somma+punti
                    if i.tipo=="verde":
                        cont_verde=cont_verde+1
                        potere1,potere2=aggiornamento_potere(turno, pg1, pg2, potere1, potere2)
                        verde_colpito=True
                if 15<=n_rossi<25:
                    molt=1
                if 10<=n_rossi<15:
                    molt=2
                if 6<=n_rossi<10:
                    molt=3
                if 3<=n_rossi<6:
                    molt=5
                if 1<=n_rossi<3:
                    molt=10
                n_colpiti=n_colpiti+len(colpiti)
            v=150
            tf=time.time()
            if self.x1<self.r:
                self.x1=int(self.x1+v*abs(tf-self.ti))
            else:
                self.animazione=False
            
            
            self.image1=pygame.transform.scale(self.image, (self.x1, self.x1))
            rect1=self.image1.get_rect()
            rect1.center=self.centro
            schermo.blit(self.image1,rect1)
            
        return somma,molt,n_rossi,n_colpiti,rosso_colpito,verde_colpito,cont_verde,potere1,potere2
            
        
    
    def attivazione(self,pg1,pg2, turno, bol_potere):

        if self.utilizzato==False and turno==1 and pg1=="Alien" and bol_potere==True:
            self.animazione=True
            self.utilizzato=True
        if self.utilizzato==False and turno==2 and pg2=="Alien" and bol_potere==True:
            #print("eccomi")
            self.animazione=True
            self.utilizzato=True
        

class Animazione_Horse():
    def __init__(self):
        self.attivo=False
        self.animazione=False
        self.sto_tirando=False
    def blit(self,palla):
        if self.animazione==True:
            palla.v=0
            palla.vx=0
            palla.vy=0
            palla.acc=0
            #print("sono qui")
            self.animazione=False
            self.sto_tirando=True
    def attivazione(self,blocco_c,turno,pg1,pg2,potere1,potere2):
        bol=False
        if potere1>0 and turno==1 and pg1=="Horse":
            bol=True
            #print("sono qui")
        if potere2>0 and turno==2 and pg2=="Horse":
            bol=True
            #print("eccomi")
        #print(blocco_c)
        if bol==True and blocco_c!=0 and self.attivo==False and self.animazione==False:
            #print("sono qui")
            
            self.attivo=True
            self.animazione=True
            
    def tiro(self,x,y,palla):
        if self.sto_tirando==True:
            self.sto_tirando=False
            m=(y-palla.centro[1])/(x-palla.centro[0])
            teta=arctan(m)
            #print(teta*180/pi)
            palla.v=700
            #palla.acc=accelerazione
            #print(palla.centro[1],y)
            if palla.centro[1]>y:
                if palla.centro[0]<x:
                    palla.vx=palla.v*cos(teta)
                if palla.centro[0]>x:
                    palla.vx=-palla.v*cos(teta)
                palla.vy=-abs(palla.v*sin(teta))
                #print(palla.vx,palla.vy)
            if palla.centro[1]<y:
                if palla.centro[0]<x:
                    palla.vx=palla.v*cos(teta)
                if palla.centro[0]>x:
                    palla.vx=-palla.v*cos(teta)
                palla.vy=abs(palla.v*sin(teta))
                #print(palla.vx,palla.vy)

class Animazione_Rocket():
    def __init__(self):
        self.attivo=False
        self.animazione=False
        self.ti=0

    def attivazione(self,bol_potere):
        
        if bol_potere==True and self.attivo==False and self.animazione==False:
            if self.ti==0:
                self.ti=time.time()
            
            self.animazione=True
            #print("sono qui")
            
                
    def blit(self,palla):
        if self.animazione==True and self.attivo==False:
            a=pygame.mouse.get_pressed(num_buttons=3)
            t2=time.time()
            if a[0]==True and abs(self.ti-t2)<4:
                x,y=pygame.mouse.get_pos()
                
                m=(y-palla.centro[1])/(x-palla.centro[0])
                teta=arctan(m)
                acc=600
                if palla.centro[1]>y:
                    if palla.centro[0]<x:
                        palla.accx=acc*cos(teta)
                    if palla.centro[0]>x:
                        palla.accx=-acc*cos(teta)
                    palla.accy=-abs(acc*sin(teta))
                    #print(palla.vx,palla.vy)
                if palla.centro[1]<y:
                    if palla.centro[0]<x:
                        palla.accx=acc*cos(teta)
                    if palla.centro[0]>x:
                        palla.accx=-acc*cos(teta)
                    palla.accy=abs(acc*sin(teta))
            else:
                palla.accx=0
                palla.accy=0
                self.attivo=True
                
class Animazione_Steroid():
    def __init__(self):
        self.attivo=False
    def blit(self,bol_potere,palla,pg1,turno,pg2):
        bol=False
        if self.attivo==False and bol_potere==True and palla.bol==1 and pg1=="Steroid" and turno==1:
            bol=True
        if self.attivo==False and bol_potere==True and palla.bol==1 and pg2=="Steroid" and turno==2:
            bol=True
        if bol==True:
            palla.dim_x=60
            palla.dim_y=60
            palla.r=palla.dim_x/2
            palla.ball=pygame.image.load('immagini/sphere-19.png')
            palla.ball=pygame.transform.scale(palla.ball, (palla.dim_x, palla.dim_y))
            self.attivo=True


class Animazione_Pot():

    def __init__(self):
        self.attivo=False
    def blit(self,bol_potere,cesto1,cesto2,pg1,pg2,turno):
        bol=False
        if self.attivo==False and bol_potere==True and pg1=="Pot" and turno==1 and palla.bol_cesto==0:
            bol=True
        if self.attivo==False and bol_potere==True and pg2=="Pot" and turno==2 and palla.bol_cesto==0:
            bol=True
        if bol==True:
            cesto1=Cesto(680,1)
            cesto2=Cesto(680,2)
            self.attivo=True
        return cesto1,cesto2



def scelta_nome():
    name[0]=entry1.get()
    name[1]=entry2.get()
    screen.destroy()
    #print("ciao")

nome1="player 1"
nome2="player 2"
name=[nome1,nome2]
screen=tk.Tk()
screen.title("My Peggle")
text=tk.Label(screen, text="Players' name")
text.grid(row=0,column=0, sticky="W",padx=20,pady=10)

entry1=tk.Entry(screen)# textvariable=entryL)
entry1.grid(row=1,column=0, sticky="W",padx=20,pady=10)

entry2=tk.Entry(screen)# textvariable=entryL)
entry2.grid(row=2,column=0, sticky="W",padx=20,pady=10)

scelta=tk.Button(text="Play", command=scelta_nome)
scelta.grid(row=3, column=0, sticky="WE", padx=10, pady=10)



tk.mainloop()

nome1=name[0]
nome2=name[1]

    

global X
global Y
global xb1
global xb2
global punti_blu
global punti_rosso
global punti_viola
global punti_giallo
global n_rossi_max
global punti_cesto
global accelerazione


X=1280
Y=720
xb1=40
xb2=1180
h=50
punti_blu=10
punti_giallo=30
punti_rosso=100
punti_viola=500
n_rossi_max=25
punti_cesto=2500
accelerazione=300
volume1=2
volume2=5
pygame.init()
#pygame.mixer.init()
#schermo=pygame.display.set_mode((X,Y))
schermo=pygame.display.set_mode((X,Y),pygame.FULLSCREEN)
clock = pygame.time.Clock()
font = pygame.font.Font("freesansbold.ttf", 20)

font2=pygame.font.Font("freesansbold.ttf", 28)
font3=pygame.font.Font("freesansbold.ttf", 44)
font4=pygame.font.Font("freesansbold.ttf", 250)
font5 = pygame.font.Font("freesansbold.ttf", 30)
font6=pygame.font.Font("freesansbold.ttf", 38)
font7=pygame.font.Font("freesansbold.ttf", 24)
do1=mixer.Sound("musica/note/do1.mp3")
re1=mixer.Sound("musica/note/re1.mp3")
mi1=mixer.Sound("musica/note/mi1.mp3")
fa1=mixer.Sound("musica/note/fa1.mp3")
sol1=mixer.Sound("musica/note/sol1.mp3")
la1=mixer.Sound("musica/note/la1.mp3")
si1=mixer.Sound("musica/note/si1.mp3")

do2=mixer.Sound("musica/note/do2.mp3")
re2=mixer.Sound("musica/note/re2.mp3")
mi2=mixer.Sound("musica/note/mi2.mp3")
fa2=mixer.Sound("musica/note/fa2.mp3")
sol2=mixer.Sound("musica/note/sol2.mp3")
la2=mixer.Sound("musica/note/la2.mp3")
si2=mixer.Sound("musica/note/si2.mp3")

do3=mixer.Sound("musica/note/do3.mp3")
re3=mixer.Sound("musica/note/re3.mp3")
mi3=mixer.Sound("musica/note/mi3.mp3")
fa3=mixer.Sound("musica/note/fa3.mp3")
sol3=mixer.Sound("musica/note/sol3.mp3")
la3=mixer.Sound("musica/note/la3.mp3")
si3=mixer.Sound("musica/note/si3.mp3")

do4=mixer.Sound("musica/note/do4.mp3")
re4=mixer.Sound("musica/note/re4.mp3")
mi4=mixer.Sound("musica/note/mi4.mp3")
fa4=mixer.Sound("musica/note/fa4.mp3")
sol4=mixer.Sound("musica/note/sol4.mp3")
la4=mixer.Sound("musica/note/la4.mp3")
si4=mixer.Sound("musica/note/si4.mp3")

note=[do1,re1,mi1,fa1,sol1,la1,si1,do2,re2,mi2,fa2,sol2,la2,si2,do3,re3,mi3,fa3,sol3,la3,si3,do4,re4,mi4,fa4,sol4,la4,si4]
beta=os.listdir("musica/")
for i in beta:
    if "mp3" not in i:
        beta.remove(i)
beta.remove("fever.mp3")
#print(musica)
bianco=(255,255,255)
nero=(0,0,0)
rosso=(255,0,0)
verde=(0,255,0)
blu=(0,0,255)
giallo=(229,191,1)

livello=1
mappa="cane"
n_palle=6
max_verdi=2
n_round=3
cont_round=1
punti_tot1=0
punti_tot2=0
mappe_random=False
run=True
while run==True:

    if livello==4:
        t1=time.time()
        pg1="Alien"
        pg2="Alien"
        #mappa="drago"
        punti1=0
        punti2=0
        cont_verde=0
        verde_colpito=False
        potere1=0
        potere2=0
        cesto1=0
        cesto2=0
        t1=0
        palle1=n_palle
        palle2=n_palle
        cont_note=0
        if pg1=="Crack-color":
            image1=pygame.image.load('immagini/poteri/girl.png')
        if pg2=="Crack-color":
            image2=pygame.image.load('immagini/poteri/girl.png')
        if pg1=="Painter":
            image1=pygame.image.load('immagini/poteri/imbianchino.png')
        if pg2=="Painter":
            image2=pygame.image.load('immagini/poteri/imbianchino.png')
        if pg1=="Ufo":
            image1=pygame.image.load('immagini/poteri/ufo.png')
        if pg2=="Ufo":
            image2=pygame.image.load('immagini/poteri/ufo.png')
        if pg1=="Tiger":
            image1=pygame.image.load('immagini/poteri/tiger.png')
        if pg2=="Tiger":
            image2=pygame.image.load('immagini/poteri/tiger.png')
        if pg1=="Alien":
            image1=pygame.image.load('immagini/poteri/alieno.png')
        if pg2=="Alien":
            image2=pygame.image.load('immagini/poteri/alieno.png')   
        if pg1=="Horse":
            image1=pygame.image.load('immagini/poteri/cavallo.png')
        if pg2=="Horse":
            image2=pygame.image.load('immagini/poteri/cavallo.png')
        if pg1=="Rocket":
            image1=pygame.image.load('immagini/poteri/razzo.png')
        if pg2=="Rocket":
            image2=pygame.image.load('immagini/poteri/razzo.png')
        if pg1=="Steroid":
            image1=pygame.image.load('immagini/poteri/pillole.png')
        if pg2=="Steroid":
            image2=pygame.image.load('immagini/poteri/pillole.png')
        if pg1=="Pot":
            image1=pygame.image.load('immagini/poteri/cesto.png')
        if pg2=="Pot":
            image2=pygame.image.load('immagini/poteri/cesto.png')

            
        oggetti=[]
        sfere=[]
        palla=Palla(h,accelerazione)
        cannone=Cannone()
        pannello=Pannello()
        targa=Traga(nome1,nome2)
        pannello_punti=Pannello_Punti()
        pannello_finale=Fine_partita(nome1, nome2, punti1, punti2)
        personaggio=Personaggio(image1,image2,pg1,pg2)
        animazione_re_color=Animazione_re_color()
        animazione_painter=Animazione_painter()
        animazione_ufo=Animazione_ufo()
        animazione_tiger=Animmazione_tiger()
        animazione_alien=Animazione_Alien()
        animazione_horse=Animazione_Horse()
        animazione_rocket=Animazione_Rocket()
        animazione_steroid=Animazione_Steroid()
        animazione_pot=Animazione_Pot()
        selezione_pg=Selezione_pg()
        menu_pausa=Menu_pausa()
        bottone_pausa=Bottone_pausa()
        url="mappe/"+mappa
        files=os.listdir(url)
        if "peg_arm.txt" in files:
            arm_peg=read_csv(url+"/peg_arm.txt",sep="\t")
            arm_peg=arm_peg.to_numpy()
            cont=0
            for i in range(len(arm_peg)):
                sfere.append(Peg_Armonico(arm_peg[cont,0],arm_peg[cont,1],arm_peg[cont,2],arm_peg[cont,3],arm_peg[cont,4],arm_peg[cont,5],arm_peg[cont,6],arm_peg[cont,7],arm_peg[cont,8]))
                cont=cont+1

        if "peg_statici.txt" in files:
            peg_statici=read_csv(url+"/peg_statici.txt",sep="\t")
            peg_statici=peg_statici.to_numpy()
            for i in range(len(peg_statici)):
                sfere.append(Peg(peg_statici[i,0],peg_statici[i,1],peg_statici[i,2],peg_statici[i,3],peg_statici[i,4]))
                
        if "blocchi_s.txt" in files:
            blocchi_s=read_csv(url+"/blocchi_s.txt",sep="\t")
            blocchi_s=blocchi_s.to_numpy()
            for i in range(len(blocchi_s)):
                oggetti.append(Blocco(blocchi_s[i,0],blocchi_s[i,1],blocchi_s[i,2],blocchi_s[i,3],blocchi_s[i,4]))
        if "peg_rot.txt" in files:
            peg_rot=read_csv(url+"/peg_rot.txt",sep="\t")
            peg_rot=peg_rot.to_numpy()
            for i in range(len(peg_rot)):
                sfere.append(Peg_Circolare(peg_rot[i,0],peg_rot[i,1],peg_rot[i,2],peg_rot[i,3],peg_rot[i,4],peg_rot[i,5],peg_rot[i,6],peg_rot[i,7]))
        if "blocchi_armonici.txt" in files:
            arm_peg=read_csv(url+"/blocchi_armonici.txt",sep="\t")
            arm_peg=arm_peg.to_numpy()
            for i in range(len(arm_peg)):
                oggetti.append(Blocco_armonico(arm_peg[i,0],arm_peg[i,1],arm_peg[i,2],arm_peg[i,3],arm_peg[i,4],arm_peg[i,5],arm_peg[i,6],arm_peg[i,7],arm_peg[i,8]))
        if "blocchi_c.txt" in files:
            arm_peg=read_csv(url+"/blocchi_c.txt",sep="\t")
            arm_peg=arm_peg.to_numpy()
            for i in range(len(arm_peg)):
                oggetti.append(Blocco_circolare(arm_peg[i,0],arm_peg[i,1],arm_peg[i,2],arm_peg[i,3],arm_peg[i,4],arm_peg[i,5],arm_peg[i,6],arm_peg[i,7]))
        if mappa=="castello con fulmini2":
            oggetti.append(Blocco_ostacolo(610,250,0,"blu",1,440,1,0,0))
            oggetti.append(Blocco_ostacolo(610,500,0,"blu",1,440,1,180,0))
            


        colorazione(sfere,oggetti)
        bordi=[]
        bordi.append(Bordo(xb1))
        bordi.append(Bordo(xb2))
        cesto=Cesto(680,0)
        verde_viola(oggetti, sfere,cont_verde,max_verdi)
        
        festa_estrema=[]
        fe_punti=[10000,25000,50000,25000,10000]
        for i in range(0,5,1):
            a=(xb2-xb1)/4
            festa_estrema.append((xb1+i*a,630))
        festa_estrema[0]=(xb1+80,630)
        festa_estrema[1]=(xb1+310,630)
        festa_estrema[2]=(xb1+535,630)
        festa_estrema[3]=(xb1+760,630)
        festa_estrema[4]=(xb1+980,630)

        n_rossi=0
        for i in sfere:
            if i.tipo=="rosso":
                n_rossi=n_rossi+1
        for i in oggetti:
            if i.tipo=="rosso":
                n_rossi=n_rossi+1
        #print(n_rossi)
        #n_rossi=n_rossi_max
        insieme_numeri=[]
        molt=1
        molt_cesto=1
        somma=0
        turno=1
        n_colpiti=0
        lista_rossi=[]
        rosso_colpito=False
        mostra_punti=False
        bol_tempo=False
        fine_partita=False
        bol_potere=False
        animazione=False
        scegliendo_pg=True
        pausa=False
        bol_musica=False
        url="immagini/scenari/"
        sfondo1=pygame.image.load(url+mappa+".png")
        sfondo1=pygame.transform.scale(sfondo1, (X-xb1-(X-xb2), Y-h))
        #musica[0].play(-1)


        #for i in range(0,360,20):
            #angoli.append(i)
            
        click=[]
        #print(len(oggetti)+len(sfere))
        t2=time.time()
        #print(t2-t1)
        i=randint(0,len(beta)-1)
        mixer.music.load("musica/"+beta[i])
        mixer.music.play(-1)
        mixer.music.set_volume(volume1/10)
        while livello==4:
            #print(palla.acc)
            clock.tick(60)
            fps = str(int(clock.get_fps()))
            #print(potere1)
            #print(fps)
            #peg_c=0
            #blocco_c=0
            acc=accelerazione
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    run=False
                    livello=-1
                #print(pygame.mouse.get_pressed(num_buttons=3))
                if pausa==True:
                    x,y=pygame.mouse.get_pos()
                    menu_pausa.passaggio(x,y)
                if scegliendo_pg==False and fine_partita==False:
                    x,y=pygame.mouse.get_pos()
                    bottone_pausa.passaggio(x,y)
                if scegliendo_pg==True:
                    x,y=pygame.mouse.get_pos()
                    selezione_pg.cambio_colore(x,y)
                if fine_partita==True:
                    #print("sono qui")
                    x,y=pygame.mouse.get_pos()
                    pannello_finale.passagio(x,y)
                animazione_rocket.blit(palla)
                if event.type==pygame.MOUSEBUTTONDOWN and animazione==False and palla.y<Y and palla.bol_cesto==0:
                    x,y=pygame.mouse.get_pos()
                    
                    if scegliendo_pg==True:
                        selezione_pg.cambio_colore(x,y)
                    if event.button==1 and scegliendo_pg==False and pausa==False:

                        if palla.bol==1:

                            animazione_ufo.attivazione(pg1, pg2, turno, bol_potere)
                            animazione_alien.attivazione(pg1, pg2, turno, bol_potere)
                            animazione_rocket.attivazione(bol_potere)
                        
                        animazione_horse.tiro(x, y, palla)
                        if y>palla.y and fine_partita==False and x>xb1:
                            b=[x,y]
                            if palla.bol==0 and turno==1:
                                palle1=palle1-1
                            if palla.bol==0 and turno==2:
                                palle2=palle2-1
                            palla.tiro(b,Y)
                        
                        pausa=bottone_pausa.click(x,y,pausa)
                    if event.button==1 and scegliendo_pg==True:
                        #print("sono qui")
                        selezione_pg.selezione(x,y)
                        scegliendo_pg, pg1,pg2,image1,image2=selezione_pg.click_play(x,y,scegliendo_pg,pg1,pg2)
                        if scegliendo_pg==False:
                            personaggio=Personaggio(image1,image2,pg1,pg2)
                    if event.button==1 and fine_partita==True:
                        cont_round,livello,punti_tot1,punti_tot2=pannello_finale.click_next(x,y,cont_round,livello,n_round,punti_tot1,punti_tot2,punti1,punti2)
                        livello=pannello_finale.click_quit(x,y,livello)
                    if event.button==1 and pausa==True and fine_partita==False and scegliendo_pg==False:
                        pausa=menu_pausa.click_resume(x,y,pausa)
                        livello=menu_pausa.click_menu(x,y,livello)
                        livello,run=menu_pausa.click_exit(x,y,livello,run)
                        
                    '''if event.button==3:
                        lista_rossi=blit_rossi(oggetti,sfere)'''

            schermo.fill(nero)
            schermo.blit(sfondo1,(xb1,h))
            #schermo.blit(scritta,(60,505))
            x,y=pygame.mouse.get_pos()
            cannone.movimento(x,y,palla)
            palla.rotazione(cannone)
            for sfera in sfere:
                sfera.colore()
            for oggetto in oggetti:
                oggetto.colore()
            if bol_tempo==False:
                palla.movimento(animazione)
                cesto.movimento()
                
                for sfera in sfere:
                    
                    if sfera.mov!=0:
                        if sfera.mov==1:
                            sfera.movimento_armonico()
                        if sfera.mov==2:
                            sfera.movimento_circolare()
                for blocco in oggetti:
                    if blocco.mov!=0:
                        if blocco.mov==1 or blocco.mov==2:
                            blocco.movimento_armonico()
                            blocco.movimento_armonico()
                        if blocco.mov==3:
                            blocco.movimento_circolare()

                        
                            
                            
            #palla.Hitbox()
            #pygame.draw.circle(schermo, rosso, (400,200), 120)
            blocco_c=palla.urto(oggetti)
            peg_c=palla.urto_palle(sfere)
            if n_rossi!=0 and animazione_tiger.attivo==False:
                palla.urto_cesto(cesto)
                if cesto1!=0 and cesto2!=0:
                    palla.urto_cesto(cesto1)
                    palla.urto_cesto(cesto2)
            palla.urto_laterale(h)
            somma,molt,n_rossi, numeri, rosso_colpito, cont_verde, potere1,potere2, verde_colpito=conteggio_punti(peg_c, blocco_c, sfere, oggetti,somma,molt,n_rossi, rosso_colpito, cont_verde,turno,potere1,potere2,verde_colpito)
            potere1,potere2,bol_potere,peg_colpiti,animazione=personaggio.re_color(potere1, potere2, bol_potere, oggetti, sfere, animazione)
            potere1,potere2,bol_potere,animazione=personaggio.poteri(potere1, potere2, bol_potere, animazione)
            potere1,potere2,bol_potere=personaggio.potere_ufo(potere1, potere2, bol_potere,verde_colpito)
            
            animazione_ufo.blit(palla)
            #print(molt,n_colpiti,n_rossi,somma)
            somma,molt,n_rossi,n_colpiti,rosso_colpito,verde_colpito,cont_verde,potere1,potere2=animazione_alien.blit(palla,sfere,oggetti,molt,n_colpiti,n_rossi,somma,rosso_colpito,verde_colpito,cont_verde,potere1,potere2,pg1,pg2,turno)
            blit_fe(n_rossi,festa_estrema,fe_punti)
            targa.blit(palle1,palle2,punti1,punti2)
            blit_nome(turno, nome1, nome2, h,bol_potere,pg1,pg2,potere1,potere2)
            personaggio.blit()
            cannone.blit()
            palla.blit()
            for oggetto in oggetti:
                oggetto.blit()
                if oggetto.n>10 and oggetto.mov!=1:
                    oggetti.remove(oggetto)
            #print(oggetti[0].n)
            for sfera in sfere:
                sfera.blit()
                if sfera.n>10:
                    sfere.remove(sfera)
            #for bordo in bordi:
                #bordo.blit(h)
            if n_rossi!=0 and animazione_tiger.attivo==False:
                cesto.blit()
                if cesto1!=0 and cesto2!=0:
                    cesto1.blit()
                    cesto2.blit()
            pannello.blit(n_rossi,molt)
            bottone_pausa.blit()
            insieme_numeri, n_colpiti,cont_note,t1=blit_punti(numeri, insieme_numeri,n_colpiti,somma,note,cont_note,t1,volume2)
            animazione=animazione_re_color.blit(peg_colpiti, oggetti, sfere, animazione, turno, pg1, pg2)
            animazione=animazione_painter.blit(animazione, sfere, oggetti, turno, pg1, pg2)
            animazione_tiger.blit(sfere, bol_potere, pg1, pg2, turno,festa_estrema,n_rossi)
            if peg_c!=0:
                blocco_c=peg_c 
            animazione_horse.attivazione(blocco_c, turno, pg1, pg2, potere1, potere2)
            animazione_horse.blit(palla)
            animazione_steroid.blit(bol_potere, palla,pg1,turno,pg2)
            cesto1,cesto2=animazione_pot.blit(bol_potere, cesto1, cesto2, pg1, pg2, turno)
            if scegliendo_pg==True:
                selezione_pg.blit()
            if pausa==True and fine_partita==False and scegliendo_pg==False:
                menu_pausa.blit(schermo)
            bol_musica=musica_festa(n_rossi,bol_musica,volume1)
            #punto=(sfere[10].rect.centerx,sfere[10].rect.centery)
            #schermo.fill(rosso,(punto,(4,4)))
            #print(sfere[10].vx,sfere[10].vy)
            #schermo.fill(rosso,((602,285),(4,4)))
            #schermo.fill(rosso,((651,406),(4,4)))
            
            '''for i in sfere:
                if i.tipo=="rosso":
                    schermo.fill(nero,(i.rect.center,(8,8)))
            for i in oggetti:
                if i.tipo=="rosso":
                    schermo.fill(nero,(i.centro,(8,8)))'''
            if palla.bol_cesto==1 and n_rossi!=0 and animazione_tiger.attivo==False:
                bonus2=0
                punti_assegnati=False
                
                if bol_tempo==False:
                    tempo=time.time()
                    bol_tempo=True
                    parz=0
                    punti_c=punti_cesto*molt_cesto
                    molt_cesto=molt_cesto+1
                    #print(punti_c)
                mostra_punti,parz=blit_punti_centro(somma, n_colpiti, punti_c,bonus2, tempo,parz,rosso_colpito,punti1,punti2,turno)
                if mostra_punti==True:
                    if turno==1:
                        if rosso_colpito==True:
                            punti1=punti1+somma*n_colpiti+punti_c
                        if rosso_colpito==False:
                            punti1=int(punti1-punti1*0.25)
                        turno=2
                        punti_assegnati=True
            
                    if turno==2 and punti_assegnati==False:
                        if rosso_colpito==True:
                            punti2=punti2+somma*n_colpiti+punti_c
                        if rosso_colpito==False:
                            punti2=int(punti2-punti2*0.25)
                        turno=1
            
                        punti_assegnati=True
                    palla=Palla(h,acc)
                    eliminazione(sfere, oggetti)
                    verde_viola(oggetti,sfere,cont_verde,max_verdi)
                    n_rossi=check_rossi(oggetti, sfere)
                    somma=0
                    n_colpiti=0
                    cesto1=0
                    cesto2=0
                    cont_note=0
                    t1=0
                    rosso_colpito=False
                    mostra_punti=False
                    bol_tempo=False
                    bol_potere=False
                    verde_colpito=False
                    animazione_ufo=Animazione_ufo()
                    animazione_alien=Animazione_Alien()
                    animazione_horse=Animazione_Horse()
                    animazione_rocket=Animazione_Rocket()
                    animazione_steroid=Animazione_Steroid()
                    animazione_pot=Animazione_Pot()
                    if palle1==0 and palle2==0:
                        fine_partita=True
                    if n_rossi==0:
                        fine_partita=True
                    continue
                
                
            if palla.y>Y:
                punti_assegnati=False
                punti_festa=punti_fe(n_rossi, palla, sfere)
                punti_tiger=animazione_tiger.punti_t(sfere, palla, turno, pg1, pg2, n_rossi)
                if bol_tempo==False:
                    tempo=time.time()
                    bol_tempo=True
                    parz=0
                mostra_punti,parz=blit_punti_centro(somma, n_colpiti, punti_festa,punti_tiger, tempo,parz, rosso_colpito,punti1,punti2,turno)

                if mostra_punti==True: 
                    #print("sono qui")
                    if turno==1:
                        if rosso_colpito==True:
                            punti1=punti1+somma*n_colpiti+punti_festa+punti_tiger
                        if rosso_colpito==False:
                            punti1=int(punti1-punti1*0.25)
                        turno=2
                        punti_assegnati=True
            
                    if turno==2 and punti_assegnati==False:
                        if rosso_colpito==True:
                            punti2=punti2+somma*n_colpiti+punti_festa+punti_tiger
                        if rosso_colpito==False:
                            punti2=int(punti2-punti2*0.25)
                        turno=1
                        punti_assegnati=True
                    
                    
                    #print(punti_festa)
                    palla=Palla(h,acc)
                    eliminazione(sfere, oggetti)
                    verde_viola(oggetti,sfere,cont_verde,max_verdi)
                    n_rossi=check_rossi(oggetti, sfere)
                    #print(n_rossi)
                    somma=0
                    n_colpiti=0
                    cesto1=0
                    cesto2=0
                    cont_note=0
                    t1=0
                    rosso_colpito=False
                    mostra_punti=False
                    bol_tempo=False
                    bol_potere=False
                    verde_colpito=False
                    animazione_ufo=Animazione_ufo()
                    animazione_tiger.rimozione(sfere)
                    animazione_alien=Animazione_Alien()
                    animazione_horse=Animazione_Horse()
                    animazione_rocket=Animazione_Rocket()
                    animazione_steroid=Animazione_Steroid()
                    animazione_pot=Animazione_Pot()
                    if palle1==0 and palle2==0:
                        fine_partita=True
                    if n_rossi==0:
                        fine_partita=True
                    
                    
            #print(fine_partita)
            
            if fine_partita==True:
                pannello_finale.blit(punti1,punti2,punti_tot1,punti_tot2,n_round,cont_round)
            
            
            aggiorna()
        

        


    if livello==3:
        bol=0
        selezione_mappa=Selezione_mappa()
        livello,mappa=selezione_mappa.selezione_random(livello,mappe_random,mappa)
        mixer.music.pause()
        while livello==3:
            clock.tick(60)
            fps = str(int(clock.get_fps()))
            
            for event in pygame.event.get():
                x,y=pygame.mouse.get_pos()
                selezione_mappa.passaggio(x,y)
                if event.type==pygame.QUIT:
                    run=False
                    livello=-1
            if event.type==pygame.MOUSEBUTTONDOWN and bol==0:

                if event.button==1:
                    selezione_mappa.cambio_pagina(x,y)
                    livello,mappa=selezione_mappa.selezione(x,y,livello)
                    livello=selezione_mappa.click_indietro(x,y,livello)
                    bol=1
                    #print("sono qui")
            if event.type==pygame.MOUSEBUTTONUP:
                #print("eccomi")
                bol=0
            selezione_mappa.blit(schermo)
            aggiorna()

    if livello==2 or livello==1:
        cont_round=1
        punti_tot1=0
        punti_tot2=0
        mixer.music.pause()
        menu_principale=Menu_principale()
        impostazioni=Impostazioni()
        while livello==1 or livello==2:
            for event in pygame.event.get():
                x,y=pygame.mouse.get_pos()
                if livello==1:
                    menu_principale.passaggio(x,y)
                if livello==2:
                    impostazioni.passaggio(x,y)
                if event.type==pygame.QUIT:
                    run=False
                    livello=-1
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if event.button==1 and livello==1:
                        livello,run=menu_principale.click(x,y,livello,run)
                    if event.button==1 and livello==2:
                        n_palle=impostazioni.click_palle(x,y,n_palle)
                        max_verdi=impostazioni.click_verde(x,y,max_verdi)
                        n_round=impostazioni.click_round(x,y,n_round)
                        mappe_random=impostazioni.click_mappe(x,y,mappe_random)
                        livello=impostazioni.click_play(x,y,livello)
                        livello=impostazioni.click_indietro(x,y,livello)
                        volume1=impostazioni.click_volume1(x,y,volume1)
                        volume2=impostazioni.click_volume2(x,y,volume2)
                        #print(volume1)
            menu_principale.blit(schermo)
            if livello==2:
                impostazioni.blit(schermo,n_palle,max_verdi,n_round,volume1,volume2)
            aggiorna()


pygame.quit()

