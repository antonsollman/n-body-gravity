import sys

sys.path.append('C:\\Users\\anton\\Dropbox\\pythoncode\\modules')
sys.path.append('C:\\Users\\anor0501\\Dropbox\\pythoncode\\modules')

from amath import *

import turtle
import time

start_solar_system = True

G = 6.6743 * 10**-11

turtle_scale = 0.006

m = 100000000

# More like a gravitational constant
time_constant = 0.01

simulation_screen = turtle.Screen()
simulation_screen.setup(800,600)
simulation_screen.title("Gravity Simulation")

class Body:
    def __init__(self, position, velocity=(0,0), mass='random', size='mass', color='random', ID='random'):
        current_time = time.time()
        time.sleep(0.01)
        
        if ID == 'random':
            ID = str(current_time)
        
        randomness = mod(int((cos(sin(current_time)*current_time))*current_time)**2,16**6)
        self.randomness = randomness

        if mass == 'default':
            mass = m
        elif mass == 'random':
            mass = randomness*8

        if color == 'random':
            color = hex(randomness).replace('0x','')
            for n in range(6-len(color)):
                color = '0'+color
            color = '#'+color
            
        if '§' in color:
            color = color.strip('§')
            secondary_color = color
        else:
            if '#' not in color:
                color = '#'+color
            color_hex = color.strip('#')
            RGB = []
            while color_hex:
                RGB.append(color_hex[:2])
                color_hex = color_hex[2:]
            
            secondary_color = '#'
            for n in range(3):
                color_value = int(RGB[n], 16)
                color_value -= 16
                if color_value <= 0:
                    color_value = 0
##                darker_color += '0'+hex(color_value).replace('0x','')
                secondary_color += '{0}'.format(hex(color_value).replace('0x','').zfill(2))
        
        
        if size == 'mass':
            size = (log(mass))**4/160000
            if size < 0.1:
                size = 0.2

        if size <= 0:
            size = 0.001

        self.ID = ID
        self.mass = mass
        self.color = color
        self.size = size

        self.position = position
        self.velocity = velocity

        print(f"\nNew body: {ID}\n Position: {position}\n Velocity: {velocity}\n Mass: {mass}\n Size: {size}\n Color: {color}\n Randomness key: {randomness}\n")
            
        self.acceleration = [0,0]

        # Turtle
        self.Body_turtle = turtle.Turtle()
        self.Body_turtle.speed(0)
        self.Body_turtle.shape('circle')
        self.Body_turtle.pencolor(color)
        self.Body_turtle.fillcolor()#secondary_color)
        self.Body_turtle.turtlesize(size,size,size)
        self.Body_turtle.penup()
        self.Body_turtle.setpos(self.position[0]/turtle_scale, self.position[1]/turtle_scale)
        self.Body_turtle.pendown()

    def updateTurtle(self):
        
        self.Body_turtle.setpos(self.position[0]/turtle_scale, self.position[1]/turtle_scale)
        
        
    def values(self):
        print(self.position,self.velocity)

class dummy:
    def __init__(self, ID, mass, position):
        self.ID = ID
        self.mass = mass
        self.position = position

    
def grid():
    class grid_line:
        direction = {
                "N":0,
                "E":90,
                "S":180,
                "W":270
            }
        
        def __init__(self, direction, screen_position=0.0):
            self.direction = direction
            self.screen_position = screen_position
            self.sim_position = screen_position*turtle_scale

            self.line = turtle.Turtle()
            self.line.speed(0)
            self.line.pencolor("#bbbbbb")
            self.line.setheading(direction)

            n = 8
            unit_length = 100
            r = 2
            
            length = unit_length * n
            sign = 1
            if direction == 180 or direction == 270:
                sign = -1
            
            for i in range(1,n+1):
                self.screen_position = i*length/n*sign
                self.line.forward(length/n)
                self.sim_position = self.screen_position*turtle_scale

                # North or South
                if direction == 90 or direction == 270:
                    self.line.setpos(r,self.screen_position)
                    self.line.setpos(-r,self.screen_position)
                    self.line.setpos(0,self.screen_position)

                # East or West
                elif direction == 0 or direction == 180:
                    self.line.setpos(self.screen_position,r)
                    self.line.setpos(self.screen_position,-r)
                    self.line.setpos(self.screen_position,0)
                
                self.line.write(around(self.sim_position,2))
                
            self.line.penup()
            self.line.hideturtle()
            
    grid_line(0)
    grid_line(90)
    grid_line(180)
    grid_line(270)
    

