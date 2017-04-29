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
		if not start_x + sprememba > sirina-sirina_poti:
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
	def __init__(self, funkcija, x, y, active=True,w = 50, h = 50):
		super().__init__()
		self.funkcija = funkcija
		self.w = w
		self.h = h
		self.active = active

		self.image = pygame.Surface((self.w,self.h))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		#1 ---> AOE
		if funkcija == 1:
			self.image.fill((255,0,0))
		#2 ---> dmg
		if funkcija == 2:
			self.image.fill((0,0,255))
		#3 ---> slow
		if funkcija == 3:
			self.image.fill((0,255,0))
		#4 ---> ozadje menija
		if funkcija == 4:
			self.image.fill((100,100,100))
	def premik(self):
		if self.active:
			nov_x = pygame.mouse.get_pos()[0]
			nov_y = pygame.mouse.get_pos()[1]

			self.rect.x = nov_x - (self.w // 2)
			self.rect.y = nov_y - (self.h // 2)

stolpi = pygame.sprite.Group()
meni = turrets(4,0,0,225,75,)
#stolpi v meniju
AOE = turrets(1,0,0,False)
DMG = turrets(2,75,0,False)
SLOW = turrets(3,150,0,False)

stolpi.add(AOE)
stolpi.add(DMG)
stolpi.add(SLOW)

stolpi.add(meni)

#GLAVNA WHILE ZANKA
while delaj:
	ura.tick(60)
	for dogodek in pygame.event.get():
		if dogodek.type == pygame.QUIT:
			delaj = False
		if dogodek.type == pygame.MOUSEBUTTONUP:
			lokacija = pygame.mouse.get_pos()
			objekti = [i for i in stolpi if i.rect.collidepoint(lokacija)]
			if objekti != [] and objekti[0] == AOE:
				x = pygame.mouse.get_pos()[0]
				y = pygame.mouse.get_pos()[1]
				stolpi.add(turrets(1,x,y,True))
			if objekti != [] and objekti[0] == DMG:
				x = pygame.mouse.get_pos()[0]
				y = pygame.mouse.get_pos()[1]
				stolpi.add(turrets(2,x,y,True))
			if objekti != [] and objekti[0] == SLOW:
				x = pygame.mouse.get_pos()[0]
				y = pygame.mouse.get_pos()[1]
				stolpi.add(turrets(3,x,y,True))

	okno.fill((200,200,255))
	odseki.draw(okno)
	stolpi.draw(okno)
	pygame.display.flip()


pygame.quit()
