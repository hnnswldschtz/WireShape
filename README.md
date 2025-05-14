# WireShape

*WireShape CNC* is a cnc-wirebending machine and CAM control software. Our low-cost machine design is similar to commercially available wire benders (such as the DI Wire), but constructed from widely available 3D-printer components, 3D-printed mechanics, stepper motors, open source control electronics, and a CNC-milled wooden base frame. 

For more details and background, check this source:
https://dl.acm.org/doi/10.1145/3623263.3623363


<img width="652" alt="machine" src="https://github.com/hnnswldschtz/WireShape/blob/master/Hardware/images/WireBending_Machine_2.jpg?raw=true">


## WireShape_CAM_Processor
svg to gcode parser and interpreter for the  
Wireshape process (freiform-heißpress). 
previews shape, outputs gcode file for the CNC Wireshaper. 

dependencies: 
- matplolib 
- svg.path

<img width="652" alt="bedning steps" src="https://github.com/hnnswldschtz/WireShape/blob/master/Hardware/images/bend_steps_fat.jpg?raw=truee">
Principle of the CNC wire bending mechanism


## Wire Shape Hardware

<img width="652" alt="assembly" src="https://github.com/hnnswldschtz/WireShape/blob/master/Hardware/images/wireshape_cnc_explosion.jpg?raw=true">


### Wireshape CNC BOM

#### Electronics
+ 1x Arduino Uno R3
+ 1x Arduino CNC shield eg https://www.ebay.de/itm/253692368532
+ 3x DRV8825 stepper driver
+ 2 x stepper motor nema 17 
+ 1x Feeder:  https://www.amazon.de/Dasing-Extruder-Bausatz-Aluminium-Creality-Rot/dp/B087F75JXY

+ 1 solenoid ncd03212v - https://linhkiendientu.vn/san-pham/chot-nam-cham-dien-day-keo-0.5n-12v-ncd03212v
+ FET driver for solenoid, like: https://www.amazon.de/Treibermodul-Dual-Hochleistungs-Switching-Schalttafel-Ar-duino/dp/B0DG8B58PM
+ Powersupply 12V

#### Mechanics
+ 1x Belt - Polyurethane timing belt T2.5 width 6mm Lw 330 132 teeth - https://www.maedler.de/Article/16061200

+ 1x Pulley - Timing belt pulley T2.5 material aluminium 20 teeth for belt width 10mm https://www.maedler.de/Article/16032000
+ 1x Axis (cut to 37 mm) -  Silver steel DIN 175 115CrV3 ground and polished diameter 6h9 x 500mm long https://www.maedler.de/Article/64700600
+ 3x Bearing for axis:  6x12x4 mmMR-126-2RS https://www.kugellager-express.de/high-precision-miniature-ball-bearing-hc-mr126-2rs-cn-p6-gs1-6x12x4-mm
+ Chassis - 9mm plywood
+ 10 x V-Groove ball bearing 4x13x6mm (ID,OD,Thk) (for straightener)
eg https://ebay.us/m/v5IUZD

#### Screws
Socket head cap screw (hex):
+ 4x  M4x16
+ 13x M4x20
+ 4x  M4x30
+ 4x  M4x35
+ 4 x M3x12 (stepper mount)

Countersunk head screw (straightener):
+ 6x M4x20

Nuts
+ 10 x M4 nut
+ 20 x M4 Nut, self locking

Details about Filament straightener 
https://www.thingiverse.com/thing:1552283

