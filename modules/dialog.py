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
import pygame, codecs, common

class clDialog(common.commonOperations):
	def __init__(self, npcName, dialogAdvance, npcFaceFileName = None):
		self.screen = pygame.display.get_surface()
		self.npcName = npcName
		self.npcFaceFileName = npcFaceFileName
		self.dialogAdvance = dialogAdvance #<- O avanco do dialogo com TODOS os personagens
		self.dialogSize = 0 #<-Tamanho do dialogo, implica em quantas falas o dialogo eh formado, para estabelecer o limite de this.speech
		self.talking = True #<- Para informar ao jogo que estamos em modo de dialogo
		self.speech = 0 #<- Todo dialogo eh formado por varias falas, essa variavel controla a fala atual a ser mostrada
		self.unlockedByDialog = []
		
		self.originalMap = self.screen.copy()
		self.readDialog()
		
	def writeDialogBox(self):
		panelBG = pygame.image.load(self.configs['images_directory'] + 'backgrounds/panel_background.png')
		self.panelPosYBlit = self.configs['screen_size'][1] - self.configs['panel_height']
		for i in range(self.configs['screen_size'][0] / panelBG.get_size()[0] + 1): #+1 para o caso de dar quebrado como 1.xxx o valor do resultado e, ao arredondar, ir para baixo
			self.screen.blit(panelBG, (i*panelBG.get_size()[0], self.panelPosYBlit))
		
	def readDialog(self):
		# O modulo "codecs" cuida para nao haver problemas com codificacao UTF-8
		dialogFile = codecs.open(self.configs['dialogs_directory'] + self.npcName + '.dial', "r", "utf-8")
		
		# Carregando o nome do player de dentro do arquivo texto em disco:
		nomePlayerFile = codecs.open(self.configs['dialogs_directory'] + 'Player.dial', "r", "utf-8")
		self.nomePlayer = nomePlayerFile.readline(0).strip()
		nomePlayerFile.close()
		
		linhas = dialogFile.readlines()
		dialogFile.close()
		self.nomeChar = linhas[0].strip()
		self.dialogo = {}
		for i in range(1, len(linhas)):
			if linhas[i].strip() != '':
				if linhas[i][0] == ':':
					chaveDict = int(linhas[i][1:len(linhas[i].strip())-1])
					self.dialogo[chaveDict] = []
				else:
					self.dialogo[chaveDict].append(linhas[i].strip())
				
		self.writeDialog()
		
	def __drawAvatar__(self, image):
		bgFace = pygame.image.load(self.configs['images_directory'] + 'backgrounds/background_face.png')
		bgFace = pygame.transform.scale(bgFace, (self.configs['panel_height'], self.configs['panel_height']))
		self.screen.blit(bgFace, (0, self.configs['screen_size'][1] - bgFace.get_size()[1]))
		marginFace = 4
		sizeFace = self.configs['panel_height'] - marginFace * 2
		#playerFace = pygame.image.load(self.configs['dialog_faces_directory'] + '/player_face.png')
		image = pygame.transform.scale(image, (sizeFace, sizeFace))
		self.screen.blit(image, (marginFace, self.configs['screen_size'][1] - image.get_size()[0] - marginFace))
	
	def writeDialog(self):
		self.playerAvatar = pygame.image.load(self.configs['dialog_faces_directory'] + '/player_face.png')
		
		if self.npcFaceFileName != None:
			self.NPCAvatar =  pygame.image.load(self.npcFaceFileName)
		
		# Carregando a quantidade de falas
		if self.dialogSize == 0:
			self.dialogSize = len(self.dialogo[self.dialogAdvance])
		
		# Verificando os UNLOCK:
		for linha in self.dialogo[self.dialogAdvance]:
			if linha[0:6] == 'UNLOCK':
				toUnlock = linha[8:len(linha)] 
				if not toUnlock in self.unlockedByDialog:
					self.unlockedByDialog.append(toUnlock)
		
		
		frase = self.dialogo[self.dialogAdvance][self.speech]
		self.writeDialogBox()
		
		#if frase[0:6] == 'UNLOCK':
		#	toUnlock = frase[8:len(frase)] 
		#	if not toUnlock in self.unlockedByDialog:
		#		self.unlockedByDialog.append(toUnlock)
		#el
		if frase[0:6] == '_GO_TO':
			nextAdvance = frase[8:len(frase)]
			if nextAdvance == 'FIM':
				self.dialogAdvance = nextAdvance
			else:
				self.dialogAdvance = int(nextAdvance)
				
			self.end()
		elif frase[0:6] != 'UNLOCK':
			self.inDialog = True
			if frase[0:6] == 'PLAYER':
				nomeConversando = self.nomePlayer
				self.__drawAvatar__(self.playerAvatar)
				#self.screen.blit(self.playerAvatar, (9, self.panelPosYBlit + 12))
			if frase[0:6] == 'COMPUT':
				nomeConversando = self.nomeChar
				if self.npcFaceFileName != None:
					self.__drawAvatar__(self.NPCAvatar)
					#self.screen.blit(self.NPCAvatar, (9, self.panelPosYBlit + 12))
			
			# Carregando o nome do char que esta falando:
			textFont = pygame.font.Font("fonts/" + self.configs['dialog_font_name'], 18)
			nameCharTalking = textFont.render(nomeConversando + ':', True, (0,0,0))
			self.screen.blit(nameCharTalking, (19 + self.playerAvatar.get_size()[0], self.panelPosYBlit + 13))
			
			nameCharTalking = textFont.render(nomeConversando + ':', True, (168,200,255))
			self.screen.blit(nameCharTalking, (18 + self.playerAvatar.get_size()[0], self.panelPosYBlit + 12))
			
			# Carregando o texto interno da fala:
			textFont = pygame.font.Font("fonts/" + self.configs['dialog_font_name'], 14)
			textoStr = self.text2lines(frase[8:len(frase)])
			
			textHeight = 0
			for linha in textoStr:
				texto = textFont.render(linha, True, (0,0,0))
				self.screen.blit(texto, (19 + self.playerAvatar.get_size()[0], self.panelPosYBlit + nameCharTalking.get_size()[1] + textHeight + 13))
				
				texto = textFont.render(linha, True, (255,255,255))
				self.screen.blit(texto, (18 + self.playerAvatar.get_size()[0], self.panelPosYBlit + nameCharTalking.get_size()[1] + textHeight + 12))
				textHeight += texto.get_size()[1]
			
			self.speech += 1
			pygame.display.update()
			
		else:
			self.end()
			
		pygame.time.wait(200) #<- Para que o dialogo nao passe muito rapido
		
		# Retorna o avanco de dialogo, para controle do jogo:
		return self.dialogAdvance
	
	def text2lines(self, text):
		textReturn = []
		linhaReturn = ""
		limiteChars = 62
		palavras = text.split(" ")
		
		for i in range(len(palavras)):
			if len(linhaReturn + palavras[i]) < limiteChars:
				linhaReturn = linhaReturn + palavras[i] + ' '
			else:
				textReturn.append(linhaReturn)
				linhaReturn = palavras[i] + ' '
		textReturn.append(linhaReturn) #<- O \n do final jah foi retirado antes. Esta eh a diferenca desta para a funcao de mesmo nome em clBattle.py.
		
		return textReturn
	
	def advance(self):
		self.writeDialog()
	
	def end(self):
		self.talking = False
		self.screen.blit(self.originalMap, (0,0))
		pygame.display.update()
		
