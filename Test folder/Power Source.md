# Power Source

A strong and stable power supply is needed to power WALDO. In order to choose an appropriate power supply, the power consumption of the individual components of WALDO first needs to be known. 

| Component                 	| Typical Current Drawn / A 	| Power       Consumption / W 	|
|---------------------------	|:-------------------------:	|:---------------------:	|
| Jetson Nano Developer Kit 	|         1.0 - 2.0         	|       5.0 - 10.0      	|
| Raspberry Pi              	|            0.7            	|          3.5          	|
| Speakers                  	|            0.6            	|          3.0          	|



As such, the power source has to be able to supply about 20W of power to ensure stable and smooth operation. The biggest source of power consumption comes from the Jetson Nano. The most efficient way to power the Jetson Nano would be through the DC barrel jack connector (please refer to the hardware connections diagram). However, in order to do so, a jumper pin needs to be placed on J48 on the Jetson board. This enables the Jetson to be powered through the barrel jack.

  

One way to power the Jetson would be to use a 4A, 5V plug-in power adapter from the mains. However, this means that WALDO would no longer be portable hence making this option not ideal.

  

As such, a large power bank was used instead. As a rule of thumb, the power bank chosen should be one capable of charging laptops and should have a DC output port. In this project, the Krisdonia Laptop Power Bank 25000mAh Portable Charger was used. This power bank has a DC output port and 2 USB ports, which fits in nicely for the number of components that require power. The Jetson Nano is connected through the DC output port, while the Raspberry Pi and speakers are connected through the 2 USB ports. The Raspberry Pi uses a USB to micro USB connection for power, as seen from the hardware connections diagram.

  

One of the reasons why a power bank as an “off the shelf” solution was used for this prototype was because of the time limitation, but also more importantly because it is safer and more reliable. The downside is that this power bank is rather costly at a retail price of £98. In the future, perhaps rechargeable lithium ion batteries coupled with some applications of power electronics could be used instead as a more cost-effective alternative.


