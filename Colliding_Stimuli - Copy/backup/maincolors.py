### Jan 22 2024 test 2
# %%
import logtocsv
# logtocsv.write_data(string)
# NOTE: Change over delay can be to or from given ball
import pygame
import sys
import os
import numpy as np
from backup.ExperimentConfigWindow import ExperimentConfigWindow  # from ExperimentConfigWindow import ExperimentConfigWindow
import tkinter as tk
# from tkinter import filedialog

from time import strftime # see format codes: https://docs.python.org/3/library/datetime.html#format-codes

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


############## INIT all values with defaults ########################
current_total_time = 0
current_phase_time = 0
start_time = 0
end_time = 0
current_phase = 1
number_phases = 2
phase_duration = 5
number_balls = 3
phase_values=None
returnedvalues = None
values=None
yoked = False
debug = False

scoring_intervals = [1,1,1,1,1,1,1]
variable_interval = [(.5,1.5),(.5,1.5),(.5,1.5),(.5,1.5),(.5,1.5),(.5,1.5),(.5,1.5)]#(min,max) # FLOAT!

reinforcement_ratio = [1,1,1,1,1,1,1]
variable_ratio = [(2,4),(2,4),(2,4),(2,4),(2,4),(2,4),(2,4)]#(min,max) #REMEMBER!  INT

change_from_delay = [2,2,2,2,2,2,2] # We will take the min and max of this
change_to_delay = [1,1,1,1,1,1,1]

initial_speed = [1,1,1,1,1,1,1]
speed_limits = [(.5,1.5),(.5,1.5),(.5,1.5),(.5,1.5),(.5,1.5),(.5,1.5),(.5,1.5)]#(min,max)

ball_colors = [BLUE, RED, GREEN, YELLOW, ORANGE, INDIGO, VIOLET]  # Rainbow colors
# Modify Clicked Colors Here NOTE: TODO: michael fix colors here
#  Blue Red Green Yellow
clicked_color = [DARK_BLUE, DARK_RED, DARK_GREEN, DARK_YELLOW, DARK_ORANGE, DARK_INDIGO, DARK_VIOLET]#[DARK_BLUE, DARK_RED, DARK_ORANGE, DARK_YELLOW, DARK_GREEN,  DARK_INDIGO, DARK_VIOLET]  # Darker shades of rainbow colors
radii = [60,60,60,60,60,60,60]
change_over_delay = [2,2,2,2,2,2,2]
block_score_until_time = [0,0,0,0,0,0,0]
block_score_until_clicks = [0,0,0,0,0,0,0]

phases = []
for n in range(number_phases):
    phase_values = {
        'phase_duration': phase_duration,
        'number_balls': phase_duration,
        'scoring_intervals':scoring_intervals,
        'variable_interval':variable_interval,
        'reinforcement_ratio':reinforcement_ratio,
        'variable_ratio':variable_ratio,
        'change_from_delay':change_from_delay,
        'change_to_delay':change_to_delay,
        'initial_speed': initial_speed,
        'speed_limits': speed_limits,
        'ball_colors': ball_colors,
        'clicked_colors':clicked_colors,
        'radii':radii,
        'block_score_until_time':block_score_until_time,
        'block_score_until_clicks':block_score_until_clicks        
    }
    
print(phase_values)
# Initialize Pygame
pygame.init()
# pygame.font.init()
font = pygame.font.Font(None, 36)  # Choose a font and size


experimentdate = strftime('%a %d %b %Y, %I:%M%p')
logtocsv.write_data(experimentdate)
print('experiment date:',experimentdate)

# Set up the window
os.environ["SDL_VIDEO_CENTERED"] = "1"
clock = pygame.time.Clock()
padding = 300
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
    "DARK_VIOLET": (80, 0, 80)
}

SQUARE_COLOR = (255, 255, 255)
SQUARE_THICKNESS = 4

reverse_lookup = {v: k for k, v in color_names.items()}

