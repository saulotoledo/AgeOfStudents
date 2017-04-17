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
import pygame, common, player
from random import randint

class clBattle(common.commonOperations):
	def __init__(self, monsterName, numMonsters, battlePlace, player):
		self.screen = pygame.display.get_surface()
		self.battlePlace = battlePlace
		self.monsterName = monsterName
		self.numMonsters = numMonsters
		self.monsters = {}
		self.player = player
		self.arrowInfo = {'coords': (-1, -1), 'image': pygame.image.load(self.configs['images_directory'] + self.configs['battle_arrow_image'])}
		self.mode = None
		self.actionSelected = None
		self.whoAttacksNow = ['player', 'computer'][randint(0,1)]
		self.mapScreen = self.screen.copy()
		
		if not "Espada" in self.player.battleOptions and "Espada" in self.player.bag:
			self.player.battleOptions.append("Espada")
		if not "Machado" in self.player.battleOptions and "Machado" in self.player.bag:
			self.player.battleOptions.append("Machado")
		if self.player.potions > 0:
			if not "Usar Po\xe7\xe3o" in self.player.battleOptions:
				self.player.battleOptions.append("Usar Po\xe7\xe3o")
		
		for i in range(2):
			self.screen.fill((0,0,0))
			pygame.display.update()
			pygame.time.wait(self.configs['battle_wait_time'])
			self.screen.blit(self.mapScreen, (0,0))
			pygame.display.update()
			pygame.time.wait(self.configs['battle_wait_time'])
			
		self.drawBattleScreen(battlePlace)
	
	def drawBattleScreen(self, battlePlace):
		imageBG = pygame.image.load(self.configs['images_directory'] + 'backgrounds/battle_' + battlePlace + '.png')
		imageBG = pygame.transform.scale(imageBG, self.configs['screen_size'])
		self.screen.blit(imageBG, (0,0))
		self.__loadMonsters__()
		self.printPanelMessage("Voc\xea est\xe1 sendo atacado por mosquitos!")
		self.nextTurn()
		pygame.display.update()
		
	def __drawBattlePanel__(self):
		panelBG = pygame.image.load(self.configs['images_directory'] + 'backgrounds/panel_background.png')
		panelPosYBlit = self.configs['screen_size'][1] - self.configs['panel_height']
		for i in range(self.configs['screen_size'][0] / panelBG.get_size()[0] + 1): #+1 para o caso de dar quebrado como 1.xxx o valor do resultado e, ao arredondar, ir para baixo
			self.screen.blit(panelBG, (i*panelBG.get_size()[0], panelPosYBlit))
		
	def __loadMonsters__(self):
		monsterImage = pygame.image.load(self.configs['images_directory'] + 'monsters/' + self.monsterName + '.png')
		monsterImageSize = monsterImage.get_size()
		firstMonsterX = self.configs['screen_size'][0]/2 - (self.numMonsters * monsterImageSize[0]/2)
		monsterY = (self.configs['screen_size'][1] - self.configs['panel_height'])/2 - monsterImageSize[1]/2
		
		if len(self.monsters.keys()) != 0:
			for monster in self.monsters.keys():
				if self.monsters[monster]['health'] <= 0:
					self.monsters.pop(monster)
				else:
					self.screen.blit(monsterImage, (self.monsters[monster]['posX'], monsterY))
		else:
			 
			for i in range(self.numMonsters):
				monsterX = firstMonsterX + i*monsterImageSize[0]
				if self.monsterName != 'queen':
					stats = {'health': 10, 'hit': 1, 'flee_percent': 1, 'armor': 3, 'posX': monsterX, 'golpes': {'Picada': {'miss': 40, 'hit': 1}, 'Picada forte': {'miss': 40, 'hit': 3}}}
				else:
					stats = {'health': 100, 'hit': 10, 'flee_percent': 1, 'armor': 15, 'posX': monsterX, 'golpes': {'Picada dolorosa': {'miss': 20, 'hit': 10}}}
				self.monsters[self.monsterName + ' ' + str(i+1)] = stats 
				self.screen.blit(monsterImage, (monsterX, monsterY))
	
	def __drawPanelArrowSelect__(self, arrowSize = None):
		if arrowSize != None:
			self.arrowInfo['size'] = arrowSize
		arrowImage = pygame.transform.scale(self.arrowInfo['image'], self.arrowInfo['size'])
		if self.arrowInfo['coords'] == (-1, -1):
			self.arrowInfo['coords'] = (20 - arrowImage.get_size()[0] - 4, self.configs['screen_size'][1] - self.configs['panel_height'] + 5)
			self.arrowInfo['selected_option'] = 0
		self.arrowInfo['surface_with_no_arrow'] = self.screen.copy()
		
		self.screen.blit(arrowImage,self.arrowInfo['coords'])
	
	def moveArrow(self, to):
		self.screen.blit(self.arrowInfo['surface_with_no_arrow'], self.arrowInfo['coords'], (self.arrowInfo['coords'][0], self.arrowInfo['coords'][1], self.arrowInfo['size'][0], self.arrowInfo['size'][1]))
		self.playSound('menu_select')
		
		if to == 'up':
			if self.arrowInfo['selected_option'] == 0:
				self.arrowInfo['selected_option'] = len(self.displayOptions) - 1
				self.arrowInfo['coords'] = (self.arrowInfo['coords'][0], self.arrowInfo['coords'][1] + (len(self.displayOptions) - 1) * self.arrowInfo['size'][1])
			else:
				self.arrowInfo['selected_option'] -= 1
				self.arrowInfo['coords'] = (self.arrowInfo['coords'][0], self.arrowInfo['coords'][1] - self.arrowInfo['size'][1])
				
		if to == 'down':
			if self.arrowInfo['selected_option'] == len(self.displayOptions) - 1:
				self.arrowInfo['selected_option'] = 0
				self.arrowInfo['coords'] = (self.arrowInfo['coords'][0], self.arrowInfo['coords'][1] - (len(self.displayOptions) - 1) * self.arrowInfo['size'][1])
			else:
				self.arrowInfo['selected_option'] += 1
				self.arrowInfo['coords'] = (self.arrowInfo['coords'][0], self.arrowInfo['coords'][1] + self.arrowInfo['size'][1])
				
				
		
		self.__drawPanelArrowSelect__()
		pygame.display.update()
		# Pequeno atraso para evitar que tudo aconteca rapido demais:
		pygame.time.wait(150)
		
	def selectOption(self):
		self.playSound('menu_select')
		if self.mode == 'selecting_action':
			self.actionSelected = self.displayOptions[self.arrowInfo['selected_option']]
			if not self.actionSelected == "Usar Po\xe7\xe3o":
				self.mode = 'selecting_target'
				self.arrowInfo['selected_option'] = 0
				self.arrowInfo['coords'] = (-1, -1)
			else:
				self.playAnimation(self.actionSelected, None)
				healthPrev = self.player.health 
				self.player.health += self.configs['battle_potion_recover']
				if self.player.health > self.configs['player_max_health']:
					self.player.health = self.configs['player_max_health']
				self.player.potions -= 1
				if self.player.potions <= 0:
					# Retirando da lista de golpes
					self.player.battleOptions.pop(self.player.battleOptions.index(self.actionSelected))
				
				self.printPanelMessage("Recuperou " + str(self.player.health - healthPrev) + " pontos de vida.")
			
				
				
				self.arrowInfo['selected_option'] = 0
				self.arrowInfo['coords'] = (-1, -1)
				if self.mode != 'ended':
					self.nextTurn()
		elif self.mode == 'selecting_target':
			self.__attack__()
			self.arrowInfo['selected_option'] = 0
			self.arrowInfo['coords'] = (-1, -1)
			
		if self.mode != 'ended':
			self.__drawBattlePanel__()
			self.__loadPlayerPanelInfo__()
			pygame.display.update()
		
			# Pequeno atraso para evitar que tudo aconteca rapido demais:
			pygame.time.wait(150)
			
	def playAnimation(self, actionName, target = None):
		
		frameSize = 192
		animImage = pygame.image.load(self.configs['images_directory'] + self.configs['battle_animations_directory'] + self.configs['battle_action_animations'][actionName])
		animImageSize = animImage.get_size()
		numFramesX = animImageSize[0]/frameSize
		numFramesY = animImageSize[1]/frameSize
		imgWithNoAnimation = self.screen.copy()
		if target == None:
			if actionName == 'Usar Po\xe7\xe3o':
				posAnimX = self.configs['screen_size'][0] - frameSize
				posAnimY = self.configs['screen_size'][1] - self.configs['panel_height'] - frameSize/2
			else:
				posAnimX = self.configs['screen_size'][0]/2 - frameSize/2
				posAnimY = (self.configs['screen_size'][1] - self.configs['panel_height'])/2 - frameSize/2
		else:
			posAnimX = self.monsters[target]['posX'] - 40
			posAnimY = (self.configs['screen_size'][1] - self.configs['panel_height'])/2 - frameSize/2
		
		self.playSound(actionName)
		for i in range(numFramesY):
			for j in range(numFramesX):
				imageRect = (j * frameSize, i * frameSize, frameSize, frameSize)
				self.screen.blit(animImage, (posAnimX, posAnimY), imageRect)
				pygame.display.update()
				pygame.time.wait(50)
				self.screen.blit(imgWithNoAnimation, (0,0))
	
	def __attack__(self):
		atackedMonster = self.monsters.keys()[self.arrowInfo['selected_option']]
		miss = False
		percent = self.monsters[atackedMonster]['flee_percent'] + self.player.useBattleOptions[self.actionSelected]['miss']
		if randint(1, 100) <= percent and randint(1, 100) <= percent:
			miss = True
			self.playSound('miss')
			self.printPanelMessage('O mosquito escapou do ataque.')
			if self.mode != 'ended':
				self.nextTurn()
		else:
			self.playAnimation(self.actionSelected, atackedMonster)
			hitValue = self.player.useBattleOptions[self.actionSelected]['hit'] - randint(0, self.monsters[atackedMonster]['armor'])
			if hitValue < 0:
				hitValue = 0
			#hitValue = 200 #<- Para facilitar os testes
			self.monsters[atackedMonster]['health'] -= hitValue

			self.printPanelMessage('Causou um dano de ' + str(hitValue) + ' pontos.')
			if self.monsters[atackedMonster]['health'] <= 0:
				self.printPanelMessage('Um inimigo foi derrotado.')
				self.numMonsters -= 1

				if self.numMonsters <= 0:
					self.end()
				if self.mode != 'ended':
					self.drawBattleScreen(self.battlePlace)
			else:
				self.nextTurn()
				
	def monsterAttack(self, monsterName):
		if monsterName == 'hornet':
			atkName = 'Picada'
		else:
			atkName = 'Picada dolorosa'
		self.playAnimation(atkName, None)
		playerArmor = self.player.armor
		if "Armadura" in self.player.bag:
			playerArmor += 8
                        
		hitValue = self.monsters[self.monsters.keys()[0]]['hit'] - randint(0, playerArmor)
		if hitValue < 0:
			hitValue = 0
		if hitValue == 0:
			self.printPanelMessage("O mosquito errou.")
		else:
			self.printPanelMessage("O mosquito atacou com \""+ atkName +"\" e causou um dano de " + str(hitValue) + " pontos.")
		self.player.health -= hitValue
	
	def __loadPlayerPanelInfo__(self):
		if self.mode == None:
			self.mode = 'selecting_action'
		if self.mode == 'selecting_action':
			self.displayOptions = self.player.battleOptions
		elif self.mode == 'selecting_target':
			self.displayOptions = []
			for monster in self.monsters.keys():
				self.displayOptions.append(monster)
		
		optionPos = (21, self.configs['screen_size'][1] - self.configs['panel_height'] + 6)
		lifeInfoPos = (self.configs['screen_size'][0], optionPos[1]) 
		textFont = pygame.font.Font(self.configs['fonts_directory'] + self.configs['dialog_font_name'], 14)
		for stroke in self.displayOptions:
			textRendered = textFont.render(stroke, True, (0,0,0))
			textHeight = textRendered.get_size()[1]
			self.screen.blit(textRendered, optionPos)
			
			textRendered = textFont.render(stroke, True, (255,255,255))
			optionPos = (optionPos[0]-1, optionPos[1]-1)
			self.screen.blit(textRendered, optionPos)
			
			optionPos = (optionPos[0]+1, optionPos[1]+textHeight+1)
			
		# Imprimindo vida:
		lifeInfoText = self.configs['battle_life_info_label'] + str(self.player.health)
		textRendered = textFont.render(lifeInfoText, True, (0,0,0))
		lifeInfoWidth = textRendered.get_size()[0]
		lifeInfoPos = (lifeInfoPos[0] - lifeInfoWidth - 9, lifeInfoPos[1])
		self.screen.blit(textRendered, lifeInfoPos)
		
		textRendered = textFont.render(lifeInfoText, True, (255,255,255))
		lifeInfoPos = (lifeInfoPos[0] - 1, lifeInfoPos[1] - 1)
		self.screen.blit(textRendered, lifeInfoPos)
		
		# Imprimindo quantidade de potions:
		if self.player.potions > 0:
			potsInfoText = self.configs['battle_potions_info_label'] + str(self.player.potions)
			textRendered = textFont.render(potsInfoText, True, (0,0,0))
			potsInfoWidth = textRendered.get_size()[0]
			potsInfoPos = (lifeInfoPos[0], lifeInfoPos[1] + textRendered.get_size()[1])
			self.screen.blit(textRendered, potsInfoPos)
			
			textRendered = textFont.render(potsInfoText, True, (255,255,255))
			potsInfoPos = (potsInfoPos[0] - 1, potsInfoPos[1] - 1)
			self.screen.blit(textRendered, potsInfoPos)
		
			
		textSizeReference = textFont.render('O', False, (0,0,0)).get_size()
		self.__drawPanelArrowSelect__(textSizeReference)

		
	def nextTurn(self):
		if self.numMonsters > 0:
			if self.whoAttacksNow == 'player':
				self.printPanelMessage('Sua vez.')
				self.__drawBattlePanel__()
				self.__loadPlayerPanelInfo__()
				self.whoAttacksNow = 'computer'
				
			elif self.whoAttacksNow == 'computer':
				self.printPanelMessage('Vez dos inimigos.')
				for i in range(len(self.monsters)):
					self.printPanelMessage('O mosquito ataca.')
					self.monsterAttack(self.monsterName)		
				self.whoAttacksNow = 'player'
				self.nextTurn()
			
		
	
	def printPanelMessage(self, message):
		self.mode = None
		self.__drawBattlePanel__()
		textFont = pygame.font.Font(self.configs['fonts_directory'] + self.configs['dialog_font_name'], 20)
		textRendered = textFont.render(message, True, (0,0,0))
		
		messagePos = (21, self.configs['screen_size'][1] - self.configs['panel_height'] + 6)
		self.screen.blit(textRendered, messagePos)
		
		textRendered = textFont.render(message, True, (255,255,255))
		messagePos = (messagePos[0] - 1, messagePos[1] - 1)
		self.screen.blit(textRendered, messagePos)
		
		pygame.display.update()
		pygame.time.wait(1000)
		
	def end(self):
		self.screen.fill((0,0,0))
		self.screen.blit(self.mapScreen, (0,0))
		self.mode = 'ended'
		pygame.display.update()
		
