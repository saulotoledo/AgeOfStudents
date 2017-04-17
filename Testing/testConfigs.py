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

class testStrings:
	GROUND_INCORRECT_LOADED = 'O nivel GROUND foi carregado incorretamente, ha linhas incompletas'
	LEVEL1_INCORRECT_LOADED = 'O nivel LEVEL1 foi carregado incorretamente, ha tiles diferentes na mesma posicao'
	LEVEL1_GREATER_THAN_GROUND_X = 'A largura do nivel LEVEL1 excede o tamanho original do mapa'
	LEVEL1_GREATER_THAN_GROUND_Y = 'A altura do nivel LEVEL1 excede o tamanho original do mapa'
	NPCPOS_INVALID_INFO = 'As informacoes de posicao dos NPCs foram incorretamente carregadas'
	NPCPOS_INVALID_COORDS = 'As coordenadas nao sao uma tupla de inteiros ou nao contem apenas 2 valores'
	NPCPOS_COORD_X_EXCEEDED = 'A coordenada X de um NPC excede o tamanho da largura do mapa'
	NPCPOS_COORD_Y_EXCEEDED = 'A coordenada Y de um NPC excede o tamanho da altura do mapa'
	NPCPOS_CONFLICT_LEVEL1 = 'Um tile do level1 (comum ou um objeto) ja foi definido na posicao de um NPC'
	NPCPOS_INVALID_LOOKINGTO = 'Opcao invalida para "lookingTo"'
	NPCPOS_EQUAL_POSITIONS = 'Ha NPCs diferentes na mesma posicao'
	IMAGES_DEF_INFO_MISSING = 'Ha tiles com informacoes faltando'
	IMAGES_DEF_INVALID_IMAGENAME_TYPE = 'O nome da imagem precisa ser string'
	IMAGES_DEF_INVALID_IMAGE_FILENAME = 'A imagem carregada nao existe'
	IMAGES_DEF_INVALID_COORDS = 'As coordenadas nao sao uma tupla de inteiros ou nao contem apenas 2 valores'
	IMAGES_DEF_INVALID_OPTIONS = 'As opcoes de configuracao de pelo menos um dos tiles eh invalida'
	CONFIG_HAS_NO_SCREEN_SIZE = 'A configuracao "screen_size" esta faltando'
	CONFIG_INVALID_SCREEN_SIZE = 'A configuracao "screen_size" nao eh uma tupla de 2 valores inteiros'
	CONFIG_HAS_NO_TILE_SIZE = 'A configuracao "tile_size" esta faltando'
	CONFIG_INVALID_TILE_SIZE = 'A configuracao "tile_size" nao eh uma tupla de 2 valores inteiros'
	CONFIG_HAS_NO_MAPS_DIRECTORY = 'O diretorio dos mapas deve ser configurado'
	CONFIG_INVALID_MAPS_DIRECTORY = 'O diretorio dos mapas nao existe ou eh de um tipo invalido'
	CONFIG_HAS_NO_IMAGES_DIRECTORY = 'O diretorio das imagens deve ser configurado'
	CONFIG_INVALID_IMAGES_DIRECTORY = 'O diretorio das imagens nao existe ou eh de um tipo invalido'
	CONFIG_HAS_NO_WINDOW_TITLE = 'Titulo da janela nao esta definido'
	CONFIG_INVALID_WINDOW_TITLE = 'Titulo da janela nao eh um string'
	CONFIG_HAS_NO_PLAYER_START_POS = 'A configuracao "player_start_pos" esta faltando'
	CONFIG_INVALID_PLAYER_START_POS = 'A configuracao "player_start_pos" nao eh uma tupla de 2 valores inteiros'

