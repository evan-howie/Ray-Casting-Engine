#https://courses.pikuma.com/courses/take/raycasting/lessons/7503321-implementing-map-collision
import pygame
import math
import sys

TILE_SIZE = 32
MAP_COLS = 24
MAP_ROWS = 24

WINDOW_WIDTH = TILE_SIZE * MAP_COLS
WINDOW_HEIGHT = TILE_SIZE * MAP_ROWS

FOV_ANGLE = 60 * (math.pi / 180)

WALL_STRIP_WIDTH = 1
NUM_RAYS = WINDOW_WIDTH // WALL_STRIP_WIDTH

MINIMAP_SCALE_FACTOR = 0.2

TEXTURE_WIDTH = 64
TEXTURE_HEIGHT = 64

pygame.init()
wn = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

texture = [[None for i in range(TEXTURE_WIDTH * TEXTURE_HEIGHT)] for o in range(8)]

texture[0] = pygame.image.load("pics/eagle.png");
texture[1] = pygame.image.load("pics/redbrick.png");
texture[2] = pygame.image.load("pics/purplestone.png");
texture[3] = pygame.image.load("pics/greystone.png");
texture[4] = pygame.image.load("pics/bluestone.png");
texture[5] = pygame.image.load("pics/mossy.png");
texture[6] = pygame.image.load("pics/wood.png");
texture[7] = pygame.image.load("pics/colorstone.png");

#(texture[0])

class Map():
    def __init__(self):
        self.grid = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 4, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 4, 0, 0, 0, 0, 5, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 4, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 4, 0, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

    def hasWallAt(self, x, y):
        mapGridIndexX = x // TILE_SIZE
        mapGridIndexY = y // TILE_SIZE
        return self.grid[mapGridIndexY][mapGridIndexX] != 0

    def wallAt(self, x, y):
        mapGridIndexX = x // TILE_SIZE
        mapGridIndexY = y // TILE_SIZE
        return self.grid[mapGridIndexY][mapGridIndexX]

    def render(self):
        for i in range(MAP_ROWS):
            for o in range(MAP_COLS):
                tile_x = o * TILE_SIZE
                tile_y = i * TILE_SIZE
                if self.grid[i][o]:
                    tile_colour = (0, 0, 0)
                else:
                    tile_colour = (255,255,255)
                pygame.draw.rect(wn, tile_colour, (int(MINIMAP_SCALE_FACTOR * tile_x),
                                                   int(MINIMAP_SCALE_FACTOR * tile_y),
                                                   int(MINIMAP_SCALE_FACTOR * TILE_SIZE + 1),
                                                   int(MINIMAP_SCALE_FACTOR * TILE_SIZE + 1)))


