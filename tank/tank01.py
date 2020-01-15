import pygame, time, random
'''
新增功能：
    加载我方坦克
'''
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
BG_COLOR = pygame.Color(0, 0, 0)
TEXT_COLOR = pygame.Color(255, 0, 0)


class MainGame:

    window = None
    myTank = None # 我方tank

    enemyTank_count = 5
    enemyTank = [] # 敌方坦克

    myBulletList = [] # 我方坦克的子弹list
    enemyBullet = [] # 敌方tank子弹

    explode_list = [] # 爆炸效果list

    def __init__(self):
        pass

    # 游戏开始
    def startGame(self):
        # 初始化游戏主窗口、设置窗口大小
        pygame.display.init()
        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption("黑衣人的tank大战")

        # 初始化我方tank
        MainGame.myTank = MyTank(350, 250)
        # 创建敌方坦克
        self.createEnemyTank()

        while True:
            time.sleep(0.02)
            # 设置主窗体的填充色
            MainGame.window.fill(BG_COLOR)
            # 事件的监听
            self.getEvent()
            # 主窗体中添加字体
            MainGame.window.blit(self.textSuface("敌方坦克剩余量%d"%len(MainGame.enemyTank)),(10, 10))
            # 显示我方tank
            MainGame.myTank.tankShow()
            # 显示敌方坦克
            self.showEnemyTank()
            # 移动我方tank的子弹
            self.showMyBullet()
            # 显示敌方tank的爆炸效果
            self.showExplode()

            if not MainGame.myTank.stop:
                MainGame.myTank.tankMove()
            pygame.display.update()


    # 游戏退出
    def gameOver(self):
        print("退出游戏")
        exit()

    # 左上角绘制文字
    def textSuface(self, text):
        pygame.font.init()
        font = pygame.font.SysFont("kaiti", 18)
        textSuface = font.render(text, True, TEXT_COLOR)
        return textSuface


    # 事件的监听
    def getEvent(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                self.gameOver()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print("UP")
                    MainGame.myTank.direction = "U"
                    MainGame.myTank.stop = False
                    # MainGame.myTank.tankMove()
                if event.key == pygame.K_DOWN:
                    print("DOWN")
                    MainGame.myTank.direction = "D"
                    MainGame.myTank.stop = False
                    # MainGame.myTank.tankMove()
                if event.key == pygame.K_LEFT:
                    print("LEFT")
                    MainGame.myTank.direction = "L"
                    MainGame.myTank.stop = False
                    # MainGame.myTank.tankMove()
                if event.key == pygame.K_RIGHT:
                    print("RIGHT")
                    MainGame.myTank.direction = "R"
                    MainGame.myTank.stop = False
                    # MainGame.myTank.tankMove()
                if event.key == pygame.K_SPACE:
                    print("发射子弹")
                    MainGame.myBulletList.append(Bullet(MainGame.myTank))
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    MainGame.myTank.stop = True

    # 敌方坦克的初始化
    def createEnemyTank(self):
        top = 100
        for i in range(self.enemyTank_count):
            left = random.randint(0, 600)
            et = EnemyTank(left, top);
            MainGame.enemyTank.append(et)

    # 敌方坦克的显示
    def showEnemyTank(self):
        for enemy in MainGame.enemyTank:
            if enemy.live:
                enemy.tankShow()
                enemy.randMove()
            else:
                MainGame.enemyTank.remove(enemy) # 移除死亡的tank

    #我方tank发射的子弹移动
    def showMyBullet(self):
        for bt in MainGame.myBulletList:
            if bt.live:
                bt.bulletShow()
                bt.bulletMove()
                bt.hitEnemyTank()
            else:
                MainGame.myBulletList.remove(bt) # 这个子弹一定要移除不然越来越多只是live=false的子弹过多

    # 显示所有的爆炸效果
    def showExplode(self):
        for ex in MainGame.explode_list:
            if ex.live:
                ex.displayExplode()
            else:
                MainGame.explode_list.remove(ex)


class Tank:

    # left距离左边的距离, top距离上边的距离
    def __init__(self, left, top):
        self.images = {
            'U':pygame.image.load('img/p1tankU.gif'),
            'D':pygame.image.load('img/p1tankD.gif'),
            'L':pygame.image.load('img/p1tankL.gif'),
            'R':pygame.image.load('img/p1tankR.gif'),
        }
        # 坦克的初始化默认设置
        self.direction = "U"
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        # 坦克距离绝对位置的左上距离
        self.rect.left = left
        self.rect.top = top
        # 坦克的移动速度
        self.speed = 5
        self.stop = True

    # 坦克的移动
    def tankMove(self):
        if self.direction == "L":
            if self.rect.left > 0:
                self.rect.left -= self.speed

        elif self.direction == "R":
            if self.rect.left + self.rect.height < SCREEN_WIDTH:
                self.rect.left += self.speed

        elif self.direction == "U":
            if self.rect.top > 0:
                self.rect.top -= self.speed

        elif self.direction == "D":
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                self.rect.top += self.speed

    # 坦克显示
    def tankShow(self):
        self.image = self.images[self.direction]
        MainGame.window.blit(self.image, self.rect)


class MyTank(Tank):
    def __init__(self, left, top):
        super(MyTank, self).__init__(left, top) # 继承调用父类的初始化方法(调用父类中的构造方法)

class EnemyTank(Tank):
    def __init__(self, left, top):
        super(EnemyTank, self).__init__(left, top) # 继承tank类
        self.images = {
            'U': pygame.image.load('img/enemy1U.gif'),
            'D': pygame.image.load('img/enemy1D.gif'),
            'L': pygame.image.load('img/enemy1L.gif'),
            'R': pygame.image.load('img/enemy1R.gif')
        }
        self.direction = self.randDirection()
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = 5
        self.moveFlag = True
        self.step = 60
        self.live = True


    def randDirection(self):
        num = random.randint(1, 4)
        if num == 1:
            return "U"
        elif num == 2:
            return "L"
        elif num == 3:
            return "R"
        elif num == 4:
            return "D"

    # 敌方坦克的随机移动
    def randMove(self):
        if self.step <= 0:
            # 修改方向
            self.direction = self.randDirection()
            # 步数复位
            self.step = 60
        else:
            self.tankMove()
            self.step -= 1

class Bullet:
    def __init__(self, tank):
        self.image = pygame.image.load('img/enemymissile.gif')
        self.direction = tank.direction # 子弹的方向取决于tank的方向
        self.rect = self.image.get_rect()
        self.speed = 6
        # 子弹的初始化位置
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        self.live = True

    # 子弹移动
    def bulletMove(self):
        if self.direction == "U":
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.live = False
        if self.direction == "R":
            if self.rect.left + self.rect.width < SCREEN_WIDTH:
                self.rect.left += self.speed
            else:
                self.live = False
        if self.direction == "L":
            if self.rect.left > 0:
                self.rect.left -= self.speed
        if self.direction == "D":
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                self.rect.top += self.speed
            else:
                self.live = False

    # 我方子弹和敌方坦克碰撞
    def hitEnemyTank(self):
        for eTank in MainGame.enemyTank:
            if pygame.sprite.collide_rect(eTank, self):
                MainGame.explode_list.append(Explode(eTank))
                self.live = False
                eTank.live = False

    # 显示子弹
    def bulletShow(self):
        # 将图片加载到窗体
        MainGame.window.blit(self.image, self.rect)

class Explode:
    def __init__(self, tank):
        self.rect = tank.rect
        self.images = [
            pygame.image.load('img/blast0.gif'),
            pygame.image.load('img/blast1.gif'),
            pygame.image.load('img/blast2.gif'),
            pygame.image.load('img/blast3.gif'),
            pygame.image.load('img/blast4.gif')
        ]
        self.step = 0
        self.image = self.images[self.step]
        self.live = True
    # 爆炸效果的展示
    def displayExplode(self):
        if self.step < len(self.images):
            MainGame.window.blit(self.image, self.rect)
            self.image = self.images[self.step]
            self.step += 1
        else:
            self.live = False
            self.step = 0


if __name__ == "__main__":
    MainGame().startGame()

