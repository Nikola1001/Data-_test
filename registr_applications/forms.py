from django.forms import ModelForm
from .models import Statement


class StatementUserForm(ModelForm):

    class Meta:
        model = Statement
        fields = ('email', 'content',  'docs')



