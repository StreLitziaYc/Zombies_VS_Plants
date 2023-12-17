import random
import time
import pgzrun

TITLE = "Zombies VS Plants"
WIDTH = 1070
HEIGHT = 640

w = 4  # 植物列数
h = 5  # 植物行数


class Card:
    value_dic = {'normal': 50,
                 'bucket': 125,
                 'football': 175}

    def __init__(self, name, x, y):
        self.value = Card.value_dic[name]
        self.name = name
        self.card = Actor(name + '_card')
        self.card.x = x
        self.card.y = y
        self.black_card = Actor(name + '_card_black')
        self.black_card.x = x
        self.black_card.y = y
        self.is_black = False
        self.icon = Actor(name + '_icon')

    def set_pos(self, x, y):
        self.icon.x = x
        self.icon.y = y

    def draw(self):
        if self.is_black:
            self.black_card.draw()
        else:
            self.card.draw()

    def draw_icon(self):
        self.icon.draw()

    def update(self):
        if Sun.total < self.value:
            self.is_black = True
        else:
            self.is_black = False

    def down(self):
        if self.name == 'normal':
            return NormalZombie()
        elif self.name == 'bucket':
            return BucketZombie()
        elif self.name == 'football':
            return FootballZombie()


class UserInterface:
    def __init__(self):
        self.next_menu = Actor('next_menu')
        self.last_menu = Actor('last_menu')
        self.end_img = Actor('game_end')
        self.last_menu.x = 600
        self.last_menu.y = 334
        self.next_menu.x = 600
        self.next_menu.y = 334
        self.end_t = None
        self.game_end = False
        self.state = 0
        self.start = False
        self.on_start = False
        self.main_menu = Actor('mainmenu')
        self.start_0 = Actor('start_0')
        self.start_1 = Actor('start_1')
        self.win_map = [False for i in range(h)]
        self.x1_limit = 640
        self.x2_limit = 1045
        self.text_x = 260
        self.text_y = 63
        self.chooser = Actor('chooser')
        self.chooser.x = 500
        self.background = Actor('bg')
        self.cards = []
        self.cards_name = ['normal', 'bucket', 'football']
        self.dis = 55
        self.x0 = 345
        self.y0 = 42
        self.on_zombie = False
        self.zombie = None
        self.win = False
        self.win_img = Actor('win')
        self.win_img.x = 600
        self.win_img.y = 334
        self.plant_sets = [[[Shooter(), Sunflower(), Tomato(), Sunflower()],
                            [Shooter(), Sunflower(), Sunflower(), Tomato()],
                            [Shooter(), Sunflower(), Shooter(), Tomato()],
                            [Sunflower(), Sunflower(), Sunflower(), Tomato()],
                            [Tomato(), Tomato(), Sunflower(), Shooter()]],
                           [[Shooter(), FireTree(), Shooter(), Sunflower()],
                            [Shooter(), Sunflower(), Sunflower(), Tomato()],
                            [Shooter(), Sunflower(), FireTree(), Sunflower()],
                            [Sunflower(), Sunflower(), Shooter(), Tomato()],
                            [Shooter(), Sunflower(), Sunflower(), FireTree()]],
                           [[Shooter(), Shooter(), Sunflower(), Sunflower()],
                            [IceShooter(), Sunflower(), Sunflower(), Tomato()],
                            [Tomato(), Sunflower(), IceShooter(), Sunflower()],
                            [Sunflower(), Sunflower(), Sunflower(), Tomato()],
                            [Sunflower(), IceShooter(), Sunflower(), Shooter()]]]
        for i in range(len(self.cards_name)):
            self.cards.append(Card(self.cards_name[i], self.x0 + self.dis * i, self.y0))

    def game_init(self, test=False, state=None):
        if self.state >= 3:
            return
        if state is not None:
            self.state = state
        zombies.clear()
        sounds.background_music.stop()
        sounds.background_music.play(-1)
        self.win = False
        self.win_map = [False for i in range(h)]
        Zombie.zombie_map = [0 for i in range(h)]
        suns.clear()
        Sun.total = 150 + 50 * self.state
        if test:
            Sun.total *= 10
        random.shuffle(self.plant_sets[self.state])
        for i in range(h):
            temp = self.plant_sets[self.state][i]
            for j in range(w):
                plant = temp[j]
                plant.set_pos(i, j)
                plants.append(plant)
        if test:
            plants.clear()

    def start_draw(self):
        button_x = 760
        button_y = 160
        self.main_menu.draw()
        self.start_0.x = button_x
        self.start_0.y = button_y
        self.start_1.x = button_x
        self.start_1.y = button_y
        if self.on_start:
            self.start_0.draw()
        else:
            self.start_1.draw()

    def draw(self):
        self.background.draw()
        self.chooser.draw()
        for card in self.cards:
            card.draw()
        screen.draw.text(str(Sun.total), (self.text_x, self.text_y), fontsize=32, color='black')

    def draw_last(self):
        if self.win:
            if self.state < 2:
                self.next_menu.draw()
            else:
                self.last_menu.draw()
                if self.end_t is None:
                    self.end_t = time.time()
        if self.game_end:
            self.end_img.draw()

    def set_zombie(self, card, pos):
        card.set_pos(pos[0], pos[1])
        self.zombie = card

    def draw_zombie(self):
        if self.on_zombie:
            self.zombie.draw_icon()

    def update_with_mouse_move(self, pos):
        if self.start_0.collidepoint(pos):
            self.on_start = True
        else:
            self.on_start = False
        if self.on_zombie:
            self.zombie.set_pos(pos[0], pos[1])

    def update(self):
        if self.end_t is not None and self.end_t != -1:
            if time.time() - self.end_t >= 5:
                zombies.clear()
                self.game_end = True
                self.end_t = -1
                sounds.background_music.stop()
                sounds.end_song.play(-1)
        if not self.win:
            self.win = True
            for flag in self.win_map:
                if not flag:
                    self.win = False
            if self.win:
                sounds.win.play()  # 此处存在bug，经过测试，此处代码肯定会被执行，但音频可能无法播放，猜测是pgzero的问题
        for card in self.cards:
            card.update()

    def zombie_down(self, pos):
        if self.on_zombie and not self.chooser.collidepoint(pos) and self.x2_limit > pos[0] > self.x1_limit:
            sounds.set_zombie.play()
            Sun.total -= self.zombie.value
            self.on_zombie = False
            temp = self.zombie.down()
            temp.set_pos(pos[0], pos[1])
            zombies.append(temp)

    def update_with_mouse_down(self, pos):
        if self.win:
            if self.next_menu.collidepoint(pos):
                sounds.click.play()
                self.state += 1
                self.game_init(test=True) # 测试模式，不会出现植物，且阳光是十倍
                # self.game_init()
        if not self.start:
            if self.start_0.collidepoint(pos):
                sounds.click.play()
                self.start = True
                self.game_init(test=True, state=2) # 测试模式，同上，且直接进入第三关
                # self.game_init()
        for card in self.cards:
            if card.card.collidepoint(pos) and not card.is_black:
                self.on_zombie = True
                self.set_zombie(card, pos)
        self.zombie_down(pos)


