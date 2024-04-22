import sys

import pygame 
from settings import  Settings  as s
from ship import Ship
from bullet import Bullet
from alien import Alien



class AlienInvasion:
	'''Класс для управления ресурсами  и поведением игры'''

	def __init__(self):
		'''Инициализирует игру и создает игровые ресурсы'''
		pygame.init()
		self.settings =  s()
		

		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.settings.screen_width =self.screen.get_rect().width
		self.settings.screen_height =self.screen.get_rect().height
		pygame.display.set_caption('Alien Invasion')

		
		self.ship = Ship(self.screen)
		self.bullets =pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()




	def _check_events(self):
		'''Вспомогательный метод обрабатывает события'''
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					self._check_keydown_events(event)
					
				elif event.type == pygame.KEYUP:
					self._check_keyup_events(event)


	def _check_keydown_events(self, event):
		'''реагирует на нажатие клавиш'''
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif  event.key == pygame.K_LEFT:
			self.ship.moving_left = True 
		elif event.key == pygame.K_ESCAPE:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

	def _check_keyup_events(self, event):
		'''реагирует на отпускание клавиш'''
		
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _fire_bullet(self):
		'''создание нового снаряда и включение его в группу bullets'''
		if len (self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		'''обновляет позицию снарядов'''
		self.bullets.update()
		for bullet in self.bullets.copy():
				if bullet.rect.bottom <= 0:
					self.bullets.remove(bullet)

	def _create_fleet(self):
		'''создание флота вторжения'''
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien_width = alien.rect.width
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height -
								(3 * alien_height) - ship_height)
		number_rows = available_space_y // (2 * alien_height)

		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)

			



	def _create_alien(self,  alien_number, row_number):
		'''Создание пришельца и размещение его в ряду'''
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y =alien.rect.height + 2 * alien.rect.height * row_number
		self.aliens.add(alien)






	def  _update_screen(self):
		'''Вспомогательный метод обновляет экран'''
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)
		pygame.display.flip()


	def run_game(self):
		'''Запуск игры'''
		while True:
			self._check_events()
			self.ship.update()
			self._update_bullets()
			self._update_screen()
			
			

 		
			


if __name__ == '__main__':
	ai = AlienInvasion()
	ai.run_game()

