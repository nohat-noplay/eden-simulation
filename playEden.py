# playEden.py
# Simulation runner and visualisation for the Eden ecosystem
# Author: Saf Flatters
# Year: 2023

"""
This script executes the Eden Simulation, coordinating the initialisation, 
timestepped evolution, and visualisation of the garden ecosystem.

Key elements:
- Simulates above-ground and below-ground environments, including trees, grass, rocks, anthills, clouds, sun, and ant tunnels.
- Models dynamic interactions between animals (Ants, Butterflies, Caterpillars, Lizards, Worms) and environmental objects (Flowers, Fossils).
- Handles environmental events, such as rain, which dynamically alter animal behaviors and terrain state.
- Visualises each timestep using animated plots with titles reflecting timestep progression, object counts, and rain status.
- Logs animal actions, lifecycle events, and ecosystem changes to the terminal.

User Inputs:
- Number of timesteps to simulate
- Choice of Day or Night visualisation mode

Supports command-line arguments or interactive prompts (see README).
"""


import matplotlib.pyplot as plt
import numpy as np
import random
import sys
import os 

from Eden import *

#(1)
#read in worldscene.csv - for background image
backdrop = []                                                                       # created list for csv numbers
rowcount = 0                                                                         # created rowcount for LIMITS

current_dir = os.path.dirname(__file__)
data_dir = os.path.join(current_dir, "data")
worldscene_path = os.path.join(data_dir, "worldscene.csv")

try:
    worldscene = open(worldscene_path, "r")                           # opened csv file worldscene.csv 
    data = worldscene.readlines()                                                            # read lines from csv file

    for line in data:                                                                    # - for loop - every line in csv file
        rowcount = rowcount + 1                                                              #count rows of lines for LIMITS
        ints = [float(x) for x in line.split(',')]                                          # (2) MADE FLOAT split line up by comma and len(ints) used for LIMITS - Prove I can use List Comprehensions
        backdrop.append(ints)                                                           # put csv numbers found into list

    worldscene.close()                                                                        #close csv file
except FileNotFoundError:
    print("The file to plot your background can not be found. Please check the file path")
    sys.exit(1)

#LEGEND FOR WORLDSCENE          To alter worldscene - open csv in excel and use conditional formatting: Color scales to see the images
#0-0.01 = clouds or border
#0.1 = tunnel
#0.2 = ground
#0.21 = fossil options
#0.25-0.27 = tree trunk or branch
#0.35 = rock
#0.5 = sun
#0.62-0.75 = bush or leaves
#0.7 = worm tail location
#0.745 = flower options
#0.755 = grass
#0.83 = blue sky

#Animals imported from alive.csv
insects = []        #butterflys
inants = []         #Ants
inliz = []          #Lizards
inworm = []         #Worms
other = []          #Future objects

#(2)
#read in alive.csv
alive_path = os.path.join(data_dir, "alive.csv")

try:
    alive = open(alive_path, "r")  # opened csv file alive.csv
    animals = alive.readlines()                                                                 # read lines from csv file

    for line in animals:                                                                    # - for loop - every line in csv file
        splitline = line.split(':')
        if splitline[0] == "Butterfly":
            insects.append(splitline)                                                       
        elif splitline[0] == "Ant":
            inants.append(splitline)
        elif splitline[0] == "Lizard":
            inliz.append(splitline)
        elif splitline[0] == "Worm":
            inworm.append(splitline)
        else:
            other.append(splitline)        

    alive.close()                                                                               #close csv file
except FileNotFoundError:
    print("The file to import your critters can not be found. Please check the file path")
    sys.exit(1)



    #Subgrid for Stepchange for all animals
def getSubgrid(t, pos):
    rmin = int(pos[0])-1
    rmax = int(pos[0])+2
    cmin = int(pos[1])-1
    cmax = int(pos[1])+2
    #print(rmin, rmax, cmin, cmax)
    sub = t[rmin:rmax,cmin:cmax]
    return sub


def main():

