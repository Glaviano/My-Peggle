import pygame
import os
import random


def funzione(x,y,freccia_sx1,freccia_dx1,freccia_sx2,freccia_dx2,frecce2,cord2,dim_x1,dim_y1):
    frecce2[0]=freccia_sx1
    frecce2[1]=freccia_dx1
    for i in range(len(frecce2)):
        if cord2[i][0]<x<cord2[i][0]+dim_x1 and cord2[i][1]<y<cord2[i][1]+dim_y1:
            if i==0:
                frecce2[0]=freccia_sx2
            if i==1:
                frecce2[1]=freccia_dx2
    return frecce2

class Selezione_mappa():
    def __init__(self):
        X=1280
        Y=720
        self.pagina=0
        self.x1=0
        self.y1=0
        self.dim_x1=X
        self.dim_y1=Y
        self.pannello=pygame.image.load("immagini/bottoni/finestra.png")
        self.pannello=pygame.transform.scale(self.pannello, (self.dim_x1, self.dim_y1))
        self.scritta=pygame.image.load("immagini/bottoni/level_select.png")
        self.scritta=pygame.transform.scale(self.scritta, (327, 58))

        self.cord=[[90,180],[530,180],[980,180],[90,410],[530,410]]
        self.dim_x2=200
        self.dim_y2=200
        self.nomi_mappe=os.listdir("mappe/")
        self.im_mappe=[]
        for i in self.nomi_mappe:
            im=pygame.image.load("immagini/scenari/"+i+".png")
            im=pygame.transform.scale(im, (self.dim_x2, self.dim_y2))
            self.im_mappe.append(im)

        self.x5=980
        self.y5=410
        self.random=pygame.image.load("immagini/bottoni/blue_panel.png")
        self.random=pygame.transform.scale(self.random, (self.dim_x2,self.dim_y2))
        font5=pygame.font.Font("freesansbold.ttf", 46)
        self.text=font5.render("Random", True, giallo)

        self.dim_x3=53
        self.dim_y3=53
        self.x3=1100
        self.y3=619
        self.freccia_dx1=pygame.image.load("immagini/bottoni/freccia_dx_blu.png")
        self.freccia_dx1=pygame.transform.scale(self.freccia_dx1, (self.dim_x3,self.dim_y3))
        self.freccia_dx2=pygame.image.load("immagini/bottoni/freccia_dx_verde.png")
        self.freccia_dx2=pygame.transform.scale(self.freccia_dx2, (self.dim_x3,self.dim_y3))
        self.x4=1000
        self.y4=619
        self.freccia_sx1=pygame.image.load("immagini/bottoni/freccia_sx_blu.png")
        self.freccia_sx1=pygame.transform.scale(self.freccia_sx1, (self.dim_x3,self.dim_y3))
        self.freccia_sx2=pygame.image.load("immagini/bottoni/freccia_sx_verde.png")
        self.freccia_sx2=pygame.transform.scale(self.freccia_sx2, (self.dim_x3,self.dim_y3))
        self.freccia_dx=self.freccia_dx1
        self.freccia_sx=self.freccia_sx1

        self.x6=100
        self.y6=619
        self.dim_x6=53
        self.dim_y6=53
        self.indietro1=pygame.image.load("immagini/bottoni/indietro_blu.png")
        self.indietro1=pygame.transform.scale(self.indietro1, (self.dim_x6,self.dim_y6))
        self.indietro2=pygame.image.load("immagini/bottoni/indietro_verde.png")
        self.indietro2=pygame.transform.scale(self.indietro2, (self.dim_x6,self.dim_y6))
        self.indietro=self.indietro1
    
    def passaggio(self,x,y):
        if self.freccia_dx==self.freccia_dx2:
            self.freccia_dx=self.freccia_dx1
        if self.x3<x<self.x3+self.dim_x3 and self.y3<y<self.y3+self.dim_y3:
            self.freccia_dx=self.freccia_dx2

        if self.freccia_sx==self.freccia_sx2:
            self.freccia_sx=self.freccia_sx1
        if self.x4<x<self.x4+self.dim_x3 and self.y4<y<self.y4+self.dim_y3:
            self.freccia_sx=self.freccia_sx2
        
        if self.indietro==self.indietro2:
            self.indietro=self.indietro1
        if self.x6<x<self.x6+self.dim_x6 and self.y6<y<self.y6+self.dim_y6:
            self.indietro=self.indietro2

    def cambio_pagina(self,x,y):
        if self.pagina<3:
            if self.x3<x<self.x3+self.dim_x3 and self.y3<y<self.y3+self.dim_y3:
                self.pagina=self.pagina+1
        if self.pagina>0:
            if self.x4<x<self.x4+self.dim_x3 and self.y4<y<self.y4+self.dim_y3:
                self.pagina=self.pagina-1

    def selezione(self,x,y,livello):
        mappa=0
        for i in range(len(self.cord)):
            if self.cord[i][0]<x<self.cord[i][0]+self.dim_x2 and self.cord[i][1]<y<self.cord[i][1]+self.dim_y2:
                livello=livello+1
                mappa=self.nomi_mappe[i+5*self.pagina]
        if self.x5<x<self.x5+self.dim_x2 and self.y5<y<self.y5+self.dim_y2:
            livello=livello+1
            i=random.randint(0,len(self.nomi_mappe)-1)
            mappa=self.nomi_mappe[i]
        return livello,mappa
    
    def selezione_random(self,livello,mappe_random,mappa):
        if mappe_random==True:
            livello=livello+1
            i=random.randint(0,len(self.nomi_mappe)-1)
            mappa=self.nomi_mappe[i]
        return livello,mappa
    def click_indietro(self,x,y,livello):
        if self.x6<x<self.x6+self.dim_x6 and self.y6<y<self.y6+self.dim_y6:
            livello=livello-1

        return livello
    def blit(self,schermo):
        schermo.blit(self.pannello,(self.x1,self.y1))
        schermo.blit(self.scritta,(480,40))
        if self.pagina<3:
            schermo.blit(self.freccia_dx,(self.x3,self.y3))
        if self.pagina>0:
            schermo.blit(self.freccia_sx,(self.x4,self.y4))
        for i in range(len(self.cord)):
            schermo.blit(self.im_mappe[i+5*self.pagina],self.cord[i])
        schermo.blit(self.random,(self.x5,self.y5))
        schermo.blit(self.text,(self.x5+10,self.y5+81))
        schermo.blit(self.indietro,(self.x6,self.y6))

