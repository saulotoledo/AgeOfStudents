#Copyright (C) 2005 Free Software Foundation

#Age of Students is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.

#Age of Students is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with Age of Students; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# Setando o diretorio de modulos
import sys, pygame 
sys.path.append('./modules')

from gamecontrol import *
from pygame.locals import *

game = clGameControl()
clock = pygame.time.Clock()

while True:
	clock.tick(12)
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
	
	game.map.player.velocity = 400
	pressed_keys = pygame.key.get_pressed()
	if pressed_keys[K_RALT] or pressed_keys[K_LALT]:
		if pressed_keys[K_RETURN]:
			game.map.toggleFullscreen()
	if pressed_keys[K_ESCAPE]:
		if game.started:
			pygame.mixer.stop()
			game.__init__()
		else:
			exit()

	if not pygame.mixer.get_busy():
		game.map.playMusic(game.map.playingMusic)
	
	if not game.started:# and not game.alreadyWon and not game.alreadyLost:
		posMouse = pygame.mouse.get_pos()
		
		botaoAtivo = None
		for itemMenu in game.menuItemsPos.keys():
			# Checando se o mouse esta dentro de um retangulo de item de menu, em x e em y,
			# usando o atributo menuItemsPos definido apenas para isso:
			if posMouse[0] >= game.menuItemsPos[itemMenu][0][0] and posMouse[0] <= game.menuItemsPos[itemMenu][0][0] + game.menuItemsPos[itemMenu][1][0]:
				if posMouse[1] >= game.menuItemsPos[itemMenu][0][1] and posMouse[1] <= game.menuItemsPos[itemMenu][0][1] + game.menuItemsPos[itemMenu][1][1]:
					if botaoAtivo != itemMenu:
						botaoAtivo = itemMenu
				else:
					if botaoAtivo == itemMenu:
						botaoAtivo = None
			else:
				botaoAtivo = None
				
			
		if botaoAtivo != None:
			mousePressed = pygame.mouse.get_pressed()
			if mousePressed[0] == 1:
				game.mousePressedEvent(botaoAtivo)
			
			
	else:
		
		
		if game.map.battle != None:
			if game.map.battle.mode == 'ended':
				if game.map.battle.monsterName == 'queen':
					botaoAtivo = None
					mousePressed = (0,0,0)
					game.won()
				else:
					game.map.playMusic('game_map')
					game.map.battle = None
					game.map.drawPlayerPanel()
					pygame.display.update()
				
		if game.map.battle != None:
			if game.map.player.health <= 0:
				game.gameover()
			
			elif game.map.battle.mode == 'selecting_action' or game.map.battle.mode == 'selecting_target':
				if pressed_keys[K_UP]:
					game.map.battle.moveArrow('up')
				if pressed_keys[K_DOWN]:
					game.map.battle.moveArrow('down')
				if pressed_keys[K_RETURN] or pressed_keys[K_SPACE]:
					game.map.battle.selectOption()
					
		elif game.dialog != None:
			if pressed_keys[K_RETURN] or pressed_keys[K_SPACE]:
				game.dialog.advance()
				if game.dialog.talking == False:
					game.map.drawPlayerPanel()
					game.dialog = None
		else:
			clock = pygame.time.Clock()
			if pressed_keys[K_LSHIFT]:
				game.map.player.velocity = 800

			if pressed_keys[K_RETURN] or pressed_keys[K_SPACE]:
				game.verifyAction()
			if pressed_keys[K_UP]:
				game.map.movePlayer('up')
			if pressed_keys[K_DOWN]:
				game.map.movePlayer('down')
			if pressed_keys[K_LEFT]:
				game.map.movePlayer('left')
			if pressed_keys[K_RIGHT]:
				game.map.movePlayer('right')
