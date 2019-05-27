#导入相应的模块
import pygame
from pygame.locals import *
import time,random
import threading

enemylist = [] #存放敌机的列表
enemybullet_list = [] #存放敌机子弹
ENEMY_RUNNING = True

class HeroPlane:
	'''玩家飞机（英雄）'''
	global enemylist,enemybullet_list
	def __init__(self,screen_temp):
		self.x = 200
		self.y = 400
		self.screen = screen_temp
		self.image = pygame.image.load("./images/me.png")
		self.bullet_list = [] #用于存放玩家的子弹列表
	def display(self):
		#绘制子弹
		for b in self.bullet_list:
			b.display()
			if b.move(0):
				self.bullet_list.remove(b)
		self.screen.blit(self.image,(self.x,self.y))
	def move_left(self):
		self.x -= 6
		if self.x <= 0:
			self.x=0
	def move_right(self):
		self.x += 6
		if self.x>=406:
			self.x=406
	def fire(self):
		self.bullet_list.append(Bullet(self.screen,self.x,self.y))
	def losecheek(self):
		# 遍历所有敌机,并执行碰撞检测
		for ep in enemylist:
			if (self.x+10)>(ep.x-74) and (ep.x+92)>(self.x+10) and (ep.y-35)<(self.y+15) and (ep.y+60)>(self.y+15):
				return True
			# 遍历所有子弹,并执行碰撞检测
		for bt in enemybullet_list:
				if ((bt.x+3>self.x+10) and (bt.x<self.x+96) and (bt.y+17>self.y+15) and (bt.y+17<self.y+55)):
					return True




class Bullet:
	'''子弹类'''
	def __init__(self,screen_temp,x,y):
		self.x = x+53
		self.y = y
		self.screen = screen_temp
		self.image = pygame.image.load("./images/pd.png")
	def display(self):
		'''绘制子弹'''
		self.screen.blit(self.image,(self.x,self.y))
	def move(self,i):
		if i==0:
			self.y -= 10
			if self.y <=-20:
				return True
		elif i==1:
			self.y +=10
			if self.y >=588:
				return True

class EnemyPlane:
	'''敌机类'''
	
	global enemybullet_list
	def __init__(self,screen_temp):
		self.x = random.choice(range(408))
		self.y = -75
		self.endx = self.x
		self.endy = self.y
		self.blastnum = 0
		self.screen = screen_temp
		self.image = pygame.image.load("./images/e"+str(random.choice(range(3)))+".png")
	def display(self):
		if self.blastnum==0:
			self.screen.blit(self.image,(self.x,self.y))
		else:
			self.blastimage = pygame.image.load("./images/blast{:1}.png".format(self.blastnum))
			self.screen.blit(self.blastimage,(self.endx,self.endy))
			self.blastnum += 1

	    #绘制子弹
	    #for b in self.bullet_list:
	    #    b.display()
	    #    if b.move(1):
	    #        self.bullet_list.remove(b)
	   

	def move(self,hero):
		if self.blastnum == 0:
		    self.y += 4
		    #敌机出屏幕
		    if self.y>568:
		        return True
		    # 遍历所有子弹,并执行碰撞检测
		    for bo in hero.bullet_list:
		        if bo.x>self.x+12 and bo.x<self.x+92 and bo.y>self.y+20 and bo.y<self.y+60:
		        	self.endx = bo.x-52
		        	self.endy = bo.y-39
		        	hero.bullet_list.remove(bo)
		        	self.blastnum += 1
		        	#return True
	def fire(self):
	    enemybullet_list.append(Bullet(self.screen,self.x,self.y))

class EnemyPlaneThread(threading.Thread):
	global enemylist,ENEMY_RUNNING

	#def __init__(self):
	#	threading.Thread.__init__(self)
		#self.enemylist = enemylist
	def run(self):
		while ENEMY_RUNNING:
		    for em in enemylist:
			    em.fire()
			    pygame.display.update()
		    time.sleep(3)


def quitgame():
	'退出游戏'
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				print("exit()")
				exit()
				

def show_blast():
	img_blast3 = pygame.image.load("./images/blast3.png")

def key_control(hero_temp):
    '''键盘控制函数'''
    spacedown = 0
    global ENEMY_RUNNING
    #执行退出操作
    for event in pygame.event.get():
        if event.type == QUIT:
            ENEMY_RUNNING = False
            print("exit()")
            exit()
        elif event.type == KEYDOWN:
        	spacedown = 1

    #获取按键信息
    pressed_keys = pygame.key.get_pressed()
    
    #做判断，并执行对象的操作
    if pressed_keys[K_LEFT] or pressed_keys[K_a]:
        print("Left...")
        hero_temp.move_left()
    elif pressed_keys[K_RIGHT] or pressed_keys[K_d]:
        print("Right...")
        hero_temp.move_right()
    if pressed_keys[K_SPACE]:
    	if spacedown == 1:
            print("space...")
            hero_temp.fire()	            


def main():
	'''主程序函数 '''
	global enemylist,ENEMY_RUNNING
	# 创建游戏窗口
	screen = pygame.display.set_mode((512,568),0,0)
	# 创建一个游戏背景
	background = pygame.image.load("./images/bg2.jpg")
	endgame = pygame.image.load("./images/endgame.jpg")
	gameover = pygame.image.load("./images/gameover.png")
	# 创建玩家飞机（英雄）
	hero = HeroPlane(screen)
	m = -968
	a = EnemyPlaneThread()
	a.start()
	screen.blit(gameover,(0,m))
	
	while True:
		#绘制gameover
		screen.blit(background,(0,m))
		m+=2
		if m>=-200:
			m = -968
		#绘制玩家飞机
		hero.display()
		#执行键盘控制
		key_control(hero)
		#检查玩家存活状态
		if hero.losecheek():
			ENEMY_RUNNING = False
			screen.blit(endgame,(5,150))
			screen.blit(gameover,(156,218))
			pygame.display.update()
			break
		#随机绘制敌机
		if random.choice(range(50))==10:
			enemylist.append(EnemyPlane(screen))
		#绘制敌机子弹
		for bt in enemybullet_list:
			bt.display()
			if bt.move(1):
				enemybullet_list.remove(bt)

		#遍历敌机并绘制移动
		for em in enemylist:
			em.display()
			em.move(hero)
			if em.blastnum==4:
				enemylist.remove(em)
			#em.fire()
		#更新显示
		pygame.display.update()
		#定时显示
		time.sleep(0.04)
	quitgame()
	



#判断当前是否是主运行程序，并调用
if __name__ == "__main__":
	main()

