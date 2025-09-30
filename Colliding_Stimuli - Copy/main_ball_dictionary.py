# %%
## TODO: implement scoring logic checks in and around line 351!
## Remember: I added the correct attributes to the sim instance and each ball instance
## Only need to get the right ones and implement the logic
import logtocsv
# logtocsv.write_data(string)
# NOTE: Change over delay can be to or from given ball
import pygame
import sys
import os
import numpy as np
from time import strftime # see format codes: https://docs.python.org/3/library/datetime.html#format-codes

## Define colors here
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)
ORANGE = (255, 165, 0)
DARK_ORANGE = (255, 140, 0)
YELLOW = (255, 255, 0)
DARK_YELLOW = (185, 185, 0)
GREEN = (0, 128, 0)
DARK_GREEN = (0, 100, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 139)
INDIGO = (75, 0, 130)
DARK_INDIGO = (54, 0, 94)
VIOLET = (128, 0, 128)
DARK_VIOLET = (80, 0, 80)
SQUARE_COLOR = (255, 255, 255)
SQUARE_THICKNESS = 4

## Define phases here
## Add global blockers based on switching the clicked stimuli
score_clicks_required = 0
last_reinforced_ball = None
last_reinforced_time = None
reinforcement_blocked_until_time = None




phase_options = {
    "phase_1": {
        "duration" : 10,
        "number_balls": 3,
        "initial_speed": [1,1,1,1,1,1,1],
        "radii": [60,60,60,60,60,60,60],
        "base_colors" : [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET],
        "clicked_colors" : [DARK_RED, DARK_ORANGE, DARK_YELLOW, DARK_GREEN, DARK_BLUE, DARK_INDIGO, DARK_VIOLET],
        "time_required" :[0.1,0.1,0.1,0.1,0.1,0.1,0.1],
        "clicks_required" :[1,1,1,1,1,1,1],
        "change_to_clicks" : [1,1,1,1,1,1,1],
        "change_to_delay" : [1,1,1,1,1,1,1],
        "change_from_clicks" : [1,1,1,1,1,1,1],
        "change_from_delay": [1,1,1,1,1,1,1],
        "block_score_until_time":[0,0,0,0,0,0,0],
        "block_score_until_clicks" : [0,0,0,0,0,0,0],
        "yoked" : False,
        "debug" : True
    },
    "phase_2": {
        "duration" : 1,
        "number_balls": 3,
        "initial_speed": [1,1,1,1,1,1,1],
        "radii": [60,60,60,60,60,60,60],
        "base_colors" : [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET],
        "clicked_colors" : [DARK_RED, DARK_ORANGE, DARK_YELLOW, DARK_GREEN, DARK_BLUE, DARK_INDIGO, DARK_VIOLET],
        "time_required" :[0.1,0.1,0.1,0.1,0.1,0.1,0.1],
        "clicks_required" :[1,1,1,1,1,1,1],
        "change_to_clicks" : [1,1,1,1,1,1,1],
        "change_to_delay" : [1,1,1,1,1,1,1],
        "change_from_clicks" : [1,1,1,1,1,1,1],
        "change_from_delay": [1,1,1,1,1,1,1],
        "block_score_until_time":[0,0,0,0,0,0,0],
        "block_score_until_clicks" : [0,0,0,0,0,0,0],
        "yoked" : False,
        "debug" : True
    },
    "phase_3":  {
        "duration" : 1,
        "number_balls": 3,
        "initial_speed": [1,1,1,1,1,1,1],
        "radii": [60,60,60,60,60,60,60],
        "base_colors" : [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET],
        "clicked_colors" : [DARK_RED, DARK_ORANGE, DARK_YELLOW, DARK_GREEN, DARK_BLUE, DARK_INDIGO, DARK_VIOLET],
        "time_required" :[0.1,0.1,0.1,0.1,0.1,0.1,0.1],
        "clicks_required" :[1,1,1,1,1,1,1],
        "change_to_clicks" : [1,1,1,1,1,1,1],
        "change_to_delay" : [1,1,1,1,1,1,1],
        "change_from_clicks" : [1,1,1,1,1,1,1],
        "change_from_delay": [1,1,1,1,1,1,1],
        "block_score_until_time":[0,0,0,0,0,0,0],
        "block_score_until_clicks" : [0,0,0,0,0,0,0],
        "yoked" : False,
        "debug" : True
    },
}


