import sys
from time import sleep

import pygame 
from settings import  Settings  as s
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from scoreboard import Scoreboard



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


		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		self.ship = Ship(self)
		self.bullets =pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()


		self.play_button = Button(self, "ИГРАТЬ")
		self.shoot_sound = pygame.mixer.Sound('sounds/gun.mp3')

		self.game_over = False
		self.game_active = False
		


	def _check_events(self):
		'''Вспомогательный метод обрабатывает события'''
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					self._check_keydown_events(event)
					
				elif event.type == pygame.KEYUP:
					self._check_keyup_events(event)

				elif event.type == pygame.MOUSEBUTTONDOWN:
					mouse_pos = pygame.mouse.get_pos()
					self._check_play_button(mouse_pos)



	def _game_over(self):
		"""Отображает игровое окно завершения игры"""
		game_over_image = pygame.image.load('images/game_over.png')
		game_over_rect = game_over_image.get_rect()
		game_over_rect.center = self.screen.get_rect().center
		self.screen.blit(game_over_image, game_over_rect)
		


	def _check_play_button(self, mouse_pos):
		"""Запускает игру при  нажатии кнопки играть"""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if  button_clicked and not self.stats.game_active: 
			self.settings.initialize_dynamic_settings()
			self.stats.reset_stats()
			self.stats.game_active = True
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()
			

			self.aliens.empty()
			self.bullets.empty()

			self._create_fleet()
			self.ship.center_ship()
			pygame.mouse.set_visible(False)


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


	def _check_aliens_bottom(self):
		"""Проверяет добрались пришельцы до нижней части экрана"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				self._ship_hit()
				break

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
			self.shoot_sound.play()

	def _update_bullets(self):
		'''обновляет позицию снарядов'''
		self.bullets.update()
		for bullet in self.bullets.copy():
				if bullet.rect.bottom <= 0:
					self.bullets.remove(bullet)
		
		self._check__bullet_alien_collisions()

	def _check__bullet_alien_collisions(self):
		"""Обработка коллизий снарядов с пришельцами"""
		collisions = pygame.sprite.groupcollide (
				self.bullets, self.aliens, True, True)

		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.stats.score += self.settings.alien_points
			self.sb.prep_score()
			self.sb.check_high_score()
		if not self.aliens:
			self.settings.increase_speed()
			self.stats.level += 1
			self._create_fleet()

			self.stats.level += 1
			self.sb.prep_level()

	def _update_aliens(self):
		'''Обновление позиции всех пришельцев'''
		self._check_fleet_edges()
		self.aliens.update()

		if pygame.sprite.spritecollideany(self.ship, self.aliens):
				self._ship_hit()

		self._check_aliens_bottom()


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


	def _check_fleet_edges(self):
		'''Реагирует на достижение пришельцем края экрана'''
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break
	def check_high_score(self):
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.check_high_score()

	def _change_fleet_direction(self):
		'''Опускает весь флот и меняет направление флота'''
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1



	def _ship_hit(self):
		"""Обрабатывает столкновения корабля с пришельцем"""
		if self.stats.ships_left > 0:
			self.stats.ships_left -= 1
			self.sb.prep_ships()

		#Очистка списка пришельцев и снарядов"""
			self.aliens.empty()
			self.bullets.empty()

		#создание нового флота и размещение корабля в центре
			self._create_fleet()
			self.ship.center_ship()

			self.stats.level += 1
			self.sb.prep_level()

		#пауза
			sleep(0.5)
		else:
			self.stats.game_active = False
			self.game_over = True
			pygame.mouse.set_visible(True)


	def  _update_screen(self):
		'''Вспомогательный метод обновляет экран'''

		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)
		self.sb.show_score()



		if not self.stats.game_active:
			self.play_button.draw_button()


		pygame.display.flip()


	def run_game(self):
		'''Запуск игры'''
		try:	

			while True:
				self._check_events()

				if self.stats.game_active:
					self.ship.update()
					self._update_bullets()
					self._update_aliens()

				self._update_screen()
			
		except Exception as e:
				print(f"Error: {e}")
				sys.exit(1)
			

 		
			


if __name__ == '__main__':
	ai = AlienInvasion()
	ai.run_game()

