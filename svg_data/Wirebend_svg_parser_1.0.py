#!/usr/bin/env python

'''
svg to gcode parser and interpreter for the freiform-heißpress 
Wirebend machine. 

copyright hnnz 2023

GPL-3.0-or-later

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.

'''


from xml.dom.minidom import parse
from math import sqrt, sin, pi, acos, degrees,floor
import re, sys, getopt
from svg.path import parse_path
import matplotlib.pyplot as plt

MAX_ANGLE = 140
 
def document_parse(file_name, outputPath):
    '''
    global document parser.
    opens a file defined by the commandline given args

    '''
    global gcode
    global vHeight
    global vWidth
    global extension
    global res


   
    openpath='./'

    try:
        datasource = open('%s%s'%(openpath,file_name))
        out_file_name=file_name.split("/")
        out_file_name=out_file_name[-1]
        outputFile=outputPath+out_file_name[:-3]+extension
     
    except IOError:
        print ("ain't no file with that name!")
        sys.exit()

    gcode=open(outputFile,'w')
    dom = parse(datasource)
    svg=dom.documentElement
    children= svg.childNodes
    vWidth=svg.getAttribute('width')
    vHeight=svg.getAttribute('height')
    

    gcode.write('G21G91G0X-29 (START, mm, relative, go to zero)\n')# init
    gcode.write("G0X14.5\n") # go to midddle point
    gcode.write("G92X0\n") # set x to zero at middle
    gcode.write("S1000\n") #set spindle (don't know if needed)
    gcode.write("M4\n") # retract pin
    print ("\nloading...\n")
    element_parse(children)
    gcode.write("M3") # pin up (deactivate solenoid)
    gcode.close()
    
    datasource.close()
    plt.show()
    return ("...done")
    

def element_parse(children):
    '''
    crawls through the svg xml defined by commandline args and prepared in domcument_parse()
    so far implemented: 'path' with lines and beziers,  does understand groups.
    '''

    for i in children:

        if i.nodeName == "path":
           # print "%s, d= %s" % (i.nodeName, i.getAttribute('d'))
            d=i.getAttribute('d')
            #pathPrint(d)
            pathParse(d)   
        elif i.nodeName == "g":
            element_parse(i.childNodes)


def Vdist(x1,y1,x2,y2):
    '''
    helper, calculates length of a vector 
    takes four ccordinates returns length
    '''
    x_diff=x2-x1
    y_diff=y2-y1
    return abs(sqrt(x_diff**2+y_diff**2))

def lineLength(line):
    '''
    returns length of a vector
    takes one Line Object
    '''
    return Vdist(line.start.real, line.start.imag, line.end.real, line.end.imag)
    
def angle_between_lines(z1, z2, w1, w2):
    '''claculates angle between two given vectors
    represented in Line objects with complex number coordinate pairs
    returns angle in degree positve and negative'''
    
    line1 = z2 - z1
    line2 = w2 - w1
    dot_product = line1.real * line2.real + line1.imag * line2.imag
    mag_product = abs(line1) * abs(line2)
    angle = acos(dot_product / mag_product)
    cross_product = line1.real * line2.imag - line1.imag * line2.real
    if cross_product < 0:
        angle = -angle
    return int(degrees(angle))


def pathParse(d):
    '''
    svg path parser and gcode writer function. 
    takes a path as argument ( retrieved from minidom ) and writes out gcode in place of the found elemnents
    v.1.0. :  straigth lines and Cubic beziers are processed.
    
    '''
    #print(parse_path(d))
    XY=[]
    p = parse_path(d)
    pathLength = len(p)
    lastElmnt = p[1] # ignore Moveto
    direction = 1
    print (p[0])
    print(f"path has {pathLength-1} elements\n")
    max_size = 0 
    last_max_size = 0


    for line in p: #
        max_size = get_max_range(line.start, line.end)
        if (max_size > last_max_size): last_max_size = max_size  

    print(f"max_size: {max_size}, last_max_size: {last_max_size}")
    for elmnt in p[1:]: #
        print(f"elmnt coords: {elmnt}")
        elmnt_name = str(elmnt)

        #print(f"lastLine: {lastLine}")
        if ("Line" in elmnt_name):
            if elmnt != lastElmnt:
                angle = angle_between_lines(elmnt.start, elmnt.end,lastElmnt.start, lastElmnt.end)
                
                print(f"elmnt lenght: {round(lineLength(elmnt),2)} mm")
                if (angle > 0): # check whether next bend goes left or right  
                    direction =-1
                    gcode.write(f"G90G0X{-25/10}\n") # move on the opposite side of wire
                else: 
                    direction = 1 
                    gcode.write(f"G90G0X{25/10}\n") # move on the opposite side of wire
                gcode.write("M3\n") # pinout
                print(f"angle between this line and last line is {angle}°")
                if (abs(angle)< MAX_ANGLE):
                    plt.text(lastElmnt.end.real, last_max_size - lastElmnt.end.imag-10, str(angle)+'°', color ='black',fontsize=8)
                else: plt.text(lastElmnt.end.real, last_max_size - lastElmnt.end.imag, str(angle)+'°',color = 'red', fontsize=8)
                
                gcode.write(f"G90G0X{angle/10}\n") # bend wire
                print(f"G90G0X{angle/10} (rotate {angle}°)")
            drawLine(elmnt.start, elmnt.end, '#bcbcbc', last_max_size )
            lastElmnt = elmnt
        elif("CubicBezier" in elmnt_name):
            draw_bezier(elmnt.start,elmnt.control1,elmnt.control2,elmnt.end, last_max_size)
        
        print(f"G91G0Y{round(lineLength(elmnt))} (advance: {round(lineLength(elmnt),2)} mm)\n")
        plt.text(lastElmnt.end.real, (last_max_size - lastElmnt.end.imag)+5, str(round(lineLength(elmnt),2))+'mm',color = 'red', fontsize=8)
        gcode.write(f"G91G0X{1*direction}\n") # move pin some mm away from wire to reduce friction for retraction
        gcode.write("M4\n") # retract
        gcode.write("G4P.5\n") #wait 0.2 secs
        gcode.write(f"G91G0Y{round(lineLength(elmnt))}\n") #advance to next bend according to actual line length
    


