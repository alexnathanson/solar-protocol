# 3rd Party Tools

## Image Dithering
Images have been dithered using:  
https://legacy.imagemagick.org/Usage/quantize/#od_posterize

Ordered Dither using Uniform Color Levels
* `convert my-image.png   -ordered-dither checks,6     my-image-dithered.gif`
* output file type must be a gif to use it as a server profile picture