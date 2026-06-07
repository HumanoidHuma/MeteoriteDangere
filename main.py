
import math
import pygame
from PhyObject import PhyObject
from PhysicsEngine import PhysicsEngine

pygame.init()

WIDTH = 1600
HEIGHT = 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meteor Explosion Simulation")
clock = pygame.time.Clock()

# =====================================================
# Камера
# =====================================================
camera_x = 0
camera_y = 0
zoom = 1.0

# =====================================================
# Физика
# =====================================================
engine = PhysicsEngine()
dt = 0.01

# =====================================================
# Создание объектов
# =====================================================
sun = PhyObject(
    mass=333000, x=0, y=0,
    Vx=0, Vy=0,
    density=333000/1300000,
    obj_type="sun"
)

earth = PhyObject(
    mass=1, x=300, y=0,
    Vx=0, Vy=33.3,
    density=1,
    obj_type="earth"
)

planets = []
planet_data = [
    {"distance": 50, "speed": 47.4, "mass": 0.055},   # Mercury
    {"distance": 100, "speed": 35.0, "mass": 0.815},  # Venus
    {"distance": 450, "speed": 24.1, "mass": 0.107},  # Mars
]

for pd in planet_data:
    planet = PhyObject(
        mass=pd["mass"],
        x=pd["distance"], y=0,
        Vx=0, Vy=pd["speed"],
        density=1,
        obj_type="planet"
    )
    planets.append(planet)

objects = [sun, earth] + planets

# =====================================================
# Метеориты
# =====================================================
current_meteor_mass = 0.001
METEOR_DENSITY = 5
create_meteor_mode = False
meteor_start_x = None
meteor_start_y = None
speed_factor = 0.2

# =====================================================
# Взрывы
# =====================================================
explosions = []

# =====================================================
# Функции
# =====================================================
def world_to_screen(x, y):
    sx = (x - camera_x) * zoom + WIDTH/2
    sy = (y - camera_y) * zoom + HEIGHT/2
    return int(sx), int(sy)

def screen_to_world(sx, sy):
    x = (sx - WIDTH/2)/zoom + camera_x
    y = (sy - HEIGHT/2)/zoom + camera_y
    return x, y

def draw_object(obj):
    sx, sy = world_to_screen(obj.getX(), obj.getY())
    radius = max(2, int(obj.getRadius() * zoom))

    if obj.getType() == "sun":
        color = (255, 255, 0)
    elif obj.getType() == "earth":
        color = (0, 120, 255)
    elif obj.getType() == "planet":
        color = (0, 255, 0)
    else:
        color = (255, 255, 255)

    pygame.draw.circle(screen, color, (sx, sy), radius)

# =====================================================
# Главный цикл
# =====================================================
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Масштаб колесиком мыши
        if event.type == pygame.MOUSEWHEEL:
            zoom *= 1.1 if event.y > 0 else 0.9
            zoom = max(0.01, min(zoom, 1000))

        # Клавиши
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                create_meteor_mode = True
                meteor_start_x = None
                meteor_start_y = None
            if event.key == pygame.K_g:
                current_meteor_mass *= 2
            if event.key == pygame.K_t:
                current_meteor_mass /= 2
            if event.key == pygame.K_RETURN and create_meteor_mode and meteor_start_x is not None:
                mx, my = pygame.mouse.get_pos()
                end_x, end_y = screen_to_world(mx, my)
                dx = end_x - meteor_start_x
                dy = end_y - meteor_start_y
                vx = dx * speed_factor
                vy = dy * speed_factor
                meteor = PhyObject(
                    mass=current_meteor_mass,
                    x=meteor_start_x, y=meteor_start_y,
                    Vx=vx, Vy=vy,
                    density=METEOR_DENSITY,
                    obj_type="meteor"
                )
                objects.append(meteor)
                create_meteor_mode = False

        if event.type == pygame.MOUSEBUTTONDOWN and create_meteor_mode and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            meteor_start_x, meteor_start_y = screen_to_world(mx, my)

    # Камера
    keys = pygame.key.get_pressed()
    speed = 10/zoom
    if keys[pygame.K_LEFT]: camera_x -= speed
    if keys[pygame.K_RIGHT]: camera_x += speed
    if keys[pygame.K_UP]: camera_y -= speed
    if keys[pygame.K_DOWN]: camera_y += speed

    # Физика
    for _ in range(3):
        engine.simulate_on_time(objects, dt)

    # Проверка столкновений всех объектов
    collisions = []
    for i in range(len(objects)):
        for j in range(i+1, len(objects)):
            obj1 = objects[i]
            obj2 = objects[j]
            dx = obj1.getX() - obj2.getX()
            dy = obj1.getY() - obj2.getY()
            distance = math.sqrt(dx*dx + dy*dy)
            if distance <= (obj1.getRadius() + obj2.getRadius()):
                collisions.append( (obj1, obj2) )

    # Обработка столкновений и создание взрывов
    for obj1, obj2 in collisions:
        speed1 = math.sqrt(obj1.getVx()**2 + obj1.getVy()**2)
        speed2 = math.sqrt(obj2.getVx()**2 + obj2.getVy()**2)
        energy = 0.5*obj1.getMass()*speed1**2 + 0.5*obj2.getMass()*speed2**2
        print(f"Collision! Energy: {energy:.6f}")
        explosions.append({
            "x": (obj1.getX() + obj2.getX())/2,
            "y": (obj1.getY() + obj2.getY())/2,
            "radius": max(obj1.getRadius(), obj2.getRadius()),
            "life": 40
        })
        if obj1 in objects: objects.remove(obj1)
        if obj2 in objects: objects.remove(obj2)

    # Взрывы
    for explosion in explosions:
        explosion["radius"] += 3
        explosion["life"] -= 1
    explosions = [e for e in explosions if e["life"]>0]

    # Рисование
    screen.fill((0,0,0))
    for obj in objects:
        draw_object(obj)

    if create_meteor_mode and meteor_start_x is not None:
        mx, my = pygame.mouse.get_pos()
        sx, sy = world_to_screen(meteor_start_x, meteor_start_y)
        pygame.draw.line(screen, (255,0,0), (sx, sy), (mx, my), 3)

    for explosion in explosions:
        sx, sy = world_to_screen(explosion["x"], explosion["y"])
        pygame.draw.circle(screen, (255,120,0), (sx, sy), int(explosion["radius"]*zoom), 3)

    font = pygame.font.SysFont(None,28)
    info = [
        f"Zoom: {zoom:.2f}",
        f"Meteor mass: {current_meteor_mass:.6f}",
        "M - create meteor",
        "G/T - mass +/-",
        "ENTER - launch"
    ]
    y = 10
    for text in info:
        img = font.render(text, True, (255,255,255))
        screen.blit(img,(10,y))
        y += 25

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

