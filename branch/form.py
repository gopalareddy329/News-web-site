from django.forms import ModelForm
from .models import User,Report,Comment


class ReportCreationForm(ModelForm):
    class Meta:
        model=Report
        fields='__all__'
        exclude=['host','participents']
        
        
class Creationform(ModelForm):
    class Meta:
        model=User
        fields=['username','email']
        
class Editcomment(ModelForm):
    class Meta:
        model=Comment
        fields=['body']
        
class ProfileEdit(ModelForm):
    class Meta:
        model=User
        fields=['username','email','bio']