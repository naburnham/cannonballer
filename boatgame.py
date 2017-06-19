import pygame
import random
import time

pygame.init()

# Pre-made Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
dark_red = (200, 0, 0)
green = (0, 255, 0)
dark_green = (0, 200, 0)
blue = (0, 0, 255)
light_blue = (175, 225, 255)

# Pre-defined Fonts
large_text = pygame.font.SysFont('arialblack', 100)
medium_text = pygame.font.SysFont('arial', 50)
small_text = pygame.font.SysFont('arial', 25)

# Game Display Settings
display_width = 1200
display_height = 675
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Cannonballer')
clock = pygame.time.Clock()

# Images
boat_img = pygame.image.load('playerboat.png')
enemy_boat_img = pygame.image.load('enemyboat.png')
cannonball_img = pygame.image.load('cannonball.png')

# Various Game Variables
level = 0
count = 0
timer = 1000
level_count = 0
start_boats = 3
points_per_boat = 250


def level_and_score(p_level, score):
    """ Displays the players level+1 and Score in the upper left hand corner of the screen """
    font = small_text
    text = font.render('Level: {}, Score: {}'.format(str(p_level+1), str(score)), True, black)
    game_display.blit(text, (5, 5))


def button(message, x, y, width, height, inactive_color, hover_color, command=None):
    """ Make an interactive button with text """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(game_display, hover_color, (x, y, width, height))
        if click[0] == 1 and command is not None:
            ready_level()
            command()
    else:
        pygame.draw.rect(game_display, inactive_color, (x, y, width, height))

    text_surface, text_rect = text_objects(message, small_text)
    text_rect.center = (x + (width / 2), y + (height / 2))
    game_display.blit(text_surface, text_rect)


def exit_game():
    """ Exits the Game """
    pygame.quit()
    quit()


def start_screen():
    """ The initial and between level landing screen """
    global level
    global count

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
        game_display.fill(white)
        start_screen_title('Cannonballer')

        button('Go!', 350, 450, 100, 50, dark_green, green, game_loop)
        button('Quit', 750, 450, 100, 50, dark_red, red, exit_game)

        instructions('W: Fire Cannonball  A: Move Left  D: Move Right')

        if level == 0 and count == 0:
            pass
        else:
            level_and_score(level, count)
        pygame.display.update()
        clock.tick(60)


def text_objects(message, font):
    text_surface = font.render(message, True, black)
    return text_surface, text_surface.get_rect()


def instructions(message):
    """ Writes a medium message near top of screen, centered """
    text_surface, text_rect = text_objects(message, medium_text)
    text_rect.center = ((display_width/2), 115)
    game_display.blit(text_surface, text_rect)


def start_screen_title(message):
    """ Displays game title on the start screen """
    text_surface, text_rect = text_objects(message, large_text)
    text_rect.center = ((display_width / 2), (display_height / 2))
    game_display.blit(text_surface, text_rect)


def message_display(message):
    """ Writes large message in center of screen """
    text_surface, text_rect = text_objects(message, large_text)
    text_rect.center = ((display_width/2), (display_height/2))
    game_display.blit(text_surface, text_rect)

    pygame.display.update()


class Cannonball:
    def __init__(self, cannonball_image, x, y, width=16, height=16):
        self.cannonball_image = cannonball_image
        self.width = width
        self.height = height
        self.y = y
        self.x = x

    def cannonball_display(self):
        game_display.blit(self.cannonball_image, (self.x, self.y))

    def update(self, y_change):
        """ Updates position of cannonball, then checks to see if it hits a boat.
        If hit boat, destroy boat. If boat player: you lose, else: Score +points.
        If position is off screen, destroys self.
        """
        global level
        global count
        global level_count
        global points_per_boat

        self.y += y_change
        if player.y + player.height > self.y > player.y - int(self.height/2):
            if player.x < self.x < player.x + player.width or player.x < self.x + self.width < player.x + player.width:
                message_display('You Were Hit!')
                reset_variables()
                time.sleep(1)
                start_screen()
        else:
            for boat in range(len(enemy_boats)-1, -1, -1):
                if enemy_boats[boat].y + enemy_boats[boat].height > self.y + self.height:
                    if enemy_boats[boat].x < self.x < enemy_boats[boat].x + enemy_boats[boat].width or \
                                            enemy_boats[boat].x < self.x + self.width < enemy_boats[boat].x + \
                                            enemy_boats[boat].width:
                        del enemy_boats[boat]
                        count += points_per_boat
        if self.y > display_height:
            del enemy_cannonballs[0]
        if self.y < 0:
            del player_cannonballs[0]


class Boat:
    def __init__(self, boat_image, x, y, width=32, height=64):
        self.boat_image = boat_image
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def boat_display(self):
        game_display.blit(self.boat_image, (self.x, self.y))

    def boat_update(self, x_change):
        self.x += x_change


player_cannonballs = []
enemy_cannonballs = []
enemy_boats = []


def make_boats(number):
    global enemy_boats

    for i in range(number):
        enemy_boats.append(Boat(enemy_boat_img, ((((display_width/number)*i)+(display_width/number)/number)+16), 36))


def reset_variables():
    global level
    global count
    global timer

    level = 0
    count = 0
    timer = 1000


def ready_level():
    global enemy_cannonballs
    global player_cannonballs
    global level_count
    global enemy_boats
    global timer
    global start_boats

    enemy_cannonballs = []
    player_cannonballs = []
    enemy_boats = []
    level_count = 0
    if level > 0 and level % 4 == 0 and timer > 500:
        timer -= 100
    if level == 0:
        make_boats(start_boats)
    else:
        make_boats(start_boats + level)


def check_collisions():
    global level
    global count
    global level_count
    if player.x > display_width-player.width or player.x < 0:
        message_display('You crashed!')
        time.sleep(1)
        reset_variables()
        level_count = 0
        start_screen()


def fire(boat, i):
    if boat == player:
        cannonball = Cannonball(cannonball_img, player.x+8, player.y-8)
        player_cannonballs.append(cannonball)
    elif boat == enemy_boats[i]:
        cannonball = Cannonball(cannonball_img, enemy_boats[i].x+8, enemy_boats[i].y+enemy_boats[i].height+16)
        enemy_cannonballs.append(cannonball)


def game_loop():
    global player
    global level
    global count
    global timer

    enemy_event = pygame.NUMEVENTS - 1
    pygame.time.set_timer(enemy_event, timer)

    player_boat_x = (display_width * 0.5) - 16
    player_boat_y = display_height * 0.8
    player = Boat(boat_img, player_boat_x, player_boat_y)

    x_change = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x_change = -5
                elif event.key == pygame.K_d:
                    x_change = 5
                elif event.key == pygame.K_w:
                    fire(player, 0)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    x_change = 0

            if event.type == enemy_event:
                if enemy_boats:
                    boat = random.randrange(0, len(enemy_boats))
                    fire(enemy_boats[boat], boat)

        player_boat_x += x_change
        check_collisions()
        game_display.fill(light_blue)

        for cannonball in player_cannonballs:
            cannonball.cannonball_display()
            cannonball.update(-5)

        for cannonball in enemy_cannonballs:
            cannonball.cannonball_display()
            cannonball.update(5)

        for boat in enemy_boats:
            boat.boat_display()

        if len(enemy_boats) == 0:
            message_display('You beat Level {}!'.format(str(level+1)))
            time.sleep(1)
            level += 1
            ready_level()
            start_screen()

        level_and_score(level, count)
        player.boat_update(x_change)
        player.boat_display()

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    start_screen()
