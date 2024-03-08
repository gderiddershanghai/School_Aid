from PIL import Image
import pytesseract

# Example for a local image file
image_path = 'path/to/handwritten_essay.jpg'
image = Image.open(image_path)

text = pytesseract.image_to_string(image, lang='eng')
print(text)
