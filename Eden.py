# Eden.py
# Core class definitions and visualisation tools for the Eden Simulation
# Author: Saf Flatters
# Year: 2023

"""
This module defines the main entities for the Eden ecosystem simulation:
- Animals: Ant, Butterfly, Caterpillar, Lizard, Worm
- Food sources: Flower, Fossil
- Environmental events: Rain

Each entity is implemented as a class, using an object-oriented design approach
with inheritance and behavior modeling. Visualisation is handled via custom
SVG-based markers.

To install dependencies, run:
    pip install -r requirements.txt
"""


import matplotlib.pyplot as plt
import numpy as np
import random                           #to allow for random movement choices by animals
import sys
from matplotlib import patches
from svgpathtools import svg2paths      #import images for objects - DEPENDENCY - NEED TO INSTALL svgpath2mpl and svgpathtools (pip)
from svgpath2mpl import parse_path      #same as above

# this is for visualisation of objects - Reference: https://petercbsmith.github.io/marker-tutorial.html
#MUST USE SVG imports for this to work 

try:
    butter1path, attributes = svg2paths("Critters/openbutter.svg")
    butter1_marker = parse_path(attributes[0]['d'])
    butter1_marker.vertices -= butter1_marker.vertices.mean(axis=0)

    butter2path, attributes = svg2paths("Critters/closedbutter.svg")
    butter2_marker = parse_path(attributes[0]['d']) 
    butter2_marker.vertices -= butter2_marker.vertices.mean(axis=0)

    lizard1path, attributes = svg2paths("Critters/lizardleft.svg")
    lizard1_marker = parse_path(attributes[0]['d'])
    lizard1_marker.vertices -= lizard1_marker.vertices.mean(axis=0)

    lizard2path, attributes = svg2paths("Critters/lizardright.svg")
    lizard2_marker = parse_path(attributes[0]['d'])
    lizard2_marker.vertices -= lizard2_marker.vertices.mean(axis=0)

    antpath, attributes = svg2paths("Critters/ant.svg")
    ant_marker = parse_path(attributes[0]['d'])
    ant_marker.vertices -= ant_marker.vertices.mean(axis=0)

    flowerpath, attributes = svg2paths("Critters/flower.svg")
    flower_marker = parse_path(attributes[0]['d'])
    flower_marker.vertices -= flower_marker.vertices.mean(axis=0)

    fossilpath, attributes = svg2paths("Critters/fossil.svg")
    fossil_marker = parse_path(attributes[0]['d'])
    fossil_marker.vertices -= fossil_marker.vertices.mean(axis=0)
    #REFERENCE: Converted PNG images to SVG with https://convertio.co/

except FileNotFoundError:
    print("An SVG cartoon file to plot your critters doesn't exist. Please check file paths. (See README)")
    sys.exit(1)
    




def flipCoords(rcpos, LIMITS):           #makes col (left to right)[1] = x, rows (up to down)[0]
    y = rcpos[0]
    x = rcpos[1]
    return (x,y)





#super classes: Animal, Food and Event #(5)

class Animal:                                                                   #(5)
    def __init__(self, name, row, column, status):
        self.name = name
        self.pos = int(row), int(column)
        self.status = status
    
    def getPos(self):                   
        return self.pos
    
class Food:                                                                     #(6)
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
    
    def getPos(self):                   
            return self.pos
    
class Event:                                                                    #(7)
    def __init__(self, name, pos, status):
        self.status = status
        self.name = name
        self.pos = pos

    def getPos(self):                   
        return self.pos



########################ANIMALS#################################
#ANTS
#Ants walk around in 0.1 to 0.21 terrain (underground). 
#They can walk through tunnels (0.1) or dig tunnels in the ground.
#They seek out to eat fossils when hungry which happens ()timesteps after their last fossil meal. (Fossils are existing or made by worms dying)
#Ants will eat fossils when they not hungry but have randomly moved to it's position but wont actively seek them out 
#Ants can not move through wormms but may be plotted next to them
#When raining, they move,dig,eat at twice the speed (done inside playEden by plotting twice in 1 timestep)
#Ants are plotted with SVG drawing of Ant (drawn by me)
#Numbers of ants are plotted as x-axis title
#FUTURE WORKS: To be born from a queen and to die by Worms or die by starvation (if self.time_since_fossil is over 60)

