Title: Quick Conversion for Panasonic Lumix Camera AVCHD Video
Category: foss
Tags: foss, ffmpeg, Panasonic, AVCHD, video, Lumix
Summary: Quick Conversion for Panasonic Lumix Camera AVCHD Video

# Quick Conversion for Panasonic Lumix Camera AVCHD Video

For those with a Panasonic Lumix camera that takes [AVCHD](https://en.wikipedia.org/wiki/AVCHD) 
video, it is pretty easy to convert to playable files. 

The first trick is to locate the video files on the SDCard. They live under 
`PRIVATE/AVCHD/BDMV/STREAM/` and are named `*.MTS` which is short for MPEG4 Transfer Stream.
Copy these somewhere, then use the following command to convert them to `.mp4` files playable 
just about anywhere.

    :::sh
    for i in *.MTS; do avconv -i $i -c:v copy -c:a copy $(echo $i | sed 's/MTS/mp4/'); done
    
This, obviously presumes that you are in the directory with the `.MTS` files; but it is easy 
enough to adapt.