# Initialize Pygame
pygame.init()
# pygame.font.init()
font = pygame.font.Font(None, 36)  # Choose a font and size

experimentdate = strftime('%a %d %b %Y, %I:%M%p')
logtocsv.write_data(experimentdate)

# Set up the window
os.environ["SDL_VIDEO_CENTERED"] = "1"
clock = pygame.time.Clock()
padding = 0
surface = pygame.display.set_mode()
displayX, displayY = surface.get_size()
windowX, windowY = displayX - padding, displayY - padding # Here I was subtracging padding
screen = pygame.display.set_mode((windowX, windowY), pygame.RESIZABLE,display=1)  #screen = pygame.display.set_mode((windowX, windowY), pygame.RESIZABLE,display=1)
pygame.display.set_caption("Resizable Window")

# Set up the square
square_color = (255, 0, 0)
min_margin = 20
square_size = min(windowX, windowY) - 2 * min_margin
square_rect = pygame.Rect((windowX - square_size) // 2, (windowY - square_size) // 2, square_size, square_size)

margin = 100
margin_left = margin
margin_right = margin
margin_top = margin
margin_bottom = margin
values = None

bounce_box_left = margin_left
bounce_box_right = windowX - margin_right
bounce_box_top = windowY - margin_top
square_rect = pygame.Rect((windowX - square_size) // 2, (windowY - square_size) // 2, square_size, square_size)
bounce_box_bottom = margin_bottom

#Random variables for right here:
total_score = 0
current_phase = 1
event = None
current_seconds = 0
#counters
clicked_on_ball = False

## This portion is key for our "Reverse lookup" dictionary
color_names = {
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "DARK_RED": (139, 0, 0),
    "ORANGE": (255, 165, 0),
    "DARK_ORANGE": (255, 140, 0),
    "YELLOW": (255, 255, 0),
    "DARK_YELLOW": (185, 185, 0),
    "GREEN": (0, 128, 0),
    "DARK_GREEN": (0, 100, 0),
    "BLUE": (0, 0, 255),
    "DARK_BLUE": (0, 0, 139),
    "INDIGO": (75, 0, 130),
    "DARK_INDIGO": (54, 0, 94),
    "VIOLET": (128, 0, 128),
    "DARK_VIOLET": (80, 0, 80),
    "SQUARE_COLOR": (255, 255, 255),
    "SQUARE_THICKNESS": 4,
}

reverse_lookup = {v: k for k, v in color_names.items()}

text_rect = None
# %%
class Balls:
    # ball = ball(x, y, dx, dy, radius, color, ball_color,clicked_colors[i],reinforcement_interval,change_over_delay)
    def __init__(self, phase_options, i):#fixed_ratio
        print('')
        x = np.random.uniform(phase_options['radii'][i], windowX - phase_options['radii'][i])
        y = np.random.uniform(phase_options['radii'][i], windowY - phase_options['radii'][i])
        angle = np.random.uniform(0, 2 * np.pi)  # Angle in radians

        # Generate random signs for direction
        dx_sign = np.random.choice([-1, 1])
        dy_sign = np.random.choice([-1, 1])

        # # Calculate dx and dy with both speed and direction
        dx = dx_sign * phase_options['initial_speed'][i]/10 * np.cos(angle)
        dy = dy_sign * phase_options['initial_speed'][i]/10 * np.sin(angle)
        color = base_colors[i]
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        # self.min_speed = speed
        # self.max_speed = None
        self.radius = phase_options['radii'][i]
        self.clicked_color = phase_options['clicked_colors'][i]
        self.default_color = phase_options['base_colors'][i]
        self.color = phase_options['base_colors'][i]
        self.colorname = reverse_lookup.get(self.color, "Unknown Color")
        self.clicked = False
        self.clicks = 0
        self.valid_clicks = 0 # set the amount of clicks to zero, so we can use the fixed ratio & interval
        self.score = 0
        self.block_score_until_time = phase_options['block_score_until_time'][i]
        self.block_score_until_clicks = phase_options['block_score_until_clicks'][i]
        self.change_to_clicks = phase_options['change_to_clicks'][i]
        self.change_to_delay = phase_options['change_to_delay'][i]
        self.change_from_clicks = phase_options['change_from_clicks'][i]
        self.change_from_delay = phase_options['change_from_delay'][i]
        self.time_required = phase_options['time_required'][i]
        self.clicks_required = phase_options['clicks_required'][i]
        

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def advance(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt

        if self.x - self.radius < bounce_box_left:
            self.x = bounce_box_left + self.radius
            self.dx = abs(self.dx)
        elif self.x + self.radius > bounce_box_right:
            self.x = bounce_box_right - self.radius
            self.dx = -abs(self.dx)

        if self.y - self.radius < bounce_box_bottom:
            self.y = bounce_box_bottom + self.radius
            self.dy = abs(self.dy)
        elif self.y + self.radius > bounce_box_top:
            self.y = bounce_box_top - self.radius
            self.dy = -abs(self.dy)

    def darken_color(self):
        self.color = self.clicked_color# tuple(int(c * 0.8) for c in self.color) #self.color = tuple(int(c * 0.8) for c in self.base_color)

    def reset_color(self):
        self.color = self.default_color

# %%
class Simulation:
    def __init__(self, phase_options): #def __init__(self, number_balls, radius=100, base_colors=None, clicked_colors=None):
        global base_colors, clicked_colors
        base_colors = phase_options['base_colors']  #base_colors = base_colors or [(0, 0, 255) for _ in range(number_balls)]
        self.last_clicked_ball = None
        self.last_scored_ball = None
        self.block_score_until_time = 0
        self.block_change_over_score_until_clicks = 0
        self.block_change_over_until_time = 0
        self.block_score_until_clicks = 0
        self.valid_clicks_since_score = 0
        self.total_clicks = 0
        self.balls = self.init_balls(phase_options) #Init balls by passing values

    def init_balls(self, phase_options):
        print('Phase Options')
        balls = []
        logtocsv.write_data(('################# INIT balls ######################'))
        # balls = []
        event_string = str(current_seconds) + ', Init stimuli, ' + str(total_score) + ', '  # event_string = str(pygame.time.get_ticks()/1000) + ', Init stimuli, ' + str(total_score) + ', '

        
        for i in range(int(phase_options['number_balls'])):
            while True:   
                ball = Balls(phase_options,i) 
                event_string += str(ball.colorname)+ ' x='+ str(int(ball.x)) + ' y='+ str(int(ball.y)) + ' dx='+ str((ball.dx))+ ' dy='+ str((ball.dy)) + ' clicks='+ str((ball.clicks))+ ' score='+ str((ball.score))+', '

                
                ### TODO: overlaps check here and edit 
                overlaps = any(
                    np.hypot(ball.x - p.x, ball.y - p.y) < ball.radius + p.radius
                    or np.hypot(ball.x - p.x, ball.y - p.y) < p.radius - ball.radius
                    for p in balls
                )


                color = reverse_lookup.get(ball.color, "Unknown Color")

                if not overlaps:
                    event_string += ' ' + str(color) +':'
                    event_string += ' x='+ str(int(ball.x)) +', '+ ' y='+ str(int(ball.y))+', ' + ' dx='+ str((ball.dx))+ ', '+' dy='+ str((ball.dy))  +', '+' clicks='+ str((ball.clicks))+', '+' score='+ str((ball.score))+','
                    balls.append(ball)
                    break
                else:
                    print('Overlap Detected')
        # for ball in balls:
        #     color = reverse_lookup.get(ball.color, "Unknown Color")
        #     event_string += ' ' + str(color) +':'
        #     event_string += ' x='+ str(int(ball.x)) +', '+ ' y='+ str(int(ball.y))+', ' + ' dx='+ str((ball.dx))+ ', '+' dy='+ str((ball.dy))  +', '+' clicks='+ str((ball.clicks))+', '+' score='+ str((ball.score))+','
        #     # 66.333, 0, Clicked ORANGE, x=370 y=540 RED x=688 y=431 dx=0.10210023218610983 dy=-0.11956539525490884 clicks=0 score=0 ORANGE x=355 y=557 dx=0.10852871091956233 dy=0.11269186047523638 clicks=1 score=0 YELLOW x=1177 y=538 dx=-0.11534114878188889 dy=-0.1124286037571398 clicks=0 score=0
        logtocsv.write_data(event_string)    
        return balls

    def handle_collisions(self):
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                if np.hypot(self.balls[i].x - self.balls[j].x,
                            self.balls[i].y - self.balls[j].y) < self.balls[i].radius + self.balls[
                    j].radius:
                    self.change_velocities(self.balls[i], self.balls[j])


    def change_velocities(self, p1, p2):
        m1, m2 = p1.radius ** 2, p2.radius ** 2
        M = m1 + m2
        r1, r2 = np.array([p1.x, p1.y]), np.array([p2.x, p2.y])
        d = np.linalg.norm(r1 - r2) ** 2
        v1, v2 = np.array([p1.dx, p1.dy]), np.array([p2.dx, p2.dy])
        u1 = v1 - 2 * m2 / M * np.dot(v1 - v2, r1 - r2) / d * (r1 - r2)
        u2 = v2 - 2 * m1 / M * np.dot(v2 - v1, r2 - r1) / d * (r2 - r1)
        p1.dx, p1.dy = u1
        p2.dx, p2.dy = u2

    def advance(self, dt):
        for ball in self.balls:
            ball.advance(dt)
        self.handle_collisions()
# %%
def main():
    global screen, windowX, windowY, bounce_box_right, bounce_box_top, square_rect, font, text_rect, current_seconds,clicked_on_ball, total_score, phase_duration, current_phase
    # callback()
    logtocsv.write_data(('################# Phase '+str(current_phase)+' ######################'))
    clock = pygame.time.Clock()
    # sim = Simulation()
    shuffle_button_rect = pygame.Rect(windowX - 150, 20, 120, 30)
    shuffle_button_color = (255, 100, 100)
    total_score = 0
    
    # while True:
    print(current_seconds)
    for phase in phase_options:
        sim = Simulation(phase_options[phase])
        print(phase_options[phase]["duration"])

        end_time = current_seconds + int(phase_options[phase]["duration"])
        print('End time:',end_time)
        start_time = current_seconds
        while current_seconds < end_time:
            # Handle events here
            current_seconds = pygame.time.get_ticks()/1000 - start_time
            # print(current_seconds)
            for event in pygame.event.get():
                event_string = str(current_seconds)+', ' + str(total_score) + ', '# start making my string
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # logtocsv.write_data(str(current_seconds)+' Testing doing a random string')
                        
                        for ball in sim.balls:
                            # if current_seconds > ball.block_score_until:
                            #     break
                            if np.hypot(event.pos[0] - ball.x, event.pos[1] - ball.y) < ball.radius: # Handle the clicked ball
                                # NOTE: Come here and handle scoring logic with changes!
                                # ball.block_score_until_time = current_seconds + ball.min_score_delay
                                clicked_on_ball = True
                                ball.darken_color()
                                ball.clicked = True
                                ball.clicks += 1
                                # color = reverse_lookup.get(ball.color, "Unknown Color")
                                #clicked_color = reverse_lookup.get(ball.color, "Unknown Color") #ball.color
                                event_string += "Clicked: "+ball.colorname + ', '
                                event_string += 'x='+ str(event.pos[0])+', ' + ' y=' + str(event.pos[1]) + ', '
                                if current_seconds < ball.block_score_until_time:
                                    print('clicked:',ball.colorname,current_seconds , "can't score now, score blocked by time", end='')
                                    for ball in sim.balls:
                                        print(ball.block_score_until_time, end=' ,')
                                    print('')
                                    break
                                elif current_seconds >= ball.block_score_until_time:  #TODO: Add blocker for click number
                                    print('scored at',current_seconds,'Was blocked until: ',ball.block_score_until_time)
                                    ball.score += 1
                                    total_score +=1
                                    ball.block_score_until_time = current_seconds + ball.time_required
                                    for ball in sim.balls:
                                        if np.hypot(event.pos[0] - ball.x, event.pos[1] - ball.y) < ball.radius:
                                            pass
                                        else:
                                            ball.block_score_until_time = current_seconds + ball.time_required

                    if not clicked_on_ball and not shuffle_button_rect.collidepoint(event.pos):
                        event_string += 'Clicked: None, '
                        event_string += f'x={event.pos[0]}, y={event.pos[1]}, '

                    clicked_on_ball = False
                    if shuffle_button_rect.collidepoint(event.pos):
                        # Check if the shuffle button is clicked
                        sim = Simulation(phase_options[phase])  # Create a new simulation to reorient all balls
                        event_string += 'Clicked: Shuffle, '
                        event_string += f'x={event.pos[0]}, y={event.pos[1]}, '
                        # print('Clicked: Shuffle')

                    for ball in sim.balls:
                        color = reverse_lookup.get(ball.color, "Unknown Color")
                        event_string += ' ' + str(color) +':'
                        event_string += ' x='+ str(int(ball.x)) +', '+ ' y='+ str(int(ball.y))+', ' + ' dx='+ str((ball.dx))+ ', '+' dy='+ str((ball.dy))  +', '+' clicks='+ str((ball.clicks))+', '+' score='+ str((ball.score))+','

                    logtocsv.write_data(event_string)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        for ball in sim.balls:
                            if ball.clicked:
                                ball.reset_color()
                                ball.clicked = False
                elif event.type == pygame.VIDEORESIZE:
                    windowX, windowY = event.w, event.h
                    screen = pygame.display.set_mode((windowX, windowY), pygame.RESIZABLE)
                    bounce_box_right = windowX - margin_right
                    bounce_box_top = windowY - margin_top
                    square_rect = pygame.Rect((windowX - square_size) // 2, (windowY - square_size) // 2, square_size,
                                            square_size)

            screen.fill((0, 0, 0))
            sim.advance(20.0)

            for ball in sim.balls:
                ball.draw(screen)

            pygame.draw.rect(screen, SQUARE_COLOR, (margin, margin, windowX - 2 * (margin), windowY - 2 * (margin)),
                            SQUARE_THICKNESS)
            pygame.draw.rect(screen, shuffle_button_color, shuffle_button_rect)
            text_score = font.render(f'Score: {total_score}', True, YELLOW)
            text_rect_score = text_score.get_rect(center=(windowX // 2, windowY - 60))
            screen.blit(text_score, text_rect_score)        
            font = pygame.font.Font(None, 36)
            text = font.render("Shuffle", True, (255, 255, 255))
            screen.blit(text, (windowX - 140, 25))
            pygame.display.flip()
            clock.tick(60)
        current_phase += 1
        print('Current time',current_seconds,'end tiime',end_time)

# %%
if __name__ == "__main__":

    main()
print(current_seconds)