#subclass - inheritance from super class 
class Ant(Animal):                                          #(5.1)     
    size = 0.5                        
    colour = "black"

    def __init__(self, name, row, column, status, hungry, fossils):
        super().__init__(name, row, column, status)
        self.hungry = hungry
        self.fossils = fossils
        self.time_since_fossil = 0              #set time since ant has eaten a fossil

    def printit(self):
        print('SPAWNED ANT! Name: ', self.name, '\tPosition ', self.pos,  "\t\"All HAIL the QUEEN!\" ")    
    
    def lookforFood(self, fossils):
        if self.hungry:
            distances = [np.linalg.norm(np.array(self.pos) - np.array(ff.getPos())) for ff in fossils]              #dist_matrix = np.linalg.norm(vector - matrix_b) < measures distance between object and fossils
            if distances:                                                                                           #https://stackoverflow.com/questions/67528536/python-using-numpy-linalg-norm-to-find-distance-matrix-how-calculated
                target_fossils = fossils[np.argmin(distances)]                                                      #Assigns closest fossil
                return target_fossils

    def stepChange(self, subgrid, fossils):

        if self.hungry == True:
            target_fossil = self.lookforFood(fossils)
            if target_fossil:
                target_pos = target_fossil.getPos()                                           #sets target position to target fossil location
                drow = target_pos[0] - self.pos[0]                                            #drow = distance in rows between target and self  
                dcol = target_pos[1] - self.pos[1]                                            #dcol = distance in cols between target and self

                if self.pos != target_pos:                                                      # if the ant is not at the target 
                    validMoves = [(-1, 0), (0, -1), (0, 1), (1, 0)]                             #von Nuemann moves
                    fosMoves = []                                                               

                    if abs(drow) > abs(dcol):                                               #to make sure only 1 row move OR 1 col move 
                        move_drow = 1 if drow > 0 else -1
                        move_dcol = 0
                    else:
                        move_drow = 0
                        move_dcol = 1 if dcol > 0 else -1

                    fosMoves.append((move_drow, move_dcol))

                    if 0 < subgrid[move_drow + 1, move_dcol + 1] < 0.22:                    #ensure move is within ground/tunnel terrain 
                        self.pos = (self.pos[0] + move_drow, self.pos[1] + move_dcol)       #move valid - do it
                    else:                                                               #OR IF NO WAY TO GET TO FOSSIL: just do random movement
                        tunMoves = []                                                #moves that are valid and in ground or tunnels 

                        for r,c in validMoves:                                       #for row and column in valid moves
                            if 0 < subgrid[r+1,c+1] < 0.22:                          # if subgrid is ground or tunnel
                                tunMoves.append((r, c))                             #add to tunMoves valid move options
        
                            if len(tunMoves) > 0:                                       #if tunnel move options are greater than 0
                                move = random.choice(tunMoves)                           #randomly choose a tunnel move
                                self.pos = (self.pos[0] + move[0], self.pos[1] + move[1]) 

                else:                                   #if ant on top of fossil:
                    #if self.pos == target_pos:
                        self.hungry = False                     #set hunger to false now ant has eaten 
                        self.time_since_fossil = 0              #reset counter (since last ate)
                        #print("Ant", self.name, "ate Fossil:", target_fossil.name, "!") #inplayEden to ensure all fossils get called out regardless if ants hungry or not

        else:                                                            #not hungry and just random crawling/digging
        
            validMoves = [(-1,0), (0,-1), (0,1), (1,0)]                  #von Nuemann valid moves in a subgrid
            tunMoves = []                                                #moves that are valid and in ground or tunnels 
                
            for r,c in validMoves:                                       #for row and column in valid moves
                if 0 < subgrid[r+1,c+1] < 0.22:                          # if subgrid is ground or tunnel
                    tunMoves.append((r, c))                             #add to tunMoves valid move options
        
            if len(tunMoves) > 0:                                       #if tunnel move options are greater than 0
                move = random.choice(tunMoves)                           #randomly choose a tunnel move
                self.pos = (self.pos[0] + move[0], self.pos[1] + move[1])       #new position xy = randomly chosen tunnel move

        self.time_since_fossil += 1                                                     #add 1 second onto time since ant ate
        if self.time_since_fossil > 20:                                                 #stay not hungry for 20 timesteps
            self.hungry = True                                                          #set hungry back to true

    def plotMe(self, ax, LIMITS):                                   #ax sets itself to plot
        XYpos = flipCoords(self.pos, LIMITS)                         #row-col xy stuff
        ax.plot(XYpos[0], XYpos[1], marker=ant_marker, markersize=6, color=self.colour, zorder=5) #matplotlib markers https://matplotlib.org/stable/api/markers_api.html, 
                                                                                                    #zorder layers: https://saturncloud.io/blog/specifying-the-order-of-matplotlib-layers-a-guide/
        #redundant but incase SVG images are removed
        #circle1 = plt.Circle(XYpos, self.size, color=self.colour)   #makes a dot 
        #ax.add_patch(circle1)                                       # puts dot into plot


