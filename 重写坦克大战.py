"""
坦克类Tank
    我方坦克 Herotank
    敌方坦克 Enemytank

"""
import pygame
import random
# pygame 初始化
pygame.init()
# 设置窗口大小
Window_W = 1080
Window_H = 720
# 创建窗口
Window = pygame.display.set_mode((Window_W,Window_H),pygame.RESIZABLE)
# 设置窗口标题
pygame.display.set_caption("坦克大战")
# 设置窗口图标
logo_img = pygame.image.load("images/a1.jpg")
pygame.display.set_icon(logo_img)


"""
Tank 
    属性:图片、坐标、血量、速度、方向
    方法：移动、发射
"""
# 父坦克类
class Tank:
    # 初始化坦克类
    def __init__(self,x,y):
        # 速度
        self.speed = 1
        # 血量
        self.blood = 2
        # 方向
        self.direction = "R"
        # 加载图片文件，返回图片对象
        self.image = pygame.image.load(f"images/p1tank{self.direction}.gif")
        # 获取图片rect矩形宽高属性
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # 新增子弹列表
        self.bullet_list = []

        # 新增旧坐标
        self.oldx = self.rect.x
        self.oldy = self.rect.y

        # 新增坦克状态
        self.is_alive = True


    # 设置坦克的移动方法
    def move(self):
        self.oldx = self.rect.x
        self.oldy = self.rect.y

        if self.direction == "U":
            if self.rect.y >= 0:
                self.rect.y = self.rect.y - self.speed
            # self.rect.y -= self.speed if self.rect.y >= 0 else 0
        if self.direction == "D":
            if self.rect.y < Window_H - self.rect.height:
                self.rect.y = self.rect.y + self.speed
            # self.rect.y += self.speed if self.rect.y <= Window_H - self.rect.height else 0
        if self.direction == "L":
            if self.rect.x >= 0:
                self.rect.x -= self.speed
        if self.direction == "R":
            if self.rect.x < Window_W - self.rect.width:
                self.rect.x += self.speed

    # 设置坦克发射方法
    def fire(self):
        """创建子弹对象"""
        bullet = Bullet(self)
        self.bullet_list.append(bullet)

    # 新增坦克撞到墙时回退的方法
    def back(self):
        self.rect.x = self.oldx
        self.rect.y = self.oldy

# 创建我方坦克类
class  HeroTank(Tank):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.blood = 1
        # 更改图片方向
        self.image = pygame.image.load(f"images/p1tank{self.direction}.gif")

    # 设置移动方法
    def move(self):
        # 设置键盘的长按事件
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
        # 更换为向左方向
            self.direction = "L"
         # 重新加载坦克图片
            self.image = pygame.image.load(f"images/p1tank{self.direction}.gif")
            # 调用父类的方法移动
            super().move()
        elif pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            # 更换为向右方向
            self.direction = "R"
            # 重新加载坦克图片
            self.image = pygame.image.load(f"images/p1tank{self.direction}.gif")
            # 调用父类的方法移动
            super().move()
        elif pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
            # 更换为向上方向
            self.direction = "U"
            # 重新加载坦克图片
            self.image = pygame.image.load(f"images/p1tank{self.direction}.gif")
            # 调用父类的方法移动
            super().move()
        elif pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
            self.direction = 'D'
            self.image = pygame.image.load(f'images/p1tank{self.direction}.gif')
            super().move()

# 创建敌方坦克
class EnemyTank(Tank):
    def __init__(self):
        super().__init__(random.randint(0,Window_W-60),0)
        self.image = pygame.image.load(f"images/enemy1{self.direction}.gif")
        self.speed = 1

    # 产生随机方向方法
    def random_direction(self):
        lst = ["U","D","R","L"]
        return random.choice(lst)

    # 设置敌方移动方法
    def move(self):
        # 继承父类移动方法
        super().move()
        # 控制速率
        n = random.randint(1,200)
        if n == 100:
            self.direction = self.random_direction()
            self.image = pygame.image.load(f"images/enemy1{self.direction}.gif")

