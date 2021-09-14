from django.db import models
from django.forms import ModelForm
from django.core.validators import RegexValidator


# Create your models here.

class CRN(models.Model):
    CRN = models.IntegerField(primary_key=True,null=False)
    class_name = models.CharField(max_length=20,null=True)
    term = models.CharField(max_length=10, null=True)

    def __str__(self):
        return str(self.CRN)


class Users(models.Model):
    email = models.EmailField(max_length=120)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list

    # all of the CRNs to this user.
    crn = models.ManyToManyField(CRN)

    def __str__(self):
        return "[ " + self.email + "  " + str(self.phone_regex) + " ] \n\n"


class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.email + "|" + self.subject







class UserForm(ModelForm):
    class Meta:
        model = Users
        fields = ['email', 'phone_number']