class Menu_principale():
    def __init__(self):
        self.sfondo=pygame.image.load("immagini/bottoni/sfondo.png")
        self.sfondo=pygame.transform.scale(self.sfondo, (1280, 720))
        self.dim_x=200
        self.dim_y=80
        self.im_bottoni=[]
        self.cord=[[50,400],[50,600]]
        self.bottone1=pygame.image.load("immagini/bottoni/bottone_rosso.png")
        self.bottone1=pygame.transform.scale(self.bottone1, (self.dim_x, self.dim_y))
        self.bottone2=pygame.image.load("immagini/bottoni/bottone_verde.png")
        self.bottone2=pygame.transform.scale(self.bottone2, (self.dim_x, self.dim_y))
        self.im_bottoni.append(self.bottone1)
        self.im_bottoni.append(self.bottone1)

        font5=pygame.font.Font("freesansbold.ttf", 50)
        text1=font5.render("Play", True, giallo)
        text2=font5.render("Quit", True, giallo)
        self.text=[text1,text2]

    
    def passaggio(self,x,y):
        if self.bottone2 in self.im_bottoni:
            var=self.im_bottoni.index(self.bottone2)
            self.im_bottoni[var]=self.bottone1
            
        for i in range(len(self.cord)):
            if self.cord[i][0]<x<self.cord[i][0]+self.dim_x and self.cord[i][1]<y<self.cord[i][1]+self.dim_y:
                self.im_bottoni[i]=self.bottone2
    
    def click(self,x,y,livello,run):
        for i in range(len(self.cord)):
            if self.cord[i][0]<x<self.cord[i][0]+self.dim_x and self.cord[i][1]<y<self.cord[i][1]+self.dim_y:
                if i==0:
                    livello=livello+1
                if i==1:
                    livello=-1
                    run=False
        return livello,run

    def blit(self,schermo):
        schermo.blit(self.sfondo,(0,0))
        for i in range(len(self.cord)):
            schermo.blit(self.im_bottoni[i],(self.cord[i][0],self.cord[i][1]))
            schermo.blit(self.text[i],(self.cord[i][0]+50,self.cord[i][1]+15))