#BUTTERFLIES
#Butterflys can fly anywhere that isn't the ground, rocks or tunnels (>0.35). 
#They eat the nectar off flowers when they are hungry which is set to turn from False to True every ()timesteps after their last meal
#Butterflys are eaten by Lizards when they are in reach (infront of it's head) or ontop of one 
#When there is less than ()Butterflies due to being eaten, a caterpillar will turn into one after it's growing process *see Caterpillar Class
#When it's raining - butterflies seek to be closer to the ground, they are set to not hungry
#Numbers of butterflies are plotted as x-axis title
#Butterflies are plotted in 2 different ways and alternating between 2 groups:
#The 2 different ways are plotted as an image with it's wings far back or plotted with wings spread open - this is to give the look that it's flying (and depends on whether the timestep is odd or even) 
#The 2 groups are so not all butterflies flap together - the groups are separated by whether the first digit in it's name is Odd or Even
#Both images are SVG drawings (drawn by me)
#FUTURE WORKS: dead butterflies become fossils 

#subclass - inheritance from super class
class Butterfly(Animal):                          #(5.3)
    size = 1  

    def __init__(self, name, row, column, colour, status, hungry, flowers): 
        super().__init__(name, row, column, status)         
        self.colour = colour                   
        self.hungry = hungry            
        self.flowers = flowers
        self.time_since_flower = 0              #set time since butterfly has landed on a flower

    def printit(self):
        print('SPAWNED BUTTERFLY! Name: ', self.name, '\tPosition ', self.pos, '\tColour: ', self.colour, "\t\"Oooo Pretty flowers!\" ")
    
    def lookforFood(self, flowers):
        if self.hungry:
            distances = [np.linalg.norm(np.array(self.pos) - np.array(f.getPos())) for f in flowers]        #dist_matrix = np.linalg.norm(vector - matrix_b) < measures distance between object and fossils
            if distances:                                                                                    #https://stackoverflow.com/questions/67528536/python-using-numpy-linalg-norm-to-find-distance-matrix-how-calculated
                target_flower = flowers[np.argmin(distances)]
                return target_flower

    def stepChange(self, subgrid, flowers, raindance):
        
        if self.status == "alive":          #If butterfly is alive, it's not raining and it's hungry:
            if raindance == False:
                if self.hungry == True:
                    target_flower = self.lookforFood(flowers)

                    if target_flower:                               #Determine move to move closer to target flower but as Moore Neighbours moves
                        target_pos = target_flower.getPos()
                        drow = target_pos[0] - self.pos[0]
                        dcol = target_pos[1] - self.pos[1]

                        if drow > 0:
                            move_drow = 1
                        elif drow < 0:
                            move_drow = -1
                        else:
                            move_drow = 0

                        if dcol > 0:
                            move_dcol = 1
                        elif dcol < 0:
                            move_dcol = -1
                        else:
                            move_dcol = 0

                        self.pos = (self.pos[0] + move_drow, self.pos[1] + move_dcol)

                        if self.pos == target_pos:
                            self.hungry = False             #set hunger to false now butterfly has eaten 
                            self.time_since_flower = 0      #reset counter (since last ate)
                            print("Butterfly", self.name, "ate some nectar from Flower:", target_flower.name, "!")

                else:                           #If butterfly is alive, it's not raining and it's not hungry
                    validMoves = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]     #MOORE NEIGHBOURS
                    flyMoves = []                                                                   #moves that are in are not into the ground and tunnels, Clouds

                    for r,c in validMoves:                                                                  #for row and column in valid moves
                        
                        if subgrid[r+1,c+1] > 0.35:                                              #subgrid 3x3 around bfly but matrix read from centre, bfly wont enter terrain cells less than 0.2 (border, ground, tunnels)
                            flyMoves.append((r, c))                                                 #confirmed moves once checked its not ground, clouds or tunnel

                    if len(flyMoves) > 0:                                                             #if fly move options are greater than 0
                        move = random.choice(flyMoves)                                              #randomly choose a fly move
                        self.pos = (self.pos[0] + move[0], self.pos[1] + move[1])                   #new position xy = randomly chosen 
                
                self.time_since_flower += 1                                                     #add 1 second onto time since butterfly ate
                if self.time_since_flower >=15:
                    self.hungry = True

            else:                                                       #If butterfly is alive, it's raining and regardless if hungry
                self.hungry = False                                     #hunger goes to false
                validrainMoves = [(1,1),(1,0),(0,0),(1,-1)]                #only down movements and not moving
                flyrainMoves = []                                                                   #moves that are in are not into the ground and tunnels, Clouds

                for r,c in validrainMoves:                                                                 #for row and column in valid moves
                    if subgrid[r+1,c+1] > 0.35:                                              #subgrid 3x3 around bfly but matrix read from centre, bfly wont enter terrain cells less than 0.2 (border, ground, tunnels)
                            flyrainMoves.append((r,c))

                    if len(flyrainMoves) > 0:                                                             #if fly move options are greater than 0
                        rainmove = random.choice(flyrainMoves)                                              #randomly choose a fly move
                        self.pos = (self.pos[0] + rainmove[0], self.pos[1] + rainmove[1]) 
          
    def butterdeath(self, killer):                                      #if butterfly is dead: the death of a butterfly triggered by being at the same position or in reach of a lizard, killer = lizards name
        self.status = "dead"
        print('\nBUTTERFLY', self.name, 'has been eaten by Lizard', killer, '!')
        print('\"Butterfly', self.name, 'has left the chat. RIP\"\n')

        #2 plots alternating to make it look like butterflies are flapping

    def plotMeopen(self, ax, LIMITS):                                 
        XYpos = flipCoords(self.pos, LIMITS)
        ax.plot(XYpos[0], XYpos[1], marker=butter1_marker, markersize=15, color=self.colour, zorder=4)  #matplotlib markers https://matplotlib.org/stable/api/markers_api.html, 
                                                                                                    #zorder layers: https://saturncloud.io/blog/specifying-the-order-of-matplotlib-layers-a-guide/
        #redundant but incase SVG images are removed
        #circle1 = plt.Circle(XYpos, self.size, color=self.colour)
        #ax.add_patch(circle1)

    def plotMeclosed(self, ax, LIMITS):                                                          
        XYpos = flipCoords(self.pos, LIMITS)
        ax.plot(XYpos[0], XYpos[1], marker=butter2_marker, markersize=15, color=self.colour, zorder=3)  #matplotlib markers https://matplotlib.org/stable/api/markers_api.html, 
                                                                                                    #zorder layers: https://saturncloud.io/blog/specifying-the-order-of-matplotlib-layers-a-guide/
        #redundant but incase SVG images are removed
        #circle1 = plt.Circle(XYpos, self.size, color= "red")                                   #makes dot red to show flapping
        #ax.add_patch(circle1)                                                                   # puts dot into plot


