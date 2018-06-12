from django.db import models

class Captcha(models.Model):
	eval_string = models.CharField(max_length=100, unique=True)
	ans = models.CharField(max_length=4)
	img_path = models.CharField(max_length=250)

	def __str__(self):
		return "{0} = {1}".format(self.eval_string, self.ans)