class Impostazioni():
    def __init__(self):
        self.x1=300
        self.y1=100
        self.b=767
        self.h=670
        self.pannello=pygame.image.load("immagini/bottoni/finestra2.png")
        self.pannello=pygame.transform.scale(self.pannello, (self.b, self.h))
        font5=pygame.font.Font("freesansbold.ttf", 50)
        font6=pygame.font.Font("freesansbold.ttf", 50)
        text1=font5.render("Number of ball", True, bianco)
        text2=font5.render("Max green block", True, bianco)
        text3=font5.render("Number of round", True, bianco)
        text4=font5.render("Volume music", True, bianco)
        text5=font5.render("Random map", True, bianco)
        text6=font5.render("Volume effect", True, bianco)
        self.text=[text1,text2,text3,text4,text6,text5]
        self.cord_text=[]
        l=80
        y0=self.y1+100
        x0=self.x1+50
        for i in range(len(self.text)):
            if self.text[i]!=text5:
                self.cord_text.append([x0,y0+i*l])
            if self.text[i]==text5:
                self.cord_text.append([x0,y0+400])
        
        self.dim_x1=53
        self.dim_y1=53
        self.freccia_dx1=pygame.image.load("immagini/bottoni/freccia_dx_blu.png")
        self.freccia_dx1=pygame.transform.scale(self.freccia_dx1, (self.dim_x1,self.dim_y1))
        self.freccia_dx2=pygame.image.load("immagini/bottoni/freccia_dx_verde.png")
        self.freccia_dx2=pygame.transform.scale(self.freccia_dx2, (self.dim_x1,self.dim_y1))
        self.freccia_sx1=pygame.image.load("immagini/bottoni/freccia_sx_blu.png")
        self.freccia_sx1=pygame.transform.scale(self.freccia_sx1, (self.dim_x1,self.dim_y1))
        self.freccia_sx2=pygame.image.load("immagini/bottoni/freccia_sx_verde.png")
        self.freccia_sx2=pygame.transform.scale(self.freccia_sx2, (self.dim_x1,self.dim_y1))
        
        self.frecce2=[self.freccia_sx1,self.freccia_dx1]
        x2=780
        y2=self.cord_text[0][1]-10
        l=120
        self.cord2=[[x2,y2],[x2+l,y2]]
        self.font6=pygame.font.Font("freesansbold.ttf", 46)

        self.frecce3=[self.freccia_sx1,self.freccia_dx1]

        y2=self.cord_text[1][1]-10
        l=120
        self.cord3=[[x2,y2],[x2+l,y2]]
        
        self.frecce4=[self.freccia_sx1,self.freccia_dx1]

        y2=self.cord_text[2][1]-10
        l=120
        self.cord4=[[x2,y2],[x2+l,y2]]


        self.frecce5=[self.freccia_sx1,self.freccia_dx1]

        y2=self.cord_text[3][1]-10
        l=120
        self.cord5=[[x2,y2],[x2+l,y2]]


        self.frecce7=[self.freccia_sx1,self.freccia_dx1]

        y2=self.cord_text[4][1]-10
        l=120
        self.cord7=[[x2,y2],[x2+l,y2]]

        self.dim_x2=53
        self.dim_y2=53
        self.conferma1=pygame.image.load("immagini/bottoni/v_verde.png")
        self.conferma1=pygame.transform.scale(self.conferma1, (self.dim_x2,self.dim_y2))
        self.conferma2=pygame.image.load("immagini/bottoni/v_grigia.png")
        self.conferma2=pygame.transform.scale(self.conferma2, (self.dim_x2,self.dim_y2))
        self.negazione1=pygame.image.load("immagini/bottoni/x_verde.png")
        self.negazione1=pygame.transform.scale(self.negazione1, (self.dim_x2,self.dim_y2))
        self.negazione2=pygame.image.load("immagini/bottoni/x_grigia.png")
        self.negazione2=pygame.transform.scale(self.negazione2, (self.dim_x2,self.dim_y2))
        self.bottoni=[self.conferma2,self.negazione1]

        y2=self.cord_text[5][1]-10

        self.cord6=[[x2,y2],[x2+self.dim_x2,y2]]

        self.dim_x=200
        self.dim_y=60
        self.x3=self.x1+500
        self.y3=self.y1+10
        self.bottone1=pygame.image.load("immagini/bottoni/bottone_rosso.png")
        self.bottone1=pygame.transform.scale(self.bottone1, (self.dim_x, self.dim_y))
        self.bottone2=pygame.image.load("immagini/bottoni/bottone_verde.png")
        self.bottone2=pygame.transform.scale(self.bottone2, (self.dim_x, self.dim_y))
        self.play=self.bottone1
        font5=pygame.font.Font("freesansbold.ttf", 44)
        self.text_play=font5.render("Play", True, giallo)

        self.x4=self.x1+120
        self.y4=self.y1+10
        self.dim_x4=60
        self.dim_y4=60
        self.indietro1=pygame.image.load("immagini/bottoni/indietro_blu.png")
        self.indietro1=pygame.transform.scale(self.indietro1, (self.dim_x4,self.dim_y4))
        self.indietro2=pygame.image.load("immagini/bottoni/indietro_verde.png")
        self.indietro2=pygame.transform.scale(self.indietro2, (self.dim_x4,self.dim_y4))
        self.indietro=self.indietro1

    def passaggio(self,x,y):
        self.frecce2=funzione(x,y,self.freccia_sx1,self.freccia_dx1,self.freccia_sx2,self.freccia_dx2,self.frecce2,self.cord2,self.dim_x1,self.dim_y1)
        self.frecce3=funzione(x,y,self.freccia_sx1,self.freccia_dx1,self.freccia_sx2,self.freccia_dx2,self.frecce3,self.cord3,self.dim_x1,self.dim_y1)
        self.frecce4=funzione(x,y,self.freccia_sx1,self.freccia_dx1,self.freccia_sx2,self.freccia_dx2,self.frecce4,self.cord4,self.dim_x1,self.dim_y1)
        self.frecce5=funzione(x,y,self.freccia_sx1,self.freccia_dx1,self.freccia_sx2,self.freccia_dx2,self.frecce5,self.cord5,self.dim_x1,self.dim_y1)
        self.frecce7=funzione(x,y,self.freccia_sx1,self.freccia_dx1,self.freccia_sx2,self.freccia_dx2,self.frecce7,self.cord7,self.dim_x1,self.dim_y1)
        self.play=self.bottone1
        if self.x3<x<self.x3+self.dim_x and self.y3<y<self.y3+self.dim_y:
            self.play=self.bottone2
        self.indietro=self.indietro1
        if self.x4<x<self.x4+self.dim_x4 and self.y4<y<self.y4+self.dim_y4:
            self.indietro=self.indietro2
        
    def click_palle(self,x,y,n_palle):
    
        for i in range(len(self.frecce2)):
            if self.cord2[i][0]<x<self.cord2[i][0]+self.dim_x1 and self.cord2[i][1]<y<self.cord2[i][1]+self.dim_y1:
                if i==0 and n_palle>1:
                    n_palle=n_palle-1
                if i==1 and n_palle<10:
                    n_palle=n_palle+1
        return n_palle

    def click_verde(self,x,y,max_verdi):
        for i in range(len(self.frecce3)):
            if self.cord3[i][0]<x<self.cord3[i][0]+self.dim_x1 and self.cord3[i][1]<y<self.cord3[i][1]+self.dim_y1:
                if i==0 and max_verdi>0:
                    max_verdi=max_verdi-1
                if i==1 and max_verdi<10:
                    max_verdi=max_verdi+1
        return max_verdi

    def click_round(self,x,y,n_round):
        for i in range(len(self.frecce4)):
            if self.cord4[i][0]<x<self.cord4[i][0]+self.dim_x1 and self.cord4[i][1]<y<self.cord4[i][1]+self.dim_y1:
                if i==0 and n_round>1:
                    n_round=n_round-1
                if i==1 and n_round<10:
                    n_round=n_round+1
        return n_round

    def click_mappe(self,x,y,mappe_random):
        for i in range(len(self.frecce4)):
            if self.cord6[i][0]<x<self.cord6[i][0]+self.dim_x1 and self.cord6[i][1]<y<self.cord6[i][1]+self.dim_y1:
                if i==0:
                    mappe_random=True
                    self.bottoni=[self.conferma1,self.negazione2]
                if i==1:
                    mappe_random=False
                    self.bottoni=[self.conferma2,self.negazione1]
    
        return mappe_random

    
    def click_volume1(self,x,y,volume1):
        for i in range(len(self.frecce5)):
            if self.cord5[i][0]<x<self.cord5[i][0]+self.dim_x1 and self.cord5[i][1]<y<self.cord5[i][1]+self.dim_y1:
                if i==0 and volume1>0:
                    volume1=volume1-1
                if i==1 and volume1<10:
                    volume1=volume1+1
        return volume1
    
    def click_volume2(self,x,y,volume2):
        for i in range(len(self.frecce7)):
            if self.cord7[i][0]<x<self.cord7[i][0]+self.dim_x1 and self.cord7[i][1]<y<self.cord7[i][1]+self.dim_y1:
                if i==0 and volume2>0:
                    volume2=volume2-1
                if i==1 and volume2<10:
                    volume2=volume2+1
        return volume2

    def click_play(self,x,y,livello):
        if self.x3<x<self.x3+self.dim_x and self.y3<y<self.y3+self.dim_y:
            livello=livello+1
        return livello

    def click_indietro(self,x,y,livello):
        if self.x4<x<self.x4+self.dim_x4 and self.y4<y<self.y4+self.dim_y4:
            livello=livello-1
        return livello


    def blit(self,schermo,n_palle,max_verdi,n_round,volume1,volume2):
        schermo.blit(self.pannello,(self.x1,self.y1))
        for i in range((len(self.cord_text))):
            schermo.blit(self.text[i],(self.cord_text[i][0],self.cord_text[i][1]))
    
        text1=self.font6.render(str(n_palle), True, rosso)
        for i in range(len(self.cord2)):
            schermo.blit(self.frecce2[i],(self.cord2[i][0],self.cord2[i][1]))
        schermo.blit(text1,(self.cord2[0][0]+65,self.cord2[0][1]+10))

        text2=self.font6.render(str(max_verdi), True, rosso)
        for i in range(len(self.cord3)):
            schermo.blit(self.frecce3[i],(self.cord3[i][0],self.cord3[i][1]))
        schermo.blit(text2,(self.cord3[0][0]+65,self.cord3[0][1]+10))
        
        text3=self.font6.render(str(n_round), True, rosso)
        for i in range(len(self.cord4)):
            schermo.blit(self.frecce4[i],(self.cord4[i][0],self.cord4[i][1]))
        schermo.blit(text3,(self.cord4[0][0]+65,self.cord4[0][1]+10))

        text4=self.font6.render(str(int(volume1)), True, rosso)
        for i in range(len(self.cord5)):
            schermo.blit(self.frecce5[i],(self.cord5[i][0],self.cord5[i][1]))
        schermo.blit(text4,(self.cord5[0][0]+65,self.cord5[0][1]+10))

        text5=self.font6.render(str(int(volume2)), True, rosso)
        for i in range(len(self.cord7)):
            schermo.blit(self.frecce7[i],(self.cord7[i][0],self.cord7[i][1]))
        schermo.blit(text5,(self.cord5[0][0]+65,self.cord7[0][1]+10))

        for i in range(len(self.cord6)):
            schermo.blit(self.bottoni[i],(self.cord6[i][0],self.cord6[i][1]))

        schermo.blit(self.play,(self.x3,self.y3))
        schermo.blit(self.text_play,(self.x3+55,self.y3+8))

        schermo.blit(self.indietro,(self.x4,self.y4))

