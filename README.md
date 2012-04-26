Image library for easy manipulation of images
===

Distort, constrain, crop, pad and rotate images. All the commands are
chainable. Auto-rotation for images for the browsers that doesn't
handle rotated images. Caches the images.

Depends on Python Imaging Library

### Quick example
        import ezImage
        img = ezImage.open('path-to-my-image.jpg')

        path_to_cached_version = img.distort(1000,2000).constrain(100,100).crop((0,0,4,4)).pad((90,80,70,60), color=(0,128,255,255)).rotate(angle=90).cache()

        print path_to_cached_version


### Distort
Distort takes width and height and sets the image to those
dimensions.

    import ezImage
    img = ezImage.open('path-to-my-image.jpg')

    path_to_cached_version = img.distort(100,100).cache()
    print path_to_cached_version


### Constrain
Constrain takes width and height and constrains the image to those
dimensions. The proportions are preserved. The image can never become
bigger than it already is with this command.

       import ezImage
       img = ezImage.open('path-to-my-image.jpg')

       path_to_cached_version = img.constrain(100,100).cache()
       print path_to_cached_version


### Crop
Crops the image based on a rectangle. The order is left, top, right,
bottom.

       import ezImage
       img = ezImage.open('path-to-my-image.jpg')

       path_to_cached_version = img.crop((50, 50, 100,100)).cache()
       print path_to_cached_version


### Pad
Pads the image with a tuple of (left, top, right, bottom) and a tuple
of color for (red, green, blue, alpha). Default for color is white and
opaque.

       import ezImage
       img = ezImage.open('path-to-my-image.png')

       path_to_cached_version = img.pad((50, 50, 100,100), (0,128,255,128)).cache()
       print path_to_cached_version


### Rotate
Rotates the image according to the angle. Accepts angle, direction,
resample and expand. Resample is what filter should be used. If expand
is set to true, PIL will expand the image to fit the rotated image
instead of cutting it.

       import ezImage
       img = ezImage.open('path-to-my-image.jpg)

       path_to_cached_version = img.rotate(180).cache()
       print path_to_cached_version