def calculateDistance(position1, position2): # Returns distance between two bodies
    
    dist_x = position2[0] - position1[0]
    dist_y = position2[1] - position1[1]
    
    distance = sqrt(dist_x**2 + dist_y**2) # Distance between the two bodies
    
    return (dist_x, dist_y, distance)

def calculateForce(body1, body2): # Returns force between two bodies
    distance = calculateDistance(body1.position, body2.position)[2]
    
    if distance**2 == 0:
        print("Collision?") # Should add masses together and turn into one body
        return 0

    force = G * body1.mass * body2.mass / distance**2
    
    return force

def calculateAcceleration(body1, body2): # Returns acceleration vectors for body1
    acceleration = calculateForce(body1, body2)/body1.mass

    distances = calculateDistance(body1.position, body2.position)

    distance = distances[2]

    proportion = acceleration / distance

    acceleration_x = proportion * distances[0]
    acceleration_y = proportion * distances[1]
    
    return (acceleration_x, acceleration_y, acceleration)

    
newNextClick = False

def newBodyVelocity(d_x, d_y, u_x, u_y):

    distance = calculateDistance((d_x, d_y),(u_x, u_y))
    velocity = (distance[0]/16,distance[1]/16)

    return velocity

def newBody(position, velocity, mass='random', ):
    
    bodylist.append(Body(position,velocity,mass))

addNew = False

def toggleNewBody(x, y):
    global KeyAction, newNextClick, addNew, down_x, down_y, up_x, up_y
    
    x *= turtle_scale
    y *= turtle_scale
    
    if newNextClick == False:
        down_x = x
        down_y = y
        print(f"down at {x, y}")
    else:
        up_x = x
        up_y = y
        print(f"up at {x, y}")
        addNew = True
        KeyAction = True

    newNextClick = not newNextClick


standard_mass = 2
def changeStandardMass():
    global standard_mass
    standard_mass = turtle.numinput("Standard Mass", "Mass:",standard_mass-2,0)+2
    print(standard_mass)

bodylist = [
    #Body((0.75,0),(0,0.004),m,color='§green'),
    #Body((-0.75,0),(0,-0.004),m,color='§magenta')
]

# Create a custom body by pressing "n"
def newCustomBody():
    
    position = turtle.numinput("Position", "Enter x coordinate:"), turtle.numinput("Position", "Enter y coordinate:")
    velocity = turtle.numinput("Velocity", "Enter x:"), turtle.numinput("Velocity", "Enter y:")
    mass = turtle.numinput("Mass", "Enter mass:", standard_mass, 0)+2
    size = turtle.numinput("Size", "Enter size:", 0.5, 0.01)
    color = '#'+turtle.textinput("Color", "Enter hex color: #")
    ID = turtle.textinput("ID", "Enter ID:")

    bodylist.append(Body(position, velocity, mass, size, color, ID))



def add_solar_system():
    earth_velocity = 0.00827
    earth_mass = 3
    earth_radius = 0.35
    bodylist.extend([
##        Body((0,0), (0,0), 300, earth_radius, "#3377dd","Earth"),
##        Body((0.0026,0), (0,0.00028), earth_mass*0.0123*0.01, earth_radius*0.25, "#888888","Moon"),
##        Body((0,0), (0,0), 300, earth_radius, "#3377dd","Earth"),
##        Body((0.05,0), (0,0.00006), earth_mass*0.0123*0.05, earth_radius*0.25, "#888888","Moon"),
        Body((0.00001,0),mass=100000000,size=1,color="#ffff00",ID="The Sun"),
        Body((0.387,0), (0,earth_velocity/sqrt(0.387)), 16.5, earth_radius*0.4, "#666666", "Mercury"),
        Body((0.723,0), (0,earth_velocity/sqrt(0.723)), 245, earth_radius*0.9, "#eebb55", "Venus"),
        Body((1,0), (0,earth_velocity/sqrt(1)), 300, earth_radius, "#3377dd","Earth"),
        Body((1+0.0026,0), (0,earth_velocity/sqrt(1+0.0026)+0.00028), earth_mass*0.0123*0.01, earth_radius*0.25, "#888888","Moon"),
        Body((1.524,0), (0,earth_velocity/sqrt(1.524)), 32, earth_radius*0.75, "#c06030", "Mars"),
        Body((5.204,0), (0,earth_velocity/sqrt(5.204)), 95500, earth_radius*2.5, "#eecc99", "Jupiter"),
        Body((9.583,0), (0,earth_velocity/sqrt(9.583)), 28500, earth_radius*2, "#ffdd77", "Saturn")
    ])