class Plant:
    pos_table = []  # 植物坐标
    x0 = 315
    y0 = 150
    dx = 85
    dy = 100
    for i in range(h):
        temp = []
        for j in range(w):
            temp.append((x0 + dx * j, y0 + dy * i))
        pos_table.append(temp)

    def __init__(self, name):
        self.eat_t1 = time.time()
        self.eat_t2 = None
        self.blood = 100
        self.j = None
        self.i = None
        self.img_num = 0
        self.t2 = None
        self.item = Actor(name)
        self.img_index = 0
        self.imgs = []
        self.t1 = time.time()
        self.item = Actor(name)

    def draw(self):
        self.imgs[self.img_index].draw()
        self.t2 = time.time()
        if self.t2 - self.t1 >= 0.1:
            self.img_index += 1
            self.img_index %= self.img_num
            self.t1 = self.t2

    def set_pos(self, i, j):
        self.i = i
        self.j = j
        self.item.x = Plant.pos_table[i][j][0]
        self.item.y = Plant.pos_table[i][j][1]
        for i in range(self.img_num):
            self.imgs[i].x = self.item.x
            self.imgs[i].y = self.item.y

    def be_eat(self, zombie=None):
        self.eat_t2 = time.time()
        if self.eat_t2 - self.eat_t1 >= 0.8 * zombie.slow_down:
            self.blood -= Zombie.eat_damage
            self.eat_t1 = self.eat_t2

        if self.blood <= 0:
            sounds.plant_end.play()
            plants.remove(self)
            return True

    def update(self):
        pass


