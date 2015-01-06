Title: Yet Another Silly Sensord Graph
Category: foss
Tags: sensord, rrd, graph, systemd
Summary: Yet Another Silly Sensord Graph

# Yet Another Silly Sensord Graph

Last night, after being awoken to carry the puppy with the sore paws outside to go potty, I 
ended up messing around with graphing the output of [lm-sensors's](http://lm-sensors.org/) 
`sensord` logging daemon. I had forgotten how flexible and just plain cool Toby Oetiker's 
[rrdtool](http://oss.oetiker.ch/rrdtool/‎) was. In many ways, lm-sensors and rrdtool are the 
epitomy of the *\*NIX* philosophy -- do one thing only and do it well.

lm-sensors just reads data from a vast array of sensor chips and buses; and, rrdtool just 
handles storing/retrieving indefinitely long time series data. No bloat, no GUIs, just simple, 
quick and reliable. That makes them lots of fun late at night, allowing the creation of pretty 
graphs like this:

![sensord](images/20130806_sensord.png)

This is a simple min/avg/max of all the available temp sensors on the computer running sensord. 
The code to get this is:

    #!/bin/sh

    END=$(date +%s)
    START=$[$END - 1209600]
                
    echo $START $END

    rrdtool graph sensord.png \
        --start $START \
        --end $END \
        -w 600 -h 400 \
        -a PNG \
        --title "sensord" \
        --vertical-label "Deg F" \
        --legend-position=south \
        --alt-autoscale \
        --x-grid HOUR:12:DAY:1:DAY:2:0:%b-%d \
        --grid-dash 3:1 \
        --font DEFAULT:0:"Source Code Pro" \
        --color BACK#0f0f0fff \
        --color CANVAS#000000ff \
        --color MGRID#bfbfbfdf \
        --color GRID#7f7f7f7f \
        --color FONT#ffffffff \
        --color AXIS#ffffffff \
        --border 0 \
        DEF:ds01=/var/log/sensord.rrd:temp1:AVERAGE \
        DEF:ds02=/var/log/sensord.rrd:temp2:AVERAGE \
        DEF:ds03=/var/log/sensord.rrd:temp3:AVERAGE \
        DEF:ds04=/var/log/sensord.rrd:temp1_0:AVERAGE \
        'CDEF:cds01=32,1.8,0.25,ds01,ds02,ds03,ds04,+,+,+,*,*,+' \
        'CDEF:cdsmin=32,1.8,ds01,ds02,ds03,ds04,MIN,MIN,MIN,*,+' \
        'CDEF:cdsmax=32,1.8,ds01,ds02,ds03,ds04,MAX,MAX,MAX,*,+' \
        TEXTALIGN:center \
        COMMENT:"From temps 1, 2, 3, 1_0\: " \
        AREA:cdsmax#ff0000ff:"Max" \
        AREA:cds01#007f00ff:"Avg" \
        AREA:cdsmin#00003fff:"Min" \

For anyone copying and pasting this, please make sure to change the paths and `ds` names to 
fit your individual system(s). And do [RTFM](http://en.wikipedia.org/wiki/RTFM), since the 
`man` pages for rrdtool, whether read in a terminal like a good penguin or on the rrdtool web 
pages, are excellent examples of well done documentation.

Also, note that I have use `rrdtune` to increase the length of my `RRA` from sensord's default 
of one week to two (604800 -> 1209600). If you try this with out running rrdtune, you'll end 
up with permanent half-graphs. 

Sleep well.
