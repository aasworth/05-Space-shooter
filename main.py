import sys, logging, json, open_color, arcade, os

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space Shooter"

NUM_ENEMIES = 16
STARTING_LOCATION = (400,100)
BULLET_DAMAGE = 10
ENEMY_HP = 50
HIT_SCORE = 1
KILL_SCORE = 10
MOVEMENT_SPEED = 5

class Bullet(arcade.Sprite):
    def __init__(self,position,velocity,damage):
        super().__init__("assets/bullet.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        self.center_x += self.dx
        self.center_y += self.dy

class Player(arcade.Sprite):

    def __init__(self):
        super().__init__("assets/playerShip1_blue.png", 0.5)
        (self.center_x, self.center_y) = STARTING_LOCATION

class Enemy(arcade.Sprite):
    def __init__(self, position):
        super().__init__("assets/ufoRed.png", 0.5)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position


class MyGame(arcade.Window):

    def __init__(self, width, height, title):

        # Call the parent class's init function
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        

        # Make the mouse disappear when it is over the window.
        # So we just see our object, not the pointer.
        self.set_mouse_visible(False)
        arcade.set_background_color(open_color.black)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0
        


    def setup(self):
        for i in range(NUM_ENEMIES//2):
            x = 90 * (i+1) 
            y = 550
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy)
        for i in range((NUM_ENEMIES//2) + 1):
            x = 90 * (i + 1) - 50
            y = 500
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy)
        for i in range(NUM_ENEMIES//2):
            x = 90 * (i + 1)
            y = 450
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy)

    def update(self, delta_time):
        self.bullet_list.update()
        if self.enemy_list:
            for e in self.enemy_list:
                collision = arcade.check_for_collision_with_list(e, self.bullet_list)
                for c in collision:
                    e.hp -= c.damage
                    c.kill()
                    self.score += HIT_SCORE
                    if e.hp <= 0:
                        e.kill()
                        self.score += KILL_SCORE
        else:
            arcade.close_window()
            print("\n")
            print("~"*30)
            print("\nYou Win! Congratulations!")
            print("\n")
            print("~"*30)
            print("\n")

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, open_color.white, 16)
        self.player.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called to update our objects. Happens approximately 60 times per second."""
        self.player.center_x = x
        

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            x = self.player.center_x
            y = self.player.center_y
            bullet = Bullet((x,y),(0,10), BULLET_DAMAGE)
            self.bullet_list.append(bullet)

           

        


    


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()