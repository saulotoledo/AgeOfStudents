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
import common, map, dialog, pygame
from os import path

class clGameControl(common.commonOperations):
	def __init__(self):
		self.menuItemsPos = {}
		self.__initPygameScreen__()
		self.map = map.clMap('main')
		self.__drawGameStartScreen__()
		self.started = False
		self.alreadyLost = False
		self.dialog = None # <- Nenhum dialogo em andamento
		self.dialogAdvance = 1
		self.unlockedByDialog = []
	
	def __initPygameScreen__(self):
		"""
		Inicializa a janela basica do jogo.
		"""
		self.__correctTileMultipleScreen__()
		
		# Inicializando o pygame e a screen
		pygame.init()
		gameIcon = pygame.image.load(self.configs['images_directory'] + self.configs['game_icon'])
		pygame.display.set_icon(gameIcon)
		pygame.display.set_caption(self.configs['game_title'])
		self.screen = pygame.display.set_mode(self.configs['screen_size'], 0)
		
	def __correctTileMultipleScreen__(self):
		"""
		Corrige 'screen_size' para que este seja multiplo de 'tile_size'.
		Isso evita preocupacoes gerais com tiles cortados em tela.
		"""
		coordX = self.configs['screen_size'][0]
		coordY = self.configs['screen_size'][1]
		if self.configs['screen_size'][0] / float(self.configs['tile_size'][0]) != self.configs['screen_size'][0] / self.configs['tile_size'][0]:
			coordX = self.configs['tile_size'][0] * (self.configs['screen_size'][0] / self.configs['tile_size'][0])
		if self.configs['screen_size'][1] / float(self.configs['tile_size'][1]) != self.configs['screen_size'][1] / self.configs['tile_size'][1]:
			coordY = self.configs['tile_size'][1] * (self.configs['screen_size'][1] / self.configs['tile_size'][1])
		if self.configs['screen_size'] != (coordX, coordY):
			self.setConfigs({'screen_size': (coordX, coordY)})
	
	def __returnTransparentTextImage__(self, listLines, font, textColor):
		"""
		Funcao usada para montar uma imagem com um texto de varias linhas e fundo transparente.
		"""
		# Se uma surface vazia nao for criada, o tamanho da surface sera o tamanho do primeiro blit,
		# portanto, ao blitar uma nova informacao abaixo, esta podera ser cortada por estar fora
		# da area da imagem original. Para resolver este problema, uma surface vazia eh criada a
		# partir de um arquivo transparente em disco.
		heightText = 0
		greaterWidth = 0
		for frase in listLines:
			line = font.render(frase, True, textColor)
			if heightText == 0:
				fullReturn = pygame.image.load(self.configs['images_directory'] + self.configs['transparent_image'])
			fullReturn.blit(line, (0, heightText))
			if line.get_size()[0] > greaterWidth:
				greaterWidth = line.get_size()[0]
			
			heightText += line.get_size()[1]
			
		return (greaterWidth, heightText, fullReturn)
	
	def __drawGameStartScreen__(self):
		
		imagemBG = pygame.image.load(self.configs['images_directory'] + self.configs['init_bg_image'])
		imagemBG = pygame.transform.scale(imagemBG, self.configs['screen_size'])
		self.screen.blit(imagemBG, (0,0))
		
		corTexto = (255,255,255)
		
		font = pygame.font.Font(self.configs['fonts_directory'] + self.configs['init_font_name'], 60)
		titulo = font.render(self.configs['game_title'], True, corTexto)
		
		# Centralizando o titulo na tela:
		self.screen.blit(titulo, ((self.configs['screen_size'][0] - titulo.get_size()[0]) / 2, 20))
		
		font = pygame.font.Font(self.configs['fonts_directory'] + self.configs['init_font_name'], 15)
		helpFont = pygame.font.Font(self.configs['fonts_directory'] + self.configs['dialog_font_name'], 15)

		greaterWidth, heightText, fullHelp = self.__returnTransparentTextImage__(self.configs['init_help_text'], helpFont, corTexto)
		self.screen.blit(fullHelp, (self.configs['screen_size'][0] - greaterWidth - 20, self.configs['screen_size'][1] - heightText - 20))
		greaterWidth, heightText, authorsInfo = self.__returnTransparentTextImage__(self.configs['init_authors_text'], helpFont, corTexto)
		self.screen.blit(authorsInfo, (20, self.configs['screen_size'][1] - heightText - 20))

		# Imprimindo o menu:
		menuItemsPos = {}
		
		posMenu = 250
		font = pygame.font.Font(self.configs['fonts_directory'] + self.configs['init_font_name'], 30)
		for item in self.configs['init_menu_itens']:
			itemMenu = font.render(item, True, corTexto)
			menuPosX = (self.configs['screen_size'][0] - itemMenu.get_size()[0]) / 2
			self.screen.blit(itemMenu, (menuPosX, posMenu))
			
			# Gravando a posicao no objeto para furura referencia (clique do mouse)
			# Sao gravados ((posicaoX, posicaoY), (altura, largura)) do item do menu
			self.menuItemsPos[item] = ((menuPosX, posMenu), itemMenu.get_size())
			
			posMenu += itemMenu.get_size()[1]
			
		pygame.display.update() #<- Desativar aqui se for ativar o mouseOver nos menus
		self.map.playMusic('menu')
		
	def mousePressedEvent(self, buttonName):
		if buttonName == 'Sair':
			exit()
		elif buttonName == 'Novo Jogo':
			print 'teste'
			self.started = True
			self.map.playMusic('game_map')
			self.map.drawMap()
			self.startDialog('Player')
			
	def startDialog(self, npcName):
		if npcName == 'Player':
			npcFaceFileName = self.configs['dialog_faces_directory'] + "Player_face.png"
		else:
			self.map.turnNPCToPlayer(npcName)
			npcFaceFileName = self.configs['dialog_faces_directory'] + path.basename(self.map.npcs[npcName]['image'][:-4] + "_face.png")
		
		
		if not path.exists(npcFaceFileName):
			npcFaceFileName = None
		self.dialog = dialog.clDialog(npcName, self.dialogAdvance, npcFaceFileName)
		for unlocked in self.dialog.unlockedByDialog:
			if not unlocked in self.unlockedByDialog:
				self.unlockedByDialog.append(unlocked)
		
	
	def verifyAction(self):
		# Aqui encontramos o tile que esta a frente do personagem e checamos se o que ha nele
		# eh um char ou qualquer outra coisa que dispare uma acao.
		tileInFrontOf = self.map.getNextTileCoord(self.map.player.lookingTo)
		
		# Checando se o char esta em frente ao portao:
		if (45,31) in self.map.level1['\xc3\xabc']:
			if self.map.player.lookingTo == 'down' and (self.map.playerPos == (46,30) or self.map.playerPos == (45,30)):
				
				if not "Chave Dourada" in self.map.player.bag:
					self.map.printPanelMessage("Est\xe1 fechado...")
				else:
					# Retirando o portao para colocar em nova posicao (aberto):
					self.map.level1['\xc3\xabc'].pop(self.map.level1['\xc3\xabc'].index((45,31)))
					self.map.level1['\xc3\xabc'].pop(self.map.level1['\xc3\xabc'].index((47,31)))
					self.map.level1['\xc3\xaba'].pop(self.map.level1['\xc3\xaba'].index((44,31)))
					self.map.level1['\xc3\xaba'].pop(self.map.level1['\xc3\xaba'].index((46,31)))
					self.map.preloadedLevel1Info.pop((44,31))
					self.map.preloadedLevel1Info.pop((45,31))
					self.map.preloadedLevel1Info.pop((46,31))
					self.map.preloadedLevel1Info.pop((47,31))
					
					# "Abrindo" o portao:
					self.map.level1['\xc3\xabc'].append((44,31))
					self.map.level1['\xc3\xabc'].append((48,31))
					self.map.level1['\xc3\xaba'].append((43,31))
					self.map.level1['\xc3\xaba'].append((47,31))
					self.map.preloadedLevel1Info[(43,31)] = '\xc3\xaba'
					self.map.preloadedLevel1Info[(44,31)] = '\xc3\xabc'
					self.map.preloadedLevel1Info[(47,31)] = '\xc3\xaba'
					self.map.preloadedLevel1Info[(48,31)] = '\xc3\xabc'
					
					self.map.drawMap()
					self.map.printPanelMessage("Voc\xea abriu o port\xe3o.")
		
		for objName in self.map.objects.keys():
			if tileInFrontOf == self.map.objects[objName]['pos']:
				if objName[:9] == 'trunk_box':
					unlockToCheck = 'trunk_box'
					message = "Uma caixa estranha..."
				else:
					unlockToCheck = 'trunk'
					message = "O que ser\xe1 que tem dentro?..."
					
				if unlockToCheck in self.unlockedByDialog:
					self.map.openBox(objName)
				else:
					self.map.printPanelMessage(message)
				
		for npcName in self.map.npcs.keys():
			if tileInFrontOf == self.map.npcs[npcName]['pos']:
				if npcName == 'Inseto Gigante':
					self.map.startBattle('queen', 1)
				else:
					if npcName[0:4] == 'Gato':
						self.playSound('cat')
					self.startDialog(npcName)
				break
		
	def won(self):
		self.started = False
		self.map.playMusic('won')
		font = pygame.font.Font("fonts/morpheus.ttf", 30)
		msgWon = font.render(self.configs['game_won_message'], True, (255,255,255))
		
		# Centralizando o titulo na tela:
		self.screen.fill((0,0,0))
		self.screen.blit(msgWon, ((self.configs['screen_size'][0] - msgWon.get_size()[0]) / 2, (self.configs['screen_size'][1] - msgWon.get_size()[1]) / 2))                                                                                                
		pygame.display.update()                                                                               
		pygame.time.wait(5000)                                                                                
		self.map.musics[self.map.playingMusic].fadeout(1000) #<- Eh preciso fazer aqui porque quando o __init__ for executado, a informacao de musica tocando eh perdida
		
		# Resetando para a tela de inicio:
		self.playerAdvance = 1
		
		self.__init__()
	
	def gameover(self):
		self.started = False
		self.alreadyLost = True
		self.map.playMusic('game_over')
		font = pygame.font.Font("fonts/liquidis.ttf", 60)
		msgLost = font.render(self.configs['game_over_message'], True, (255,255,255))
		
		# Centralizando o titulo na tela:
		self.screen.fill((0,0,0))
		self.screen.blit(msgLost, ((self.configs['screen_size'][0] - msgLost.get_size()[0]) / 2, (self.configs['screen_size'][1] - msgLost.get_size()[1]) / 2))
		pygame.display.update()
		pygame.time.wait(3000)
		self.map.musics[self.map.playingMusic].fadeout(1000) #<- Eh preciso fazer aqui porque quando o __init__ for executado, a informacao de musica tocando eh perdida
		
		# Resetando para a tela de inicio:
		self.playerAdvance = 1
		self.__init__()