#(4) (2)print("\nWelcome to Eden...\n")                                     #introduction to user

    if len(sys.argv) == 3:                                               #command line argument [1] is timestep number, [2] is sundial (day or night)
        timestep1 = sys.argv[1]
        sundial = str(sys.argv[2]).upper()

        try:
            timestep = int(timestep1)
        except ValueError:
                print("Command Argument for timestep is invalid. Please answer these questions \n")
                timestep = None                                                   #how many timesteps to plot
                while timestep is None:
                    try:
                        input1 = input("How many timesteps do you want to play? (3 timesteps per second):   ")
                        timestep = int(input1)
                    except ValueError:                                             #must be integer or Exception Handling
                        print("\'", input1, "\' is an invalid input. Please enter a valid number...")

                sundial = None
                while sundial is None:                                          #choose day or night colourmap
                    try:
                        input2 = input("Is it Day or Night? Type 'D' or 'N'... ").upper()
                        if input2 not in ('D', 'N'):                                #must be D, N, d, n or Exception Handling
                            raise ValueError("Error!", input2, "is an invalid input as it is not 'D' or 'N' ")
                        sundial = str(input2)
                    except ValueError as e:
                        print(e)


        if sundial not in ('D', 'N'):                                   #if sundial is invalid letters
            print("Command Argument for sundial is invalid. Please answer these questions \n")
            timestep = None                                                   #how many timesteps to plot
            while timestep is None:
                try:
                    input1 = input("How many timesteps do you want to play? (3 timesteps per second):   ")
                    timestep = int(input1)
                except ValueError:                                             #must be integer or Exception Handling
                    print("\'", input1, "\' is an invalid input. Please enter a valid number...")

            sundial = None
            while sundial is None:                                          #choose day or night colourmap
                try:
                    input2 = input("Is it Day or Night? Type 'D' or 'N'... ").upper()
                    if input2 not in ('D', 'N'):                                #must be D, N, d, n or Exception Handling
                        raise ValueError("Error!", input2, "is an invalid input as it is not 'D' or 'N' ")
                    sundial = str(input2)
                except ValueError as e:
                    print(e)

    else:
        timestep = None                                                                                     #how many timesteps to plot
        while timestep is None:
            try:
                input1 = input("How many timesteps do you want to play? (3 timesteps per second):   ")
                timestep = int(input1)
            except ValueError:                                             #must be integer or Exception Handling
                print("\'", input1, "\' is an invalid input. Please enter a valid number...")

        sundial = None
        while sundial is None:                                          #choose day or night colourmap
            try:
                input2 = input("Is it Day or Night? Type 'D' or 'N'... ").upper()
                if input2 not in ('D', 'N'):                                #must be D, N, d, n or Exception Handling
                    raise ValueError("Error!", input2, "is an invalid input as it is not 'D' or 'N' ")
                sundial = str(input2)
            except ValueError as e:
                print(e)


#(1)
    #plot scene
    LIMITS = np.array(backdrop)
    terrain = np.array(backdrop)                                                        #sets background SET THIS TO BACKDROP LIST CREATED FROM READING CSV
    plt.figure(figsize=(8,8))                                                       #sets window size >>>>CHANGED FOR EDITING ONLY(1) ((DEPENDS ON THE COMPUTER SCREEN BEING USED))
    ax = plt.axes()                                                                 #makes plot boxes square
    ax.set_aspect("equal")                                                              #makes plot boxes square

    #lists of animals 

    ants = []                                   
    bflys = []                                  
    lizzys = []
    worms = []
    catp = []
    

    #lists of food locations
    flowerpos = []
    fossilpos = []

    #list for worm tail position
    tail = []

    #random number generator for length of worm life before dying of old age
    wormlifeexp = random.randint(12, 30)

    #dead critters
    wormtofossil = []
    deadbflys = []

    #rain
    rain = []
    raindance = False
    allflooded = []

    #counts
    catpcount = 0
    finalcatp = 0
    initialcode = 0  
    originalbflys = len(insects)     #to make sure caterpillars replenish butterflies when they die                                                              

