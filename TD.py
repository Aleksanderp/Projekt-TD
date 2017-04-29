import pygame
from random import randint


pygame.init()
#dolocimo velikost igralnega okna
sirina = 800
visina = 800
delaj = True
ura = pygame.time.Clock()
okno = pygame.display.set_mode([visina,sirina])


class pot(pygame.sprite.Sprite):
	def __init__(self, start, end, sirina, barva=(255,180,10)):
		super().__init__()
		self.zacetek = start
		self.konec = end
		self.sirina = sirina
		self.barva = barva

		dolzina = abs(self.zacetek[0]-self.konec[0])+self.sirina*4
		y_sirina = abs(self.zacetek[1]-self.konec[1])+ self.sirina*4
		self.image = pygame.Surface((dolzina,y_sirina),pygame.SRCALPHA)

		y = min(self.zacetek[1], self.konec[1])-self.sirina*2
		x = min(self.zacetek[0], self.konec[0])-self.sirina*2
		pygame.draw.line(self.image, self.barva, (self.zacetek[0]-x,self.zacetek[1]-y),
						(self.konec[0]-x, self.konec[1]-y), self.sirina)
		pygame.draw.circle(self.image,self.barva,(self.konec[0]-x,self.konec[1]-y),
							(self.sirina//2),0)

		self.rect = self.image.get_rect()
		self.rect.x = x 
		self.rect.y = y

odseki = pygame.sprite.Group()
#sirina poti
sirina_poti = sirina // 16

#VEDNO KRATEK PRVI ODSEK POTI
odseki.add(pot([sirina_poti,visina],[sirina_poti,visina-(visina // 20)],sirina_poti))

#spremenljivke za naslednjo "while" zanko

start_x = sirina_poti #gleda na prej dodani kratki zacetek
start_y = visina - (visina // 20) #gleda na prej dodani kratki zacetek
prvi = True
drugi = True

#USTVARJANJE POTI PO ODSEKIH (IZ LEVEGA SPODNJEGA V DESNI ZGORNJI KOT)
while prvi or drugi:
	#1 --> naslednji odsek gre naprej po X
	#2 --> naslednji odsek gre naprej po Y
	smer = randint(1,2)
	if smer == 1 and prvi:
		sprememba = randint((sirina/16),(sirina//8))
		if not start_x + sprememba > sirina:
			odseki.add(pot([start_x,start_y],[start_x+sprememba,start_y],sirina_poti))
			start_x += sprememba
		else:
			prvi = False
	if smer == 2 and drugi:
		sprememba = randint((visina//16),(visina//8))
		if not start_y - sprememba < sirina_poti :
			odseki.add(pot([start_x,start_y],[start_x,start_y-sprememba],sirina_poti))
			start_y -= sprememba
		else:
			drugi = False

#DOVRŠITEV ZAKLJUČKA POTI (DO ROBA EKRANA)
if smer == 1:
	odseki.add(pot([start_x,start_y],[start_x,start_y-(visina-start_y)],sirina_poti))
if smer == 2:
	odseki.add(pot([start_x,start_y],[start_x+(sirina-start_x),start_y],sirina_poti))
	

class turrets(pygame.sprite.Sprite):
	def __init__(self, funkcija, x, y, w = 50, h = 50):
		super().__init__()
		self.funkcija = funkcija
		self.w = w
		self.h = h

		self.image = pygame.Surface((self.w,self.h))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		#1 ---> AOE
		if funkcija == 1:
			self.image.fill((100,0,0))
		#2 ---> dmg
		if funkcija == 2:
			self.image.fill((0,0,100))
		#3 ---> slow
		if funkcija == 3:
			self.image.fill((0,100,0))
		#4 ---> ozadje menija
		if funkcija == 4:
			self.image.fill((100,100,100))

stolpi = pygame.sprite.Group()

#pozicije stolpov v meniju na x osi, Y JE PRI VSEH ENAK 0!!!
AOE = 0 #y = 0
DMG = 150 #y = 0
SLOW = 75 #y = 0

#stolpi v meniju
stolpi.add(turrets(1,AOE,0))
stolpi.add(turrets(2,DMG,0))
stolpi.add(turrets(3,SLOW,0))

#dodajanje ozadja menija
stolpi.add(turrets(4,0,0,225,75))


#GLAVNA WHILE ZANKA
while delaj:
	ura.tick(60)
	for dogodek in pygame.event.get():
		if dogodek.type == pygame.QUIT:
			delaj = False

	okno.fill((200,200,255))
	odseki.draw(okno)
	stolpi.draw(okno)
	pygame.display.flip()


pygame.quit()






































"""

import pygame
pygame.init()
#dolocimo velikost igralnega okna
sirina = 800
visina = 800
delaj = True
ura = pygame.time.Clock()
okno = pygame.display.set_mode([visina,sirina])


class pot(pygame.sprite.Sprite):
	def __init__(self, start, end, sirina=50, barva=(255,180,10)):
		super().__init__()
		self.zacetek = start
		self.konec = end
		self.sirina = sirina
		self.barva = barva

		dolzina = abs(self.zacetek[0]-self.konec[0])+self.sirina*4
		y_sirina = abs(self.zacetek[1]-self.konec[1])+ self.sirina*4
		self.image = pygame.Surface((dolzina,y_sirina),pygame.SRCALPHA)

		y = min(self.zacetek[1], self.konec[1])-self.sirina*2
		x = min(self.zacetek[0], self.konec[0])-self.sirina*2
		pygame.draw.line(self.image, self.barva, (self.zacetek[0]-x,self.zacetek[1]-y),
						(self.konec[0]-x, self.konec[1]-y), self.sirina)
		pygame.draw.circle(self.image,self.barva,(self.konec[0]-x,self.konec[1]-y),self.sirina//2,0)

		self.rect = self.image.get_rect()
		self.rect.x = x 
		self.rect.y = y

odseki = pygame.sprite.Group()

odseki.add(pot([50,800],[50,600]))
odseki.add(pot([50,600],[200,600]))
odseki.add(pot([200,600],[400,600]))
odseki.add(pot([400,600],[400,400]))
odseki.add(pot([400,400],[600,400]))
odseki.add(pot([600,400],[600,250]))
odseki.add(pot([600,250],[750,250]))
odseki.add(pot([750,250],[750,0]))

class turrets(pygame.sprite.Sprite):
	def __init__(self, funkcija, x, y, w = 50, h = 50):
		super().__init__()
		self.funkcija = funkcija
		self.w = w
		self.h = h

		self.image = pygame.Surface((self.w,self.h))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		#1 ---> AOE
		if funkcija == 1:
			self.image.fill((100,0,0))
		#2 ---> dmg
		if funkcija == 2:
			self.image.fill((0,0,100))
		#3 ---> slow
		if funkcija == 3:
			self.image.fill((0,100,0))

stolpi = pygame.sprite.Group()

stolpi.add(turrets(1,0,0))
stolpi.add(turrets(3,75,0))
stolpi.add(turrets(2,150,0))




while delaj:
	ura.tick(60)
	for dogodek in pygame.event.get():
		if dogodek.type == pygame.QUIT:
			delaj = False

	okno.fill((200,200,255))
	odseki.draw(okno)
	stolpi.draw(okno)
	pygame.display.flip()


pygame.quit()
"""