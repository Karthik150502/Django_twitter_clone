from django import forms
from .models import June, Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


# Profile Extras
class TheProfilePicForm(forms.ModelForm):
	profile_image = forms.ImageField(label = "Profile Picture")
	
	profile_bio = forms.CharField(label = "Profile Biography", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Profile Bio!'}))
	website_link = forms.CharField(label = "Website Link", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Website Link!'}))
	facebook_link = forms.CharField(label = "Facebook Link", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Facebook Link!'}))
	instagram_link = forms.CharField(label = "Instagram Link", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Instagram Link!'}))
	linkedin_link = forms.CharField(label = "LinkedIn Link", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'LinkedIn Link!'}))
	class Meta:
		model = Profile
		fields = ('profile_image','profile_bio','website_link','facebook_link','instagram_link','linkedin_link')




class JuneForm(forms.ModelForm):
    body = forms.CharField(
        required = True,
        widget = forms.widgets.Textarea(
            attrs={'placeholder':"Enter the june!",
                   'class':'form-control'}
        ),
        label="",
        )
    class Meta:
        model = June
        exclude = ("user","likes")

'''

Why do we need to have a bodu field in JuneForm, when we have a body field in Meta class June?

Django allows you to override the default behavior of form fields defined in the associated model. This flexibility enables you to create a user-friendly interface and perform form-specific actions while keeping the data consistency intact in the database through the model.

In Django, the JuneForm is a form that is associated with the June model. When you specify the model attribute in the Meta class of the JuneForm, it automatically generates form fields based on the fields of the associated model. However, you can still define form fields explicitly in the form class for additional customization and control.

The body field in the JuneForm is explicitly defined to allow for customizing its behavior within the form, such as setting the required attribute, specifying a custom widget, or adding additional validation logic that is specific to the form. By defining the field explicitly in the form class, you have more control over its behavior within the form.

In your specific case, the body field is customized to have a TextArea widget with a placeholder and a custom CSS class. The label is also set to an empty string, which means that the label won't be displayed for this field. These customizations are specific to how the form is rendered and presented to the user, and they provide a more tailored user experience for the input of the body field.

Even though the body field is already present in the June model, defining it explicitly in the JuneForm allows you to customize its behavior within the form without affecting the original model's field. This separation of concerns enables you to manage the presentation and validation of the form independently from the underlying data model.
'''




class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
		
class TheUpdateForm(forms.ModelForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')

	def __init__(self, *args, **kwargs):
		super(TheUpdateForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