text_rect = None
# %%
class Balls:

    def __init__(self, x, y, dx, dy, radius, ball_color, clicked_color,min_score_delay,speed_limits,change_over_delay,scoring_intervals,reinforcement_ratio):#reinforcement_ratio
        print('Speed limits',speed_limits)
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.min_speed = speed_limits[0] 
        self.max_speed = speed_limits[1]
        self.radius = radius
        self.clicked_color = clicked_color
        self.default_color = ball_color
        self.color = ball_color
        self.colorname = reverse_lookup.get(self.color, "Unknown Color")
        self.clicked = False
        self.clicks = 0
        self.score = 0
        self.block_score_until_time = 0
        self.min_score_delay = min_score_delay
        self.change_over_delay = change_over_delay
        self.no_score_until = 0
        self.valid_clicks = 0 # set the amount of clicks to zero, so we can use the fixed ratio & interval
        self.scoring_intervals = scoring_intervals
        
        self.reinforcement_ratio = reinforcement_ratio

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
    def __init__(self, number_balls, radii): #def __init__(self, number_balls, radius=100, ball_colors=None, clicked_colors=None):
        global ball_colors, clicked_colors
        ball_colors = ball_colors  #ball_colors = ball_colors or [(0, 0, 255) for _ in range(number_balls)]
        clicked_colors = clicked_colors or [(128, 128, 128) for _ in range(number_balls)]
        self.balls = self.init_balls(number_balls, radii, ball_colors, clicked_colors,initial_speed,speed_limits,scoring_intervals,change_over_delay,block_score_until_time,reinforcement_ratio) #Init balls by passing values

    def init_balls(self, number_balls, radii, ball_colors, clicked_colors,initial_speed,speed_limits,min_score_delay,change_over_delay,block_score_until,reinforcement_ratio):
        balls = []
        logtocsv.write_data(('################# INIT balls ######################'))

        event_string = str(current_seconds) + ', Init stimuli, ' + str(total_score) + ', '  # event_string = str(pygame.time.get_ticks()/1000) + ', Init stimuli, ' + str(total_score) + ', '

        for i in range(int(number_balls)):  
            # reinforcement_ratio = reinforcement_ratio[i]  
            radius = radii[i]
            speed = initial_speed[i]/10

            while True:
                x = np.random.uniform(radius, windowX - radii[i])
                y = np.random.uniform(radius, windowY - radii[i])
                angle = np.random.uniform(0, 2 * np.pi)  # Angle in radians

                # Generate random signs for direction
                dx_sign = np.random.choice([-1, 1])
                dy_sign = np.random.choice([-1, 1])

                # # Calculate dx and dy with both speed and direction
                dx = dx_sign * speed * np.cos(angle)
                dy = dy_sign * speed * np.sin(angle)
                color = ball_colors[i]
                radius = radii[i]
                # ball_color = reverse_lookup.get(color)
                print('Fixed Ratio',reinforcement_ratio)
                ball = Balls(x, y, dx, dy, radius,ball_colors[i],clicked_colors[i],min_score_delay[i],speed_limits[i],block_score_until[i],scoring_intervals[i],reinforcement_ratio[i]) # ball = ball(x, y, dx, dy, radius, color, ball_colors[i],clicked_colors[i],min_score_delay[i],change_over_delay[i],block_score_until[i],scoring_intervals[i],reinforcement_ratio[i])
                event_string += str(ball.colorname)+ ' x='+ str(int(ball.x)) + ' y='+ str(int(ball.y)) + ' dx='+ str((ball.dx))+ ' dy='+ str((ball.dy)) + ' clicks='+ str((ball.clicks))+ ' score='+ str((ball.score))+', '

                ### TODO: overlaps check here and edit 
                overlaps = any(
                    np.hypot(ball.x - p.x, ball.y - p.y) < ball.radius + p.radius
                    or np.hypot(ball.x - p.x, ball.y - p.y) < p.radius - ball.radius
                    for p in balls
                )

                if not overlaps:
                    print('Appending ball to list')
                    balls.append(ball)
                    break
                else:
                    print('Overlap Detected')
                color = reverse_lookup.get(ball.color, "Unknown Color")
                event_string += ' ' + str(color) +':'
                event_string += ' x='+ str(int(ball.x)) +', '+ ' y='+ str(int(ball.y))+', ' + ' dx='+ str((ball.dx))+ ', '+' dy='+ str((ball.dy))  +', '+' clicks='+ str((ball.clicks))+', '+' score='+ str((ball.score))+','

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
    global screen, windowX, windowY, bounce_box_right, bounce_box_top, square_rect, font, current_phase, number_phases, text_rect, current_seconds,clicked_on_ball, total_score, phase_duration, end_time, phase_values,returnedvalues
    # callback()
    logtocsv.write_data(('################# Phase '+str(current_phase)+' ######################'))
    clock = pygame.time.Clock()
    sim = Simulation(number_balls, radii)

    shuffle_button_rect = pygame.Rect(windowX - 150, 20, 120, 30)
    shuffle_button_color = (255, 100, 100)

    total_score = 0

    # while True:
    print(current_seconds)
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

                            # ball.block_score_until_time = current_seconds + ball.min_score_delay
                            clicked_on_ball = True
                            ball.darken_color()
                            ball.clicked = True
                            ball.clicks += 1
                            # color = reverse_lookup.get(ball.color, "Unknown Color")
                            #clicked_color = reverse_lookup.get(ball.color, "Unknown Color") #ball.color
                            event_string += "Clicked: "+ball.colorname +', '
                            event_string += 'x='+ str(event.pos[0])+', ' + ' y='+ str(event.pos[1])+', '
                            if current_seconds < ball.block_score_until_time:
                                print('clicked:',ball.colorname,current_seconds , "can't score now, score blocked by time", end='')
                                for ball in sim.balls:
                                    print(ball.block_score_until_time, end=' ,')
                                print('')
                                break
                            elif current_seconds >= ball.block_score_until_time:
                                print('scored at',current_seconds,'Was blocked until: ',ball.block_score_until_time)
                                ball.score += 1
                                total_score +=1
                                ball.block_score_until_time = current_seconds + ball.min_score_delay
                                for ball in sim.balls:
                                    if np.hypot(event.pos[0] - ball.x, event.pos[1] - ball.y) < ball.radius:
                                        pass
                                    else:
                                        ball.block_score_until_time = current_seconds + ball.change_over_delay

                if not clicked_on_ball and not shuffle_button_rect.collidepoint(event.pos):
                    event_string += 'Clicked: None, '
                    event_string += f'x={event.pos[0]}, y={event.pos[1]}, '

                clicked_on_ball = False
                if shuffle_button_rect.collidepoint(event.pos):
                    # Check if the shuffle button is clicked
                    sim = Simulation(number_balls, radii)  # Create a new simulation to reorient all balls
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
        clock.tick(30)
    current_phase += 1
    print('Current time',current_seconds,'end tiime',end_time)
    if current_phase <= number_phases:
        print('Current Phase',current_phase,'Number of Phases',number_phases,'Current time',current_seconds,'end time:',end_time,'Phase time:',phase_duration)
        phase_duration = phase_values[current_phase-1]['duration_of_phase'] # GET all values like thisvalues[0]['number_phases'] # GET all values like this values[current_phase-1]['phase_duration'] # GET all values like this
        print('phase time',phase_duration)
        # end_time = current_seconds+int(phase_duration)
        clock = pygame.time.Clock()
        load_phase_settings()
        main()
