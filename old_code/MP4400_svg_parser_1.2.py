#!/usr/bin/env python

# todo
#- python 3 port
#- pen change support
#-paper size

from xml.dom.minidom import parse
from math import sqrt, sin, pi
import re, sys, getopt



def document_parse(file_name, outputPath):
    '''
    global document parser.
    opens a file defined by the commandline given args

    '''
    global hpgl
    global vHeight
    global vWidth
    global xFakt
    global yFakt
    global extension
    global res
    global rasterize

    #res=1.
    openpath=''


    try:
        datasource = open('%s%s'%(openpath,file_name))
        out_file_name=file_name.split("/")
        out_file_name=out_file_name[-1]
        outputFile=outputPath+out_file_name[:-3]+extension
        #print outputPath+out_file_name
    except IOError:
        print ("ain't no file with that name!")
        sys.exit()

    hpgl=open(outputFile,'w')
    dom = parse(datasource)
    svg=dom.documentElement
    children= svg.childNodes
    vWidth=svg.getAttribute('width')
    vHeight=svg.getAttribute('height')
    vWidth=float(vWidth[:-2])
    vHeight=float(vHeight[:-2])
    plotterXSteps=17280
    plotterYSteps=11880
    paperXSteps= 16160
    paperYSteps=11400

    srcAspectRatio=vWidth/vHeight
    plotterAspectRatio=plotterXSteps/plotterYSteps

    if (srcAspectRatio>=plotterAspectRatio):
        xFakt=plotterXSteps/vWidth
        yFakt=plotterXSteps/vWidth
    elif (srcAspectRatio<plotterAspectRatio):
        xFakt=plotterYSteps/vHeight
        yFakt=plotterYSteps/vHeight

    hpgl.write('IN;IW0,0,%s,%s;\nVS40;\nSP1;\n'%(paperXSteps,paperYSteps))#DIN A3
    print ("creating intermediate.") #" Resolution = %2.1f"%res)
    print ("loading...")
    element_parse(children)
    hpgl.write('PA%s,%s;\n'%(paperXSteps,paperYSteps))
    hpgl.write('SP0;\n')

    hpgl.close()
    datasource.close()
    return ("...done")

def element_parse(children):
    '''
    crawls through the svg xml defined by commandline args and prepared in domcument_parse()
    so far implemented: beziers ('path') line, rect, circle, ellipse. does understand groups.
    '''

    for i in children:

        if i.nodeName == "path":
           # print "%s, d= %s" % (i.nodeName, i.getAttribute('d'))
            d=i.getAttribute('d')
            pathPrint(d)
            hpgl.write('PU;\n')
        elif i.nodeName == "line":
            #print "line: x1: %s y1: %s x2: %s y2: %s" % (i.getAttribute('x1'),i.getAttribute('y1'),i.getAttribute('x2'),i.getAttribute('y2'))
            line_xy={'x1':0,'y1':0,'x2':0,'y2':0}
            for q in line_xy:
                line_xy[q]=float(i.getAttribute(q))
            lineto_rasterizer(line_xy['x1'],line_xy['y1'],line_xy['x2'],line_xy['y2'])

        elif i.nodeName == "rect":
            # print "rect: x: %s y: %s width: %s height: %s" % (i.getAttribute('x'),i.getAttribute('y'),i.getAttribute('width'),i.getAttribute('height'))

            if i.getAttribute('x'): x1=float(i.getAttribute('x'))
            else:  x1=0.0
            if i.getAttribute('y'): y1=float(i.getAttribute('y'))
            else: y1=0.0

            width=float(i.getAttribute('width'))
            height=float(i.getAttribute('height'))

            lineto_rasterizer(x1,y1,x1+width,y1)
            lineto_rasterizer(x1+width,y1,x1+width,y1+height)
            lineto_rasterizer(x1+width,y1+height,x1,y1+height)
            lineto_rasterizer(x1,y1+height,x1,y1)


        elif i.nodeName == "polygon":
            points = i.getAttribute('points')
            polygonPrint(points)

        elif i.nodeName == "circle":
            # print "rect: x: %s y: %s width: %s height: %s" % (i.getAttribute('x'),i.getAttribute('y'),i.getAttribute('width'),i.getAttribute('height'))
            cx=float(i.getAttribute('cx'))
            cy=float(i.getAttribute('cy'))
            rx=float(i.getAttribute('r'))
            circle_rasterizer(cx,cy,rx,rx)
        elif i.nodeName == "ellipse":
            # print "rect: x: %s y: %s width: %s height: %s" % (i.getAttribute('x'),i.getAttribute('y'),i.getAttribute('width'),i.getAttribute('height'))
            cx=float(i.getAttribute('cx'))
            cy=float(i.getAttribute('cy'))
            rx=float(i.getAttribute('rx'))
            ry=float(i.getAttribute('ry'))
            circle_rasterizer(cx,cy,rx,ry)

        elif i.nodeName == "g":
          element_parse(i.childNodes)

