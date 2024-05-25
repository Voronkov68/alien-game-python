import pygame 
from  settings import Settings
class Ship():
	'''Класс для управление кораблем'''

	def __init__(self, screen):
		'''Инициализирует корабль и задает  его начальную позицию'''
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.settings = Settings()

		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)
		#Флаги перемещения
		self.moving_right = False 
		self.moving_left = False

	def update(self):
		'''Обновляет позицию коробля с учетом флага'''
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed

		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed


		self.rect.x = self.x



	def blitme(self):
		'''рисует корабль в текущей позиции'''
		self.screen.blit(self.image, self.rect)



	def center_ship(self):
		"""Размещает корабль в центе нижней стороны"""
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)