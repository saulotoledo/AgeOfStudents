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
import common, pygame

class clPlayer(common.commonOperations):
	lookingTo = 'down'
	
	health = common.commonOperations.configs['player_start_health']
	maxHealth = common.commonOperations.configs['player_max_health']
	armor = 2
	bag = []
	potions = 0
	velocity = 30
	
	def __init__(self):
		self.playerImage = pygame.image.load(self.configs['images_directory'] + 'people/player.png')
		self.name = ''
		
		self.useBattleOptions = {}
		# miss => X%, 40 significa 40% de chance de errar
		# hit eh o dano basico do golpe
		self.useBattleOptions['Soco'] = {'miss': 40, 'hit': 5}
		self.useBattleOptions['Espada'] = {'miss': 30, 'hit': 10}
		self.useBattleOptions['Machado'] = {'miss': 60, 'hit': 14}
		self.useBattleOptions['Usar Pocao'] = {'miss': 0, 'hit': 0}
		
		self.battleOptions = ['Soco']
		
		
	def getImageCoord(self, lookingTo, legsImage = 1):
		if lookingTo == 'down':
			return (legsImage, 0)
		if lookingTo == 'left':
			return (legsImage, 1)
		if lookingTo == 'right':
			return (legsImage, 2)
		if lookingTo == 'up':
			return (legsImage, 3)
		