class Shooter(Plant):
    def __init__(self):
        name = 'shooter'
        super().__init__(name)
        self.img_num = 13
        self.shoot_t1 = time.time()
        self.shoot_t2 = None
        for i in range(self.img_num):
            self.imgs.append(Actor(name + '_' + str(i)))

    def update(self):
        if Zombie.zombie_map[self.i] == 0:
            pass
        else:
            self.shoot_t2 = time.time()
            if self.shoot_t2 - self.shoot_t1 >= 1.3:
                bullets.append(Bullet(self.i, self.j))
                self.shoot_t1 = self.shoot_t2


class IceShooter(Shooter):
    def __init__(self):
        name = 'ice_shooter'
        super().__init__()
        self.imgs.clear()
        self.img_num = 15
        self.shoot_t1 = time.time()
        self.shoot_t2 = None
        for i in range(self.img_num):
            self.imgs.append(Actor(name + '_' + str(i)))

    def update(self):
        if Zombie.zombie_map[self.i] == 0:
            pass
        else:
            self.shoot_t2 = time.time()
            if self.shoot_t2 - self.shoot_t1 >= 1.3:
                bullets.append(IceBullet(self.i, self.j))
                self.shoot_t1 = self.shoot_t2


class Sunflower(Plant):
    def __init__(self):
        name = 'sunflower'
        super().__init__(name)
        self.img_num = 18
        for i in range(self.img_num):
            self.imgs.append(Actor(name + '_' + str(i)))

    def be_eat(self, zombie=None):
        self.eat_t2 = time.time()
        if self.eat_t2 - self.eat_t1 >= 0.8:
            self.blood -= Zombie.eat_damage
            self.eat_t1 = self.eat_t2

        if self.blood <= 0:
            self.die()
            sounds.plant_end.play()
            plants.remove(self)
            return True

    def die(self):
        for i in range(6):
            Sun(self)


class Tomato(Plant):
    damage = 1000

    def __init__(self):
        self.exp_img = []
        self.exp_img.append(Actor('bomb'))
        self.exp_img.append(Actor('bomb_end'))
        name = 'tomato'
        self.is_exp = None
        super().__init__(name)
        self.img_num = 8
        for i in range(self.img_num):
            self.imgs.append(Actor(name + '_' + str(i)))

    def draw(self):
        if self.is_exp is None:
            self.imgs[self.img_index].draw()
            self.t2 = time.time()
            if self.t2 - self.t1 >= 0.1:
                self.img_index += 1
                self.img_index %= self.img_num
                self.t1 = self.t2
        else:
            if self.is_exp >= 150:
                self.exp_img[1].draw()
                self.exp_img[0].draw()
            else:
                self.exp_img[1].draw()

    def update(self):
        if self.is_exp is not None:
            self.is_exp -= 1
            if self.is_exp < 0:
                plants.remove(self)

    def be_eat(self, zombie=None):
        if self.is_exp is None:
            zombie.hit(self)
            self.explode()
        return True

    def explode(self):
        sounds.tomato_bomb.play()
        for img in self.exp_img:
            img.x = self.item.x
            img.y = self.item.y
        self.is_exp = 200


class Bullet:
    def __init__(self, i, j, name='bullet'):
        self.damage = 10
        self.item = Actor(name)
        self.speed = 5
        self.end_img = Actor(name + '_end')
        self.item.x = Plant.pos_table[i][j][0] + 33
        self.item.y = Plant.pos_table[i][j][1] - 19
        self.timer = None

    def update(self):
        if self.item.x > WIDTH + 40:
            bullets.remove(self)
        for z in zombies:
            if self.item.colliderect(z.item) and self.timer is None:
                self.end()
                z.hit(self)
        if self.timer is not None and self.timer <= 0:
            bullets.remove(self)
        if self.timer is None:
            self.item.x += self.speed

    def draw(self):
        if self.timer is None:
            self.item.draw()
        else:
            self.end_img.draw()
            self.timer -= 1

    def end(self):
        self.end_img.x = self.item.x + 20
        self.end_img.y = self.item.y
        self.timer = 10