class Menu_pausa():
    def __init__(self):
        self.x1=450
        self.y1=120
        self.pannello=pygame.image.load("immagini/bottoni/pausa.png")
        #self.pannello=pygame.transform.scale(self.pannello, (self.b, self.h))
        self.dim_x=200
        self.dim_y=80
        self.bottone1=pygame.image.load("immagini/bottoni/bottone_rosso.png")
        self.bottone1=pygame.transform.scale(self.bottone1, (self.dim_x, self.dim_y))
        self.bottone2=pygame.image.load("immagini/bottoni/bottone_verde.png")
        self.bottone2=pygame.transform.scale(self.bottone2, (self.dim_x, self.dim_y))
        self.im_bottoni=[]
        self.im_bottoni.append(self.bottone1)
        self.im_bottoni.append(self.bottone1)
        self.im_bottoni.append(self.bottone1)
        self.x2=self.x1+80
        self.y2=self.y1+63
        self.cord=[]
        l=120
        for i in range(len(self.im_bottoni)):
            self.cord.append([self.x2,self.y2+l*i])

        font5=pygame.font.Font("freesansbold.ttf", 40)
        text1=font5.render("Resume", True, giallo)
        text2=font5.render("Menu", True, giallo)
        text3=font5.render("Exit", True, giallo)
        self.text=[text1,text2,text3]
    

    def passaggio(self,x,y):
        for i in range(len(self.cord)):
            self.im_bottoni[i]=self.bottone1
            if self.cord[i][0]<x<self.cord[i][0]+self.dim_x and self.cord[i][1]<y<self.cord[i][1]+ self.dim_y:
                self.im_bottoni[i]=self.bottone2

    def click_resume(self,x,y,pausa):
        if self.cord[0][0]<x<self.cord[0][0]+self.dim_x and self.cord[0][1]<y<self.cord[0][1]+ self.dim_y:
            pausa=False
        return pausa

    def click_menu(self,x,y,livello):
        if self.cord[1][0]<x<self.cord[1][0]+self.dim_x and self.cord[1][1]<y<self.cord[1][1]+ self.dim_y:
            livello=1
        return livello
    
    def click_exit(self,x,y,livello,run):
        if self.cord[2][0]<x<self.cord[2][0]+self.dim_x and self.cord[2][1]<y<self.cord[2][1]+ self.dim_y:
            livello=-1
            run=False
        return livello,run
    def blit(self,schermo):
        schermo.blit(self.pannello,(self.x1,self.y1))
        for i in range(len(self.im_bottoni)):
            schermo.blit(self.im_bottoni[i],(self.cord[i][0],self.cord[i][1]))
            schermo.blit(self.text[i],(self.cord[i][0]+35,self.cord[i][1]+15))

giallo=(229,191,1)
bianco=(255,255,255)
rosso=(255,0,0)
#print(pygame.font.get_fonts())