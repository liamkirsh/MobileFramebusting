from PIL import Image
import os

output = open("isBlank.txt", "w")
d = "./screenshots/"

for filename in os.listdir(d):
    if filename.endswith(".png"):
        im = Image.open(d+filename)
	hist = im.histogram()
	#Image.close(im)
	count = 0
	for val in hist:
		if val < 30:
			count += 1
	if count >= 650:
		output.write(filename + " is blank\n")
	else:
		output.write(filename + " is not blank\n")
