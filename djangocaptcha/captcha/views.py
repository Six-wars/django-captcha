from django.shortcuts import render, render_to_response
import random
import string
from PIL import Image, ImageFont, ImageDraw
from captcha.models import Captcha
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

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
		return existing_version.img_path, existing_version.ans, existing_version.eval_string, existing_version.id

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

	return file_name, answer, eval_string, new.id

def retrieve_answer(ref_id):
	result = Captcha.objects.filter(id=ref_id)

	if not result:
		return None

	item = result[0]

	return item.ans

def login_page(request, template_name="login.html"):
    context = {'title': 'Login Page'}
    file_name, answer, _, result_id = generate_captcha()
    context['captcha_url'] = '/' + file_name
    context['ref_id'] = result_id
    return render_to_response(template_name, context)

def login_ajax(request):
	response = {'status': None}

	if request.method == 'POST':
		data = json.loads(request.body)
		username, password, ans, ref_id = data['username'], data['password'], data['captcha-result'], data['captcha-ref-id']

		actual_ans = retrieve_answer(ref_id)

		if ans == actual_ans: #Captcha Verification Complete, move on to password verification
			user_exists = User.objects.filter(username=username)

			if user_exists: #check password...
				user = user_exists[0]
				password_ok = user.check_password(password)

				if password_ok: #ok move to logging in user
					pass

					#just incase...
					response['status'] = 'failed'
				else: #password failed...
					response['status'] = 'failed'

					file_name, ans, _, ref_id = generate_captcha()
					response['captcha-url'] = '/' + file_name
					response['ref-id'] = ref_id
					response['error-message'] = 'Wrong Username/Password Combination'

			else: #no matching user found
				response['status'] = 'failed'
				file_name, ans, _, ref_id = generate_captcha()
				response['captcha-url'] = '/' + file_name
				response['ref-id'] = ref_id
				response['error-message'] = 'Wrong Username/Password Combination'
		else: #Captcha Verification Failed, return new Captcha and ID so user can try again
			response['status'] = 'failed'
			file_name, ans, _, ref_id = generate_captcha()
			response['captcha-url'] = '/' + file_name
			response['ref-id'] = ref_id
			response['error-message'] = 'Wrong Answer to Calculation'
		
		

	else:
		response['error'] = 'no post data found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)