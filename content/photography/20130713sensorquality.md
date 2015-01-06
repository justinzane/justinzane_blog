Title: Sensor Quality
Category: photography
Tags: photography, digital camera, sensor, quality
Summary: Thoughts on MegaPixels, Quantum Efficiency, etc.

# Sensor Quality

## More MegaPixels is Bad
One of the perpetual myths, aided by general ignorance and massive marketing effort, of digital 
photography is that **more pixels are always better**. Since pixel count in digital sensors is 
commonly cited in megapixels (i.e. million pixels, 1e6 pixels) this is the *megapixel myth*. If 
you feel experimental, go into any big box store and ask the "technology" staffperson what the 
megapixel listing on the camera display means.

>The electro-optical qualities of image sensor pixels have a great dependence on their ability 
to efficiently convert light (photons) to an exploitable electrical signal. The overall tendency 
of the imaging industry has been to reduce the size of the pixel aperture in order to increase 
resolution. The consumer imaging segment is a spectacular example of this accelerated race to 
shrink pixels to a point where their width approaches the wavelength of visible light. 
[ECNMag](http://www.ecnmag.com/articles/2011/12/image-sensor-quantum-efficiency-versus-wavelength-optimization)

What just about everyone fails to think about is what a pixel on a digital image sensor does. 
Its job is to turn incoming photons into electrons. That's all. The rest of the camera's 
electronics detect the amount of electrons generated in the sensor pixels and process this into 
a digital image format for storage.

Since the sole purpose of a pixel is to use the energy of incoming photons to generate free 
electron-hole pairs that can be electrically sensed, amplified, etc. there are two critical 
features of the pixel that determine its quality. 

1. **Size** - The size, in units of area, of a sensors determines how many photons will hit it 
for a given level of luminant flux. Doubling the area of the sensor doubles the number of 
incoming photons that hit it for a given fixed exposure.

2. **Quantum Efficiency** - Roughly speaking, the percentage of incoming photons that actually 
produce free electrons that are measurable at the sensor's interface. Ideally, every photon 
would create one free electron and no free electrons would be create without an incoming photon. 
In reality, efficiency in converting incoming light is less than 100% and there are free electrons 
created in the dark, *dark noise*.

Number two, quantum efficiency, is a highly technical topic that is the focus of chemical and 
physics research now and ongoing. Size is super simple. And, it is critical to busting the 
megapixel myth. 

>Similar to the lens aperture, the sensor’s individual pixels apertures or pixel surface area 
has a direct influence on its sensitivity. Simply put, the smaller the pixel, the less photons 
it collects during its integrating period, and therefore low-light performance can impose the 
lower limit on pixel size.
[ECNMag](http://www.ecnmag.com/articles/2011/12/image-sensor-quantum-efficiency-versus-wavelength-optimization)

### Pixel Size/Resolution for APS-C Sensors

Mpix | [rggb Bayer pix] | um^2    | Example
----:| ----------------:| -------:|:--------------
   2 |  1997 x 1331     |  144.36 | Nikon D1
   6 |  3024 x 2016     |   62.95 | **Nikon D70**
  10 |  3911 x 2607     |   37.65 | Nikon D80
  12 |  4295 x 2863     |   31.22 | Nikon D90
  16 |  4929 x 3286     |   23.70 | Nikon D7000
  24 |  6037 x 4024     |   15.80 | Nikon D7100
  48 |  8485 x 5656     |    8.00 | 
  80 | 10988 x 7325     |    4.77 | 

### Pixel Size/Resolution for 2.7" x 4" Large Format Sensors

Mpix | [rggb Bayer pix] | um^2 
---- | ---------------- | -----
   2 |  1997 x 1331     | 10025.06
   6 |  3024 x 2016     | 4371.58
  10 |  3911 x 2607     | 2614.38
  12 |  4295 x 2863     | 2168.02
  16 |  4929 x 3286     | 1646.09
  24 |  6037 x 4024     | 1097.39
  48 |  8485 x 5656     |  555.56
  80 | 10988 x 7325     |  331.26

As you can see, even with the relatively large APS-C sensors, pixel areas become miniscule quite
quickly which means that low light photography is only possible with extreme levels of noise 
reduction. On the other hand the $10,000+ large format scanning sensors have exceptionally large 
pixels allowing them to generate images with tremendous dynamic range in low light without 
the hack of noise reduction post-processing.

### Data from [http://www.sensorgen.info/](http://www.sensorgen.info/)

Pixel Size um | Photons/Pixel Relative | Stops DR | Camera
-----: | ---------: | -----: | :---
  9.68 |    1404.88 |  10.74 | D2H
  5.56 |     712.26 |  10.67 | D2X
  7.93 |    1510.82 |  11.67 | D40
  5.59 |     905.37 |  11.87 | D300
  5.59 |    1092.68 |  13.72 | D5000
  5.94 |    1234.29 |  13.69 | D3X
  8.45 |    2713.39 |  13.42 | D700
  3.98 |     682.31 |  13.61 | D3200
  4.87 |    1137.78 |  14.26 | D7000
  3.99 |     828.55 |  14.70 | D7100
  3.99 |     844.48 |  14.26 | D5200
  7.30 |    2826.67 |  15.92 | D4
  4.31 |     982.94 |  14.73 | D600
  2.86 |     441.74 |  12.17 | 1_V2
  4.88 |    1332.89 |  14.08 | D800
  8.45 |    4070.08 |  14.87 | D3s
  
### Examples of Illuminance [Wikipedia](https://en.wikipedia.org/wiki/Lux)

Illuminance (lux) | Example:
----------------: | :--------
0.00001    | Moonless, overcast night sky (starlight)
0.002      | Moonless clear night sky with airglow
1.0        | Maximum of full moon on a clear night
**3.4**    | **Dark limit of civil twilight under a clear sky**
50         | Family living room lights
80         | Office building hallway/toilet lighting
100        | Very dark overcast day
410        | Office lighting
400        | Sunrise or sunset on a clear day.
1000       | Overcast day; typical TV studio lighting
17500      | Full daylight (not direct sun)
**130000** | **Maximum direct sunlight**

Note that there is a 15.2 stop difference in photon flux per unit area in light conditions that 
I would want to take pictures in. That is a pretty challenging range, especially considering 
that an image sensor should be able to get at least 8 clean bits per channel throughout that range.
