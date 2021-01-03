# Additional notes on the code


## Admin console

<p>
default password is 'password'
</p>

## API Key


## Image Dithering
Images have been dithered using:  
https://legacy.imagemagick.org/Usage/quantize/#od_posterize

Ordered Dither using Uniform Color Levels
 convert gradient.png   -ordered-dither checks,6     od_checks_6.gif