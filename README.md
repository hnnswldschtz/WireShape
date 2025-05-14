# WireShape

*WireShape CNC* is a cnc-wirebending machine and machine-specifc CAM control software. Our low-cost machine design is
similar to commercially available wire benders (such as the DI Wire), but constructed from widely available
3D-printer components, 3D-printed mechanics, stepper motors, open source control electronics, and a CNC-milled wooden base frame. 
For more details and Background, check this source:
https://dl.acm.org/doi/10.1145/3623263.3623363

## WireShape_CAM_Processor
svg to gcode parser and interpreter for the  
Wireshape process (freiform-heißpress). 
previews shape, outputs gcode file for the CNC Wireshaper. 

dependencies: 
- matplolib 
- svg.path




## Wire Shape Hardware

### Wireshape CNC BOM

#### Electronics
1x Arduino Uno R3
1x Arduino CNC shield eg https://www.ebay.de/itm/253692368532
3x DRV8825 stepper driver
2 x stepper motor nema 17 
1x Feeder:  https://www.amazon.de/Dasing-Extruder-Bausatz-Aluminium-Creality-Rot/dp/B087F75JXY

1 solenoid ncd03212v - https://linhkiendientu.vn/san-pham/chot-nam-cham-dien-day-keo-0.5n-12v-ncd03212v
FET driver for solenoid like: https://www.amazon.de/Treibermodul-Dual-Hochleistungs-Switching-Schalttafel-Ar-duino/dp/B0DG8B58PM
Powersupply 12V

#### Machanics
1x Belt - Polyurethane timing belt T2.5 width 6mm Lw 330 132 teeth - https://www.maedler.de/Article/16061200
1x Pulley - Timing belt pulley T2.5 material aluminium 20 teeth for belt width 10mm https://www.maedler.de/Article/16032000
1x Axis (cut to 37 mm) -  Silver steel DIN 175 115CrV3 ground and polished diameter 6h9 x 500mm long https://www.maedler.de/Article/64700600

3x Bearing for axis:  6x12x4 mmMR-126-2RS https://www.kugellager-express.de/high-precision-miniature-ball-bearing-hc-mr126-2rs-cn-p6-gs1-6x12x4-mm


Chassis - 9mm plywood

10 x V-Groove ball bearing 4x13x6mm (ID,OD,Thk) (for straightener)
http://www.ebay.com/itm/10Pcs-Metal-Sealed-Guide-Wire-Line-Track-Deep-V-Groove-Pulley-Rail-Ball-Bearing-/321898243903?hash=item4af2a1673f:g:jJQAAOSwT5tWJeYd

##### screws

10 x M4 nut
20 x M4 Nut, self locking

Socket head cap screw (hex):
4x  M4x16
13x M4x20
4x  M4x30
4x  M4x35
4 x M3x12 (stepper mount)

Countersunk head screw (straightener):
6x M4x20


Details about Filament straightener 
https://www.thingiverse.com/thing:1552283


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
