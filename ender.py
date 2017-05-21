import random, math
import pygame
pygame.init()

WIDTH, HEIGHT = 1000, 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((0, 0, 0))

class Field():
    def generate(self):
        star = pygame.transform.scale(pygame.image.load("star.png"), (100, 100))
        starPos = [[int(WIDTH*(1/3)-50), int(HEIGHT*(1/4)-50)],
                   [int(WIDTH*(1/3)-50), int(HEIGHT*(3/4)-50)],
                   [int(WIDTH*(2/3)-50), int(HEIGHT*(1/4)-50)],
                   [int(WIDTH*(2/3)-50), int(HEIGHT*(3/4)-50)],
                   [int(WIDTH*(1/2)-50), int(HEIGHT*(1/2)-50)]]
        for pos in starPos:
            screen.blit(star, pos)
        pygame.draw.circle(screen, (255, 127, 0), (-200, int(HEIGHT/2)), 250)
        pygame.draw.circle(screen, (0, 255, 127), (WIDTH+200, int(HEIGHT/2)), 250)

class Player():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.heading = math.atan((WIDTH/2-x)/(HEIGHT/2-y))
        if self.y > WIDTH/2:
            self.heading += math.pi
        self.color = color
    def generate(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 30)
        #if self.y < HEIGHT/2:
        #    line_end = (40*math.sin(self.heading)+self.x,
        #                40*math.cos(self.heading)+self.y)
        #else:
        #    line_end = (-40*math.sin(self.heading)+self.x,
        #                -40*math.cos(self.heading)+self.y)
        line_end = (40*math.sin(self.heading)+self.x,
                    40*math.cos(self.heading)+self.y)
        pygame.draw.line(screen, self.color, (self.x, self.y), line_end, 5)
    def turn(self, h):
        self.heading += h
    def move(self):
        line_end = (20*math.sin(self.heading)+self.x,
                    20*math.cos(self.heading)+self.y)
        #if self.y < HEIGHT/2:
        #    line_end = (20*math.sin(self.heading)+self.x,
        #                20*math.cos(self.heading)+self.y)
        #else:
        #    line_end = (-20*math.sin(self.heading)+self.x,
        #                -20*math.cos(self.heading)+self.y)
        self.x, self.y = line_end
        self.x, self.y = int(self.x), int(self.y)

    def check_collision(self):
        collisionZones = [[int(WIDTH*(1/3)-80), int(HEIGHT*(1/4)-80)],
                          [int(WIDTH*(1/3)-80), int(HEIGHT*(3/4)-80)],
                          [int(WIDTH*(2/3)-80), int(HEIGHT*(1/4)-80)],
                          [int(WIDTH*(2/3)-80), int(HEIGHT*(3/4)-80)],
                          [int(WIDTH*(1/2)-80), int(HEIGHT*(1/2)-80)]]
        while self.heading > 2*math.pi:
            self.heading -= 2*math.pi
        while self.heading < 0:
            self.heading +=2*math.pi
        for zone in collisionZones:
            if zone[0] < self.x < zone[0]+160 and \
               zone[1] < self.y < zone[1]+160:
                if self.y < zone[1]+30:
                    if self.x < zone[0]+30 or self.x > zone[0]+130:
                        print("Collision with top corner")
                        self.heading -= math.pi
                        if self.x < zone[0]+30:
                            self.x, self.y = zone[0]-10, zone[1]-10
                        else:
                            self.x, self.y = zone[0]+170, zone[1]-10
                    else:
                        print("Collision with top side")
                        print(self.heading)
                        if self.heading > math.pi:
                            self.heading -= math.pi/2
                        else:
                            self.heading += math.pi/2
                        self.y = zone[1]-10
                elif self.y > zone[1]+130:
                    if self.x < zone[0]+30 or self.x > zone[0]+130:
                        print("Collision with bottom corner")
                        self.heading -= math.pi
                        if self.x < zone[0]+30:
                            self.x, self.y = zone[0]-10, zone[1]+170
                        else:
                            self.x, self.y = zone[0]+170, zone[1]+170
                    else:
                        print("Collision with bottom side")
                        print(self.heading)
                        if self.heading > math.pi:
                            self.heading += math.pi/2
                        else:
                            self.heading -= math.pi/2
                        self.y = zone[1]+170
                else:
                    if self.x < zone[0]+80:
                        print("Collision with left side")
                        if self.heading > (3/2)*math.pi:
                            self.heading += math.pi/2
                        else:
                            self.heading -= math.pi/2
                        self.x = zone[0]-10
                    else:
                        print("Collision with right side")
                        print(self.heading)
                        if self.heading > (3/2)*math.pi:
                            self.heading += math.pi/2
                        else:
                            self.heading -= math.pi/2
                        self.x = zone[0]+170

            if self.y < 10:
                print("Collision with top")
                if self.heading > math.pi:
                    self.heading += math.pi/2
                else:
                    self.heading -= math.pi/2
                self.y = 15
            elif self.y > HEIGHT-10:
                print("Collision with bottom")
                if self.heading > math.pi:
                    self.heading -= math.pi/2
                else:
                    self.heading += math.pi/2
                self.y = HEIGHT-15
            if self.x < 10:
                print("Collision with left")
                if self.heading > (3/2)*math.pi:
                    self.heading += math.pi/2
                else:
                    self.heading -= math.pi/2
                self.x = 15
            elif self.x > WIDTH-10:
                print("Collision with right")
                if self.heading > (3/2)*math.pi:
                    self.heading += math.pi/2
                else:
                    self.heading -= math.pi/2
                self.x = WIDTH-10


f = Field()
f.generate()

players = [Player(60, 60, (0, 255, 127)),
           Player(60, HEIGHT-60, (0, 255, 127)),
           Player(WIDTH-60, 60, (255, 127, 0)),
           Player(WIDTH-60, HEIGHT-60, (255, 127, 0))]

for p in players:
    p.generate()

q = False
while not q:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            q = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                q = True
            elif event.key == ord("a"):
                players[0].turn(0.5)
            elif event.key == ord("s"):
                players[0].turn(-0.5)
            elif event.key == ord("w"):
                players[0].move()
            elif event.key == ord("f"):
                players[1].turn(0.5)
            elif event.key == ord("g"):
                players[1].turn(-0.5)
            elif event.key == ord("t"):
                players[1].move()
            elif event.key == ord("h"):
                players[2].turn(0.5)
            elif event.key == ord("j"):
                players[2].turn(-0.5)
            elif event.key == ord("u"):
                players[2].move()
            elif event.key == ord("k"):
                players[3].turn(0.5)
            elif event.key == ord("l"):
                players[3].turn(-0.5)
            elif event.key == ord("o"):
                players[3].move()

    for player in players:
        player.check_collision()

    screen.fill((0, 0, 0))

    f.generate()
    for player in players:
        player.generate()
        
    pygame.display.flip()
    
            

pygame.quit()