#FOOD
    #flowers    #(6.1)
    flower_rows, flower_cols = np.where(terrain == 0.745)                                                      #REFERENCE for np.where - https://ioflood.com/blog/np-where/
    flowerpos = [Flower("F"+str(i), (row,col)) for i, (row,col) in enumerate(zip(flower_rows, flower_cols))]   #ENUMERATE AND ZIP https://note.nkmk.me/en/python-for-enumerate-zip/    
    



#ANIMALS #
    
   #animal import loops and messages to user
    for i in range(len(inants)):
        ants.append(Ant(inants[i][1], inants[i][2], inants[i][3], inants[i][4], inants[i][5], inants[i][6]))
        
        ants[i].printit()                                                    #All Hail the Queen
       
    for k in range(len(insects)):
        bflys.append(Butterfly(insects[k][1], insects[k][2], insects[k][3], insects[k][4], insects[k][5], insects[k][6], insects[k][7]))
        
        bflys[k].printit()                                                  #Oooo Pretty flowers

    for l in range(len(inliz)):
        lizzys.append(Lizard(inliz[l][1], inliz[l][2], inliz[l][3], inliz[l][4], inliz[l][5]))

        lizzys[l].printit()                                                  #Slurp slurp
    
    for w in range(len(inworm)):
        worms.append(Worm(inworm[w][1], inworm[w][2], inworm[w][3], inworm[w][4], inworm[w][5]))

        worms[w].printit()                                                  #Hello! I'm Dr Worm

#Rain                                                                                   #REFERENCE for np.where - https://ioflood.com/blog/np-where/
    rain_rows, rain_cols = np.where((terrain > 0.36) | (terrain == 0.27))               #REFERENCE | (pipe) Operator used as union - https://ridwanray.medium.com/the-pipe-symbol-in-python-133239503fec
    rain = [Raining("R"+str(r), (row,col), False) for r, (row,col) in enumerate(zip(rain_rows, rain_cols))]    #preloading the rain #REFERENCE: https://note.nkmk.me/en/python-for-enumerate-zip/


#TIMESTEP
    for t in range(timestep):                                                   #each timestep loop (from user input)
   

#ANTS #(5.2)
        for i in range(len(ants)):
            if raindance == True:                                                           #if raining, ants move twice as fast (plot twice)
                ants[i].stepChange(getSubgrid(terrain, ants[i].getPos()), fossilpos)
                tunnel = ants[i].getPos()                                               #ant position changes terrain to 0.1 to show tunnel dug to user
                tunnel_row, tunnel_col = tunnel
                terrain[tunnel_row][tunnel_col] = 0.1
                ants[i].stepChange(getSubgrid(terrain, ants[i].getPos()), fossilpos)
                tunnel = ants[i].getPos()                                               
                tunnel_row, tunnel_col = tunnel
                terrain[tunnel_row][tunnel_col] = 0.1
                ants[i].plotMe(ax,LIMITS)

              

                for f in range(len(fossilpos)):                                             #if raining and for all fossils: if ant is ontop of fossil, fossil is eaten and disappears
                    if ants[i].getPos() == fossilpos[f].getPos():
                        print("Ant", ants[i].name, "ate Fossil:", fossilpos[f].name, "!")
                        eatenfos = ants[i].getPos()                                               #ant position changes terrain to 0.1 to show tunnel dug to user
                        fosrow, foscol = eatenfos
                        terrain[fosrow][foscol] = 0.1

            if raindance == False:
                ants[i].stepChange(getSubgrid(terrain, ants[i].getPos()), fossilpos)   #if not raining, ants move at normal speed
                ants[i].plotMe(ax,LIMITS)                                               
                tunnel = ants[i].getPos()                                               #ant position changes terrain to 0.1 to show tunnel dug to user
                tunnel_row, tunnel_col = tunnel
                terrain[tunnel_row][tunnel_col] = 0.1

                for f in range(len(fossilpos)):                                             #if not raining and for all fossils: if ant is ontop of fossil, fossil is eaten and disappears
                    if ants[i].getPos() == fossilpos[f].getPos():
                        print("Ant", ants[i].name, "ate Fossil:", fossilpos[f].name, "!")
                        eatenfos = ants[i].getPos()                                               #ant position changes terrain to 0.1 to show tunnel dug to user
                        fosrow, foscol = eatenfos
                        terrain[fosrow][foscol] = 0.1
  

