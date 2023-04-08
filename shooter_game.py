from pygame import *
from random import*
font.init()
font1 = font.SysFont('Areal', 80)
win = font1.render("You win", True, (255, 255, 255))
los1 = font1.render("you lost", True, (180, 0, 0))

font2 = font.SysFont('Areal', 36)
goal = 10

#фоновая музыка
mixer.init()
mixer.music.load('Instasamka_-_ZA_DENGI_DA_75137048.mp3')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')



#нам нужны такие картинки:
img_back = "galaxy.jpg" #фон игры
img_hero = "rocket.png" #герой
img_enemy = "ufo.png"
img_bullet =  "bullet.png"

score = 0
lost = 0

#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)


       #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed


       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 #метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#класс главного игрока
class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 #метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(sprite.Sprite):
    def update(self):
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if  self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
        
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

#Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


#создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()

for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()



#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
while run:
   #событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()    

    if not finish:
        #обновляем фон
        window.blit(background,(0,0))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score +1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= 3:
            finish = True
            window.blit(los1, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render('Убил:' + str(score), 1, (255, 255,255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропустил:" + str(lost), 1, (255, 255,255))
        window.blit(text_lose, (10, 50))

       #производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()

       #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
    #цикл срабатывает каждые 0.05 секунд
    time.delay(20)
