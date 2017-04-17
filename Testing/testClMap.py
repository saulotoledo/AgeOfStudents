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

import unittest, testConfigs
import map
from os import path

class testingMapOnlyPossibilities(unittest.TestCase):
		
	def testLoadedGround(self):
		for linha in self.map.ground:
			self.failIf(len(linha) != len(self.map.ground[0]), self.GROUND_INCORRECT_LOADED)
			
	def testLoadedLevel1(self, testing = True):
		
		# Testando se ha mais de um tile ocupando a mesma posicao no mesmo nivel.
		# Eh um caso impossivel haver dois tiles na mesma posicao, nem o mesmo tile
		# pode aparecer duas vezes na mesma posicao:
		todasPos = []
		posUnicas = []
		for posicoes in self.map.level1.values():
			todasPos = todasPos + posicoes
		
		# Removendo elementos repetidos:
		for item in todasPos:
			if not item in posUnicas:
				posUnicas.append(item)
		
		if testing:
			self.failIf(todasPos != posUnicas, self.LEVEL1_INCORRECT_LOADED)
		else:
			return posUnicas
	
	def testLevel1InsideGround(self):
		# Testando se o level1 nao eh maior que o ground
		allPosLevel1 = self.testLoadedLevel1(False)
		for posLevel1 in allPosLevel1:
			self.failIf(posLevel1[0] > len(self.map.ground)-1, self.LEVEL1_GREATER_THAN_GROUND_X)
			self.failIf(posLevel1[0] > len(self.map.ground)-1, self.LEVEL1_GREATER_THAN_GROUND_Y)
	
	def testLoadedNPCs(self):
		
		# Se testing for False em testLoadedLevel1, ela, ao inves de testar, retorna
		# as posicoes ocupadas pelos tiles do Level1. Estas posicoes serao usadas pra
		# comparar se algum NPC foi colocado em um desses tiles.
		posOcupadasLevel1 = self.testLoadedLevel1(False)
		
		for npc in self.map.npcs.keys():
			
			# Verificando se nao ha falta ou excesso de informacao no dicionario de npcs:
			if len(self.map.npcs[npc]) != 2:
				self.fail(self.NPCPOS_INVALID_INFO)
			else:
				npcTileCoords = self.map.npcs[npc]['pos']
				npcLookingTo = self.map.npcs[npc]['lookingTo']
				
				# Verificando tipos de dados e se eles estao corretamente carregados:
				self.failIf(self.is2dCoord(npcTileCoords) == False, self.NPCPOS_INVALID_COORDS)
				
				# Verificando se as coordenadas dos NPCs nao excedem largura e/ou
				# altura do mapa. (-1 porque a o tile superior esquerdo eh o (0,0)).
				if npcTileCoords[1] > len(self.map.ground)-1:
					self.fail(self.NPCPOS_COORD_Y_EXCEEDED)
				elif npcTileCoords[0] > len(self.map.ground[0])-1:
					self.fail(self.NPCPOS_COORD_X_EXCEEDED)
				
				# Verificando se o NPC nao esta em uma posicao ocupada por um tile de level1
				self.failIf(npcTileCoords in posOcupadasLevel1, self.NPCPOS_CONFLICT_LEVEL1)
				
				# Verificando se "lookingTo" possui um valor valido:
				self.failIf(npcLookingTo not in ['up', 'down', 'left', 'right'], self.NPCPOS_INVALID_LOOKINGTO)
		
	def testNPCsPositions(self):
		# Sera verificado se ha mais de um char na mesma posicao.
		charPos = []
		charPosUnicas = []
		for char in self.map.npcs.keys():
			charPos.append(self.map.npcs[char]['pos'])
		
		# Retirando posicoes repetidas:
		for item in charPos:
			if not item in charPosUnicas:
				charPosUnicas.append(item)
		
		self.failIf(charPos != charPosUnicas, self.NPCPOS_EQUAL_POSITIONS)
 		
 	def testImageDefs(self):
 		for tileName in self.map.images:
 			# Falha se faltar alguma informacao no dicionario ('image' e 'tile')
 			self.failUnless(self.map.images[tileName].has_key('image') and self.map.images[tileName].has_key('tile') and self.map.images[tileName].has_key('options'), self.IMAGES_DEF_INFO_MISSING)
 			
 			# Falha se o tipo do dado de 'image' nao for um str ou se o arquivo de imagem nao existe
 			self.failIf(type(self.map.images[tileName]['image']) != str, self.IMAGES_DEF_INVALID_IMAGENAME_TYPE)
 			self.failUnless(path.exists(self.config['configImagesPath'] + self.map.images[tileName]['image']), self.IMAGES_DEF_INVALID_IMAGE_FILENAME)
 			
 			# Falha se as coords informadas nao sao validas ou se 'options' nao eh uma lista de valores
 			self.failUnless(self.is2dCoord(self.map.images[tileName]['tile']), self.IMAGES_DEF_INVALID_COORDS)
 			self.failIf(type(self.map.images[tileName]['options']) != list, self.IMAGES_DEF_INVALID_OPTIONS)
 	
 	def testBasicConfigs(self):
 		self.failUnless(self.map.configs.has_key('screen_size'), self.CONFIG_HAS_NO_SCREEN_SIZE)
 		self.failUnless(self.is2dCoord(self.map.configs['screen_size']), self.CONFIG_INVALID_SCREEN_SIZE)
 		
 		self.failUnless(self.map.configs.has_key('tile_size'), self.CONFIG_HAS_NO_TILE_SIZE)
 		self.failUnless(self.is2dCoord(self.map.configs['tile_size']), self.CONFIG_INVALID_TILE_SIZE)
 		
 		self.failUnless(self.map.configs.has_key('maps_directory'), self.CONFIG_HAS_NO_MAPS_DIRECTORY)
 		self.failUnless(type(self.map.configs['maps_directory']) == str, self.CONFIG_INVALID_MAPS_DIRECTORY)
 		self.failUnless(path.exists(self.map.configs['maps_directory']), self.CONFIG_INVALID_MAPS_DIRECTORY)
 		
 		self.failUnless(self.map.configs.has_key('images_directory'), self.CONFIG_HAS_NO_IMAGES_DIRECTORY)
 		self.failUnless(type(self.map.configs['images_directory']) == str, self.CONFIG_INVALID_IMAGES_DIRECTORY)
 		self.failUnless(path.exists(self.map.configs['images_directory']), self.CONFIG_INVALID_IMAGES_DIRECTORY)
 		
 		self.failUnless(self.map.configs.has_key('window_title'), self.CONFIG_HAS_NO_WINDOW_TITLE)
 		self.failUnless(type(self.map.configs['window_title']) == str, self.CONFIG_INVALID_WINDOW_TITLE)
 		
 		self.failUnless(self.map.configs.has_key('player_start_pos'), self.CONFIG_HAS_NO_PLAYER_START_POS)
 		self.failUnless(self.is2dCoord(self.map.configs['player_start_pos']), self.CONFIG_INVALID_PLAYER_START_POS)
 	
	def is2dCoord(self, variable):
		if type(variable) != tuple:
			return False
		elif len(variable) != 2:
			return False
		elif type(variable[0]) != int or type(variable[1]) != int:
			return False
		return True
	
	def setUp(self):
		self.map = map.clMap('main')
	
	def tearDown(self):
		pass
	

		
	
	
