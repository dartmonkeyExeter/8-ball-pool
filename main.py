import pygame
import random

# POOL !!!

pygame.init()
running = True
fps = 75
clock = pygame.time.Clock()
table_size_mod = 4
screen = pygame.display.set_mode((213 * table_size_mod, 122 * table_size_mod))

# the playing field is 183cm x 91.5cm
# the table is 213cm x 121cm

class Ball:
    def __init__(self, x, y, radius, color, screen, number=None):
        self.x = x
        self.y = y
        self.velocity = pygame.math.Vector2(0, 0)
        self.spin = pygame.math.Vector2(0, 0)
        self.radius = radius
        self.color = color
        self.screen = screen
        self.number = number
        self.is_numbered = True if number is not None else False

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
        if self.is_numbered:
            pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), self.radius - 8)
            font = pygame.font.Font(None, 22)
            text = font.render(str(self.number), True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.x, self.y))
            self.screen.blit(text, text_rect)

    def move(self):
        self.x += self.velocity.x
        self.y += self.velocity.y
        if self.x - self.radius < 0:
            self.x = self.radius
            self.velocity.x = abs(self.velocity.x)
        elif self.x + self.radius > 213 * table_size_mod:
            self.x = 213 * table_size_mod - self.radius
            self.velocity.x = -abs(self.velocity.x)
        if self.y - self.radius < 0:
            self.y = self.radius
            self.velocity.y = abs(self.velocity.y)
        elif self.y + self.radius > 121 * table_size_mod:
            self.y = 121 * table_size_mod - self.radius
            self.velocity.y = -abs(self.velocity.y)

    def apply_friction(self):
        self.velocity.x *= 0.96
        self.velocity.y *= 0.96

def collide(ball_one, ball_two):
    distance = ((ball_one.x - ball_two.x) ** 2 + (ball_one.y - ball_two.y) ** 2) ** 0.5
    if distance < ball_one.radius + ball_two.radius:
        overlap = (ball_one.radius + ball_two.radius) - distance
        normal = pygame.math.Vector2(ball_two.x - ball_one.x, ball_two.y - ball_one.y).normalize()
        displacement = normal * overlap * 0.5
        ball_one.x -= displacement.x
        ball_one.y -= displacement.y
        ball_two.x += displacement.x
        ball_two.y += displacement.y
        relative_velocity = ball_two.velocity - ball_one.velocity
        impulse = normal * relative_velocity.dot(normal) * 2 / (1 + 1)
        ball_one.velocity += impulse
        ball_two.velocity -= impulse

balls = []
ball_colours = [(255, 255, 0), (0, 0, 255), (255, 0, 0), (128, 0, 128), (255, 165, 0), (0, 128, 0), (165, 42, 42),
                (0, 0, 0)]

eight_ball_position = (48.38, 60.5)

ball_positions = [(68.125, 60.5), 
                  (58.25, 54.8), (58.25, 66.2), 
                  (48.38, 49.1), (48.38, 71.9),
                  (38.5, 43.4), (38.5, 54.8), (38.5, 66.2), (38.5, 77.6),
                  (28.63, 37.7), (28.63, 49.1), (28.63, 60.5), (28.63, 71.9), (28.63, 83.3)]

for i in range(15):
    color_index = i % len(ball_colours)  
    if i == 7: 
        balls.append(Ball(eight_ball_position[0] * table_size_mod, eight_ball_position[1] * table_size_mod, 5.7 * table_size_mod, ball_colours[color_index], screen, i + 1))
    else:
        position = random.choice(ball_positions)
        balls.append(Ball(position[0] * table_size_mod, position[1] * table_size_mod, 5.7 * table_size_mod, ball_colours[color_index], screen, i + 1))
        ball_positions.remove(position)

cueball = Ball(144.625 * table_size_mod, 60.5 * table_size_mod, 5.7 * table_size_mod, (255, 255, 255), screen)

shooting = False
allowed_to_shoot = True

while running:
    screen.fill((0, 200, 0))
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if cueball.x - cueball.radius < mouse_pos[0] < cueball.x + cueball.radius and cueball.y - cueball.radius < \
                    mouse_pos[1] < cueball.y + cueball.radius and allowed_to_shoot:
                shooting = True
                allowed_to_shoot = False
        if event.type == pygame.MOUSEBUTTONUP:
            if shooting:
                shooting = False
                cueball.velocity = pygame.math.Vector2((cueball.x - mouse_pos[0]) / 10,
                                                       (cueball.y - mouse_pos[1]) / 10)

    for ball in balls:
        ball.draw()
        ball.move()
        ball.apply_friction()

    for ball in balls:
        collide(ball, cueball)
        for ball_two in balls:
            if ball != ball_two:
                collide(ball, ball_two)
                pass

    if shooting:
        pygame.draw.line(screen, (0, 0, 0), (cueball.x, cueball.y), 
                        ((cueball.x + (cueball.x - mouse_pos[0])), (cueball.y + (cueball.y - mouse_pos[1]))), 3)

    cueball.draw()
    cueball.move()
    cueball.apply_friction()

    if cueball.velocity.length() < 0.1:
        allowed_to_shoot = True
        for ball in balls:
            if ball.velocity.length() > 0.1:
                allowed_to_shoot = False
                break
    pygame.display.flip()
    clock.tick(fps)