def lineto_rasterizer(x1,y1,x2,y2):

    '''
    takes 4 floats or ints, returns nothing. Prints to the opened .hpgl file.
    resolves given ccordinate pairsof lines into a rasterized set of coordinates on the straight connection of those given endpoints.
    the start and endpoint are taken as float 2d coordinates.
    '''
    global res
    global rasterize
    #res=1. # 08_2017: war 0.2# hier resolution einstellen
    hpgl.write('PA%s,%s;\nPD;\n'% (int(round(x1*xFakt)),int(round((vHeight-y1)*yFakt))))
    if (rasterize):
        x_diff=x2-x1
        y_diff=y2-y1
        distance=abs(sqrt(x_diff**2+y_diff**2))
        x_diff_count=0.0
        y_diff_count=0.0
        # print "sad",distance
        while abs(sqrt((x2-(x_diff_count+x1))**2+(y2-(y1+y_diff_count))**2))>res:
            #print abs(sqrt((x2-(x_diff_count+x1))**2+(y2-(y1+y_diff_count))**2))
            hpgl.write('PA%s,%s;\n'% (int(round((x1+x_diff_count)*xFakt)),int(round((vHeight-y1-y_diff_count)*yFakt))))
            if distance == 0.0:
                x_diff_count+=x_diff
                y_diff_count+=y_diff
            else:
                x_diff_count+=float(x_diff)/distance*res
                y_diff_count+=float(y_diff)/distance*res
    else:
        hpgl.write('PA%s,%s;\n'% (int(round(x2*xFakt)),int(round((vHeight-y2)*yFakt))))
    hpgl.write('PU;\n')



def circle_rasterizer(cx,cy,r1,r2):
    '''
    takes 4 ints or floats, returns nothing. Prints to the opened .hpgl file.
    resolves given ccordinate pair of a circle center and a two radixesinto a rasterized set of coordinates of a circle or ellipsoid.
    the coordinates and radixes are taken as float 2d coordinates.
    '''
    global res
    global rasterize
    #res=1. #war 0.05
    if (rasterize or r1!=r2):
        hpgl.write('PA%s,%s;\nPD;\n'% (int(round(sin(0)*r1*xFakt+cx*xFakt)),int(round(sin(0+pi/2)*r2*yFakt+(vHeight-cy)*yFakt))))
        distance=abs(sqrt(r1**2+r2**2))
        diff_count=0.0
        #hpgl.write('!!res: %s'%res)
        while diff_count<=2*pi:
            diff_count+=2*pi/distance*res
            hpgl.write('PA%s,%s;\n'% (int(round(sin(0+diff_count)*r1*xFakt+cx*xFakt)),int(round(sin(0+diff_count+pi/2)*r2*yFakt+(vHeight-cy)*yFakt))))
    else:
        hpgl.write('PA%s,%s;\nCI%s;\n'% (int(round(cx*xFakt)),int(round((vHeight-cy)*yFakt)),int(round(r1*xFakt))))
    hpgl.write('PU;\n')

