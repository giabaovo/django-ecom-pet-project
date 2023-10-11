from django import forms

from shop.models import ReviewRating

class ReviewRatingForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ["title", "content", "rating"]