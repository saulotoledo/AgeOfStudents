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

import common, player, battle, pygame
from random import randint

class clMap(common.commonOperations):
	"""
	Classe basica de controle de mapas, responsavel pelos desenhos em tela.
	"""
	def __init__(self, mapName):
		"""
		Inicializacao basica de um mapa. Carrega o arquivo de mapas para seu uso.
		
		@param mapName: O nome do mapa a ser carregado (deve ser o nome do arquivo em disco sem a extensao).
		"""
		self.playerPos = self.configs['player_start_pos']
		self.ground = []
		self.level1 = {}
		self.npcs = {}
		self.objects = {}
		self.images = {}
		self.loadedGraphics = {}

		self.player = player.clPlayer()
		self.screen = pygame.display.get_surface()
		mapFile = open(self.configs['maps_directory'] + mapName + self.configs['map_file_type'])
		self.battle = None
		
		linhaLevel1Checking = 0
		self.preloadedLevel1Info = {} #<- Para evitar loops grandes que causam lentidao em "canMoveTo"
		for linha in mapFile:
			linha = linha.strip()
			if linha != '':
				if linha[0] == ':':
					loadingInfo = linha[1:]
					continue
				if loadingInfo == 'GROUND':
					self.ground.append(linha.split(' '))
				elif loadingInfo == 'LEVEL1':
					
					linhaLevel1 = linha.split(' ')
					for i in range(0, len(linhaLevel1)):
						if linhaLevel1[i] != '--':
							if not self.level1.has_key(linhaLevel1[i]):
								self.level1[linhaLevel1[i]] = []
							self.level1[linhaLevel1[i]].append((i, linhaLevel1Checking))
							self.preloadedLevel1Info[(i, linhaLevel1Checking)] = linhaLevel1[i]
					linhaLevel1Checking += 1
					
				elif loadingInfo == 'NPCPOS':
					npcInfo = linha.split(':')
					npcInfo[0] = npcInfo[0].strip()
					
					npcConfigs = npcInfo[1].split(',')
					npcCoords = tuple(npcConfigs[1].strip(' ()').split(';'))
					npcCoords = (int(npcCoords[0]), int(npcCoords[1]))
					npcLookingTo = npcConfigs[2].strip()
					
					if not self.npcs.has_key(npcInfo[0]):
						self.npcs[npcInfo[0]] = {}
					self.npcs[npcInfo[0]]['image'] = npcConfigs[0].strip()
					self.npcs[npcInfo[0]]['pos'] = npcCoords
					self.npcs[npcInfo[0]]['lookingTo'] = npcLookingTo
				
				elif loadingInfo == 'OBJECTS':
					objInfo = linha.split(':')
					objInfo[0] = objInfo[0].strip()
					
					objConfigs = objInfo[1].split(',')
					objCoords = tuple(objConfigs[1].strip(' ()').split(';'))
					objCoords = (int(objCoords[0]), int(objCoords[1]))
					objInside = objConfigs[2].strip()
					
					if not self.objects.has_key(objInfo[0]):
						self.objects[objInfo[0]] = {}
					self.objects[objInfo[0]]['image'] = objConfigs[0].strip()
					self.objects[objInfo[0]]['pos'] = objCoords
					self.objects[objInfo[0]]['has'] = objInside
					self.objects[objInfo[0]]['tile'] = (0,0)
					
				elif loadingInfo == 'IMGDEF':
					imgInfo = linha.split(':')
					imgInfo[0] = imgInfo[0].strip()
					
					imgConfigs = imgInfo[1].split(',')
					imgPath = imgConfigs[0].strip()
					imgProperties = imgConfigs[1].strip(' []').split(';')
					
					imgCoordsIntoFile = tuple(imgConfigs[2].strip(' ()').split(';'))
					imgCoordsIntoFile = (int(imgCoordsIntoFile[0]), int(imgCoordsIntoFile[1]))
					
					if not self.images.has_key(imgInfo[0]):
						self.images[imgInfo[0]] = {}
					self.images[imgInfo[0]]['image'] = imgPath
					self.images[imgInfo[0]]['tile'] = imgCoordsIntoFile
					self.images[imgInfo[0]]['options'] = imgProperties
					
		self.__preloadSounds__()
	
	def __submapToPrint__(self):
		"""
		Retorna o submapa a ser impresso na tela.
		"""
		submapX = 0
		submapY = 0
		lenX, lenY = self.__returnLenScreen__()
		if self.playerPos[0] > (lenX -1): #-1 para o primeiro ser 0
			submapX = self.playerPos[0] / (lenX)
		if self.playerPos[1] > (lenY -1): #-1 para o primeiro ser 0
			submapY = self.playerPos[1] / (lenY)
		return (submapX, submapY)
		
	def __returnLenScreen__(self):
		"""
		Retorna a quantidade de tiles em X e em Y que cabem na configuracao atual de tela.
		"""
		return ((self.configs['screen_size'][0] / self.configs['tile_size'][0]), ((self.configs['screen_size'][1] / self.configs['tile_size'][1]) - (self.configs['panel_height'] / self.configs['tile_size'][1])))
	
	def __getTileRect__(self, tileCoords):
		"""
		Retorna como Rect as coordenadas do tile na imagem carregadas do mapa.
		O formato retornado eh (PixelInicialX, PixelInicialY, lenX, lenY). 
		"""
		return (tileCoords[0]*self.configs['tile_size'][0], tileCoords[1]*self.configs['tile_size'][1], self.configs['tile_size'][0], self.configs['tile_size'][1])
		
	def __getPlayerPixelCoords__(self):
		"""
		Retorna as coordenadas do player em pixels e relativas aos cantos da tela.  
		
		Para a impressao do player na tela, coordenadas em pixels da posicao do player devem ser retornadas.
		Se o player estiver em um submapa diferente de (0,0) (o primeiro submapa, superior esquerdo), estas
		coordenadas em pixeis devem ser relativas ao canto da tela, caso contrario a impressao do desenho
		sera feita fora das areas visiveis da tela.
		"""
		return self.__getPixelCoords__(self.playerPos)
		
	def __getPixelCoords__(self, pos):
		lenX, lenY = self.__returnLenScreen__()
		coordX = (pos[0] - ((pos[0] / lenX) * lenX)) * self.configs['tile_size'][0]
		coordY = (pos[1] - ((pos[1] / lenY) * lenY)) * self.configs['tile_size'][1]
		return (coordX, coordY)
		
	def getNextTileCoord(self, to):
		if to == 'up':
			return (self.playerPos[0], self.playerPos[1]-1)
		elif to == 'down':
			return (self.playerPos[0], self.playerPos[1]+1)
		elif to == 'left':
			return (self.playerPos[0]-1, self.playerPos[1])
		elif to == 'right':
			return (self.playerPos[0]+1, self.playerPos[1])
		return None
		
	def __preloadImages__(self):
		"""
		Pre-carrega as imagens para evitar carregar a mesma imagem varias vezes
		"""
		self.preloadedImages = {}
		imagesList = []
		for tilesName in self.images.keys():
			if not self.images[tilesName]['image'] in imagesList:
				imagesList.append(self.images[tilesName]['image'])
		for npcName in self.npcs.keys():
			if not self.npcs[npcName]['image'] in imagesList:
				imagesList.append(self.npcs[npcName]['image'])
		for objName in self.objects.keys():
			if not self.objects[objName]['image'] in imagesList:
				imagesList.append(self.objects[objName]['image'])
				
		for img in imagesList:
			self.preloadedImages[img] = pygame.image.load(self.configs['images_directory'] + img)
	
	def drawMap(self):
		"""
		Desenha o mapa baseado na posicao do player.
		"""
		self.__preloadImages__()
		lenX, lenY = self.__returnLenScreen__()
		submapToPrint = self.__submapToPrint__()
				
		# Limpa a tela:
		self.screen.fill((0,0,0))
		
		for y in range(0 + (submapToPrint[1] * lenY), (1 + submapToPrint[1]) * lenY):
			for x in range(0 + (submapToPrint[0] * lenX), (1 + submapToPrint[0]) * lenX):
				self.drawGround(x, y)
				self.drawLevel1(x, y)
				
		self.drawNPCs()
		self.drawObjects()
		self.drawPlayerPanel()
		self.drawPlayer(self.player.lookingTo)
		#pygame.display.update()
		

	def drawGround(self, TileX, TileY):
		if len(self.ground) > TileY:
			if len(self.ground[TileY]) > TileX:
				groundTile = self.ground[TileY][TileX]
			else:
				groundTile = '\xc3\xaa3'
		else:
			groundTile = '\xc3\xaa3'
		
		lenX, lenY = self.__returnLenScreen__()
		image = self.preloadedImages[self.images[groundTile]['image']]
		tileCoordsOnScreen = ((TileX - (TileX / lenX) * lenX)*self.configs['tile_size'][0], (TileY - (TileY / lenY) * lenY)*self.configs['tile_size'][1])
		tileRect = self.__getTileRect__(self.images[groundTile]['tile'])
		self.screen.blit(image, tileCoordsOnScreen, tileRect)
			
				
	def drawLevel1(self, TileX, TileY):
		if len(self.ground) > TileY:
			if len(self.ground[TileY]) > TileX:
				for tileName in self.level1.keys():
					if (TileX, TileY) in self.level1[tileName]:
						lenX, lenY = self.__returnLenScreen__()
						tileCoordsOnScreen = ((TileX - (TileX / lenX) * lenX)*self.configs['tile_size'][0], (TileY - (TileY / lenY) * lenY)*self.configs['tile_size'][1])
						image = self.preloadedImages[self.images[tileName]['image']]
						tileRect = self.__getTileRect__(self.images[tileName]['tile'])
						self.screen.blit(image, tileCoordsOnScreen, tileRect)
						break
				


		
	def canMoveTo(self, TileX, TileY):
		# Bloqueando os limites do mapa:
		if TileX < 0 or TileY < 0 or TileX >= len(self.ground[0]) or TileY >= len(self.ground):
			return False
		
		# Verificando tiles bloqueados em "ground":
		grounTile = self.ground[TileY][TileX]
		if 'blocked' in self.images[grounTile]['options']:
			return False
		
		# Verificando tiles bloqueados em level1:
		if (TileX, TileY) in self.preloadedLevel1Info.keys():
			tileName = self.preloadedLevel1Info[(TileX, TileY)]
			if 'blocked' in self.images[tileName]['options']:
				return False
		
		
		objPositions = []
		for objName in self.objects.keys():
			objPositions.append(self.objects[objName]['pos'])
		if (TileX, TileY) in objPositions:
			return False
		
		npcPositions = []
		for npcName in self.npcs.keys():
			npcPositions.append(self.npcs[npcName]['pos'])
		if (TileX, TileY) in npcPositions:
			return False
			
		return True
		
	
	def __drawNPC__(self, npcName, lookingTo):
		npcCoords = self.npcs[npcName]['pos']
		image = self.preloadedImages[self.npcs[npcName]['image']]
		npcCoordsOnScreen = self.__getPixelCoords__(npcCoords)
		npcRect = self.__getTileRect__(self.player.getImageCoord(lookingTo, 1)) #<- Para nao reescrever a mesma funcao, aproveitamos a do player
		self.screen.blit(image, npcCoordsOnScreen, npcRect)
	
	def drawNPCs(self):
		lenX, lenY = self.__returnLenScreen__()
		submap = self.__submapToPrint__()
		for npcName in self.npcs.keys():
			if self.npcs[npcName]['pos'][0] / lenX == submap[0] and self.npcs[npcName]['pos'][1] / lenY == submap[1]:
				self.__drawNPC__(npcName, self.npcs[npcName]['lookingTo'])
	
	def __drawObject__(self, objName):
		objCoords = self.objects[objName]['pos']
		image = self.preloadedImages[self.objects[objName]['image']]
		objCoordsOnScreen = self.__getPixelCoords__(objCoords)
		objRect = self.__getTileRect__(self.objects[objName]['tile'])
		self.screen.blit(image, objCoordsOnScreen, objRect)
		
	def drawObjects(self):
		lenX, lenY = self.__returnLenScreen__()
		submap = self.__submapToPrint__()
		for objName in self.objects.keys():
			if self.objects[objName]['pos'][0] / lenX == submap[0] and self.objects[objName]['pos'][1] / lenY == submap[1]:
				self.__drawObject__(objName)
	
	def printPanelMessage(self, message):
		screenCopy = self.screen.copy()
		self.__drawPanelBackground__()
		
		textFont = pygame.font.Font(self.configs['fonts_directory'] + self.configs['dialog_font_name'], 20)
		textRendered = textFont.render(message, True, (0,0,0))
		
		messagePos = (21, self.configs['screen_size'][1] - self.configs['panel_height'] + 6)
		self.screen.blit(textRendered, messagePos)
		
		textRendered = textFont.render(message, True, (255,255,255))
		messagePos = (messagePos[0] - 1, messagePos[1] - 1)
		self.screen.blit(textRendered, messagePos)
		
		pygame.display.update()
		pygame.time.wait(1000)
		
		self.screen.blit(screenCopy, (0,0))
		self.__drawInventory__()
	
	def openBox(self, boxName):
		if self.objects[boxName]['tile'] == (0,0):
			self.sounds['open_box'].play()
			for i in range(3):
				self.__drawObject__(boxName)
				pygame.display.update()
				pygame.time.wait(100)
				self.objects[boxName]['tile'] = (self.objects[boxName]['tile'][0], self.objects[boxName]['tile'][1] + 1)
			self.objects[boxName]['tile'] = (self.objects[boxName]['tile'][0], self.objects[boxName]['tile'][1] - 1)
		
			if self.objects[boxName]['has'] != 'Monsters':
				if self.objects[boxName]['has'][-4:] == 'erva':
					self.player.potions += int(self.objects[boxName]['has'][:2])
					message = "Recebeu " + self.objects[boxName]['has'][:2] + ' Po\xe7\xf5es de erva'
				else:
					self.player.bag.append(self.objects[boxName]['has'])
					message = "Recebeu " + self.objects[boxName]['has']
				
				
			else:
				message = "Muitos mosquitos na caixa!!"
				
			
			self.printPanelMessage(message)
			
			if self.objects[boxName]['has'] == 'Monsters':
				"""
				groundTile = self.ground[self.playerPos[1]][self.playerPos[0]]
				battlePlace = None
				if groundTile == '__' or groundTile == '\xc30' or groundTile == '\xc32': #<- A grama
					battlePlace = 'grass'
				elif groundTile == 'N4':
					battlePlace = 'road'
				else:
					battlePlace = 'inside_castle'
				"""
				#self.battle = battle.clBattle('hornet', 4, battlePlace, self.player)
				self.startBattle('hornet', 4)
			
	
	def turnNPCToPlayer(self, npcName):
		
		lenX, lenY = self.__returnLenScreen__()
		submap = self.__submapToPrint__()
		# Verificando se o NPC esta na tela atual:
		if self.npcs[npcName]['pos'][0] / lenX == submap[0] and self.npcs[npcName]['pos'][1] / lenY == submap[1]:
			# Para o NPC virar para o player:
			if self.player.lookingTo == 'up':
				npcLookingTo = 'down'
			elif self.player.lookingTo == 'down':
				npcLookingTo = 'up'
			elif self.player.lookingTo == 'left':
				npcLookingTo = 'right'
			else:
				npcLookingTo = 'left'
			
			self.drawGround(self.npcs[npcName]['pos'][0], self.npcs[npcName]['pos'][1])
			self.__drawNPC__(npcName, npcLookingTo)
			self.drawLevel1(self.npcs[npcName]['pos'][0], self.npcs[npcName]['pos'][1])
			pygame.display.update()
	
	def drawPlayer(self, to, pixelCoords = None):
		clock = pygame.time.Clock()
		clock.tick(self.player.velocity)
		if pixelCoords == None:
			# O tile seguinte so deve ser desenhado se a chamada ao drawPlayer for feita para desenhar
			# o player em movimento, fora estes casos, o tile da frente pode ser redesenhado, e alguns
			# objetos ou NPCs podem sumir indevidamente.
			# pixelCoords so eh diferente de None quando o char for desenhado andando. 
			drawNextTile = False
			pixelCoords = self.__getPlayerPixelCoords__()
		else:
			drawNextTile = True
		#print "pc", pixelCoords	
		# Definindo a imagem do personagem a ser impressa na tela
		# Verifica-se qual a coordenada que nao eh multipla de tile_size, pois eh nela que o personagem muda o tile da perna
		legsImage = 1
		valueToCheck = None
		if pixelCoords[0] / float(self.configs['tile_size'][0]) != pixelCoords[0] / self.configs['tile_size'][0]:
			valueToCheck = pixelCoords[0]
		if pixelCoords[1] / float(self.configs['tile_size'][1]) != pixelCoords[1] / self.configs['tile_size'][1]:
			valueToCheck = pixelCoords[1]
		if valueToCheck != None:
			# Os valores pares representam posicoes com as pernas juntas (legsImage = 1)
			# Os impares divisiveis por 3 representam as terceiras posicoes de pernas na imagem do boneco (legsImage = 2)
			# Todos os outros impares representam as primeiras posicoes de pernas na imagem do boneco (legsImage = 0)
			if valueToCheck % 3 == 0:
				legsImage = 2
			elif valueToCheck % 2 != 0:
				legsImage = 0
			
		# JA FOI CHECADO EM UP E LEFT OS LIMITES (0,0), FALTA VERIFICAR DOWN E RIGHT			
		
		# Redesenhando os tiles anterior e final para evitar as repeticoes de personagem:
		self.drawGround(self.playerPos[0], self.playerPos[1])
		self.screen.blit(self.player.playerImage, pixelCoords, self.__getTileRect__(self.player.getImageCoord(to, legsImage)))
		if drawNextTile:
			if to == 'up' and (self.playerPos[1] - 1) >= 0:
				self.drawGround(self.playerPos[0], self.playerPos[1] - 1)
				self.screen.blit(self.player.playerImage, pixelCoords, self.__getTileRect__(self.player.getImageCoord(to, legsImage)))
				self.drawLevel1(self.playerPos[0], self.playerPos[1] - 1)
			elif to == 'down':
				self.drawGround(self.playerPos[0], self.playerPos[1] + 1)
				self.screen.blit(self.player.playerImage, pixelCoords, self.__getTileRect__(self.player.getImageCoord(to, legsImage)))
				self.drawLevel1(self.playerPos[0], self.playerPos[1] + 1)
			elif to == 'left' and (self.playerPos[0] - 1) >= 0:
				self.drawGround(self.playerPos[0] - 1, self.playerPos[1])
				self.screen.blit(self.player.playerImage, pixelCoords, self.__getTileRect__(self.player.getImageCoord(to, legsImage)))
				self.drawLevel1(self.playerPos[0] - 1, self.playerPos[1])
			elif to == 'right':
				self.drawGround(self.playerPos[0] + 1, self.playerPos[1])
				self.screen.blit(self.player.playerImage, pixelCoords, self.__getTileRect__(self.player.getImageCoord(to, legsImage)))
				self.drawLevel1(self.playerPos[0] + 1, self.playerPos[1])
		self.drawLevel1(self.playerPos[0], self.playerPos[1])
		
		#self.player.lookingTo = to
		pygame.display.update()
	
	def movePlayer(self, to):
		# Para verificar possiveis mudancas no cenario, caso o char tenha ido pra outro bloco do mapa:
		lenX, lenY = self.__returnLenScreen__()
		submap = self.__submapToPrint__()
		
		pixelCoord = self.__getPlayerPixelCoords__()
		
		self.player.lookingTo = to
		
		nextTile = self.getNextTileCoord(to)
		if self.canMoveTo(nextTile[0], nextTile[1]):
			if (to == 'up' and self.playerPos[1] == (submap[1]) * (lenY)) \
			or (to == 'down' and self.playerPos[1] == (submap[1] + 1) * (lenY)-1) \
			or (to == 'left' and self.playerPos[0] == (submap[0]) * (lenX)) \
			or (to == 'right' and self.playerPos[0] == (submap[0] + 1) * (lenX)-1): # Mudanca de tela
				self.playerPos = nextTile
				self.drawMap()
			else:
				if (to == 'up' or to == 'down'): rangeLim = self.configs['tile_size'][1]
				if (to == 'left' or to == 'right'): rangeLim = self.configs['tile_size'][0]
				for i in range(rangeLim):
					if (to == 'up'): pixelCoord = (pixelCoord[0], pixelCoord[1] - 1)
					if (to == 'down'): pixelCoord = (pixelCoord[0], pixelCoord[1] + 1)
					if (to == 'left'): pixelCoord = (pixelCoord[0] - 1, pixelCoord[1])
					if (to == 'right'): pixelCoord = (pixelCoord[0] + 1, pixelCoord[1])
					self.drawPlayer(to, pixelCoord)
				self.playerPos = nextTile
				self.__sortBattle__()
		else:
			self.drawPlayer(to)
		
	def __sortBattle__(self):
		# Sorteado 2 vezes abaixo para diminuir as chances de batalha
		if randint(1, 100) <= self.configs['battle_chance_percent'] and randint(1, 100) <= self.configs['battle_chance_percent']:
			self.startBattle('hornet')
		
	def startBattle(self, monsterName, numMonsters = None):
		# Atualizando dados do player:
		
		"""
		opcoes = ["Machado", "Espada"]
		for opcao in opcoes:
			if self.player.potions > 0:
				if not opcao in self.player.battleOptions: 
					self.player.battleOptions.append(opcao)
			else:
				if opcao in self.player.battleOptions:
					self.player.battleOptions.pop(self.player.battleOptions.index(opcao))
					
		if self.player.potions > 0:
			self.player.battleOptions.append("Usar Po\xe7\xe3o")
		"""
				
		groundTile = self.ground[self.playerPos[1]][self.playerPos[0]]
		battlePlace = None
		if groundTile == '__' or groundTile == '\xc30' or groundTile == '\xc32': #<- A grama
			battlePlace = 'grass'
		elif groundTile == 'N4':
			battlePlace = 'road'
		elif groundTile == '\xc3\xaa2':
			battlePlace = 'center'
		elif groundTile == '\xc3\x826' or groundTile == '\xc3\x825' or groundTile == '\xc3\x824':
			battlePlace = 'bridge'
		else:
			battlePlace = 'inside_castle'
			
		if numMonsters == None:
			numMonsters = randint(1,3)
			
		self.playMusic('battle')
		self.battle = battle.clBattle(monsterName, numMonsters, battlePlace, self.player)
	
	def toggleFullscreen(this):
		pygame.display.toggle_fullscreen()
		
	def __drawPanelBackground__(self):
		panelBG = pygame.image.load(self.configs['images_directory'] + 'backgrounds/panel_background.png')
		panelPosYBlit = self.configs['screen_size'][1] - self.configs['panel_height']
		for i in range(self.configs['screen_size'][0] / panelBG.get_size()[0] + 1): #+1 para o caso de dar quebrado como 1.xxx o valor do resultado e, ao arredondar, ir para baixo
			self.screen.blit(panelBG, (i*panelBG.get_size()[0], panelPosYBlit))
		
	def __drawInventory__(self):
		inventoryImage = pygame.image.load(self.configs['images_directory'] + 'backgrounds/inventory.png')
		inventoryImage = pygame.transform.scale(inventoryImage, (self.configs['panel_height'], self.configs['panel_height']))
		self.screen.blit(inventoryImage, (self.configs['screen_size'][0] - inventoryImage.get_size()[0], self.configs['screen_size'][1] - inventoryImage.get_size()[1]))
		if 'Armadura' in self.player.bag:
			itemImage = pygame.image.load(self.configs['images_directory'] + 'icons/item_armor.png')
			self.screen.blit(itemImage, (self.configs['screen_size'][0] - itemImage.get_size()[0] - 50, self.configs['screen_size'][1] - itemImage.get_size()[1] - 52))
		if 'Espada' in self.player.bag:
			itemImage = pygame.image.load(self.configs['images_directory'] + 'icons/item_sword.png')
			self.screen.blit(itemImage, (self.configs['screen_size'][0] - itemImage.get_size()[0] - 8, self.configs['screen_size'][1] - itemImage.get_size()[1] - 8))
		if 'Machado' in self.player.bag:
			itemImage = pygame.image.load(self.configs['images_directory'] + 'icons/item_axe.png')
			self.screen.blit(itemImage, (self.configs['screen_size'][0] - itemImage.get_size()[0] - 7, self.configs['screen_size'][1] - itemImage.get_size()[1] - 52))
		if 'Chave Dourada' in self.player.bag:
			itemImage = pygame.image.load(self.configs['images_directory'] + 'icons/item_key.png')
			self.screen.blit(itemImage, (self.configs['screen_size'][0] - itemImage.get_size()[0] - 50, self.configs['screen_size'][1] - itemImage.get_size()[1] - 9))
		if self.player.potions > 0:
			itemImage = pygame.image.load(self.configs['images_directory'] + 'icons/item_potion.png')
			posPotionBlit = (self.configs['screen_size'][0] - inventoryImage.get_size()[0] - itemImage.get_size()[0] - 10, self.configs['screen_size'][1] - itemImage.get_size()[1] - 18)
			self.screen.blit(itemImage, posPotionBlit)
			
			textFont = pygame.font.Font("fonts/" + self.configs['dialog_font_name'], 30)
			numPotions = textFont.render(str(self.player.potions), True, (0,0,0))
			posNumPotionsBlitX = posPotionBlit[0] + (itemImage.get_size()[0] - numPotions.get_size()[0])/2
			posNumPotionsBlitY = posPotionBlit[1] + (itemImage.get_size()[1] - numPotions.get_size()[1])/2
			self.screen.blit(numPotions, (posNumPotionsBlitX+1, posNumPotionsBlitY+1))
			
			numPotions = textFont.render(str(self.player.potions), True, (255,255,255))
			self.screen.blit(numPotions, (posNumPotionsBlitX, posNumPotionsBlitY))
			
									
	
	def drawPlayerPanel(self):
		self.__drawPanelBackground__()
		
		# Carregando a face:
		bgFace = pygame.image.load(self.configs['images_directory'] + 'backgrounds/background_face.png')
		bgFace = pygame.transform.scale(bgFace, (self.configs['panel_height'], self.configs['panel_height']))
		self.screen.blit(bgFace, (0, self.configs['screen_size'][1] - bgFace.get_size()[1]))
		marginFace = 4
		sizeFace = self.configs['panel_height'] - marginFace * 2
		playerFace = pygame.image.load(self.configs['dialog_faces_directory'] + '/player_face.png')
		playerFace = pygame.transform.scale(playerFace, (sizeFace, sizeFace))
		self.screen.blit(playerFace, (marginFace, self.configs['screen_size'][1] - playerFace.get_size()[0] - marginFace))
		
		# Carregando estado:
		textFont = pygame.font.Font(self.configs['fonts_directory'] + self.configs['dialog_font_name'], 14)
			
		lifeInfoText = self.configs['battle_life_info_label'] + str(self.player.health)
		textRendered = textFont.render(lifeInfoText, True, (0,0,0))
		lifeInfoPos = (bgFace.get_size()[0] + 10, self.configs['screen_size'][1] - self.configs['panel_height'] + 10)
		self.screen.blit(textRendered, (lifeInfoPos[0] + 1, lifeInfoPos[1] + 1))
		
		textRendered = textFont.render(lifeInfoText, True, (255,255,255))
		self.screen.blit(textRendered, lifeInfoPos)
		
		# Carregando o inventario:
		self.__drawInventory__()
		