#CATERPILLARS
#Caterpillars are born when there is less than the original amount of butterflies
#Only 1 caterpillar exists at a time so butterflies don't get rejuvinated numbers easily
#Caterpillars are born in random location at specific height on 1 tree in the plot
#They can only move left and right and do not enter the sky
#After ()timesteps of caterpillar being born, they turn into a cacoon
#The cacoon sits in position of caterpillars last position
#After ()timesteps of cacoon, it turns into a butterfly and joins butterfly class
#Caterpillars are plotted as a horizonta Ellipse patch with green edge and red fill
#Cacoonss are plotted as a vertical Ellipse patch - olive colour
#Numbers of Caterpillars are plotted as x-axis title
#FUTURE WORKS: more caterpillars, more locations, SVG images to replace plot patches (drawn by me), caterpillars to seek leaves to eat

#subclass - inheritance from super class
class Caterpillar(Animal):                          #(5.4)

    def __init__(self, name, row, column, status):
        super().__init__(name, row, column, status)


    def printit(self):
        print('\nSPAWNED CATERPILLAR! Name: ', self.name, '\tPosition ', self.pos,)
        print("\t\"i'M a HUnGRy HUnGRy CAtErpilLAR!\" ")    
    
    def stepChange(self, subgrid):
        validMoves = [(0,-1), (0, 1)]                                                               #only can move left and right
        branchMoves = []                                                                             #moves that are valid and in grass or tree trunks (not sky)
               
        for r,c in validMoves:                                                                      #for row and column in valid moves
            if subgrid[r+1,c+1] <0.8:                                                          # if subgrid is on tree
                branchMoves.append((r, c))                                                       #add to branchMoves -confirmed move option if valid

        if len(branchMoves) > 0:                                                                 
            move = random.choice(branchMoves)                                                    
            self.pos = (self.pos[0] + move[0], self.pos[1] + move[1])                               

    def plotMe(self, ax, LIMITS):                                               
        XYpos = flipCoords(self.pos, LIMITS) 
        ellipse1 = patches.Ellipse(XYpos, 3, 1, facecolor="red", edgecolor="green", zorder=3)   #Reference for learning about Ellipse patches: https://matplotlib.org/3.1.1/gallery/units/ellipse_with_units.html#sphx-glr-gallery-units-ellipse-with-units-py 
        ax.add_patch(ellipse1)
        
    def plotCacoon(self, ax, LIMITS):                                                                 
        XYpos = flipCoords(self.pos, LIMITS)                    
        ellipse2 = patches.Ellipse(XYpos, 1, 4, facecolor="olive", edgecolor="black", zorder=3)  #Reference for learning about Ellipse patches: https://matplotlib.org/3.1.1/gallery/units/ellipse_with_units.html#sphx-glr-gallery-units-ellipse-with-units-py 
        ax.add_patch(ellipse2)