#BUTTERFLIES     #(5.3)
        for i in range(len(bflys)):
            if raindance == False:              #butterfly sends rain status to class through StepChange
                bflys[i].stepChange(getSubgrid(terrain, bflys[i].getPos()), flowerpos, False)   
            if raindance == True:   
                bflys[i].stepChange(getSubgrid(terrain, bflys[i].getPos()), flowerpos, True)
                                                                                         
            #butterflys plotted to look like they flap (and not all together so half flap opposite to other half) *see description in class Eden.py file
            if t % 2 != 0:
                if int(bflys[i].name[1:]) % 2 != 0:
                    bflys[i].plotMeopen(ax, LIMITS)                                            
                else:
                    bflys[i].plotMeclosed(ax, LIMITS)
            else: 
                if int(bflys[i].name[1:]) % 2 == 0:
                    bflys[i].plotMeopen(ax, LIMITS)                                           
                else:
                    bflys[i].plotMeclosed(ax, LIMITS)

            #butterflies eaten by lizards if they are ontop or next to lizards tongue
            for l in range(len(lizzys)):
                if bflys[i].getPos() == lizzys[l].getPos():                         #lizards eat butterflys that are right on top of them
                    bflys[i].butterdeath(lizzys[l].name)
                    deadbflys.append(i)

            for l in range(len(lizzys)):
                if bflys[i].getPos() == lizzys[l].inReach():                         #lizards eat butterflys that are in reach of their tongue (1 row higher)
                    bflys[i].butterdeath(lizzys[l].name)
                    deadbflys.append(i)



#CATERPILLAR    #(5.4)
        babybflys = []
        if len(bflys) < originalbflys:                                                      #if there are less than the original number of butterflies
            if len(catp) == 0:                                                              #if there is no caterpillars existing at that timestep
                catp.append(Caterpillar("C"+str(t), 14, 50+random.randint(0,4), "alive"))
                catpcount = catpcount +1
                finalcatp = finalcatp + 1   

                for c in range(len(catp)): 
                        catp[c].printit()                                                   #announce arrival

            elif 0 < catpcount < 10:                                                        #first 9 timesteps its a caterpillar moving in a tree
                for c in range(len(catp)):
                    catp[c].stepChange(getSubgrid(terrain, catp[c].getPos()))
                    catp[c].plotMe(ax, LIMITS)
 
                    catpcount = catpcount +1

            elif 9 < catpcount < 16:                                                       #10-15 timesteps its a cacoon hanging off a tree
                    for c in range(len(catp)):
                        catp[c].plotCacoon(ax, LIMITS)
  
                        if catpcount == 11:
                            print("\nCATERPILLAR HAS TURNED INTO COCOON")
                            print("\t\"shhhh Caterpillar baby is sleeping...zz.zzz.zzz\"")
                        catpcount = catpcount +1

            elif catpcount ==16:
                    for c in range(len(catp)):                                                             #at 16 timesteps, butterfly is born
                        print("\nCATERPILLAR HAS TURNED INTO BUTTERFLY!")
                        print("\t\"Hear me ROAR!\"")
                        babybflys.append(Butterfly("C"+str(t), 16, 52, "black", "alive", True, flowerpos)) #made black colour to track new born butterflies from existing
                        babybflys[-1].printit()
                                                                         #print the latest baby butterfly (only 1 born per 16 timesteps)
                        catp.pop(0)
                                                       #delete number of caterpillars back to 0
                        catpcount = 0                                            #add each time step to count for above code

        #to ensure indexing is correct, each timestep, butterflies not eaten (still set to "alive") go to new list and end of timestep, surviving butterflies are now the entire bfly list
        survivingbflys = []
                
        for x in range(len(bflys)):
            if bflys[x].status == "alive":
                survivingbflys.append(bflys[x])
        survivingbflys.extend(babybflys)                                                    #surviving bfly list must be extended to allow for new butterflies born at that time step

        bflys = survivingbflys
        babybflys = []                                                                      #delete baby butterflies list once added to surviving butterflies
 


