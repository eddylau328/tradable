from django import forms
from .models import Item


class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'name',
            'description',
            'price',
            'condition',
        ]

    def is_valid(self, request):
        # run the parent validation first
        valid = super(ItemCreateForm, self).is_valid()
        # we're done now if not valid
        if not valid:
            return valid

        self.instance.seller = request.user
        # all good
        return True