class Player():
    def __init__(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.radius = 5
        self.turnDirection = 0
        self.walkDirection = 0
        self.heading = math.pi / 2
        self.moveSpeed = 4.5
        self.rotationSpeed = 1 * (math.pi / 180)

    def update(self):
        global keys
        """mouse = pygame.mouse.get_pos()

        if mouse[0] == self.x:
            if mouse[1] > self.y:
                self.heading = math.pi / 2
            else:
                self.heading = math.pi * 1.5
        else:
            a = (mouse[1] - self.y) / (mouse[0] - self.x)
            if mouse[1] > self.y and mouse[0] > self.x:
                self.heading = math.atan(a)
            elif mouse[1] > self.y and mouse[0] < self.x:
                self.heading = math.pi - math.atan(abs(a))
            elif mouse[1] < self.y and mouse[0] < self.x:
                self.heading = math.pi + math.atan(a)
            elif mouse[1] < self.y and mouse[0] > self.x:
                self.heading = math.atan(a)"""
        #pygame.mouse.set_pos(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)


        delta_x = pygame.mouse.get_rel()[0]
        self.heading += delta_x * 0.004 % (math.pi * 2)
        #print(self.heading)

    def render(self):
        pygame.draw.circle(wn, (255, 0, 0), (int(MINIMAP_SCALE_FACTOR * self.x),
                                             int(MINIMAP_SCALE_FACTOR * self.y)), self.radius)
        # pygame.draw.line(wn, (0, 0, 0), (self.x, self.y), (self.x + 20 * math.cos(self.heading), self.y + 20 * math.sin(self.heading)))


class Ray:
    def __init__(self, rayAngle):
        self.rayAngle = normalizeAngle(rayAngle)
        self.wallHitX = 0
        self.wallHitY = 0
        self.distance = 0
        self.hit = None
        self.offset = 0

        self.wasHitV = False

        self.isRayFacingDown = self.rayAngle < math.pi and self.rayAngle > 0
        self.isRayFacingUp = not self.isRayFacingDown

        self.isRayFacingLeft = self.rayAngle > math.pi / 2 and self.rayAngle < math.pi * 1.5
        self.isRayFacingRight = not self.isRayFacingLeft

    def cast(self, columnId):
        ############################################
        # HORIZONTAL RAY-GRID INTERSECTION CODE
        ############################################
        # Find the y-coordinate of the closest horizontal grid intersection
        foundHW = False
        hwallX = 0
        hwallY = 0
        hwallHit = None

        yint = (player.y // TILE_SIZE) * TILE_SIZE
        if self.isRayFacingDown:
            yint += TILE_SIZE
        # Find the x-coordinate of the closest horizontal grid intersection
        xint = (yint - player.y) / math.tan(self.rayAngle) + player.x

        ystep = TILE_SIZE
        if self.isRayFacingUp:
            ystep *= -1

        xstep = ystep / math.tan(self.rayAngle)
        if self.isRayFacingLeft and xstep > 0:
            xstep *= -1
        elif self.isRayFacingRight and xstep < 0:
            xstep *= -1

        nexthx = xint
        nexthy = yint

        while nexthx >= 0 and nexthx <= WINDOW_WIDTH and nexthy <= WINDOW_HEIGHT and nexthy >= 0:
            if grid.hasWallAt(int(nexthx), int(nexthy) - int(self.isRayFacingUp)):
                foundHW = True
                hwallX = nexthx
                hwallY = nexthy
                hwallHit = grid.wallAt(int(nexthx), int(nexthy) - int(self.isRayFacingUp))
                break
            else:
                nexthx += xstep
                nexthy += ystep

        ##########################################
        # VERTICAL RAY-GRID INTERSECTION CODE
        ##########################################
        # Find the x-coordinate of the closest horizontal grid intersection
        foundVW = False
        vwallX = 0
        vwallY = 0
        vwallHit = None

        xint = (player.x // TILE_SIZE) * TILE_SIZE
        if self.isRayFacingRight:
            xint += TILE_SIZE
        # Find the y-coordinate of the closest horizontal grid intersection
        yint = (xint - player.x) * math.tan(self.rayAngle) + player.y

        xstep = TILE_SIZE
        ystep = xstep * math.tan(self.rayAngle)

        if self.isRayFacingLeft:
            xstep *= -1
        if self.isRayFacingUp and ystep > 0:
            ystep *= -1
        elif self.isRayFacingDown and ystep < 0:
            ystep *= -1

        nextvx = xint
        nextvy = yint

        while nextvx >= 0 and nextvx <= WINDOW_WIDTH and nextvy <= WINDOW_HEIGHT and nextvy >= 0:
            if grid.hasWallAt(int(nextvx) - int(self.isRayFacingLeft), int(nextvy)):
                foundVW = True
                vwallX = nextvx
                vwallY = nextvy
                vwallHit = grid.wallAt(int(nextvx) - int(self.isRayFacingLeft), int(nextvy))
                break
            else:
                nextvx += xstep
                nextvy += ystep

        # Calculate both distances, choose smallest
        if foundHW:
            horzdistance = distance(player.x, player.y, hwallX, hwallY)
        else:
            horzdistance = 99999999999999
        if foundVW:
            vertdistance = distance(player.x, player.y, vwallX, vwallY)
        else:
            vertdistance = 99999999999999

        # Smaller distance
        if horzdistance > vertdistance:
            self.distance = vertdistance
            self.wallHitX = vwallX
            self.wallHitY = vwallY
            self.hit = vwallHit
            self.offset = self.wallHitY % TILE_SIZE
        else:
            self.distance = horzdistance
            self.wallHitX = hwallX
            self.wallHitY = hwallY
            self.hit = hwallHit
            self.offset = self.wallHitX % TILE_SIZE


    def render(self):
        pygame.draw.line(wn, (255, 200, 0), (int(MINIMAP_SCALE_FACTOR * player.x),
                                             int(MINIMAP_SCALE_FACTOR * player.y)),
                                            (int(MINIMAP_SCALE_FACTOR * self.wallHitX),
                                            int(MINIMAP_SCALE_FACTOR * self.wallHitY)))


# objects
grid = Map()
player = Player()
rays = []


def keyPressed():
    keys = pygame.key.get_pressed()

    xvel = 0
    yvel = 0

    if keys[pygame.K_w]:
        xvel += int(math.cos(player.heading) * player.moveSpeed)
        yvel += int(math.sin(player.heading) * player.moveSpeed)
    if keys[pygame.K_s]:
        xvel -= int(math.cos(player.heading) * player.moveSpeed)
        yvel -= int(math.sin(player.heading) * player.moveSpeed)
    if keys[pygame.K_a]:
        xvel += int(math.cos(player.heading - math.pi / 2) * player.moveSpeed)
        yvel += int(math.sin(player.heading - math.pi / 2) * player.moveSpeed)
    if keys[pygame.K_d]:
        xvel -= int(math.cos(player.heading - math.pi / 2) * player.moveSpeed)
        yvel -= int(math.sin(player.heading - math.pi / 2) * player.moveSpeed)

    new_x = player.x + xvel
    new_y = player.y + yvel

    if not grid.hasWallAt(new_x, new_y):
        #print('hi')
        player.x = new_x
        player.y = new_y

    if keys[pygame.K_ESCAPE]:
        sys.exit()

def cast_rays():
    global rays

    columnId = 0

    rayAngle = player.heading - (FOV_ANGLE / 2)

    rays = []

    for i in range(NUM_RAYS):
        rays.append(Ray(rayAngle))
        rays[i].cast(columnId)

        rayAngle += FOV_ANGLE / NUM_RAYS

        columnId += 1

def renderProjectedWalls():
    for i in range(len(rays)):
        ray = rays[i]
        rayDistance = ray.distance * math.cos(ray.rayAngle - player.heading)

        distanceProjectionPlane = (WINDOW_WIDTH / 2) / math.tan(FOV_ANGLE / 2)

        if rayDistance == 0.00:
            wallStripHeight = WINDOW_HEIGHT
        else:
            wallStripHeight = (TILE_SIZE / rayDistance) * distanceProjectionPlane


        if ray.distance > 100:
            shade = (ray.distance - 100) / 2
        else:
            shade = 1

        if shade > 255: shade = 255
        elif shade < 1: shade = 1

        #print(shade)
        #print(colour)


        tempTexture = texture[ray.hit]
        tempTexture = tempTexture.subsurface((int(ray.offset), 0, int(WALL_STRIP_WIDTH), TILE_SIZE))
        tempTexture = pygame.transform.scale(tempTexture, (int(WALL_STRIP_WIDTH), int(wallStripHeight)))
        shader = pygame.Surface((tempTexture.get_size())).convert_alpha()
        shader.fill((0, 0, 0, shade))
        copied = tempTexture.copy()
        copied.blit(shader, (0, 0))


        wn.blit(copied, (i * WALL_STRIP_WIDTH,
                                int(WINDOW_HEIGHT / 2 - wallStripHeight / 2)))
        #print(shade)

        '''pygame.draw.rect(wn, (255, 255, 255), (i * WALL_STRIP_WIDTH,
                                      int(WINDOW_HEIGHT // 2 - wallStripHeight // 2),
                                      WALL_STRIP_WIDTH,
                                      int(wallStripHeight)))'''



def normalizeAngle(angle):
    if angle < 0:
        return math.pi * 2 + angle
    else:
        return angle % (math.pi * 2)


def distance(x1, y1, x2, y2):
    return math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)


def setup():
    pygame.display.set_caption("Ray Casting")


def update():
    player.update()
    cast_rays()


def draw():
    update()
    wn.fill((0,0,0))

    renderProjectedWalls()

    grid.render()
    player.render()

    for ray in rays:
        ray.render()

    '''tempTexture = pygame.transform.scale(texture[0], (256, 256))
    tempTexture = pygame.transform.chop(tempTexture, (10, 0, 40, 0))
    wn.blit(tempTexture, (0, 0))'''

    pygame.display.update()


run = True

while run:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            sys.exit()

    keyPressed()
    draw()
