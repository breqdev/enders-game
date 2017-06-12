from __future__ import division

import random, math, time
import pygame, cwiid
pygame.init()

WIDTH, HEIGHT = 1024, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
screen.fill((0, 0, 0))

class Field():
    def generate(self):
        star = pygame.transform.scale(pygame.image.load("star.png"), (100, 100))
        starPos = [[int(WIDTH*(1/3)-50), int(HEIGHT*(1/4)-50)],
                   [int(WIDTH*(1/3)-50), int(HEIGHT*(3/4)-50)],
                   [int(WIDTH*(2/3)-50), int(HEIGHT*(1/4)-50)],
                   [int(WIDTH*(2/3)-50), int(HEIGHT*(3/4)-50)]]
                   #[int(WIDTH*(1/2)-50), int(HEIGHT*(1/2)-50)]]
        for pos in starPos:
            screen.blit(star, pos)
        pygame.draw.circle(screen, (255, 127, 0), (-200, int(HEIGHT/2)), 250)
        pygame.draw.circle(screen, (0, 255, 127), (WIDTH+200, int(HEIGHT/2)), 250)

class Player():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.heading = math.atan((WIDTH/2-x)/(HEIGHT/2-y))
        if self.x > WIDTH/2:
            self.heading += math.pi
        self.color = color
        self.v = 0
        self.frozen = False
        
    def generate(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 30)
        #if self.y < HEIGHT/2:
        #    line_end = (40*math.sin(self.heading)+self.x,
        #                40*math.cos(self.heading)+self.y)
        #else:
        #    line_end = (-40*math.sin(self.heading)+self.x,
        #                -40*math.cos(self.heading)+self.y)
        line_end = (40*math.cos(self.heading)+int(self.x),
                    40*math.sin(self.heading)+int(self.y))
        pygame.draw.line(screen, self.color, (int(self.x), int(self.y)), line_end, 5)
    def turn(self, h):
        self.heading += h
    def move(self):
        if self.frozen:
            return
        line_end = (self.v*math.cos(self.heading)+self.x,
                    self.v*math.sin(self.heading)+self.y)
        #if self.y < HEIGHT/2:
        #    line_end = (20*math.sin(self.heading)+self.x,
        #                20*math.cos(self.heading)+self.y)
        #else:
        #    line_end = (-20*math.sin(self.heading)+self.x,
        #                -20*math.cos(self.heading)+self.y)
        self.x, self.y = line_end
        #self.x, self.y = int(self.x), int(self.y)
        self.v *= 0.98 # Near-vacuum so little slowdown.

    def shoot(self):
        Flash(self.x, self.y, self.heading)

    def check_collision(self):
        collisionZones = [[int(WIDTH*(1/3)-80), int(HEIGHT*(1/4)-80)],
                          [int(WIDTH*(1/3)-80), int(HEIGHT*(3/4)-80)],
                          [int(WIDTH*(2/3)-80), int(HEIGHT*(1/4)-80)],
                          [int(WIDTH*(2/3)-80), int(HEIGHT*(3/4)-80)]]
                         # [int(WIDTH*(1/2)-80), int(HEIGHT*(1/2)-80)]]
        while self.heading > 2*math.pi:
            self.heading -= 2*math.pi
        while self.heading < 0:
            self.heading +=2*math.pi
        for zone in collisionZones:
            if zone[0] < self.x < zone[0]+160 and \
               zone[1] < self.y < zone[1]+160:
                self.v = 0
                if self.y < zone[1]+30 and zone[0]+30 < self.x < zone[0]+130:
                    self.heading = -self.heading
                    self.y = zone[1]-10
                elif self.y > zone[1]+130 and zone[0]+30 < self.x < zone[0]+130:
                    self.heading = -self.heading
                    self.y = zone[1]+170
                else:
                    if self.x < zone[0]+80:
                        self.heading = -self.heading + math.pi
                        self.x = zone[0]-10
                    else:
                        self.heading = -self.heading + math.pi
                        self.x = zone[0]+170

            if self.y < 10:
                self.heading = -self.heading
                self.y = 10
            elif self.y > HEIGHT-10:
                self.heading = -self.heading
                self.y = HEIGHT-10
            if self.x < 10:
                self.heading = -self.heading + math.pi
                self.x = 15
            elif self.x > WIDTH-10:
                self.heading = -self.heading + math.pi
                self.x = WIDTH-10

    def freeze(self):
        self.frozen = True
        self.v = 0

def reset():
    global flashes, players, f
    flashes = []
    
    players = [Player(60, 60, (0, 255, 127)),
               Player(60, HEIGHT-60, (0, 255, 127)),
               Player(WIDTH-60, 60, (255, 127, 0)),
               Player(WIDTH-60, HEIGHT-60, (255, 127, 0))]
    f = Field(); f.generate()
    for p in players:
        p.generate()
    
reset()
    
class Flash():
    def __init__(self, x, y, h):
        self.x = x
        self.y = y
        self.heading = h
        flashes.append(self)

    def generate(self):
        self.x += 20*math.cos(self.heading)
        self.y += 20*math.sin(self.heading)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 5)
        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            flashes.remove(self)
        for p in players:
            if math.sqrt((self.x-p.x)**2 + (self.y-p.y)**2) < 10:
                p.freeze()


wms = []
while len(wms) < 4:
    try:
        print("Attempting connection number "+str(len(wms)))
        wms.append(cwiid.Wiimote())
        wms[len(wms)-1].rpt_mode = cwiid.RPT_BTN
    except Exception as e:
        print("Fail! "+str(e))
    else:
        print("Success!")

c = pygame.time.Clock()

font = pygame.font.SysFont("Ubuntu Mono", 30)

def runGame():
    q = False
    global winner
    while not q:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE): exit()
        for i, p in enumerate(players):
            buttons = wms[i].state["buttons"]
            #print(buttons)
            if buttons & cwiid.BTN_LEFT:
                p.turn(-0.02)
            if buttons & cwiid.BTN_RIGHT:
                p.turn(0.02)
            if buttons & cwiid.BTN_UP:
                p.v += 0.2
            if buttons & cwiid.BTN_B:
                p.shoot()
            p.move()
            p.check_collision()

        screen.fill((0, 0, 0))

        f.generate()
        for player in players:
            player.generate()
        for flash in flashes:
            flash.generate()

        if players[0].frozen and players[1].frozen or players[2].frozen and players[3].frozen:
            q = True
            if players[0].frozen:
                winner = "Orange"
            else:
                winner = "Green"
        
        pygame.display.flip()
        c.tick(30)
            
while True:
    runGame()
    screen.blit(font.render(winner+" Wins!", True, (255, 127, 0) if winner == "Orange" else (0, 255, 127)), (WIDTH/2-font.size(winner+" Wins!")[0]/2, HEIGHT/2-font.size(winner+" Wins!")[1]/2))
    pygame.display.flip()
    pygame.time.wait(10000)
    q = False
    reset()

        
pygame.quit()