setsolarsystem = False
def set_solar_system():
    global KeyAction, setsolarsystem
    setsolarsystem = True
    KeyAction = True

start_solar_system = False

if start_solar_system == True:
    set_solar_system()

KeyAction = False

time.sleep(0.5)

turtle.onscreenclick(toggleNewBody)
turtle.onkey(newCustomBody,'n')
turtle.onkey(changeStandardMass, 'm')
turtle.onkey(add_solar_system, 's')
turtle.onkey(set_solar_system, 'c')
# grid can't interfere with simulation, so no KeyAction check thing required
turtle.onkey(grid, '+')
turtle.listen()

# Time at start of loop
loop_start = time.time()

simulation_on = True

while simulation_on:
    if KeyAction == True:
        if setsolarsystem == True:
            for body in bodylist:
                body.Body_turtle.hideturtle()
            bodylist = []
            add_solar_system()
            setsolarsystem = False

        if addNew == True:
            velocity = newBodyVelocity(down_x, down_y, up_x, up_y)
            newBody((down_x, down_y), velocity, standard_mass)
            print("new body added at", down_x, down_y)
            addNew = False
            
        KeyAction = False
        
    if bodylist == []:
        print("Adding new body at 0,0 to prevent crash")
        newBody((0.000001,0),(0,0),m)
    
    frame = []
    for body in bodylist:
        #print(f"{bodylist[4].position[0]-bodylist[3].position[0]}\n{bodylist[4].position[1]-bodylist[3].position[1]}")
        if aabs(body.position[0]) > 2000*turtle_scale or aabs(body.position[1]) > 2000*turtle_scale:
            bodylist.remove(body)
            print(f"terminated {body.ID} (outside of perimeter)")
            continue
        
        frame.append(dummy(body.ID, body.mass, body.position))
        
    
    for body in bodylist:
        body.acceleration[0] = 0
        body.acceleration[1] = 0

        for other_body in frame:
            if body.ID != other_body.ID:
                acceleration = calculateAcceleration(body, other_body)
                
                body.acceleration[0] += acceleration[0]
                body.acceleration[1] += acceleration[1]

        # Flawed system

        delta_velocity_x = body.acceleration[0]*time_constant
        delta_velocity_y = body.acceleration[1]*time_constant

        body.velocity = (body.velocity[0] + delta_velocity_x, body.velocity[1] + delta_velocity_y)
        body.position = (body.position[0] + body.velocity[0], body.position[1] + body.velocity[1])
        
    for body in bodylist:
        body.updateTurtle()


## Heading
##        if self.velocity[0] == 0:
##            self.Body_turtle.hideturtle()
##        else:
##            self.Body_turtle.showturtle()
##            angle = degrees(atan(self.velocity[1]/self.velocity[0]))
##            
##            if self.velocity[0] < 0:
##                angle += 180
##            
##            self.Body_turtle.setheading(angle)
        
        #Body("1", "blue", 0.5, 1*m,(1*r,0),(0,1*v)),
        #Body("1", "green", 0.5, 1*m,(-1*r,0),(0,-1*v)),
        #Body("1", "orange", 0.5, 1*m,(1*r,-0.5*r),(0,1*v)),
        #Body("1", "purple", 0.5, 1*m,(-1*r,2*r),(2*v,-3*v)),
        #Body("1", "brown", 0.5, 1*m,(-1.5,-5),(0,-0.04))
