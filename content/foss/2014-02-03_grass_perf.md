Title: GRASS perf
Category: foss
Tags: foss, GRASS, GIS, perf
Summary: GRASS perf

# GRASS Performance

For those who do not know, GRASS is an amazingly capable free and open source GIS toolkit. I 
recently had the desire to do a viewshed analysis; and, GRASS immediately sprang to mind. I 
installed [Arch](http://www.archlinux.org)'s grass70-svn package and started importing USGS DEMs
for the area in question.

The next step was importing some shapefiles from [OpenStreetMap](http://www.osm.org) to provide 
context for the DEMS. And here I ran into a problem. Importing was **painfully, brutally slow**. 
I mean ~25 primitives per second slow, when according to the GRASS devs it should have been two 
to three orders of magnitude faster.

I assumed that this was because GRASS was writing to a SQLite DB on an NFS mount. So, I rebuilt 
with `--with-mysql` and used a known good database on a local server. ** *Doh!* ** No improvement.

I then rebuilt GRASS and GDAL with `CFLAGS="-Og -g" CXXFLAGS="$CFLAGS"` so that I could run under 
`perf`. In the process of getting some data, I noticed that the database did **not** have tables
or columns for geometry data. Which meant that GRASS was persisting that to the filesystem. Which 
was still on an NFS mount.

Moving the `grassdata` directory to a local disk with btrfs and retesting gave a tremendous 
improvement. The bottleneck is somewhere outside the database driver and in the geometry persistence.

An initial test done with grass70-svn, using MySQL as the DB and a local disk as the grassdata 
directory yielded an ~46x speed improvement to about 1163 primitives per second. The script 
and dotchart follow:

    :::sh
    perf record -e cycles:u -o grass.prof -g -- \
        grass70-svn -text /home/justin/maps/grassdata/osm_data/OSM; 
    perf script -k /tmp/vmlinux -i grass.prof | \
        gprof2dot -f perf  | \
        dot -Tpng -o output.png;
    # IN GRASS SHELL
    g.remove vect=roads;
    time v.in.ogr dsn=./downloads/osm_CA/roads.shp output=roads; 
    exit;

![perf](images/grass70-svn_mysql_local.png)

As I am far from a perf guru, input about how to improve this analysis is most welcome!

## Sideline on NFS vs Local

I did a really simple test of open, write, close cycles on both an NFS mount and a local disk. 

NumChars | Local (s)  | NFS (s)   | NFS/Local
:--------|-----------:|----------:|---------:
00000002 |   000.0386 |  000.2817 |  007.2940
00000008 |   000.0548 |  000.3111 |  005.6811
00000032 |   000.1260 |  000.4040 |  003.2059
00000128 |   000.4014 |  000.7244 |  001.8045
00000512 |   001.5126 |  001.7911 |  001.1841

As you can see, once the size of the writes (appends, actually) gets big enough, NFS and local 
btrfs perform about the same. When doing lots of tiny open-write-close cycles, the overhead of 
NFS becomes a huge penalty.

    :::python
    ##---------------------------------------------------------------------------------------------
    # @file    minifstest
    # @brief
    # @author  Justin Zane Chudgar <justin@justinzane.com>
    # @copyright   Copyright 2014
    # @section License GPLv3+
    # minifstest  is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.
    #
    # minifstest is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.
    #
    # You should have received a copy of the GNU General Public License
    # along with minifstest .  If not, see http://www.gnu.org/licenses/.
    #----------------------------------------------------------------------------------------------

    import random
    import time

    def get_rnd_str(chars=32):
        if chars < 1:
            chars = 1
        if chars > 65536:
            chars = 65536
        retstr = ""
        for i in range(0, chars):
            retstr += str(random.randint(0, 10))
        return retstr


    def test(target, iterations, length):
        for i in range(iterations):
            s = get_rnd_str(length)
            fh = open(target, 'a')
            fh.write(s)
            fh.close()


    if __name__ == '__main__':
        localpath = "/home/justin/deleteme"
        localfile = open(localpath, 'w')
        localfile.write("x")
        localfile.close()
        nfspath = "/home/justin/shared-docs/deleteme"
        nfsfile = open(nfspath, 'w')
        nfsfile.write("x")
        nfsfile.close()

        for len in [2, 8, 32, 128, 512]:
            localstart = time.clock()
            for its in [512]:
                test(localpath, its, len)
            localdur = time.clock() - localstart

            nfsstart = time.clock()
            for its in [512]:
                test(nfspath, its, len)
            nfsdur = time.clock() - nfsstart

            print("%08d:  %08.4f, %08.4f, %08.4f" % (len, localdur, nfsdur, nfsdur / localdur))
            
## Back to GRASS on NFS

Doing a test like the one above, but with grassdata on NFS, I immediate notices from `nfsstat` 
that I'm consistently getting ~27 writes per second -- almost exactly one primitive per write. 