# 父墙类
class Wall:
    """
    墙类
        砖墙 Brickwall
        钢墙 Stealwall
        草墙 Grasswall
        水墙 Waterwall

    属性：血量、类型、坐标、图片
    方法：阻挡其他元素

    """
    def __init__(self,type_,x,y):
        self.blood = 10000
        self.image = pygame.image.load(f"images/{type_}.gif")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # 新增墙的状态
        self.is_alive = True

    def block_item(self,item):
        """区别坦克和子弹"""
        if isinstance(item,Tank):
            # 如果坦克撞上墙
            if pygame.Rect.colliderect(self.rect,item.rect):
                # 调用坦克回退上一次位置的方法back
                item.back()
            # 如果时子弹撞到墙上，则通过
        if isinstance(item,Bullet):
            if pygame.Rect.colliderect(self.rect,item.rect):
                # 如果碰撞了，就修改子弹的状态
                item.is_alive = False
                self.blood -= 1
                if self.blood <= 0:
                    self.is_alive = False

# 定义砖墙
class BrickWall(Wall):
    def __init__(self,type_,x,y):
        super().__init__(type_,x,y)
        self.blood = 3

# 定义水墙
class WaterWall(Wall):
    def block_item(self,item):
        if isinstance(item,Tank):
            if pygame.Rect.colliderect(self.rect,item.rect):
                item.back()

# 定义钢墙
class StealWall(Wall):

        pass

# 定义草墙
class GrassWall(Wall):
    def block_item(self,item):
        pass

# 子弹类
class Bullet:
    """
    属性：速度、伤害、图片、坐标、方向
    方法：移动
    """
    def __init__(self,tank):
        self.speed = 1
        self.direction = tank.direction   # 使子弹的方向与坦克一致
        self.image = pygame.image.load("images/enemymissile.gif")

        self.rect = self.image.get_rect()
        self.rect.centerx = tank.rect.centerx
        self.rect.centery = tank.rect.centery

        # 添加子弹状态
        self.is_alive = True

    def move(self):
        if self.direction == "U":
            if self.rect.y > -self.rect.height:
                self.rect.y -= self.speed
            else:
                self.is_alive = False

        if self.direction == "D":
            if self.rect.y < Window_H + self.rect.height:
                self.rect.y += self.speed
            else:
                self.is_alive = False

        if self.direction == "R":
            if self.rect.x < Window_W + self.rect.width:
                self.rect.x += self.speed
            else:
                self.is_alive = False

        if self.direction == "L":
            if self.rect.x > -self.rect.width:
                self.rect.x -= self.speed
            else:
                self.is_alive = False

    # 新增方法 子弹击中敌人
    def hit_enemy(self,item):
        if pygame.Rect.colliderect(self.rect,item.rect):
            self.is_alive = False
            item.blood -= 1
            if item.blood <= 0:
                item.is_alive = False

# 老鹰类
class Eagle:
    pass