class IceBullet(Bullet):
    def __init__(self, i, j):
        super().__init__(i, j, 'ice_bullet')


class FireBullet(Bullet):
    def __init__(self, i, j):
        name = 'fire_bullet'
        super().__init__(i, j, name)
        self.damage = 15
        self.t1 = time.time()
        self.t2 = None
        self.imgs = []
        self.img_num = 2
        self.img_index = 0
        for i in range(self.img_num):
            self.imgs.append(Actor(name + '_' + str(i)))
            self.imgs[i].x = self.item.x
            self.imgs[i].y = self.item.y

    def set_pos(self, bullet):
        self.item.x = bullet.item.x
        for i in range(self.img_num):
            self.imgs[i].x = self.item.x

    def draw(self):
        if self.timer is None:
            self.t2 = time.time()
            self.imgs[self.img_index].draw()
            if self.t2 - self.t1 >= 0.1:
                self.img_index += 1
                self.img_index %= self.img_num
                self.t1 = self.t2

        else:
            self.end_img.draw()
            self.timer -= 1

    def update(self):
        if self.item.x > WIDTH + 40:
            bullets.remove(self)
        for z in zombies:
            if self.item.colliderect(z.item) and self.timer is None:
                self.end()
                z.hit(self)
        if self.timer is not None and self.timer <= 0:
            bullets.remove(self)
        if self.timer is None:
            self.item.x += self.speed
            for img in self.imgs:
                img.x += self.speed


class Sun:
    x_dest = 266
    y_dest = 30
    total = 1500

    def __init__(self, sunflower):
        self.is_collecting = False
        self.item = Actor('sun')
        self.step = 20
        self.life = 1000
        self.vx = 3 + random.uniform(0, 5)
        self.vy = -4
        self.v0 = 4
        self.g = 0.5
        self.item.x = sunflower.item.x
        self.item.y = sunflower.item.y
        suns.append(self)

    def draw(self):
        self.item.draw()

    def update(self):
        if self.is_collecting:
            self.item.x -= self.vx
            self.item.y -= self.vy
            if self.item.x < Sun.x_dest and self.item.y < Sun.y_dest:
                suns.remove(self)
                Sun.total += 25
        elif self.step >= 0:
            self.item.x += self.vx
            self.item.y += self.vy
            self.vy += self.g
            self.step -= 1
        self.life -= 1
        if self.life <= 0:
            suns.remove(self)

    def update_with_mouse_down(self, pos):
        if self.item.collidepoint(pos):
            self.collect()

    def collect(self):
        sounds.sun.play()
        self.is_collecting = True
        c = (((self.item.x - Sun.x_dest) ** 2 + (self.item.y - Sun.y_dest) ** 2) ** 0.5)
        self.vx = self.v0 * (self.item.x - Sun.x_dest) / c
        self.vy = self.v0 * (self.item.y - Sun.y_dest) / c


class FireTree(Plant):
    def __init__(self):
        name = 'firetree'
        super().__init__(name)
        self.img_num = 9
        for i in range(self.img_num):
            self.imgs.append(Actor(name + '_' + str(i)))

    def update(self):
        for i in range(len(bullets)):
            if self.item.colliderect(bullets[i].item) and type(bullets[i]) is not FireBullet:
                sounds.fire.play()
                temp = bullets[i]
                bullets[i] = FireBullet(self.i, self.j)
                bullets[i].set_pos(temp)


