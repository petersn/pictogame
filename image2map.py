#!/usr/bin/python

import PIL
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance

def posterize(im):
	"""posterize(image) -> new image

	Processes the image to allow the extraction of world geometry.
	"""
	# Compute a wide Gaussian blur, then subtract this blur from the original image.
	# This is a little bit of an edge-detection filter, and acts like a local AGC to control for local lighting.
	# Finally, negate the image, so zero (blackness) is no edge. Thus, compute (blur - im), not (im - blur).
	blur = im.filter(ImageFilter.GaussianBlur(radius=50))
	edges = PIL.ImageChops.subtract(blur, im)
	# Make the result grayscale after the above filtration.
	edges = edges.convert("L")
	# We then blur a little more to eliminate specks.
	# TODO: Do some better non-linear filtration here.
	edges = edges.filter(ImageFilter.GaussianBlur(radius=2))
	# We compute a threshold to posterize around.
	hist = edges.histogram()
	maximum_pixel_value = max(xrange(len(hist)), key=lambda i: i * (hist[i] != 0))
	total = sum(hist)
	cumulative = [sum(hist[:i+1]) / float(total) for i in xrange(len(hist))]
	get_cumulative = lambda x: max([0] + [i for i in xrange(len(cumulative)) if cumulative[i] < x])
	# The threshold we use is half the 99th percentile.
	threshold = get_cumulative(0.99) * 0.5
	print "Threshold: %s/%s" % (threshold, maximum_pixel_value)
	poster = edges.point(lambda x: 255 * (x > threshold))
	return poster

#def extract_objects

im = Image.open("examples/image1_small.jpg")
im = posterize(im)
im.save("output.png")

