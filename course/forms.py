from django import forms
from .models import *
from django.contrib.admin import widgets
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User



class userform(forms.ModelForm):
    pass2 = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
    def clean_pass2(self):
        pass2 = self.cleaned_data.get("pass2")

        return pass2
    def save(self, commit=True):
        user = super(userform, self).save(commit=False)
        user.set_password(self.cleaned_data['pass2'])
        if commit:
            user.save()
        return user

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('course_title', 'course_img', 'course_overview', 'course_price', 'course_level')
        widgets = {
            'course_title': forms.TextInput(attrs={'placeholder': 'title', 'class': 'w3-input w3-border w3-round'}),
            'course_img': forms.FileInput(attrs={'placeholder': 'add any image for course', 'class': 'w3-input w3-border w3-round'}),
            'course_overview': forms.TextInput(attrs={'placeholder': 'overview', 'class': 'w3-input w3-border w3-round'}),
            'course_duration': forms.TimeInput(attrs={'placeholder': 'duration', 'class': 'w3-input w3-border w3-round'}),
            'course_level': forms.Select(attrs={'placeholder': 'course level', 'class': 'w3-input w3-border w3-round'}),
        }

class DescriptionForm(forms.ModelForm):
    class Meta:
        model = Description
        fields = ['title', 'description', 'prerequisites', 'certificate', 'no_of_learners']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'title', 'class': 'w3-input w3-border w3-round'}),
            'course_img': forms.FileInput(attrs={'placeholder': 'certificate of completion', 'class': 'w3-input w3-border w3-round'}),
            'prerequisites': forms.Textarea(attrs={'placeholder': 'any prerequisites for the course ?', 'class': 'w3-input w3-border w3-round'}),
            'certificate': forms.FileInput(attrs={'placeholder': 'certificate', 'class': 'w3-input w3-border w3-round'}),
            'no_of_learners': forms.NumberInput(attrs={'placeholder': 'no. of learners in techsnap', 'class': 'w3-input w3-border w3-round'}),
        }

class WhatYouGetForm(forms.ModelForm):
    class Meta:
        model = WhatYouGet
        fields = ('description', 'text')

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ('name', 'thoughts', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'name', 'class': 'w3-input w3-border w3-round'}),
            'image': forms.FileInput(attrs={'placeholder': 'image', 'class': 'w3-input w3-border w3-round'}),
            'thoughts': forms.Textarea(attrs={'placeholder': 'what do you think about this course ??', 'class': 'w3-input w3-border w3-round'}),
        }

class FrequentlyAskedQuestionForm(forms.ModelForm):
    class Meta:
        model = FrequentlyAskedQuestion
        fields = ('question', 'answer')
        widgets = {
            'question': forms.TextInput(attrs={'placeholder': 'enter you question here ', 'class': 'w3-input w3-border w3-round'}),
            'answer': forms.Textarea(attrs={'placeholder': 'answer the question here', 'class': 'w3-input w3-border w3-round'}),
        }

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ('title', 'brief', 'due')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'title', 'class': 'w3-input w3-border w3-round'}),
            'brief': forms.Textarea(attrs={'placeholder': 'tell us brief about the course', 'class': 'w3-input w3-border w3-round'}),
            'due': forms.DateInput(attrs={'type': "date", 'class': "w3-input w3-round w3-border"})
        }

class AnouncementForm(forms.ModelForm):
    class Meta:
        model = Anouncement
        fields = ('body',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('anouncement', 'name', 'thoughts', 'img')

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('five', 'four', 'three', 'two', 'one')
        widgets = {
            'five': forms.NumberInput(attrs={'placeholder': 'no. of five stars', 'class': 'w3-input w3-border w3-round'}),
            'four': forms.NumberInput(attrs={'placeholder': 'no. of four stars', 'class': 'w3-input w3-border w3-round'}),
            'three': forms.NumberInput(attrs={'placeholder': 'no. of three stars', 'class': 'w3-input w3-border w3-round'}),
            'two': forms.NumberInput(attrs={'placeholder': 'no. of two stars', 'class': 'w3-input w3-border w3-round'}),
            'one': forms.NumberInput(attrs={'placeholder': 'no. of one stars', 'class': 'w3-input w3-border w3-round'}),
        }
        labels = {
            'five': 'No. of 5 stars',
            'four': 'No. of 4 stars',
            'three': 'No. of 3 stars',
            'two': 'No. of 2 stars',
            'one': 'No. of 1 stars',
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('name', 'img', 'stars', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'name', 'class': 'w3-input w3-border w3-round'}),
            'img': forms.FileInput(attrs={'placeholder': 'img', 'class': 'w3-input w3-border w3-round'}),
            'stars': forms.NumberInput(attrs={'placeholder': 'stars', 'class': 'w3-input w3-border w3-round'}),
            'body': forms.Textarea(attrs={'placeholder': 'what do you think about this course ??', 'class': 'w3-input w3-border w3-round'}),
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ( 'title', 'resource', 'resource_name', 'resource_link')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'title', 'class': 'w3-input w3-border w3-round'}),
            'duration_Seconds': forms.TimeInput(attrs={'placeholder': 'expected duration to complete the lesson', 'class': 'w3-input w3-border w3-round'}),
            'duration_Minutes': forms.TimeInput(attrs={'placeholder': 'expected duration to complete the lesson', 'class': 'w3-input w3-border w3-round'}),
            'xp': forms.NumberInput(attrs={'placeholder': 'rewarded xp on completion', 'class': 'w3-input w3-border w3-round'}),
            'resource': forms.FileInput(attrs={'placeholder': 'tell us brief about the course', 'class': 'w3-input w3-border w3-round'}),
            'resource_name': forms.TextInput(attrs={'placeholder': 'name for the resource file ', 'class': 'w3-input w3-border w3-round'}),
            'resource_link': forms.URLInput(attrs={'placeholder': 'tell us brief about the course', 'class': 'w3-input w3-border w3-round'}),
        }