#LIZARDS        #(5.4)
        for i in range(len(lizzys)):                                                
            lizzys[i].stepChange(getSubgrid(terrain, lizzys[i].getPos()))           
            
        #plots 2 different plots so lizards walk left right left right (and not all together):    
            if t % 2 != 0:                                      #for every odd timestep
                if int(lizzys[i].name[1:]) % 2 != 0:            #if lizard name number is odd
                    lizzys[i].plotMeright(ax, LIMITS)           #right foot out infront                                 
                else:
                    lizzys[i].plotMeleft(ax, LIMITS)            #left foot out infront
            else:                                               #for every even timeste
                if int(lizzys[i].name[1:]) % 2 == 0:            #if lizard name number is even
                    lizzys[i].plotMeright(ax, LIMITS)           #right foot out infront                                 
                else:
                    lizzys[i].plotMeleft(ax, LIMITS)            #left foot out infront
        


#WORMS      #(5.5)
        for i in range(len(worms)):                                                 
            worms[i].stepChange(getSubgrid(terrain, worms[i].getPos()))             
            worms[i].storeoldtail()                                                #worm class store location of current position into old tail list 
            for i in range(len(worms)):                                             
                for pos in worms[i].oldtail:                                       #for each position listed in oldtail list
                    worms[i].pos = pos                                             #make position a current position
                    worms[i].plotMytail(ax, LIMITS)                                #plot worm tail at old positions (to make it grow)

            worms[i].plotMe(ax, LIMITS)                                             #stops worm from touching itself, stops ants from building tunnels through worm (makes terrain 0.7)
            tail = worms[i].getPos()
            tail_row, tail_col = tail
            terrain[tail_row][tail_col] = 0.7                                     #worms change terrain to 0.7

            #deathmarch of the worm
            if len(worms[i].oldtail) == wormlifeexp:                               #at a random time chosen by wormlifeexp (earlier in code), checked against tail length (age)

                for row in range(terrain.shape[0]):                                 #nested loop collecting all locations of where worm has been
                    for col in range(terrain.shape[1]):
                        if terrain[row, col] == 0.7:    
                            wormtofossil.append((row, col))

                for k, (row, col) in enumerate(wormtofossil):                       #for all locations, worm is plotted, add to wormtofossil list
                    fossilpos.append(Fossil("FFT" + str(k), (row, col)))            #makes old worm location into fossil position which get changed to fossils at end of timestep

                terrain[terrain == 0.7] = 0.21                                      #makes old worm terrain 0.7 into fossil ground
            #Remove dead worm 
                worms[i].wormdeath()                                                #wormdeath clears oldtail list, changes status to dead and notifys user
                worms.pop(i)                                                        #removes worm from worms list


        #birth of new worm
        if len(worms) == 0:                                                         #when worm is 
            worms.append(Worm("W"+str(i), 35+random.randint(0,15), 10+random.randint(0,90), "alive", False))
            for w in range(len(worms)): 
                worms[w].printit()
       


#FOOD          (#6)
        for flower in flowerpos:                                    #(6.1)
            flower.plotMe(ax, LIMITS)                                               #plots flowers at all positons that is 0.745

        fossil_rows, fossil_cols = np.where(terrain == 0.21)                  #(6.2)      #REFERENCE for np.where - https://ioflood.com/blog/np-where/
        fossilpos = [Fossil("FF"+str(f), (row,col)) for f, (row,col) in enumerate(zip(fossil_rows, fossil_cols))]       #ENUMERATE AND ZIP https://note.nkmk.me/en/python-for-enumerate-zip/

        for fossil in fossilpos:                                                    #plots fossils at all positions that is 0.21
            fossil.plotMe(ax, LIMITS)



