Title: HPOJ7500a Color Profile
Category: foss
Tags: color, icc, argyll, hp, officejet, 7500a, e910
Summary: Creating ICC Color Profiles for an HP officeJet 7500a

# Creating ICC Color Profiles for an HP officeJet 7500a

One of the annoying things about many "consumer grade" printers and scanners is that they are 
only vaguely consistent with the very limited [sRGB](https://en.wikipedia.org/wiki/Srgb) profile.
Fortunately, the FOSS world has a very nice tool for generating accurate profiles, [ArgyllCMS](http://www.argyllcms.com/doc/Scenarios.html#PS2).

## Scanner Input Profile

Because color management is inherently based on associating the digital with the physical, it is
impossible to create color profiles without well defined physical objects and environments to 
analyze. For scanners, this is easy. Simply buy a "target" like the ones listed on Argyll's site
and use the data files provided with it.

In this case, I used a Kodak Q60 target like [this](http://www.bhphotovideo.com/c/product/163309-REG/Kodak_1907914_Q_60R2_Target_5x7_Endura.html). The batch calibration file for these targets 
are downloadable as instructed on the Argyll site.

Using `xsane` I scanned the Q60 target at 300 DPI to a tiff file. (*Note that using 2400 DPI 
causes problems with Argyll*.) I then create a `ti3` file using Argyll's `scanin`, which I used 
to generate the profile with `colprof`.

    :::sh
    scanin HPOJ7500a_e910_KodakQ60_2013-12-24_sm.tiff \
        /usr/share/argyllcms/ref/it8.cht R2201305.Q60
    colprof -v -A "HP" -M "OJ7500a" -D "HP OfficeJet 7500a e910" \
        -u -ax -Zp -qh  HPOJ7500a_e910_KodakQ60_2013-12-24_sm
    sudo cp HPOJ7500a_e910_KodakQ60_2013-12-24_sm.icc /usr/share/color/icc/
    
That is all there is to it. Really.

Though I do not know how consistent HP's scanners are from device to device, feel free to give 
[my profile](images/HPOJ7500a_e910_KodakQ60_2013-12-24_sm.icc.tar.gz) a try it you have 
an OfficeJet 7500a (e910).
