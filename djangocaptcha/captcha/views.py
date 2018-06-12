from django.shortcuts import render, render_to_response
import random
import string
from PIL import Image, ImageFont, ImageDraw
from captcha.models import Captcha

def random_filename(path=None, length=None):
	text = string.ascii_letters + string.digits

	if path == None:
		path = 'media/images/'

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

	pre_check = Captcha.objects.filter(eval_string=eval_string)

	if pre_check:
		existing_version = pre_check[0]
		return existing_version.img_path, existing_version.ans, existing_version.eval_string

	answer = eval(eval_string)

	image = Image.new('RGB', (44, 23), (255, 255, 255))
	file_name = random_filename()
	image.save(file_name, "PNG")

	draw = ImageDraw.Draw(image)

	font = ImageFont.truetype("/home/muiruri_samuel/webapp/django-captcha/djangocaptcha/static/fonts/arial.ttf", 16)
	draw.text((5, 5), eval_string, (0,0,0), font=font)
	
	image.save(file_name, "PNG")

	new = Captcha(img_path=file_name, ans=answer, eval_string=eval_string)
	new.save()

	return file_name, answer, eval_string

def login_page(request, template_name="login.html"):
    context = {'title': 'Login Page'}
    file_name, answer, _ = generate_captcha()
    context['captcha_url'] = '/' + file_name
    return render_to_response(template_name, context)