def hnnz_bezier(x1,y1,x2,y2,x3,y3,x4,y4):
    global res
    bXold=x1
    bYold=y1
    distance=Vdist(x2,y2,x1,y1)+Vdist(x1,y1,x4,y4)+Vdist(x4,y4,x3,y3)
    # print (distance )
    res=0.7 #0.7 ## unbedingt <0,  diesen wert an das Zielmedium anpassen!!!! 0,1 gut mit 0,003 sleep
    if (distance<=0):distance =0.01
    diff_count=1./distance*res ## 0.01; je hoeher desto grober
    global last_coord_x
    global last_coord_y
    t=0
    hpgl.write('PA%s,%s;\n'% (int(round(x1*xFakt)),int(round((vHeight-y1)*yFakt))))
    while t<1:
        bX = x1*(1-t)**3+3*t*(1-t)**2*x2+3*t**2*(1-t)*x3+t**3*x4
        bY = y1*(1-t)**3+3*t*(1-t)**2*y2+3*t**2*(1-t)*y3+t**3*y4
        if abs(bX-bXold)>=res or abs(bY-bYold)>=res:
            hpgl.write('PA%s,%s;\n'% (int(round(bX*xFakt)),int(round((vHeight-bY)*yFakt))))
            bXold =bX
            bYold =bY
            t+=diff_count
        else:
            bX = x4
            bY = y4
            hpgl.write('PA%s,%s;\n'% (int(round(bX*xFakt)),int(round((vHeight-bY)*yFakt))))
            last_coord_x=round(bX*xFakt)
            last_coord_y=round((vHeight-bY)*yFakt)

def getNextXY(index,d):

    d_length =len(d)
    lastIndex=index
    count=0
    countShift=0
    howManyPairs=0.0
    last_key='a'
    chk=''
    keyNow='a'
    crsr=[]
    tempList=[]

    for i in range(index, len(d)):
        chk = d[i]
        if chk in "McCsSlLvVhHz," or (chk=='-'and(i-lastIndex)>1) or i==d_length-1:
            if lastIndex!=i:   #letzer key index muss ungeich sein
                if last_key=='-':
                    if (i==d_length-1):
                        tempList.append(round(float(d[lastIndex:i+1]),3))
                    else:
                        tempList.append(round(float(d[lastIndex:i]),3))
                    lastIndex=i
                    last_key=chk
                else:
                    if i==d_length-1 and chk!='z':
                        tempList.append(round(float(d[lastIndex+1:i+1]),3))
                    else:
                        tempList.append(round(float(d[lastIndex+1:i]),3))
                    lastIndex=i
                    last_key=chk

            if count==0:
                keyNow=chk
                if chk=='M' or chk=='l' or chk=='L':
                    howManyPairs=1
                elif chk=='s'or chk=='S':
                    howManyPairs=2
                elif chk=='c'or chk=='C':
                    howManyPairs=3
                elif chk in "hHvV":
                    howManyPairs=0.5
            if count==int(howManyPairs*2):
                return tempList
            count+=1
    return tempList

def Vdist(x1,y1,x2,y2):
    x_diff=x2-x1
    y_diff=y2-y1
    return abs(sqrt(x_diff**2+y_diff**2))

def polygonPrint(points):

    midPoints = points.replace(",", " ")
    points=midPoints.split(" ")
    while("" in points):
        points.remove("")
    p_length=len(points)

    for i in range(0,p_length-2,2): # run through list in bi steps and stop two before end
        lineto_rasterizer(float(points[i]), float(points[i+1]), float(points[i+2]), float(points[i+3]))

    lineto_rasterizer(float(points[-2]), float(points[-1]),float(points[0]), float(points[1]))