def drawLine(start, end, c,size):
    '''
    drawas a given line object 
    takes for arguments: Line Start, Line end, color and max object size for 
    correct scaling and inverting of Y values 
    '''

    x = [start.real, end.real]
    y = [size - start.imag, size - end.imag]
    #y = [start.imag, end.imag]
    plt.xlim(0, size)
    plt.ylim(0, size)
    plt.axis('off')
    plt.gca().set_aspect('equal')
    plt.plot(x,y, color=c)
    #trans_plot(x,y,'green','shift') #not yet done, autmoatic scaling and shifting

def drawLineInt(x1,y1,x2,y2, c,size):

    '''
    draws a given line as a set of integer coordinates 
    takes 6 arguments: Line Start x and y, Line end x and y, color and max object size for 
    correct scaling and inverting of Y values 
    '''
    x = [x1,x2]
    y = [size - y1, size - y2]
    #y = [start.imag, end.imag]
    plt.xlim(0, size)
    plt.ylim(0, size)
    plt.axis('off')
    plt.gca().set_aspect('equal')

    plt.plot(x,y, color=c)


def trans_plot(x,y,c,t):
    if (t == 'shift'):
        print (f't== {t}')
        for i in range(len(x)): 
            x[i]=x[i]+0
        for i in range(len(y)):
            y[i]=y[i]+0
    if (t == 'scale'):
        print (f't== {t}')
        for i in range(len(x)): 
            x[i]=x[i]+20
        for i in range(len(y)):
            y[i]=y[i]+20
    plt.plot(x,y, color=c)

def draw_bezier(start,c1,c2,end, size):

    '''
    draws a given Cubic bezier object 
    takes 6 arguments: Cubic Bezier Start, control1, control2, Cubic bezier end and object size for 
    correct scaling and inverting of Y values 
    '''

    start_x = start.real
    start_y = start.imag
    c1x = c1.real
    c1y = c1.imag
    c2x = c2.real
    c2y = c2.imag
    end_x = end.real
    end_y = end.imag 
    res = 1
    bXold=start_x
    bYold=start_y
    distance=Vdist(start_x,start_y,c1x,c1y)+Vdist(start_x,start_y,end_x,end_y)+Vdist(c2x,c2y,end_x,end_y)
    print (f'distance: {distance} steps: {distance/8}, res {floor(distance/8)}' )
    steps = distance/8
    res=round(steps) #0.7 ## unbedingt <0,  diesen wert an das Zielmedium anpassen!!!! 0,1 gut mit 0,003 sleep
    if (distance<=0):distance =0.01
    diff_count=1./distance*res ## 0.01; je hoeher desto grober
    
    t=0
    print(f"start: {start_x},{start_y}") 

    while t<1:
        bX = start_x*(1-t)**3+3*t*(1-t)**2*c1x+3*t**2*(1-t)*c2x+t**3*end_x
        bY = start_y*(1-t)**3+3*t*(1-t)**2*c1y+3*t**2*(1-t)*c2y+t**3*end_y
        if abs(bX-bXold)>=res or abs(bY-bYold)>=res:
            drawLineInt(bXold, bYold, bX, bY, 'black', size)
            bXold =bX
            bYold =bY
        t+=diff_count
    else:
        bX = end_x
        bY = end_y
        drawLineInt(bXold, bYold, bX, bY, 'black', size)
        


def get_max_range (h,v):
    ''' get max height of path to calculate correct 
    max height for scaling and inverting of y values. 
    (pyplot is drawing with xy0 in lower left corner,
    svgs zero x/zero y is upper left corner. 
    )
    '''
    coords = [h.imag, v.imag]
    last_max_val = 0 
    for size in coords: 
        if (size > last_max_val): last_max_val = size
    return last_max_val
        

def checkLines(file_name, outputPath):
    '''
    checks number of lines in the written file
    '''
    out_file_name=file_name.split("/")
    out_file_name=out_file_name[-1]
    fo = open(outputPath+out_file_name[:-3]+extension, "r")
    gu=fo.readlines()
    gu_len=(len(gu)//10)*10
    print("about %s commmands\n"%gu_len)
    fo.close()


def main(argv):

    global extension
    global res

    std_file='hexa.svg'
    extension="nc"
    outputPath='./'


    try:
        opts, args = getopt.getopt(argv,"i:o:r:h")
    except getopt.GetoptError:
        print ('-i <inputfile> -o <output DIR> -r <resolution> (1=default)')
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            #print ('\n')
            print ('\nusage: -i <inputfile> -o <output DIR> -r <resolution> (1=default)')
            print ('setting a resolution with -r switchs on rasterizing on all standart gcode commands')
            print ('which causes a massive increase of points and slower plotting\n')
            sys.exit()
        elif opt in ("-i"):
            file_name=str(arg)
            k=file_name.rfind("/")
            #print(file_name)
            outputPath=file_name[:k+1]
            print (outputPath)
        elif opt in ("-o"):
            outputPath=str(arg)
        elif opt in ("-r"):
            res=float(arg)
            rasterize=True;
      
    file_name=std_file
    #print(os.getcwd())
    print (document_parse(file_name, outputPath))
    checkLines(file_name, outputPath)
  

if __name__ == "__main__":
    main(sys.argv[1:])
