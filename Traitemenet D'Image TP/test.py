from PIL import Image 

img = Image.open("image.png")
img.show()

print(img.format)
print(img.size)
print(img.mode)

gray = img.convert("L")
gray.show()
gray.save("gray_image.png")
print(img)