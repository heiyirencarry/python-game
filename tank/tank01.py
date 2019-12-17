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
    myTank = None

    enemyTank_count = 5
    enemyTank = []

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
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN:
                    MainGame.myTank.stop = True

    # 敌方坦克的初始化
    def createEnemyTank(self):
        top = 100
        for i in range(self.enemyTank_count):
            left = random.randint(0, 600)
            MainGame.enemyTank.append(EnemyTank(left, top))

    # 敌方坦克的显示
    def showEnemyTank(self):
        for enemy in MainGame.enemyTank:
            enemy.tankShow()
            enemy.randMove()



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
    def __init__(self):
        pass
    # 子弹移动
    def bulletMove(self):
        pass
    # 显示子弹
    def bulletShow(self):
        pass


if __name__ == "__main__":
    MainGame().startGame()

