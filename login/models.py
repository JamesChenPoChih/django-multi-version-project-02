from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=64)
    pwd = models.CharField(max_length=64)
    _time = models.DateField(auto_now_add=True)

    def _str_(self):
        return self.email
    class Meta:
        ordering = ['-_time']
        verbose_name= 'Client Database'
        verbose_name_plural= 'Clients Database'