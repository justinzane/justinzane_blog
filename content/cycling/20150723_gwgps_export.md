Title: A Quicker Way to Export Ride Data from RideWithGPS
Category: cycling
Tags: cycling, foss, shell
Summary: A Quicker Way to Export Ride Data from RideWithGPS

# A Quicker Way to Export Ride Data from RideWithGPS

[RideWithGPS](http://ridewithgps.com/) is one of the better Android cycling apps. Unfortunately, for reasons that are unclear, it does not work well with CyanogenMod 11 on my particular phone. So, I wanted to export the 88 rides from RWGPS to my laptop and import them into [SportsTracker](http://www.sports-tracker.com/). RWGPS is very nice in that it lets one export in three different formats, TCX with sensor data, TCX without sensor data and GPX. Unfortunately, it does not seem to have a bulk export button.

So, the trick I used is to go the the rides page in FireFox and, using the DOM Inspector tool, select and copy the table containing the list of rides. I then pasted this into a text file. *Note that this is one single line, some some editors or shells may choke. KDE's Kate works well.*

Assuming that one has named the text file `list`, the following strips out everythign but the URLs of the individual rides:

    sed -r 's/(href=\"[\/a-zA-Z0-9_-]+\")/\n\1\n/g' list | \
    grep -oh -E '^href.+' | grep -v edit > list_cleaned

The actual URL for the ride data in TCX format with data is `http://ridewithgps.com/trips/<TRIPNUMBER>.tcx?sub_format=history`. To get our list to be just the trip numbers:

    sed -r 's/href="\/trips\/([0-9]+)"/\1/' list_cleaned
    
Next we use `wget` to fetch the actual data:

    for i in $(cat list02); do 
        wget -O "$i.tcx" -t 2 -nc -w 2 \
        --load-cookies cookies.txt --keep-session-cookies \
        --save-cookies cookies.txt \
        "http://ridewithgps.com/trips/$i.tcx?sub_format=history"; 
    done;

One important part of this is the options dealing with cookies. Since one needs to be logged in to RWGPS to export, it is necessary to save the cookies from that domain using FireBug or similar into a text file. The '-w 2' is just a polite 2 second delay between fetches. 

That's it. Files fetched.

## GPX Conversion

IF you need to use the more common GPX format instead of TCX, it is quite easy to convert all your TCX files in one go with gpsbabel:

    for i in *.tcx; do \
        gpsbabel -i gtrnctr -f $i -o gpx -F $(echo $i | sed 's/tcx/gpx/'); \
    done;
    
I like keeping the TCX files because I've got cadence sensor data for some of my rides. It's up to you...
