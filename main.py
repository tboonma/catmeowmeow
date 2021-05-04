import math
from random import randint, random

import tkinter as tk

from gamelib import Sprite, GameApp, Text

from consts import *

class Fruit(Sprite):
    reward = 1
    def __init__(self, app, img, x, y):
        super().__init__(app, img, x, y)

        self.app = app
    
    def update(self):
        if self.x < -30:
            self.to_be_deleted = True

class SlowFruit(Fruit):
    def __init__(self, app, x, y):
        super().__init__(app, 'images/apple.png', x, y)

    def update(self):
        super().update()
        self.x -= FRUIT_SLOW_SPEED


class FastFruit(Fruit):
    reward = 2
    def __init__(self, app, x, y):
        super().__init__(app, 'images/banana.png', x, y)

    def update(self):
        super().update()
        self.x -= FRUIT_FAST_SPEED


class SlideFruit(Fruit):
    reward = 3
    def __init__(self, app, x, y):
        super().__init__(app, 'images/cherry.png', x, y)
        self.direction = randint(0,1)*2 - 1

    def update(self):
        super().update()
        self.x -= FRUIT_FAST_SPEED
        self.y += self.direction * 5


class CurvyFruit(Fruit):
    reward = 3
    def __init__(self, app, x, y):
        super().__init__(app, 'images/pear.png', x, y)

        self.t = randint(0,360) * 2 * math.pi / 360

    def update(self):
        super().update()
        self.x -= FRUIT_SLOW_SPEED * 1.2
        self.t += 1
        self.y += math.sin(self.t*0.08)*10


class Cat(Sprite):
    def __init__(self, app, x, y):
        super().__init__(app, 'images/cat.png', x, y)

        self.app = app
        self.direction = None

    def update(self):
        if self.direction == CAT_UP:
            if self.y >= CAT_MARGIN:
                self.y -= CAT_SPEED
            else:
                self.y = CANVAS_HEIGHT + 20
        elif self.direction == CAT_DOWN:
            if self.y <= CANVAS_HEIGHT - CAT_MARGIN:
                self.y += CAT_SPEED
            else:
                self.y = -20

    def check_collision(self, fruit):
        if self.distance_to(fruit) <= CAT_CATCH_DISTANCE:
            fruit.to_be_deleted = True
            self.app.score += 1
            self.app.update_score()


class CatGame(GameApp):
    def init_game(self):
        self.cat = Cat(self, 50, CANVAS_HEIGHT // 2)
        self.elements.append(self.cat)

        self.score = 0
        self.score_text = Text(self, 'Score: 0', 100, 40)
        self.fruits = []

    def update_score(self):
        self.score_text.set_text('Score: ' + str(self.score))

    def random_fruits(self):
        if random() > 0.95:
            p = random()
            y = randint(50, CANVAS_HEIGHT - 50)
            if p <= 0.3:
                new_fruit = SlowFruit(self, CANVAS_WIDTH, y)
            elif p <= 0.6:
                new_fruit = FastFruit(self, CANVAS_WIDTH, y)
            elif p <= 0.8:
                new_fruit = SlideFruit(self, CANVAS_WIDTH, y)
            else:
                new_fruit = CurvyFruit(self, CANVAS_WIDTH, y)

            self.fruits.append(new_fruit)

    def process_collisions(self):
        for f in self.fruits:
            self.cat.check_collision(f)

    def update_and_filter_deleted(self, elements):
        new_list = []
        for e in elements:
            e.update()
            e.render()
            if e.to_be_deleted:
                e.delete()
            else:
                new_list.append(e)
        return new_list

    def post_update(self):
        self.process_collisions()

        self.random_fruits()

        self.fruits = self.update_and_filter_deleted(self.fruits)

    def on_key_pressed(self, event):
        if event.keysym == 'Up':
            self.cat.direction = CAT_UP
        elif event.keysym == 'Down':
            self.cat.direction = CAT_DOWN
    

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Fruit Cat")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = CatGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