class Zombie:
    wall = 220
    eat_damage = 10
    zombie_pos = []
    pos_0 = 30
    zombie_map = [0 for temp in range(h)]
    for i in range(h):
        zombie_pos.append([pos_0 + i * 100, pos_0 + (i + 1) * 100])

    def __init__(self, name):
        self.is_iced = None
        self.speed = -0.3
        self.slow_down = 1
        self.blood = 100
        self.hit_img = Actor(name + '_hit')
        self.is_hit = False
        self.i = -1
        self.t2 = None
        self.item = Actor(name)
        self.img_num = None
        self.img_index = 0
        self.imgs = []
        self.eat_img_num = None
        self.eat_img_index = 0
        self.eat_imgs = []
        self.ice_imgs = []
        self.ice_eat_imgs = []
        self.t1 = time.time()
        self.is_eating = False
        self.eat_bias = 10
        self.death_imgs = [[], []]
        self.death_img_num = (10, 12)
        self.death_t1 = [time.time(), time.time()]
        self.death_t2 = [None, None]
        self.is_death = None
        self.death_img_index = [0, 0]
        for i in range(self.death_img_num[0]):
            self.death_imgs[0].append(Actor('zombie_death_' + str(i)))
        for i in range(self.death_img_num[1]):
            self.death_imgs[1].append(Actor('zombie_head_' + str(i)))

    def draw(self):
        if self.is_death is None:
            self.t2 = time.time()
            if self.is_eating:
                if self.is_iced is None:
                    self.eat_imgs[self.eat_img_index].draw()
                elif self.is_iced >= 0:
                    self.ice_eat_imgs[self.eat_img_index].draw()
                if self.t2 - self.t1 >= 0.15 * self.slow_down:
                    if self.eat_img_index % 5 == 0:
                        sounds.be_eat.play()
                    self.eat_img_index += 1
                    self.eat_img_index %= self.eat_img_num
                    self.t1 = self.t2
            else:
                if self.is_iced is None:
                    self.imgs[self.img_index].draw()
                elif self.is_iced >= 0:
                    self.ice_imgs[self.img_index].draw()
                if self.t2 - self.t1 >= 0.15 * self.slow_down:
                    self.img_index += 1
                    self.img_index %= self.img_num
                    self.t1 = self.t2
            if self.is_hit:
                self.hit_img.x = self.item.x
                if self.is_eating:
                    self.hit_img.x += self.eat_bias
                self.hit_img.y = self.item.y
                self.hit_img.draw()
        else:
            self.death_t2 = [time.time(), time.time()]
            self.death_imgs[0][self.death_img_index[0]].draw()
            self.death_imgs[1][self.death_img_index[1]].draw()
            if self.death_t2[0] - self.death_t1[0] >= 0.1:
                if self.death_img_index[0] < self.death_img_num[0] - 1:
                    self.death_img_index[0] += 1
                    self.death_t1[0] = self.death_t2[0]
            if self.death_t2[1] - self.death_t1[1] >= 0.05:
                if self.death_img_index[1] < self.death_img_num[1] - 1:
                    self.death_img_index[1] += 1
                    self.death_t1[1] = self.death_t2[1]

    def out_ice(self):
        self.slow_down = 1
        self.is_iced = None

    def update(self):
        if self.is_death is None:
            if self.is_iced is not None:
                self.is_iced -= 1
                if self.is_iced <= 0:
                    self.out_ice()
            if self.is_hit > 0:
                self.is_hit -= 1
            if not self.is_eating:
                self.item.x += self.speed / self.slow_down
                for i in range(self.img_num):
                    self.imgs[i].x += self.speed / self.slow_down
                    self.ice_imgs[i].x += self.speed / self.slow_down
            else:
                for plant in plants:
                    if not plant.item.colliderect(self.item):
                        self.is_eating = False
            for plant in plants:
                if plant.item.colliderect(self.item):
                    self.eat()
                    if plant.be_eat(self):
                        self.is_eating = False
            if self.wall >= self.item.x > 0:
                self.eat()
                ui.win_map[self.i] = True
        else:
            self.is_death -= 1
            if self.is_death <= 0:
                zombies.remove(self)

    def set_pos(self, x, y):
        xx = x
        yy = 0
        self.item.x = x
        for pp in Zombie.zombie_pos:
            self.i += 1
            if pp[0] <= y <= pp[1]:
                self.item.y = pp[1]
                yy = pp[1]
                break
        if y > Zombie.zombie_pos[-1][1]:
            self.item.y = Zombie.zombie_pos[-1][1]
            yy = Zombie.zombie_pos[-1][1]
            self.i = len(Zombie.zombie_pos) - 1
        Zombie.zombie_map[self.i] += 1
        for i in range(self.img_num):
            self.imgs[i].x = xx
            self.imgs[i].y = yy
            self.ice_imgs[i].x = xx
            self.ice_imgs[i].y = yy

    def be_iced(self):
        self.slow_down = 2
        self.is_iced = 300

    def hit_sound(self):
        sounds.be_hit.play()

    def hit(self, bullet):
        if type(bullet) is not Tomato:
            self.hit_sound()
        self.blood -= bullet.damage
        if self.zombie_map[self.i] > 1 and type(bullet) is Tomato:
            for z in zombies:
                if z != self and z.i == self.i and abs(z.item.x - bullet.item.x) <= 100:
                    z.die()
        if type(bullet) is IceBullet:
            self.be_iced()
        self.is_hit = 3
        if self.blood <= 0:
            self.die()

    def eat(self):
        self.is_eating = True
        for img in self.eat_imgs:
            img.x = self.item.x
            img.y = self.item.y
        for img in self.ice_eat_imgs:
            img.x = self.item.x
            img.y = self.item.y

    def die(self):
        Zombie.zombie_map[self.i] -= 1
        sounds.zombie_end.play()
        for img in self.death_imgs[0]:
            img.x = self.item.x
            img.y = self.item.y
        for img in self.death_imgs[1]:
            img.x = self.item.x
            img.y = self.item.y
        self.is_death = 100
        self.item.x = -1
        self.item.y = -1