def pathPrint(d):

  d_length=len(d)
  lastIndex=0
  tempLength=0
  count=0
  countShift=0
  last_key='a'
  crsr=[]
  init=[]
  XY=[]
  tmpXY=[0,0]

  global last_coord_x
  global last_coord_y

  for i in range(d_length): # von hier bis
    chk = d[i]

    if chk=='M':
      crsr=getNextXY(i, d)
      init=getNextXY(i, d)

      if round(crsr[0]*xFakt)!=last_coord_x or round((vHeight-crsr[1])*yFakt)!=last_coord_y:
        hpgl.write('PU;\n')
        hpgl.write("PA%s,%s;\n" % (int(round(crsr[0]*xFakt)),int(round((vHeight-crsr[1])*yFakt))    ))
        hpgl.write('PD;\n')

      last_coord_x=round(crsr[0]*xFakt)
      last_coord_y=round((vHeight-crsr[1])*yFakt)

    if chk=='z'or chk=='Z':
      hpgl.write("PA%s,%s;\n"%(int(round(init[0]*xFakt)),int(round((vHeight-init[1])*yFakt))))
      hpgl.write("PU;\n");

    if chk=='c'or chk=='C':  # cubic bezier
      XY=getNextXY(i, d)
      if chk=='c':
        for k in range(0,len(XY),2):
          XY[k]+=crsr[0]
          XY[k+1]+=crsr[1]
      hnnz_bezier(crsr[0], crsr[1], XY[0], XY[1], XY[2], XY[3], XY[4], XY[5])
      crsr[0]=XY[-2]
      crsr[1]=XY[-1]

    if chk=='s' or chk=='S':# erster cpunkt gespiegelt uber cursor
      tmpXY[0]=(2*XY[-2]-XY[-4]) #einfgen des neuen punkts
      tmpXY[1]=(2*XY[-1]-XY[-3])
      XY=getNextXY(i,d)

      if chk=='s':
        for k in range (0,len(XY),2):
          XY[k]+=crsr[0]
          XY[k+1]+=crsr[1]

      XY=tmpXY+XY #neue punkte plus die beiden kontrollpunkte
     # if (showControls&&txt_cntrl) show_cntrl(crsr, XY, 1);
      hnnz_bezier(crsr[0], crsr[1], XY[0], XY[1], XY[2], XY[3], XY[4], XY[5])
      crsr[0]=XY[-2]
      crsr[1]=XY[-1]

    if chk=='h'or chk=='H':
      XY=getNextXY(i,d)
      if chk=='h':
        XY[0]=XY[0]+crsr[0]

      XY.append(crsr[1])
      lineto_rasterizer(crsr[0], crsr[1], XY[0], XY[1])

      last_coord_x=round(XY[0]*xFakt)
      last_coord_y=round((vHeight-XY[1])*yFakt)
      crsr=XY


    if chk=='v' or chk=='V':
      XY=getNextXY(i, d)
      if chk=='v':
        XY[0]=XY[0]+crsr[1]
      XY.append(XY[0])
      XY[0]=crsr[0]
      lineto_rasterizer(crsr[0], crsr[1], XY[0], XY[1])
      last_coord_x=round(XY[0]*xFakt)
      last_coord_y=round((vHeight-XY[1])*yFakt)
      crsr=XY


    if chk=='l' or chk=='L':
      XY=getNextXY(i, d)
      if chk=='l':
        for k in range (0,len(XY),2):
          XY[k]=XY[k]+crsr[0]
          XY[k+1]=XY[k+1]+crsr[1]

      lineto_rasterizer(crsr[0], crsr[1], XY[0], XY[1])
      last_coord_x=round(XY[0]*xFakt)
      last_coord_y=round((vHeight-XY[1])*yFakt)
      crsr=XY


def checkLines(file_name, outputPath):
    openpath=''
    out_file_name=file_name.split("/")
    out_file_name=out_file_name[-1]
    fo = open(outputPath+out_file_name[:-3]+extension, "r")
    gu=fo.readlines()
    gu_len=(len(gu)//10)*10
    print"about %s points"%gu_len
    fo.close()


def main(argv):
    global extension
    global res
    global rasterize
    global last_coord_x
    global last_coord_y

    lazer_on=False;
    std_file='TESTBILD.svg'

    extension="hpgl"
    outputPath=''
    last_coord_x =0.0
    last_coord_y =0.0
    res=1.
    rasterize=False


    #xFakt=78.0 #war 68.0
    #yFakt=78.0 #war 75.0

    try:
        opts, args = getopt.getopt(argv,"i:o:r:h")
    except getopt.GetoptError:
        print ('-i <inputfile> -o <output DIR> -r <resolution> (1=default)')
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print ('usage: -i <inputfile> -o <output DIR> -r <resolution> (1=default)\n')
            print ('setting a resolution wit -r switchs on rasterizing on all standart HPGL commands')
            print ('which causes a massive increase of points and slower plotting\n')
            sys.exit()
        elif opt in ("-i"):
			file_name=str(arg)
			k=file_name.rfind("/")
			outputPath=file_name[:k+1]
 			print (outputPath)
        elif opt in ("-o"):
            outputPath=str(arg)
        elif opt in ("-r"):
            res=float(arg)
            rasterize=True;


	print (outputPath)
    print document_parse(file_name, outputPath)
    checkLines(file_name, outputPath)
            #to_i2c(file_name)

    # else:
    #     file_name=std_file
    #     print "nothing chosen: opening %s" % file_name
    #     print "creating intermediate"
    #     print document_parse()
    #     to_i2c(file_name)



if __name__ == "__main__":
   main(sys.argv[1:])
