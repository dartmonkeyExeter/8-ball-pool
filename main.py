import pygame

# POOL !!!

pygame.init()
running = True
fps = 75
clock = pygame.time.Clock()
table_size_mod = 4
screen = pygame.display.set_mode((213 * table_size_mod, 121 * table_size_mod))

class PoolBall:
    def __init__(self, x, y, radius, color, screen, number):
        self.x = x
        self.y = y
        self.velocity = pygame.math.Vector2(0, 0)
        self.radius = radius
        self.color = color
        self.screen = screen
        self.number = number
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), self.radius - 8)
        font = pygame.font.Font(None, 22)
        text = font.render(str(self.number), True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x, self.y))
        self.screen.blit(text, text_rect)
    def move(self):
        self.x += self.velocity.x
        self.y += self.velocity.y
        if self.x - self.radius < 0 or self.x + self.radius > 213 * table_size_mod:
            self.velocity.x *= -1
        if self.y - self.radius < 0 or self.y + self.radius > 121 * table_size_mod:
            self.velocity.y *= -1
    def apply_friction(self):
        self.velocity.x *= 0.97
        self.velocity.y *= 0.97

class CueBall:
    def __init__(self, x, y, radius, color, screen):
        self.x = x
        self.y = y
        self.velocity = pygame.math.Vector2(0, 0)
        self.radius = radius
        self.color = color
        self.screen = screen
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
    def move(self):
        self.x += self.velocity.x
        self.y += self.velocity.y
        if self.x - self.radius < 0 or self.x + self.radius > 213 * table_size_mod:
            self.velocity.x *= -1
        if self.y - self.radius < 0 or self.y + self.radius > 121 * table_size_mod:
            self.velocity.y *= -1
    def apply_friction(self):
        self.velocity.x *= 0.97
        self.velocity.y *= 0.97

balls = []
ball_colours = [(255, 255, 0), (0, 0, 255), (255, 0, 0), (128, 0, 128), (255, 165, 0), (0, 128, 0), (165, 42, 42), (0, 0, 0)]

for i in range(1, 16):
    balls.append(PoolBall(i * 50, 300, 5.7 * table_size_mod, ball_colours[(i - 1) % len(ball_colours)], screen, i))

cueball = CueBall(50, 300, 5.7 * table_size_mod, (255, 255, 255), screen)

shooting = False

while running:
    screen.fill((0, 200, 0))
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:    
            if cueball.x - cueball.radius < mouse_pos[0] < cueball.x + cueball.radius and cueball.y - cueball.radius < mouse_pos[1] < cueball.y + cueball.radius:
                shooting = True
        if event.type == pygame.MOUSEBUTTONUP:
            if shooting:
                shooting = False
                cueball.velocity = pygame.math.Vector2((cueball.x - mouse_pos[0]) / 10, (cueball.y - mouse_pos[1]) / 10)

    
    for ball in balls:
        ball.draw()
        ball.move()
        ball.apply_friction()
    cueball.draw()
    cueball.move()
    cueball.apply_friction()


    pygame.display.flip()
    clock.tick(fps)
