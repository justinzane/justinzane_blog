Title: Sensor Net Project
Category: FOSS
Tags: FOSS, FOHW, HVAC, Sensor Net, Domotics
Summary: HVAC Monitor/Control Sensor Network Project

# HVAC Monitor/Control Sensor Network Project

## Goal

The goal of this project is to develop and implement a sensor/controller network to monitor 
environmental parameters and control HVAC and lighting.

## Restrictions

- **Cost**: Overall cost must be kept as low as possible. This is a non-commercial project and 
will have a limited timeframe from cost recovery through efficiency optimization. 

- **Flexibility**: Overall system needs to be able to work with whatever fans, heat sources, 
cooling sources, etc. are available. This includes:

    - Wood stoves/fireplaces with separate fan units
    - Oil/gas room units
    - Oil/gas furnaces
    - Room AC units
    - Air/ground heat pumps
    - Ducted air handlers
    - Ductless AC fans
    - DC PWM Fans
    
- **Freedom**: All components should be free and open source hardware and software wherever 
possible. Generally, this refers primarily to microcontrollers and their software stacks.

## Components

### Network

All components of the system shall be integrated and managed by existing or new FOSS software. 
The main "intelligence" of the system will be based on a daemon or set of daemons written in 
C/C++/Python running on a Linux server.

Each individual sensor or controller should be able to communicate over the same physical and 
protocol layers with the server. *Note that this includes mesh and routed communications.*

Possible options for physical layer are wireless ISM band radio and Cat5e UTP cable. If wired 
communications are chosen, they should ideally provide power as well as signal transmission.

Wireless options include IEEE 802.11 WiFi, IEEE 801.15.4 LR-WPAN with either ZigBee or 6LowPAN 
protocols or custom protocols over 433/915/2400 MHz radio. IP packets, as used with 6LowPAN or 
802.11, make integration extremely easy. Unfortunately, most non-ARM microcontrollers currently 
do not have integrated radios and fully optimized IP stacks. 

For wired communications, more information is necessary on options for multidrop networks. As 
far as I can tell, TIA/RS-485 is ideal, but again is not natively supported by most microcontrollers,
significantly raising the cost per device.

### Sensors

Range of sensors:
- Temp (-20 to 50 deg C)
- Temp (0 to 500 deg C)
- Rel hum.
- Barometric pressure
- Air flow
- Irradiance
- Color Temp

Initially near-room-temperature temp sensors are the most critical. Though analog output sensors 
are dirt cheap, I2C/SPI digital output sensors may be optimal based on choice of sensor boards. 

There are innumerable microcontroller boards to choose from. The overarching challenge is limiting
total "mote" cost considering the sum of costs of:
- microcontroller board
- uC to sensor interface
- sensor
- communication interface
- power supply
- network cabling

Possible Microcontroller Board Choices

TABLEHERE

### Controllers

WRITEME

