

INSTRUCTIONS: 




1. SVG PARSER: 

run 
python Wirebend_svg_parser_1.0.py -i <file.svg> -o <output path eg "./">

outputs a *.nc

2. run with GCODE sender such as candle

garble setup 

use modified config.h from grbl-master.
grbl1.1 rund on arduino cnc shield clone 

3. grbl settings:

$$ < $0=10
$1=25
$2=0
$3=0
$4=0
$5=0
$6=0
$10=1
$11=0.010
$12=0.002
$13=0
$20=0
$21=0
$22=0
$23=0
$24=25.000
$25=500.000
$26=250
$27=1.000
$30=1000
$31=0
$32=1
$100=77.000
$101=25.000
$102=250.000
$110=2000.000
$111=2000.000
$112=500.000
$120=30.000
$121=50.000
$122=10.000
$130=200.000
$131=200.000
$132=200.000


4. Maschine paramters/notes:

Power supply: approx. 13V 1.5A
X_max(bis Anschlag) 29 (reflecting ruffly 290 degree of rotation = 145 on each side)
$100 = 77 steps/mm X
$101 = 25 steps /mm Y
Rücksetz routine 
G91 relativ mode
g90 absolute mode
G21G91G0x-29 (START, mm, relative, set zero)
G90 (Absolute)
G92X0 (0 X coordinates)
G92Y0 (0 Y coordinates)
G90G0x-14.5 (ganz rechts)
G90G0x14.5 (ganz links)
x Verfahrens weg von 0 - 29
x_offset 10 (um neben dem Draht zu landen)
145° = 14,5 mm Verfahrensweg
G91G0y20 (20mm forward)
G91G0Y-10 (10mm backwards)
M4 retract pin (activate solenoid)
M3 release pin (deactivate solenoid)