# %%
if __name__ == "__main__":
    root_main = tk.Tk()

    def load_phase_settings():
        global phase_duration, number_phases, phase_values, end_time, clock, start_time, initial_speed, number_balls, values, radii, ball_colors, clicked_colors
        clock = pygame.time.Clock()  # Reset the clock
        start_time = pygame.time.get_ticks()/1000
        phase_duration = phase_values[current_phase-1]['duration_of_phase']  # GET all values like this
        end_time = current_seconds + int(phase_duration)  # end_time += pygame.time.get_ticks()/1000+int(phase_duration)
        # number_balls = phase_values[current_phase-1]['number_balls']
        # radii= phase_values[current_phase-1]['radii']
        # radii = radii.strip('[]')
        # radii = [int(value) for value in radii.split(',')]
        initial_speed_str = phase_values[current_phase-1]['initial_speeds']
        initial_speed_str = initial_speed_str.strip('[]')  # Remove brackets # initial_speed = [value.strip("[]") for value in initial_speed]
        ball_colors = [color.strip('[]') for color in phase_values[current_phase-1]['ball_colors'].split()]
        #ball_colors = (phase_values[current_phase-1]['ball_colors'].split()).strip('[]') # phase_values[current_phase-1]['ball_colors']  #phase_values[current_phase-1]['ball_colors']
        clicked_colors = [clicked_color.strip('[]') for clicked_color in phase_values[current_phase-1]['clicked_colors'].split()] if phase_values[current_phase-1]['clicked_colors'] is not None else []


        try:
            initial_speed = [float(value) for value in initial_speed_str.split(',')] # initial_speed = [int(value) for value in initial_speed]
        except:
            print('Had to select default initial speeds, fix the program you dummy!')
            initial_speed = [1,1,1,1,1,1,1]#[float(value) for value in initial_speed_str.split(',')] # initial_speed = [int(value) for value in initial_speed]

    def callback(returnedvalues): # reassign all values
        global phase_duration, number_phases, phase_values, end_time, clock, start_time, initial_speed, number_balls, values, radii
        start_time = pygame.time.get_ticks()/1000
        number_phases = returnedvalues[0]['number_phases']
        print('Returned Values',returnedvalues)
        phase_values = returnedvalues
        config_window.root.destroy()
        load_phase_settings()

    # Create an instance of the ExperimentConfigWindow class
    config_window = ExperimentConfigWindow(root_main)
    config_window.callback = callback  # Set the callback attribute

    # Start the Tkinter event loop
    root_main.mainloop()
    main()
print(current_seconds)