#LIZARDS
#Lizards can only walk through grass, climb trees and rocks
#Only () lizards at a time to ensure butterfly populationn does not fall
#Lizards can move in Moore Neighbourhoods
#Lizards do not die and will eat butterflies if they are in reach (infront of their head) or ontop of them but do not seek prey (in playEden)
#Lizards are not affected by rain
#Numbers of Lizards are plotted as x-axis title
#Lizards are plotted with 2 SVG Images (drawn by me)
#Lizards are plotted in 2 different ways and alternating between 2 groups:
#Lizards either have their left leg in front or their right leg in front to give the impression they are walking/climbing
#Lizards are plotted alternatively in these positions (using their name digit, odd or even method) so they don't all walk the same way
#FUTURE WORKS: Lizards to be born, die of starvation, change colour in the rain, more lizards, make it more likely for lizards to eat butterflies(more inreach positions), different images depending whether they walking or climbing

#subclass - inheritance from super class
class Lizard(Animal):                 #(5.4)                                                    
    size = 1.5                         
    colour = "darkgoldenrod"

    def __init__(self, name, row, column, status, hungry):
        super().__init__(name, row, column, status)                   
        self.hungry = hungry
    
    def printit(self):
        print('SPAWNED LIZARD! Name: ', self.name, '\tPosition ', self.pos, "\t\"Slurp Slurp!\" ")    
    
    def inReach(self):                              #one row above their head to check butterfly location is inreach to eat
        return (self.pos[0]-1, self.pos[1])

    def stepChange(self, subgrid):

        validMoves = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]                  #Moore
        grassMoves = []                                                                             #moves that are valid and in grass or tree trunks or rocks
               
        for r,c in validMoves:                                                                      #for row and column in valid moves
            if 0.24 < subgrid[r+1,c+1] < 0.79:                                                           # if subgrid is in grass or rock or on tree
                grassMoves.append((r, c))                                                       #add to grassMoves -confirmed move option if valid

        if len(grassMoves) > 0:                                                                 #if grassmoves move options are greater than 0
            move = random.choice(grassMoves)                                                    #randomly choose a grass move
            self.pos = (self.pos[0] + move[0], self.pos[1] + move[1])                               #new position xy = randomly chosen tunnel move

        #2 plots alternating to make it look like lizards are walking/climbing
    def plotMeright(self, ax, LIMITS):                                               
        XYpos = flipCoords(self.pos, LIMITS) 
        ax.plot(XYpos[0], XYpos[1], marker=lizard1_marker, markersize=45, color=self.colour, zorder=6)  #matplotlib markers https://matplotlib.org/stable/api/markers_api.html, 
                                                                                                    #zorder layers: https://saturncloud.io/blog/specifying-the-order-of-matplotlib-layers-a-guide/
        #redundant but incase SVG images are removed 
        #circle1 = plt.Circle(XYpos, self.size, color=self.colour)                                   
        #ax.add_patch(circle1)                                                                  

    def plotMeleft(self, ax, LIMITS):                                                          #for walking animation - left, right, left, right
        XYpos = flipCoords(self.pos, LIMITS) 
        ax.plot(XYpos[0], XYpos[1], marker=lizard2_marker, markersize=45, color=self.colour, zorder=7) #matplotlib markers https://matplotlib.org/stable/api/markers_api.html, 
                                                                                                    #zorder layers: https://saturncloud.io/blog/specifying-the-order-of-matplotlib-layers-a-guide/
        #redundant but incase SVG images are removed
        #circle1 = plt.Circle(XYpos, self.size, color= "red")                                   
        #ax.add_patch(circle1)                                                                  



