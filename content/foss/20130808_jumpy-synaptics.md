Title: Jumpy Cursors&comma; Cursing Synaptics&comma; XINPUT
Category: foss
Tags: synaptics, touchpad, cursor, mouse, xinput, jumpy cursor
Summary: Fixing a crappy Synaptics Touchpad with XINPUT

# Jumpy Cursors&comma; Cursing Synaptics&comma; XINPUT

The problem: a Dell Inspiron 14z *UltraBook* with a Synaptics touchpad and a **very** jumpy 
cursor. The problem is a little more difficult to explain 
than "jumpiness" or "hypersensitivity". The problem only exists when stopping navigating -- when
I have positioned the cursor where I need it to be and lift my finger from the pad. 

At the "instant of lifting", limited by the accuracy of my human perceptual abilities, the 
cursor will "jump" -- move by ~2-10 pixels -- in an apparently random direction. This is hugely 
annoying, especially when exact pointer position is required. Examples of the times when this is 
problematic are: clicking a link in a vertical list of links, resizing rows in a spreadsheet, 
selecting text from within a paragraph, etc. Super annoying as you can tell.

None of the adjustments in KDE's `synaptiks` touchpad control panel are of any use. Fortunately,
this is Linux so there is `xinput`, which allows comprehensive control of all applicable 
settings.

To see what devices are available, use `xinput list`:

    :::sh
    [Thu 13/08/08 12:29 PDT][pts/2][x86_64/linux-gnu/3.10.3-1-ARCH][5.0.2]
    <justin@justin-14z:~>
    zsh/2 1073 % xinput list
    ⎡ Virtual core pointer                          id=2    [master pointer  (3)]
    ⎜   ↳ Virtual core XTEST pointer                id=4    [slave  pointer  (2)]
    ⎜   ↳ SynPS/2 Synaptics TouchPad                id=12   [slave  pointer  (2)]
    ⎣ Virtual core keyboard                         id=3    [master keyboard (2)]
        ↳ Virtual core XTEST keyboard               id=5    [slave  keyboard (3)]
        ↳ Power Button                              id=6    [slave  keyboard (3)]
        ↳ Video Bus                                 id=7    [slave  keyboard (3)]
        ↳ Power Button                              id=8    [slave  keyboard (3)]
        ↳ Sleep Button                              id=9    [slave  keyboard (3)]
        ↳ Laptop_Integrated_Webcam_HD               id=10   [slave  keyboard (3)]
        ↳ AT Translated Set 2 keyboard              id=11   [slave  keyboard (3)]
        ↳ Dell WMI hotkeys                          id=13   [slave  keyboard (3)]

In my case, the offending dohicky is ID 12. In entering commands, you can use either the ID 
number or the name string -- `12` or `"SynPS/2 Synaptics TouchPad"`. To check what the xserver 
knows about this particular device, use `xinput list-props ##` with the number or quoted name.

    :::sh
    [Thu 13/08/08 13:06 PDT][pts/2][x86_64/linux-gnu/3.10.3-1-ARCH][5.0.2]
    <justin@justin-14z:~>
    zsh/2 1077 % xinput list-props 12                            
    Device 'SynPS/2 Synaptics TouchPad':
        Device Enabled (133):   1
        Coordinate Transformation Matrix (135): 
            1.000000, 0.000000, 0.000000, 
            0.000000, 1.000000, 0.000000, 
            0.000000, 0.000000, 1.000000
        Device Accel Profile (257):     1
        Device Accel Constant Deceleration (258):       2.000000
        Device Accel Adaptive Deceleration (259):       2.000000
        Device Accel Velocity Scaling (260):    12.500000
        Synaptics Edges (261):  1766, 5382, 1645, 4563
        Synaptics Finger (262): 25, 30, 0
        Synaptics Tap Time (263):       180
        Synaptics Tap Move (264):       237
        Synaptics Tap Durations (265):  180, 180, 100
        Synaptics ClickPad (266):       0
        Synaptics Middle Button Timeout (267):  75
        Synaptics Two-Finger Pressure (268):    282
        Synaptics Two-Finger Width (269):       7
        Synaptics Scrolling Distance (270):     96, 32
        Synaptics Edge Scrolling (271): 1, 1, 0
        Synaptics Two-Finger Scrolling (272):   0, 0
        Synaptics Move Speed (273):     0.300000, 2.000000, 0.117000, 0.000000
        Synaptics Off (274):    0
        Synaptics Locked Drags (275):   0
        Synaptics Locked Drags Timeout (276):   5000
        Synaptics Tap Action (277):     0, 0, 0, 0, 1, 0, 0
        Synaptics Click Action (278):   1, 1, 1
        Synaptics Circular Scrolling (279):     0
        Synaptics Circular Scrolling Distance (280):    0.100007
        Synaptics Circular Scrolling Trigger (281):     0
        Synaptics Palm Detection (282): 0
        Synaptics Palm Dimensions (283):        10, 200
        Synaptics Coasting Speed (284): 0.000000, 50.000000
        Synaptics Pressure Motion (285):        30, 160
        Synaptics Pressure Motion Factor (286): 1.000000, 1.000000
        Synaptics Grab Event Device (287):      1
        Synaptics Gestures (288):       0
        Synaptics Capabilities (289):   1, 0, 1, 1, 1, 1, 1
        Synaptics Pad Resolution (290): 78, 45
        Synaptics Area (291):   0, 0, 0, 0
        Synaptics Noise Cancellation (292):     64, 64
        Device Product ID (251):        2, 7
        Device Node (252):      "/dev/input/event12"