# 游戏类
class Game:
    # 初始化
    def __init__(self):
        # 加载背景图片
        self.background = pygame.image.load("images/background.jpg")
        #  创建坦克
        self.tank = HeroTank(600,360)

        # 创建敌方坦克

        self.enemy_tank_list = [EnemyTank() for i in range(10)]

        #创建我方子弹对象
        # self.bullet = Bullet(self.tank)
        # 定义一个记录所有墙的空列表
        self.wall_list = []

        for i in range(50):
            if i % 2 == 0:
                brick = BrickWall("walls",random.randrange(0,Window_W-60,60),random.randrange(60,Window_H-120,60))
                self.wall_list.append((brick))
            elif i % 3 ==0:
                steel = StealWall('steels',random.randrange(0,Window_W-60,60),random.randrange(60,Window_H-120,60))
                self.wall_list.append(steel)
            elif i % 5 !=0:
                grass = GrassWall('grass',random.randrange(0,Window_W-60,60),random.randrange(60,Window_H-120,60))
                self.wall_list.append(grass)
            else:
                water = WaterWall('water',random.randrange(0,Window_W-60,60),random.randrange(60,Window_H-120,60))
                self.wall_list.append(water)
    # 贴图 (指定坐标,将图片绘制到窗口上)

    def draw(self):
        # 贴背景图
        Window.blit(self.background,(0,0))
        # 贴坦克图
        if self.tank.is_alive:
            Window.blit(self.tank.image,(self.tank.rect.x,self.tank.rect.y))
        else:
            print("游戏结束")
            exit()

        # 贴敌方坦克图
        for enemy_tank in self.enemy_tank_list:
            if enemy_tank.is_alive:
                Window.blit(enemy_tank.image,(enemy_tank.rect.x,enemy_tank.rect.y))
            else:
                self.enemy_tank_list.remove(enemy_tank)
                # 贴敌方子弹图
            for bullet in enemy_tank.bullet_list:
                if bullet.is_alive:
                    Window.blit(bullet.image,(bullet.rect.x,bullet.rect.y))
                else:
                    enemy_tank.bullet_list.remove(bullet)
        # # 贴子弹图
        # Window.blit(self.bullet.image,(self.bullet.rect.x,self.bullet.rect.y))
        # 贴我方子弹图
        for bullet in self.tank.bullet_list:
            if bullet.is_alive:
                Window.blit(bullet.image,(bullet.rect.x,bullet.rect.y))
            else:
                self.tank.bullet_list.remove(bullet)

        # 贴墙图
        for wall in self.wall_list:
            if wall.is_alive:
                Window.blit(wall.image,(wall.rect.x,wall.rect.y))
            else:
                self.wall_list.remove(wall)
        # print(len(self.tank.bullet_list))

    def block_item(self):
        for wall in self.wall_list:
            # 与我方坦克碰撞
            wall.block_item(self.tank)

            # 我方子弹
            for bullet in self.tank.bullet_list:
                wall.block_item(bullet)

            # 与敌方坦克碰撞
            for enemy_tank in self.enemy_tank_list:
                wall.block_item(enemy_tank)
                # 敌方子弹
                for bullet in enemy_tank.bullet_list:
                    # 与墙碰撞
                    wall.block_item(bullet)
                    # 敌方子弹和我方坦克碰撞
                    bullet.hit_enemy(self.tank)
            # 我方子弹和敌方坦克
        for bullet in self.tank.bullet_list:
            for enemy_tank in self.enemy_tank_list:
                bullet.hit_enemy(enemy_tank)

    # 创建一个元素移动的方法
    def move(self):
        self.tank.move()
        # 敌方坦克移动
        for enemy_tank in self.enemy_tank_list:
            enemy_tank.move()
            # 敌方子弹移动
            for bullet in enemy_tank.bullet_list:
                bullet.move()

        # # 子弹移动
        # self.bullet.move()
        # 我方子弹移动
        for bullet in self.tank.bullet_list:
            bullet.move()

    # 刷新页面
    def update(self):
        pygame.display.update()

    # 添加事件
    def event(self):
        for event in pygame.event.get():
            # 当鼠标点击关闭窗口
            if event.type == pygame.QUIT:
                # 关闭程序
                exit()
            if event.type == pygame.KEYDOWN:
                # 判断用户按键0
                if event.key == pygame.K_SPACE:
                    print("射击")
                    self.tank.fire()
                if event.key == pygame.K_0:
                    for enemy_tank in self.enemy_tank_list:
                        enemy_tank.fire()

                if event.key == pygame.K_ESCAPE:
                    self.wall_list.clear()
                    self.enemy_tank_list.clear()
    # 运行
    def run(self):
        # 设置循环贴图
        while True:
            # 运行贴图方法
            self.draw()
            # 调用事件
            self.event()
            # 调用移动方法0
            self.move()
            # 调用阻挡子弹的方法00
            self.block_item()
            # 刷新
            self.update()

if __name__ == '__main__':
    game =Game()
    game.run()