#WORMS
#Worms can only move underground
#There is only 1 worm at a time and with each timestep it grows longer 
#Worms can only move VonNuemann Neighbourhoods and can not move throught itself
#After random interval of (*-*)timesteps a worm has been alive, it dies and all the positions it took up now have fossils in place (to be eaten by ants)
#A new worm is born in random underground location when existing worm dies
#Worms and worm tails are plotted with circle patches (head being slightly bigger)
#Numbers of worms are plotted as x-axis title
#FUTURE WORKS: Worms to eat ants, worm head and tail to be plotted with SVG images (drawn by me)
#subclass - inheritance from super class

class Worm(Animal):             #(5.5)
    size = 1.2                          
    colour = "darkseagreen"

    def __init__(self, name, row, column, status, hungry):                             #1 worm appears at start of Eden and then 1 is born when the existing dies
        super().__init__(name, row, column, status)
        self.hungry = hungry
        self.oldtail = [self.pos]                                                     #list of positions of tail so worms grow and slowly take over ground

    def printit(self):                      
        print('\nSPAWNED WORM! Name: ', self.name, '\tPosition ', self.pos, "\t\"Hello, I'm Dr Worm!\"")    

    def storeoldtail(self):                                                           #store location of current position into  tail list
        self.oldtail.append(self.pos)
    
    def stepChange(self, subgrid):
        if self.status == "alive": 
            validMoves = [(-1,0), (0,-1), (0,0), (0,1), (1,0)]                                         #von Nuemann valid moves in a subgrid
            slugMoves = []
             
            for r,c in validMoves:                                                          #for row and column in valid moves
                if 0 < subgrid[r+1,c+1] < 0.21:                                          # if subgrid is ground or tunnel and NOT OLD tail (0.7) and not fossils (0.21)
                    slugMoves.append((r, c))                                        #add to slugMoves -valid move options
        
            if len(slugMoves) > 0:                                                      #if slugMoves move options are greater than 0
                move = random.choice(slugMoves)                                      #randomly choose a valid slug move
                self.pos = (self.pos[0] + move[0], self.pos[1] + move[1])           #new position xy = randomly chosen tunnel move

    def wormdeath(self):                                                        #Worm dies after ()timesteps of being alive, worm turns into fossils 
        self.oldtail.clear()
        self.status = "dead"
        print('\nWORM ', self.name, 'has DIED from old age! \t\"Goodbye cruel world!\" ')
        print("\t Worm has become ant-food. RIP")

    def plotMe(self, ax, LIMITS):                                               #plots head
        XYpos = flipCoords(self.pos, LIMITS)   
        circle1 = plt.Circle(XYpos, self.size, color=self.colour)  
        ax.add_patch(circle1)          

    def plotMytail(self, ax, LIMITS):                                       #plots worm tail smaller than head
        XYpos = flipCoords(self.pos, LIMITS)   
        circle1 = plt.Circle(XYpos, 0.7, color=self.colour)  
        ax.add_patch(circle1)    


