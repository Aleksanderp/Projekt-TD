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