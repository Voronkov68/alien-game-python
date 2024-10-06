class GameOverScreen:

	def __init__(self, ai_game):

		self.ai_game = ai_game
 		self.screen = ai_game.screen
		self.game_over_text = ai_game.font.render("Game Over", True, (255, 255, 255))
		self.try_again_text = ai_game.font.render("Try Again", True, (255, 255, 255))
		self.try_again_button = pygame.Rect(100, 100, 200, 50)

	def draw(self):
		self.screen.fill((0, 0, 0))
		self.screen.blit(self.game_over_text, (100, 100))
		self.screen.blit(self.try_again_text, (100, 200))
		pygame.draw.rect(self.screen, (255, 255, 255), self.try_again_button)