class NormalZombie(Zombie):
    def __init__(self):
        name = 'normal'
        super().__init__(name)
        self.eat_img_num = 21
        self.img_num = 18
        for i in range(self.img_num):
            self.imgs.append(Actor(name + '_' + str(i)))
            self.ice_imgs.append(Actor(f'ice_{name}_{str(i)}'))
        for i in range(self.eat_img_num):
            self.eat_imgs.append(Actor(name + '_eat_' + str(i)))
            self.ice_eat_imgs.append(Actor(f'ice_{name}_eat_{str(i)}'))


class BucketZombie(Zombie):
    def __init__(self):
        name = 'bucket'
        super().__init__(name)
        self.blood = 500
        self.img_num = 15
        self.eat_img_num = 11
        for i in range(self.img_num):
            self.imgs.append(Actor(name + '_' + str(i)))
            self.ice_imgs.append(Actor(f'ice_{name}_{str(i)}'))
        for i in range(self.eat_img_num):
            self.eat_imgs.append(Actor(name + '_eat_' + str(i)))
            self.ice_eat_imgs.append(Actor(f'ice_{name}_eat_{str(i)}'))

    def hit_sound(self):
        sounds.bucket_hit.play()


class FootballZombie(Zombie):
    def __init__(self):
        name = 'football'
        super().__init__(name)
        self.slow_down = 0.5
        self.speed = -0.8
        self.blood = 500
        self.img_num = 11
        self.eat_img_num = 10
        for i in range(self.img_num):
            self.imgs.append(Actor(name + '_' + str(i)))
            self.ice_imgs.append(Actor(f'ice_{name}_{str(i)}'))
        for i in range(self.eat_img_num):
            self.eat_imgs.append(Actor(name + '_eat_' + str(i)))
            self.ice_eat_imgs.append(Actor(f'ice_{name}_eat_{str(i)}'))
        self.death_imgs = [[], []]
        self.death_img_num = (10, 7)
        self.death_t1 = [time.time(), time.time()]
        self.death_t2 = [None, None]
        self.is_death = None
        self.death_img_index = [0, 0]
        for i in range(self.death_img_num[0]):
            self.death_imgs[0].append(Actor(name + '_death_' + str(i)))
        for i in range(self.death_img_num[1]):
            self.death_imgs[1].append(Actor('zombie_head_' + str(i)))

    def out_ice(self):
        self.slow_down = 0.5
        self.is_iced = None


zombies = []
plants = []
bullets = []
suns = []
ui = UserInterface()


def draw():
    if not ui.start:
        ui.start_draw()
    else:
        ui.draw()
        for plant in plants:
            plant.draw()
        for z in zombies:
            z.draw()
        for bullet in bullets:
            bullet.draw()
        for sun in suns:
            sun.draw()
        ui.draw_zombie()
        ui.draw_last()
    pass


def update():
    for z in zombies:
        z.update()
    for plant in plants:
        plant.update()
    for bullet in bullets:
        bullet.update()
    for sun in suns:
        sun.update()
    ui.update()
    pass


def on_mouse_move(pos):
    ui.update_with_mouse_move(pos)
    pass


def on_mouse_down(pos):
    global ui
    ui.update_with_mouse_down(pos)
    for sun in suns:
        sun.update_with_mouse_down(pos)


pgzrun.go()
