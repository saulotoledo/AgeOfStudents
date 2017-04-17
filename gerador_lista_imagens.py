#coding: UTF-8


# Gerador de lista:
lista = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','ä','ë','ï','ö','ü','á','é','í','ó','ú','â','ê','î','ô','û','à','è','ì','ò','ù','ã','ẽ','ĩ','õ','ũ','Ä','Ë','Ï','Ö','Ü','Á','É','Í','Ó','Ú','Â','Ê','Î','Ô','Û','À','È','Ì','Ò','Ù','Ã','Ẽ','Ĩ','Õ','Ũ']

y=-1
for i in range(0,12):
	y += 1
	for j in range(0,16):
		print lista[i] + lista[j] + ': tiles/TileA1.png, [], (' + str(j) + ';' + str(y) + ')'
		
y=-1
for i in range(12,24):
	y += 1
	for j in range(0,16):
		print lista[i] + lista[j] + ': tiles/TileA2.png, [], (' + str(j) + ';' + str(y) + ')'
		
y=-1
for i in range(24,32):
	y += 1
	for j in range(0,16):
		print lista[i] + lista[j] + ': tiles/TileA3.png, [], (' + str(j) + ';' + str(y) + ')'
		
		
y=-1
for i in range(32,47):
	y += 1
	for j in range(0,16):
		print lista[i] + lista[j] + ': tiles/TileA4.png, [], (' + str(j) + ';' + str(y) + ')'


y=-1
for i in range(47,63):
	y += 1
	for j in range(0,8):
		print lista[i] + lista[j] + ': tiles/TileA5.png, [], (' + str(j) + ';' + str(y) + ')'

y=-1
for i in range(63,79):
	y += 1
	for j in range(0,16):
		print lista[i] + lista[j] + ': tiles/TileB.png, [], (' + str(j) + ';' + str(y) + ')'


y=-1
for i in range(79,95):
	y += 1
	for j in range(0,16):
		print lista[i] + lista[j] + ': tiles/TileC.png, [], (' + str(j) + ';' + str(y) + ')'

y=-1
for i in range(95,111):
	y += 1
	for j in range(0,16):
		print lista[i] + lista[j] + ': tiles/TileD.png, [], (' + str(j) + ';' + str(y) + ')'