To change settings at runtime, critical for getting thing to work just the way you want, I 
recommend using the device ID number and the property id number, which is listed in parentheses 
after the property name string as arguments to `xinput set-prop`. That is, for my setup, to 
change the `"Device Accel Profile"`, I would use `xinput set-prop 12 257 2`. For properties 
that take multiple parameters, use a space separated list like `xinput set-prop 12 262 20 30 0`.

The properties relating to pointer acceleration (257, 258 , 259, 260) are important and are 
documented at [www.x.org](http://www.x.org/wiki/Development/Documentation/PointerAcceleration/):

> **"AdaptiveDeceleration" / "Device Accel Adaptive Deceleration" [int]** Allows the 
acceleration profile to actually decelerate the pointer by the given factor. Adaptive 
deceleration is a good tool allowing precise pointing, while maintaining pointer speed in 
general. ... Default is 1
>
> **"ConstantDeceleration" / "Device Accel Constant Deceleration" [int]** Constantly decelerates the mouse by given 
factor. ...
>
> **"AccelerationProfile" / "Device Accel Profile" [int]** Select the acceleration profile by number. Default is 0, 
except if the driver says otherwise (none currently does). In this section, threshold and 
acceleration specify the corresponding X controls (xset m acc_num/acc_den thres).
>
> -1. **"none"** no velocity-dependent pointer acceleration or deceleration. If constant 
deceleration is also unused, motion processing is suppressed, saving some cycles. 
>
> 0. classic (the default) similar to old behaviour, but more predictable. Selects between 
'polynomial' and 'simple' based on threshold =/!= 0.
> 1. **"device-dependent"** available if the hardware driver installs it. May be coming for synaptics. 
>
> 2. **"polynomial"** Scales polynomial: velocity serves as the coefficient, acceleration being 
the exponent. Very useable, **the recommended profile**. 
>
> 3. **"smooth linear"** scales mostly linear, but with a smooth (non-linear) start. 
>
> 4. **"simple"** Transitions between accelerated/unaccelerated, but with a smooth transition 
range. This has the fundamental problem of accelerating on two niveaus, on which acceleration 
stays independent of velocity. Traditionally the default however. 
>
> 5. **"power"** accelerates by a power function. velocity is the exponent here. Adheres to 
threshold. Will easily get hard to control, so it is important you have properly tuned your 
velocity estimation. 
>
> 6. **"linear"** just linear to velocity and acceleration. Simple and clean. 
>
> 7. **"limited"** smoothly ascends to acceleration, maxing out at threshold, where it becomes 
flat (is limited). 

At the moment I am using 

    :::sh
    Device Accel Profile (257):     3
    Device Accel Constant Deceleration (258):       1.000000
    Device Accel Adaptive Deceleration (259):       2.000000
    Device Accel Velocity Scaling (260):    1.000000

These seem to work well enough for basic tasks. I'll mess around in the Gimp soon to see how 
well they do when pixel-poking. 

You will note that the xorg documentation refers to the cryptic `xset m acc_num/acc_den thresh`. 
`xinput` allows access to these values through `xinput get-feedbacks <ID/name>` and 
`xinput set-ptr-feedback <ID/name> <threshold> <numerator> <denominator>`.

    :::sh
    [Thu 13/08/08 14:15 PDT][pts/2][x86_64/linux-gnu/3.10.3-1-ARCH][5.0.2]
    <justin@justin-14z:~>
    zsh/2 1119 % xinput set-ptr-feedback 12 3 25 10 ; xinput get-feedbacks 12
    1 feedback class
    PtrFeedbackClass id=0
            accelNum is 20
            accelDenom is 10
            threshold is 2

Other properties that may matter for other hardware but did not make much difference on my box 
are `Coasting Speed` and `Noise Cancellation`, the latter of which is also referred to as 
`Horiz/Vert Hysteresis` in some tools. I did set the noise cancellation values up to 12 from the
default 8 and left them there. That, however, was only after experimenting with a large range of
different values and getting little improvement.

Once you have figured out values that fit your hardware and your preferences, you can make them 
persistent by adding them to your `xorg.conf` file **as appropriate for your distribution and 
setup**. In Arch, the way to do this is to add the relevant lines to 
`/etc/X11/xorg.conf.d/51-custom-synaptics.conf`:

    :::sh
    Section "InputClass"
        Identifier "Prevent jumpy touchpad pointer"
        MatchIsTouchpad "on"
        Option "AccelerationProfile" "3"
        Option "ConstantDeceleration" "1"
        Option "AdaptiveDeceleration" "2"
    EndSection

Because different distros locate their xorg configurations in different places, **please** do 
not just copy and paste this on your system. Check to see how your distro does things first. 
And, if you are using *wayland* or *mir*, good luck. This probably helps you as much as the 
Windows docs.
