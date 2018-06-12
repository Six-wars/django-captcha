from django.shortcuts import render, render_to_response
import random
import string
from PIL import Image, ImageFont

def random_filename(path=None, length=None):
	text = string.uppercase + string.lowercase + string.digits

	if path == None:
		path = 'djangocaptcha/media/images/'

	if length == None:
		guess = random.randrange(8,15)
		length = range(guess)

	return path + ''.join( [random.choice(text) for x in length] ) + '.png'

def generate_captcha():
	first_digit = random.randint(30, 90)
	second_digit = random.randint(3, 9)

	operations = ['+', '-']
	chosen_operation = random.choice(operations)

	eval_string = "{0}{1}{2}".format(first_digit, chosen_operation, second_digit)
	answer = eval(eval_string)

	image = Image.new('RGB', (100, 50), (255, 255, 255))

	font = ImageFont.truetype("djangocaptcha/static/fonts/sans-serif.ttf", 16)
	image.text((5, 5), eval_string, (0,0,0), font=font)
	file_name = random_filename()
	image.save(file_name, "PNG")

	return file_name, answer, eval_string

def login_page(request, template_name="login.html"):
    context = {'title': 'Login Page'}
    return render_to_response(template_name, context)
