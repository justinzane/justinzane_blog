Title: Gimp Tricks 2013-08-21
Category: foss
Tags: gimp, image, astronomy, astrophotography, speed, Nikon, D200
Summary: Hide Layers for Astrophoto Speed

# Gimp Astrophoto Tricks 2013-08-21

## Background

I've been messing with the *Interval Shooting* mode of the 
[Nikon D200](http://www.kenrockwell.com/nikon/d200.htm‎). Basically, this is a 
built in function of the camera to take a specified number of images at a specified interval. 
This is most commonly referred to as "time lapse" shooting; and, it does indeed allow one to 
make awesome time lapse animations/videos out of extremely high quality images. 

My current interest, however, is a little different. I've been doing a bit of reading about 
different techniques that astronomers use to select or enhance earth-based photos of space 
objects. In astronomy, the main motivation for this is that any picture of an astronomical 
subject taken from the surface of the earth is distorted by the earth's atmosphere. In particular, 
differences in temperature cause moving convection currents. Since the refractive index of air 
is in part due to its density, and its density is strongly influenced by temperature, the end 
result is like taking a picture through a bowl of jiggly jello.

Additionally, though it may seem obvious, most objects in space are **very** dim. That means 
that the response of an image sensor to photons from these dim objects is barely above the 
noise floor; that is, actual image electrons are intermingled with random electrons caused by 
quantum fluctuations. 

One class of solutions to these difficulties is to use a *stack* of images of the subject. In 
this context, a stack is simply a series of images of the same scene taken over a -- normally --
short span of time. And, that is something that the interval mode of the D200 excels at.

## Hide Layers for Astrophoto Speed

The [GIMP](http://www.gimp.org/) has a set of [astronomy plugins](http://registry.gimp.org/node/2352), 
which makes visual -- not 
scientific -- experimentation very easy. One problem with these is due to the typical image 
editor "live update" process. By live update, I refer to the way that any editing actions are 
almost immediately displayed in the editor window. While this is ideal for 99.9% of users, it 
causes major havok with large stacks of layers.

In attempting to *normalize* a stack of seventy (70) 16-bit, 10 Mpix, greyscale layers, a single 
iteration was taking over 15 minutes. A stroke of inspiration hit me then: 
**hide all the layers**.

Indeed, the simple act of hiding all the layers freed the GIMP's UI from constantly recalculating 
a view based on a 1500MB buffer. That allows the whole process of normalization to finish in a 
couple of minutes.

To be clear, the tip is this:

**When working with dozens of layers, using the GIMP's Astronomy plugins, hide all the layers.**
You'll see a speedup of perhaps two or three orders of magnitude!

Extra tip:

**To hide all layers quickly, <shift>+<click> on the "eye" on any layer, then <click> it.** The 
Shifted click hide all layers *except* that one. Clicking again hides that layer, showing 
nothing but the empty frame.

## Example Workflow

- Setup D200 to take images at 5 sec intervals, 35 frames, set the timer and tripod and wait. I 
was photographing *Mount Shasta* from an overpass on *Interstate 5* on a very smoky evening.

- Repeat above.

- Move images to accessible disk.

- Convert the Nikon NEF raw files to **16-bit** tiffs with 
[dcraw](http://www.cybercom.net/~dcoffin/dcraw/), 
[ufraw](http://ufraw.sourceforge.net/) or a similar CLI based tool. These settings are for a 
terrestrial subject. Google for astro-specific settings.

- Split the color channels into separate tiffs with 
[imagemagick](http://www.imagemagick.org/script/index.php) or similar.

- *Example of above two steps*:

        :::sh
        # Convert NEF with ufraw;
        # then split channels with imagemagick.
        for i in $(seq $SRC_START $SRC_END); do \
            ufraw-batch \
            --wb=camera \
            --gamma=0.45 \
            --linearity=0.0 \
            --exposure=0 \
            --restore=clip \
            --clip=digital \
            --saturation=1.0 \
            --wavelet-denoising-threshold=0.0 \
            --base-curve=camera \
            --curve=linear \
            --black-point=0.0 \
            --interpolation=four-color \
            --rotate=no \
            --out-type=tiff \
            --out-depth=16 \
            --zip \
            --noexif \
            --out-path=$TMP_PATH \
            --overwrite \
            $SRC_PATH$BASENAME$i".NEF";
            convert $TMP_PATH$BASENAME$i.tif -channel R -separate $DST_PATH"red_"$i".tif";
            convert $TMP_PATH$BASENAME$i.tif -channel G -separate $DST_PATH"grn_"$i".tif";
            convert $TMP_PATH$BASENAME$i.tif -channel B -separate $DST_PATH"blu_"$i".tif";
            rm $TMP_PATH$BASENAME$i.tif;
            sleep 0.1;
        done;

- Import all the red images into GIMP using `File / Import as layers`.

- Hide all layers.

        :::python
        # To be run from the Python-Fu console within the GIMP.
        img = gimp.image_list()[0]
        for l in img.layers:
    ...     gimp.pdb.gimp_image_set_active_layer(img, l)
    ...     gimp.pdb.gimp_item_set_visible(l, 0)
    ...     gimp.pdb.plug_in_fft_dir(img, l)
    ...     gimp.pdb.plug_in_unsharp_mask(img, l, 1.0, 1.0, 0)
    ...     gimp.pdb.plug_in_fft_inv(img, l)

- Run `Filters / Astronomy / Normalize all layers` on the whole stack.

- Run `Filters / Astronomy / Merge all layers` on the whole stack. In this case I tried both 
a plain average and an average of layers within 1.0 sigma of the median.

- Save merged image(s) as tiffs.

- Repeat above 5 steps for the green and blue layers.

- Merge the latest results into a color image with *imagemagick*.

