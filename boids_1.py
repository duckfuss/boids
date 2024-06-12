import pygame
import random
#\import tkinter
import math as maths

class Boid():
    def __init__(self):
        self.max_speed = 3
        self.location = [random.randint(0,WIDTH),random.randint(0,HEIGTH)]
        self.detect_rad = 30#2000

        self.vector = [0,0]
        random_x = random.randint(-2,2)
        random_y = (2-(random_x**2))
        if random.randint(1,2) == 2:
            random_y *= -1
        self.vector[0] = random_x
        self.vector[1] = random_y

        self.separation_strength = 8
        self.alignment_strength = 3
        self.cohesion_strength = 1/2
        self.speed_limited = True

        #used only for random movement ¬
        self.angle = random.randint(0,360)
        self.random_speed = 10
        
        self.colour = (219,219,219)#(random.randrange(255), random.randrange(255), random.randrange(255)) 
        self.first_time = True
        self.DEBUG_DRAW = True
    def find_vector(self):
        #to find alignment vector
        align_vec = [0,0]
        #align_vec[0] += self.vector[0]
        #align_vec[1] += self.vector[1]        
        #to find Centre Of Mass (for cohesion vector)
        COMx_numerator, COMy_numerator = 0, 0
        cohesion_vec = [0,0]
        separation_vec = [0,0]
        #for colours
        col_r = 0
        col_g = 0
        col_b = 0
        self.local_boid_num = 0
        for boid in BOIDS_DICT:
            if (boid.location[0]-self.location[0])**2 + (boid.location[1]-self.location[1])**2 < self.detect_rad**2 and boid.location != self.location:
                self.local_boid_num += 1

                COMx_numerator += 1 + boid.location[0]
                COMy_numerator += 1 + boid.location[1]
                
                align_vec[0] += boid.vector[0]
                align_vec[1] += boid.vector[1]

                separation_vec[0] += (1/(boid.location[0] - self.location[0])) * -self.separation_strength
                separation_vec[1] += (1/(boid.location[1] - self.location[1])) * -self.separation_strength
                
                col_r, col_g, col_b = col_r+boid.colour[0],  col_g+boid.colour[1], col_b+boid.colour[2]
        if self.local_boid_num != 0:
            COMx, COMy = COMx_numerator/self.local_boid_num, COMy_numerator/self.local_boid_num
            cohesion_vec = [COMx-self.location[0], COMy-self.location[1]]
            align_vec[0] *= self.alignment_strength 
            align_vec[1] *= self.alignment_strength
            separation_vec[0] *= self.separation_strength
            separation_vec[1] *= self.separation_strength
            cohesion_vec[0] *= self.cohesion_strength
            cohesion_vec[1] *= self.cohesion_strength
            
            target_vector_x = (align_vec[0] + cohesion_vec[0] + separation_vec[0])
            target_vector_y =  (align_vec[1] + cohesion_vec[1] + separation_vec[1])
            self.vector[0] += (target_vector_x - self.vector[0])/2 
            self.vector[1] += (target_vector_y - self.vector[1])/2
            
            col_rand_r = 0#random.randint(-1, 1)
            col_rand_g = 0#random.randint(-1, 1)
            col_rand_b = 0#random.randint(-1, 1)
            colour_r = (((col_r+self.colour[0]+ col_rand_r)/(self.local_boid_num+1))) % 255 
            colour_g = (((col_g+self.colour[0]+ col_rand_g)/(self.local_boid_num+1))) % 255
            colour_b = (((col_b+self.colour[0]+ col_rand_b)/(self.local_boid_num+1))) % 255

            #self.colour = (colour_r, colour_g, colour_b)
            
            self.first_time = True
            if self.DEBUG_DRAW:
                pygame.draw.circle(screen, (255,255,0), (COMx, COMy), 3)
                pygame.draw.line(screen, (255,0,255), self.location, (self.location[0]+cohesion_vec[0], self.location[1]+cohesion_vec[1]))
                pygame.draw.line(screen, (0,0,255), self.location, (self.location[0]+align_vec[0], self.location[1]+align_vec[1]))
                pygame.draw.line(screen, (0,255,0), self.location, (self.location[0]+separation_vec[0], self.location[1]+separation_vec[1]))
            
        else:
            if self.first_time:
                #self.colour = (random.randrange(100,255), random.randrange(100,255), random.randrange(100,255))
                self.first_time = False
            #random angle based movement (bc couldn't get it to work w/t vectors)
            self.angle += random.randint(-5,5)
            self.angle = self.angle % 360
            i = 90 - self.angle
            if (i > 90 and i < 180) or i > 270:
                self.vector[0] = maths.sin(maths.radians(i))*self.random_speed*1
                self.vector[1] = maths.cos(maths.radians(i))*self.random_speed*1
            else:
                self.vector[0] = maths.cos(maths.radians(i))*self.random_speed*1
                self.vector[1] = maths.sin(maths.radians(i))*self.random_speed*1
            
            '''self.random_x = random.randint(-4,4)
             self.random_y = (4-(self.random_x**2))
             if random.randint(1,2) == 2:
                 self.random_y *= -1
             self.vector[0] += (self.random_x)# - self.vector[0])/2
             self.vector[1] += (self.random_y)# - self.vector[1])/2'''
        self.vector[0] /= 2
        self.vector[1] /= 2

        #afraid of the edge
        if self.location[0] < 10:
            self.vector[0] *= -1
            self.angle += 180
            self.location[0] += 10
        elif self.location[0] > WIDTH-10:
            self.vector[0] *= -1
            self.angle += 180
            self.location[0] -= 10
        elif self.location[1] < 10:
            self.vector[1] *= -1
            self.angle += 180
            self.location[1] += 10
        elif self.location[1] > HEIGTH-10:
            self.vector[1] *= -1
            self.angle += 180
            self.location[1] -= 10

        #cap boid speed
        speed_sqrd = self.vector[0]**2 + self.vector[1]**2
        if speed_sqrd > self.max_speed**2:
            scale_factor = self.max_speed/maths.sqrt(speed_sqrd)
            self.vector[0] *= scale_factor
            self.vector[1] *= scale_factor

    def update(self):
        if pygame.time.get_ticks() % 1 == 0:
            self.find_vector()
        self.location[0] += self.vector[0]
        self.location[1] += self.vector[1]
        if self.local_boid_num != 0 and self.DEBUG_DRAW:
            pygame.draw.circle(screen, (255,0,0), self.location, self.detect_rad, width=1)
        elif self.DEBUG_DRAW:
            pygame.draw.circle(screen, (0,255,0), self.location, self.detect_rad, width=1)

        BOIDS_DICT[self] = (self.location[0], self.location[1])

    def draw(self):
        pygame.draw.circle(screen, self.colour, self.location, 5)
        if self.DEBUG_DRAW:
            pygame.draw.line(screen, (0,0,0), self.location, (self.location[0] + self.vector[0]*10, self.location[1]))
            pygame.draw.line(screen, (0,0,0), self.location, (self.location[0], self.location[1] + self.vector[1]*10))
            pygame.draw.line(screen, (0,255,255), self.location, (self.location[0] + self.vector[0]*10, self.location[1] + self.vector[1]*10))
