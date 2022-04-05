import numpy as np
import pygame as pg

result = np.array([1, -1, 1, -1, 1, -1, -1, 1, 1, -1])

Points = np.array([
        [1, 1, 1],
        [9.4, 6.4, 1],
        [2.5, 2.1, 1],
        [8, 7.7, 1],
        [0.5, 2.2, 1],
        [7.9, 8.4, 1],
        [7, 7, 1],
        [2.8, 0.8, 1],
        [1.2, 3, 1],
        [7.8, 6.1, 1]
        ])

W = np.array([0.75, 0.5, -0.6])

def sign(x):
	if x > 0: return 1
	return -1

def calcNet(Points, W):
        return round(sum(Points*W),5)

def calcW(l_rate, W, point, need_res, calcN):
	return W + l_rate * (need_res - sign(calcN)) * point

def checkNet(calcN, result):
        return sign(calcN) == sign(result)

def value_line(x, W):
	return (-W[0]/W[1])*x - (W[2]/W[1])

def init_display():
	screen.fill(LIGHT_BLUE)
	pg.draw.line(screen, PURPLE, [size_x/2, 0.01*size_y], [size_x/2, size_y-0.01*size_y], 5)
	pg.draw.line(screen, PURPLE, [0.01*size_x, size_y/2], [size_x-0.01*size_x, size_y/2], 5)
	pg.display.update()

def check_line():
	pos = pg.mouse.get_pos()
	mouse_x, mouse_y = pos[0]-size_x/2, size_y/2-pos[1]
	if value_line(mouse_x, W) < mouse_y:
		pg.draw.circle(screen, PINK, [pos[0], pos[1]], 2)
		pg.display.update()
	elif value_line(mouse_x, W) > mouse_y:
		pg.draw.circle(screen, LIME, [pos[0], pos[1]], 2)
		pg.display.update()
	else:
		pg.draw.circle(screen, RED, [pos[0], pos[1]], 2)
		pg.display.update()
	print(mouse_x, mouse_y)

size_x = 700
size_y = 700

# Голубой
LIGHT_BLUE = (64, 128, 255)
# Зелёный
GREEN = (0, 200, 64)
# Розовый
PINK = (230, 50, 230)
# Фиолетовый
PURPLE = (86, 2, 110)
# Лайм
LIME = (191, 255, 0)
# Красный
RED = (255, 0, 0)

pg.init()
WINDOW_SIZE = (size_x, size_y)
screen = pg.display.set_mode(WINDOW_SIZE)

init_display()

cnt=0
while True:
		cnt_error=0
		print(f'---\nПроход цикла под шагом {cnt+1}')
		for i in range(len(Points)): 
			net = calcNet(Points[i], W)
			if checkNet(net, result[i]) == False:
					W = calcW(0.2, W, Points[i], result[i], net)
					cnt_error+=1
					print(f'Результат сети на {i+1} шаге: {net}')
					print(f'Значения весов на {i+1} шаге: {W}')
			pg.draw.line(screen, GREEN, [-size_x/2+size_x/2,size_y/2-value_line(-size_x/2,W)],[size_x/2+size_x/2,size_y/2-value_line(size_x/2, W)],3)
			pg.display.update()
			pg.time.delay(50)
			init_display()
		print(f'Количество ошибок на {cnt+1} шаге внешнего цикла: {cnt_error}')
		print('---')
		cnt+=1
		if cnt_error == 0: break

pg.draw.line(screen, GREEN, [-size_x/2+size_x/2,size_y/2-value_line(-size_x/2,W)],[size_x/2+size_x/2,size_y/2-value_line(size_x/2, W)],3)
pg.display.update()

clock = pg.time.Clock()
FPS = 60
startDraw = False

run=True
while run:
	clock.tick(FPS)
	for event in pg.event.get():
		if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
			startDraw = True
			check_line()
		elif event.type == pg.MOUSEMOTION:
			if startDraw:
				check_line()
		elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
			startDraw = False
		elif event.type == pg.QUIT:
			pg.quit()
			run = False
