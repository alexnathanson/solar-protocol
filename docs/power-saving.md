# Power Saving

## Image Dithering

Images have been dithered using https://legacy.imagemagick.org/Usage/quantize/#od_posterize

This saves on file size, and therefore power usage 

Ordered Dither using Uniform Color Levels (output must be a gif to use it as a server profile picture)

    convert my-image.png \
      -ordered-dither checks,6 \
      my-image-dithered.gif