###############################FOOD###########################################

#FLOWERS
#Flowers are in positions that are 0.745 in Terrain (in Trees and on grass)
#Flowers are seeked out by Butterflies when they are hungry to provide nectar
#Flowers are permanent 
#Numbers of flowers are plotted as x-axis title
#Flowers are plotted using SVG image (drawn by me)

#subclass - inheritance from super class
class Flower(Food):                            #(6.1)     #flowers created for butterflys to land on and eat nectar (only placed at 0.745)

    def __init__(self, name, pos):
        super().__init__(name, pos)
        self.colour = "pink"            
        self.size = 0.5                   


    def plotMe(self, ax, LIMITS):
        XYpos = flipCoords(self.pos, LIMITS)
        ax.plot(XYpos[0], XYpos[1], marker=flower_marker, markersize=5, color=self.colour, zorder=1) #matplotlib markers https://matplotlib.org/stable/api/markers_api.html, 
                                                                                                    #zorder layers: https://saturncloud.io/blog/specifying-the-order-of-matplotlib-layers-a-guide/
        #redundant but incase SVG images are removed
        #circle1 = plt.Circle(XYpos, self.size, color=self.colour)
        #ax.add_patch(circle1)


#FOSSILS
#Fossils are in positions that are 0.21 in Terrain (in the ground)
#Fossils are at the beginning of eden and also created by worms when they die
#Fossils are seeked out by ants when they are hungry and are eaten by ants (disappear)
#Numbers of fossils are plotted as x-axis title
#Fossils are plotted using SVG image (drawn by me)

#subclass - inheritance from super class
class Fossil(Food):                                         #fossils created for ants to crawl to and chew on (only places at 0.21)

    def __init__(self, name, pos):
        super().__init__(name, pos)
        self.colour = "white"            
        self.size = 0.2 
    
    def plotMe(self, ax, LIMITS):
        XYpos = flipCoords(self.pos, LIMITS)
        ax.plot(XYpos[0], XYpos[1], marker=fossil_marker, markersize=4, color=self.colour)  #matplotlib markers https://matplotlib.org/stable/api/markers_api.html, 
                                                                                                   
        #circle1 = plt.Circle(XYpos, self.size, color=self.colour)
        #ax.add_patch(circle1)


############################EVENTS#######################

#RAIN
#Raining is triggered for ()timesteps at ()timesteps into the play
#It is plotted in playEden as a scatterplot - (plotting as objects in here required too much computational power)
#Raining triggers other objects (Ants and Butterflies) to perform different movements *see object classes above
#Rain drops are plotted on two different scatterplots so that it looks like its moving (using odd and even timesteps)
#When it rains, it plots a subtitle on the plot to tell us

#subclass - inheritance from super class
class Raining(Event):           #(7.1)

    def __init__(self, name, pos, status):
        super().__init__(name, pos, status)