#RAIN (event)           #(7.1)
#Plot raindrops as simple dots (rather than an object as my computer could not handle the process)
        rain_r = []  
        rain_c = []  
        rain_r2 = []  
        rain_c2 = []  

        if 35 < initialcode < 50:                            #select time (between timestep * and timestep *)

            print("MA! THE RAINS ARE HERE!")                    #each timestep it rains
            raindance = True                                #raining
            for drop in rain[::2]:                          #every second raindrop in rain list
                drop.status = "on"
                if drop.status == "on":
                    rain_r.append(drop.getPos()[1])         #plot position row
                    rain_c.append(drop.getPos()[0])         #plot position col

            for drop in rain[1::2]:                          #every other raindrop in rain list
                drop.status = "on"
                if drop.status == "on":
                    rain_r2.append(drop.getPos()[1])        #plot position row
                    rain_c2.append(drop.getPos()[0])        #plot position col

        else: 
            for drop in rain:                               #not raining
                drop.status = "off"
                raindance = False

        #Plot raindrops as dots alternating positions
        if t % 2 != 0: 
            ax.scatter(rain_r, rain_c, c='blue', marker='d', s=1)
        if t % 2 == 0: 
            ax.scatter(rain_r2, rain_c2, c='blue', marker='d', s=1)  

        if raindance == True:
            floodrow = None
            flooded = []
            
            
            for row in range(len(terrain)):
                for col in range(len(terrain[row])):
                    if terrain[row][col] == 0.1:
                        if floodrow is None:
                            floodrow = row
                        if row == floodrow:
                                terrain[row][col] = 0.2
                                flooded.append((row,col))

            allflooded.extend(flooded)                    

            for i in range(len(allflooded)):
                row, col = allflooded[i]                    
                ax.plot(col, row, "D", markersize=5, color="blue")



                            

#PLOT
        #Print numbers of objects at the beginning and print numbers of objects at the end
        if t ==1 :
            print("Started:  ",len(fossilpos), " Fossils ",len(bflys), " Butterflies  ",len(catp), " Caterpillars  ", len(ants), " Ants  ", len(lizzys), " Lizards  ", len(worms), " Worms  ", len(flowerpos), " Flowers")
        if t == timestep -1: 
            print("Survived: ", len(fossilpos), " Fossils ",len(bflys), " Butterflies  ",len(catp), " Caterpillars  ", len(ants), " Ants  ", len(lizzys), " Lizards  ", len(worms), " Worms  ", len(flowerpos), " Flowers")


        initialcode = initialcode + 1                                                    #add one each timestep for plot title

        #colour map the terrain
        if sundial == "N":
            cmap = plt.get_cmap("twilight_r")                                                   #MATPLOTLIB Twilight colour (reverse) into plot #REFERENCE https://matplotlib.org/stable/users/explain/colors/colormaps.html
            plt.title("Eden Timesteps After Sundown: "+str(initialcode), fontsize="18") 
        else:
            cmap = plt.get_cmap("terrain_r")                                                    #MATPLOTLIB Terrain colour (reverse) into plot #REFERENCE https://matplotlib.org/stable/users/explain/colors/colormaps.html
            plt.title("Eden Timesteps After Dawn: "+str(initialcode), fontsize="18")
        plt.set_cmap(cmap)

        #print plot
        plt.imshow(terrain)                                                                 #shows background 

        #plot titles and axes (timestep and number of objects at each timestep)
        plt.xlabel(str(len(fossilpos))+" Fossils "+str(len(bflys))+" Butterflies  "+str(finalcatp)+" Caterpillars  "+str(len(ants))+" Ants  "+str(len(lizzys))+" Lizards  "+str(len(worms))+" Worms  "+str(len(flowerpos))+" Flowers  ")
        
        #plots subtitle when raining
        if raindance == True:
                secax = ax.secondary_xaxis('top', functions=(None))                         #REFERENCE: https://matplotlib.org/stable/gallery/subplots_axes_and_figures/secondary_axis.html
                secax.set_xlabel('It\'s Raining!')    

        plt.pause(0.01)                                                                      #0.01 second pause showing plot (3 TIMESTEPS PER SECOND)
        plt.cla()                                                                             #clears axes to show next loop without deleting plot 

if __name__ == "__main__":                      
    main()
