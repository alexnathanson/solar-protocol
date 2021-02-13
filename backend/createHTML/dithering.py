from PIL import Image
import hitherdither

img = Image.open('../../frontend/images/tega-server.jpg')
palette = hitherdither.palette.Palette.create_by_median_cut(img)
img_dithered = hitherdither.ordered.bayer.bayer_dithering(
    img, palette, [256/4, 256/4, 256/4], order=8)