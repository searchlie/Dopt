from django import forms

class UserForm(forms.Form):
    levels = forms.CharField(label='各因子の水準数', max_length=100)
    number_of_experiments = forms.IntegerField(label='実施する実験回数', max_value=1000, min_value=1)
    number_of_trials = forms.IntegerField(label='計算回数（探索する計画の数）', max_value=1000000, min_value=1, initial=1000)
    pass