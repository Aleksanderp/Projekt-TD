import pygame
from random import randint
from pygame.sprite import spritecollide as sc

pygame.init()
#dolocimo velikost igralnega okna
sirina = 800
visina = 800
denar = 800
delaj = True

#potem dodamo glede na meni !!!! ZA MAIN MENU
dificulty = 200

#seznam za preimkanje... elementi: smer in sprememba v tej smeri
vrstni_red = []

ura = pygame.time.Clock()
okno = pygame.display.set_mode([visina,sirina])


class pot(pygame.sprite.Sprite):
	def __init__(self, start, end, sirina, barva=(255,180,10)):
		super().__init__()
		self.zacetek = start
		self.konec = end
		self.sirina = sirina
		self.barva = barva

		dolzina = abs(self.zacetek[0]-self.konec[0])+self.sirina
		y_sirina = abs(self.zacetek[1]-self.konec[1])+self.sirina
		self.image = pygame.Surface((dolzina,y_sirina), pygame.SRCALPHA)

		y = min(self.zacetek[1], self.konec[1])-self.sirina//2
		x = min(self.zacetek[0], self.konec[0])-self.sirina//2
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
vrstni_red.append(("y",visina//20))
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
			vrstni_red.append(("x",sprememba))
		else:
			prvi = False
	if smer == 2 and drugi:
		sprememba = randint((visina//16),(visina//8))
		if not start_y - sprememba < sirina_poti :
			odseki.add(pot([start_x,start_y],[start_x,start_y-sprememba],sirina_poti))
			start_y -= sprememba
			vrstni_red.append(("y",sprememba))
		else:
			drugi = False

#DOVRŠITEV ZAKLJUČKA POTI (DO ROBA EKRANA)

if smer == 1:
	vrstni_red.append(("y",start_y - visina))
	odseki.add(pot([start_x,start_y],[start_x,start_y-(visina-start_y)],sirina_poti))
if smer == 2:
	odseki.add(pot([start_x,start_y],[start_x+(sirina-start_x),start_y],sirina_poti))
	vrstni_red.append(("x",sirina - start_x))
	

class turrets(pygame.sprite.Sprite):
	def __init__(self, funkcija, x, y, active="static", pot=None,
		stolpi = None, r = 25, cost = 0):
		super().__init__()
		self.cost = cost
		self.funkcija = funkcija
		self.r = r
		self.active = active
		self.pot = pot
		self.stolpi = stolpi
		##############################
				#1 ---> AOE
		if self.funkcija == 1:
			self.barva = (0,255,0)
			velikost = pygame.font.SysFont("comicsansms", 20)
			self.text = velikost.render("AOE", True, (0, 0, 0))

		#2 ---> dmg
		if self.funkcija == 2:
			self.barva = (255,0,0)
			velikost = pygame.font.SysFont("comicsansms", 20)
			self.text = velikost.render("DMG", True, (0, 0, 0))
		#3 ---> slow
		if self.funkcija == 3:
			self.barva = (0,0,255)
			velikost = pygame.font.SysFont("comicsansms", 20)
			self.text = velikost.render("SLOW", True, (0, 0, 0))
		#4 ---> money
		if self.funkcija == 4:
			self.barva = (200,200,255)
			velikost = pygame.font.SysFont("comicsansms", 20)
			self.text = velikost.render(str(denar), True, (255, 255, 255))
		#5 ---> smetnjak
		if self.funkcija == 5:
			self.barva = (10,10,10)
			velikost = pygame.font.SysFont("comicsansms", 16)
			self.text = velikost.render("TRASH", True, (255, 255, 255))
		####################################################3
		self.image = pygame.Surface((self.r*2,self.r*2),pygame.SRCALPHA)
		self.rect = self.image.get_rect()
		pygame.draw.circle(self.image,self.barva, (self.r,self.r),
							self.r,0)

		self.rect.x = x
		self.rect.y = y
	def update(self):
		global denar
		if self.active == "moving":
			x = pygame.mouse.get_pos()[0]
			y = pygame.mouse.get_pos()[1]
			self.rect.x = x - self.r
			self.rect.y = y - self.r
		if self.active == "tested":
			for dotikanje in sc(na_preverjanju,self.pot,False):
				if dotikanje != None:
					denar += na_preverjanju.cost
					na_preverjanju.kill()
					break
			else:
				for tower in sc(na_preverjanju,self.stolpi,False):
					if tower.active == "placed" or tower.active == "static":
						denar += na_preverjanju.cost
						na_preverjanju.kill()
						break
				else:
					self.active = "placed"
		#1 ---> AOE
		if self.funkcija == 1:
			self.image.blit(self.text, (self.r//5, self.r-10))
		#2 ---> dmg
		if self.funkcija == 2:
			self.image.blit(self.text, (self.r//5, self.r-10))
		#3 ---> slor
		if self.funkcija == 3:
			self.image.blit(self.text, (self.r//15, self.r-10))
		#4 ---> money
		if self.funkcija == 4:
			self.image.blit(self.text, (self.r//16,self.r-8))
		#5 ---> smetnjak
		if self.funkcija == 5:
			self.image.blit(self.text, (self.r//16,self.r-10))


stolpi = pygame.sprite.Group()
#ozadje menija
#meni = turrets(4,0,0,False,300,75)

#stolpi v meniju
AOE = turrets(1,0,0)
DMG = turrets(2,75,0)
SLOW = turrets(3,150,0)
smetnjak = turrets(5,225,0)
m_display = turrets(4,300,5)

#stolpi.add(meni)
stolpi.add(AOE)
stolpi.add(DMG)
stolpi.add(SLOW)
stolpi.add(smetnjak)
stolpi.add(m_display)

class enemy(pygame.sprite.Sprite):
	def __init__(self,idx,hp = 0, speed = 0, prostor = 0,x=sirina_poti,y=visina, barva=(255,255,255),
			r=10, hitrost = 0):
		super().__init__()
		self.idx = idx
		self.count = 0
		self.r = r
		self.prostor = vrstni_red[self.count][1]
		self.speed = speed
		self.hitrost = hitrost
		self.barva = barva
		#hiter, low hp
		if self.idx == 1:
			self.speed = 5
			self.hp = 10
			self.barva = (134,189,0)
		if self.idx == 2:
			self.speed = 2
			self.hp = 200
			self.barva = (45,189,97)
		if self.idx == 3:
			self.speed = 1
			self.hp = 500
			self.barva = (76,10,134)

		self.image = pygame.Surface((self.r*2,self.r*2),pygame.SRCALPHA)
		pygame.draw.circle(self.image, self.barva, [self.r, self.r], self.r, 0)
		self.rect = self.image.get_rect()
		self.rect.x = x - r
		self.rect.bottom = y + r
	def update(self):
		self.premik()
	def premik(self):
		global vrstni_red
		hitrost = self.speed
		while self.speed > 0:
			if vrstni_red[self.count][0] == "x":
				if self.prostor - self.speed >= 0:
					self.rect.x += self.speed
					self.prostor -= self.speed
					self.speed = 0
				else:
					self.rect.x += self.prostor
					self.speed -= self.prostor
					self.count += 1
					self.prostor = vrstni_red[self.count][1]
			elif vrstni_red[self.count][0] == "y":
				if self.prostor - self.speed >= 0:
					self.rect.y -= self.speed
					self.prostor -= self.speed
					self.speed = 0
				else:
					self.rect.y -= self.prostor
					self.speed -= self.prostor
					self.count += 1
					self.prostor = vrstni_red[self.count][1]
		self.speed = hitrost

napad = pygame.sprite.Group()
napad.add(enemy(3))

#GLAVNA WHILE ZANKA
#spremenljivka, da vemo kdaj z misko"drzimo" en stolp
attached = False
while delaj:
	ura.tick(30)
	for dogodek in pygame.event.get():
		if dogodek.type == pygame.QUIT:
			delaj = False
		if dogodek.type == pygame.MOUSEBUTTONDOWN:
			#ce smo z misko kliknili in drzimo stolp, ga zelimo postaviti
			if attached:
				#preverimo ce smo kliknili na smetnjak
				lokacija = pygame.mouse.get_pos()
				objekti = [i for i in stolpi if i.rect.collidepoint(lokacija)]
				if objekti != [] and smetnjak in objekti:
					attached = False
					zacasni.kill()
				#ce nismo ustvarimo turret, a ker se ne vemo ce je slucajno na poti ali na drugem turetu... :
				else:
					if denar - zacasni.cost >=  0:
						denar -= zacasni.cost
						na_preverjanju = turrets(zacasni.funkcija,zacasni.rect.x,zacasni.rect.y,
						"tested",pot=odseki,stolpi=stolpi,cost = zacasni.cost)
						stolpi.add(na_preverjanju)
			#ce z misko kliknemo na dolocen turret v meniju, 
			#bo ta seldil miski(zato self.active=True)
			if attached == False:
				lokacija = pygame.mouse.get_pos()
				objekti = [i for i in stolpi if i.rect.collidepoint(lokacija)]
				if objekti != [] and AOE in objekti:
					attached = True
					x = pygame.mouse.get_pos()[0]
					y = pygame.mouse.get_pos()[1]
					zacasni = turrets(1,x,y,"moving", cost = 50)
					stolpi.add(zacasni)
				elif objekti != [] and DMG in objekti:
					attached = True
					x = pygame.mouse.get_pos()[0]
					y = pygame.mouse.get_pos()[1]
					zacasni = turrets(2,x,y,"moving", cost = 100)
					stolpi.add(zacasni)
				elif objekti != [] and SLOW in objekti:
					attached = True
					x = pygame.mouse.get_pos()[0]
					y = pygame.mouse.get_pos()[1]
					zacasni = turrets(3,x,y,"moving", cost = 20)
					stolpi.add(zacasni)
	if randint(0,dificulty) == 1:
		napad.add(enemy(3))
	if randint(0,dificulty-dificulty//4) == 1:
		napad.add(enemy(1))
	if randint(0,dificulty*(dificulty//8)) == 1:
		napad.add(enemy(2))
	napad.update()
	stolpi.update()
	okno.fill((200,200,255))
	stolpi.draw(okno)
	odseki.draw(okno)
	napad.draw(okno)
	pygame.display.flip()


pygame.quit()






#PROBLEMI / NAPAKE
"""
-MENI ZA STOLPE: vcasih prekrije stolpe znotraj menija!
"""