'''
def update_boids(v):
    for boid in BOIDS_DICT:
        boid.alignment_strength = align_scale_var.get()
        boid.cohesion_strength = cohes_scale_var.get()
        boid.separation_strength = separ_scale_var.get()
        boid.detect_rad = detra_scale_var.get()

window = tkinter.Tk()
window.title("GUI")
'''
HEIGTH = int(2880/3)
WIDTH = int(5120/3)
'''
align_scale_var = tkinter.IntVar()
align_scale = tkinter.Scale(window, variable=align_scale_var, from_=0, to=10, length=500, command=update_boids, orient='horizontal').pack()
cohes_scale_var = tkinter.IntVar()
cohes_scale = tkinter.Scale(window, variable=cohes_scale_var, from_=0, to=10, length=500, command=update_boids, orient='horizontal').pack()
separ_scale_var = tkinter.IntVar()
separ_scale = tkinter.Scale(window, variable=separ_scale_var, from_=0, to=10, length=500, command=update_boids, orient='horizontal').pack()
detra_scale_var = tkinter.IntVar()
detra_scale = tkinter.Scale(window, variable=detra_scale_var, from_=0, to=WIDTH, length=500, command=update_boids, orient='horizontal').pack()
'''
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGTH))
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 24)
count_font = 0

BOIDS_DICT = {}
boid_num = 200
Boids = [Boid() for i in range(boid_num)]
main_character = Boid()
main_character.DEBUG_DRAW = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.fill((100,100,100))
    for boid in Boids:
        boid.update()
        boid.draw()

    main_character.update()
    main_character.draw()

    if count_font % 50 == 0:
        text = font.render("boids: " + str(boid_num) + "   fps: " + str(int(clock.get_fps())), True, (0,255,0))
    count_font += 1
    screen.blit(text, (20, 20))

    pygame.display.update()
    clock.tick(120)
    #window.update_idletasks()
    #window.update()