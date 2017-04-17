#coding: UTF-8
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
import pygame
from random import randint

class commonOperations:
	"""
	Operacoes comuns aos modulos, como configuracoes e inicializacoes basicas.
	Eh iniciado com a tela do jogo
	"""
	configs = {
	'screen_size': (800,600),
	'tile_size': (32, 32),
	'panel_height': 96, 
	'maps_directory': 'maps/',
	'images_directory': 'images/',
	'fonts_directory': 'fonts/',
	'sounds_directory': 'sounds/',
	'map_file_type': '.map',
	'transparent_image':  'backgrounds/transparent.png',
	
	'game_title': 'Age of Students',
	'game_icon': 'icons/gameicon.png',
	'game_won_message': 'Voc\xea venceu! A universidade est\xe1 salva.',
	'game_over_message': 'Game Over',
	
	'game_musics': {
	'menu': 'music_town1.ogg',
	'game_map': ['music_housewaltz.ogg', 'music_lingering_doubt.ogg', 'music_mountainwoods.ogg', 'music_quietruins.ogg'],
	'battle': 'music_battlesong.ogg',
	'won': 'music_Victory2.ogg',
	'game_over': 'music_grievances.ogg'
	},
	
	'game_sounds': {
	'menu_select': 'sound_inventory03.ogg',
	'Soco': 'sound_Blow2.ogg',
	'Espada': 'sound_Flash2.ogg',
	'Machado': 'sound_Slash10.ogg',
	'Usar Po\xe7\xe3o': 'sound_Heal7.ogg',
	'Picada': 'sound_Poison.ogg',
	'Picada dolorosa': 'sound_Poison.ogg',
	'open_box': 'sound_Chest.ogg',
	'miss': 'sound_Miss.ogg',
	'cat': 'sound_Cat.ogg',
	'game_over': 'sound_thunder1.ogg'
	},
	
	'player_start_pos': (1,98),
	'player_start_health': 100,
	'player_max_health': 100,
	
	'init_menu_itens': ['Novo Jogo', 'Sair'],
	'init_font_name': 'morpheus.ttf',
	'init_help_text': ['Para jogar:', '- Movimento: Setas direcionais', '- A\xe7\xe3o: Barra de espa\xe7o', '- Fullscreen ou normal: ALT + ENTER'],
	'init_authors_text': ['Autoria:', '- Saulo Toledo', 'Agradecimentos:', '- Emanuele Montenegro, pelo mapa e sugest\xe3o da hist\xf3ria'],
	'init_bg_image': 'backgrounds/start_screen.png',
	
	'dialog_font_name': 'Comic Sans MS.ttf',
	'dialogs_directory': 'dialogs/',
	'dialog_faces_directory': 'images/faces/',
	
	'battle_wait_time': 200,
	'battle_chance_percent': 5,
	'battle_arrow_image': 'icons/arrow_select.png',
	'battle_life_info_label': 'Pontos de vida: ',
	'battle_potions_info_label': 'N\xfam. po\xe7\xf5es: ',
	'battle_animations_directory': 'animations/',
	'battle_action_animations': {'Soco': 'Attack1.png', 'Espada': 'Sword1.png', 'Machado': 'Spear2.png', 'Usar Po\xe7\xe3o': 'Heal5.png', 'Picada': 'Special3_invert.png', 'Picada dolorosa': 'Special3_invert.png'},
	'battle_potion_recover': 10
	}
	
	sounds = {}
	musics = {}
	playingMusic = ''
	
	def setConfigs(self, configs):
		for configToUpdate in configs.keys():
			self.configs[configToUpdate] = configs[configToUpdate]
			
	def __preloadSounds__(self):
		pygame.mixer.init()
		
		for musicName in self.configs['game_musics'].keys():
			if type(self.configs['game_musics'][musicName]) == list:
				self.musics[musicName] = pygame.mixer.Sound(self.configs['sounds_directory'] + self.configs['game_musics'][musicName][randint(0, len(self.configs['game_musics'][musicName])-1)])
			else:
				self.musics[musicName] = pygame.mixer.Sound(self.configs['sounds_directory'] + self.configs['game_musics'][musicName])
																				
		for soundName in self.configs['game_sounds'].keys():
			self.sounds[soundName] = pygame.mixer.Sound(self.configs['sounds_directory'] + self.configs['game_sounds'][soundName])
	
	def playMusic(self, musicName):
		if self.playingMusic != '':
			self.musics[self.playingMusic].fadeout(1000)
		
		self.playingMusic = musicName
		self.musics[musicName].play()
	
	def playSound(self, soundName):
		self.sounds[soundName].play()
