from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import (Classroom, Chapter, QuesModel,
                     Student, ChapterResult, Lesson, Video, Image, PDFs,
                     Audio, PPT, GIF, Exercise, Example, Topic_Reference, ILSmodel, Pretest_Model,
                     Pretest_Result)
from django import forms
class PretestForm(ModelForm):
    class Meta:
        model = Pretest_Model
        fields = ('question', 'op1', 'op2', 'op3', 'op4', 'ans')
    def __init__(self, *args, **kwargs):
        super(PretestForm, self).__init__(*args, **kwargs)
        self.fields['question'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter question...'})
        self.fields['op1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter option 1...'})
        self.fields['op2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter option 2...'})
        self.fields['op3'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter option 3...'})
        self.fields['op4'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter option 4...'})
        self.fields['ans'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter answer...'})

class TestChapter(ModelForm):
    class Meta:
        model = Chapter
        fields = ('title', 'description')
    def __init__(self, *args, **kwargs):
        super(TestChapter, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class':'form-control','placeholder':'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control','placeholder':'Enter description...'})

class TestLesson(ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'description')
    def __init__(self, *args, **kwargs):
        super(TestLesson, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class':'form-control','placeholder':'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control','placeholder':'Enter description...'})

class TestClassroom(ModelForm):
    class Meta:
        model = Classroom
        fields = ('status',)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control','placeholder':'Enter username...'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control','placeholder':'Enter password...'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control','placeholder':'Confirm password...'})
#Classroom form
class ClassroomForm(ModelForm):
    class Meta:
        model = Classroom
        fields = ('section', 'subject')
    def __init__(self, *args, **kwargs):
        super(ClassroomForm, self).__init__(*args, **kwargs)
        self.fields['section'].widget.attrs.update({'class':'form-control','placeholder':'Enter section...'})
        self.fields['subject'].widget.attrs.update({'class': 'form-control','placeholder':'Enter subject...'})

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'img', 'age', 'section')
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class':'form-control','placeholder':'Enter firstname...'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control','placeholder':'Enter lastname...'})
        self.fields['img'].widget.attrs.update({'class': 'form-control','placeholder':'Upload Image...'})
        self.fields['age'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter age...'})
        self.fields['section'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter section...'})

class addQuestionform(ModelForm):
    class Meta:
        model=QuesModel
        fields= ('question', 'op1', 'op2', 'op3', 'op4', 'ans', 'chapter')
    def __init__(self, *args, **kwargs):
        super(addQuestionform, self).__init__(*args, **kwargs)
        self.fields['question'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter question...'})
        self.fields['op1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter option 1...'})
        self.fields['op2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter option 2...'})
        self.fields['op3'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter option 3...'})
        self.fields['op4'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter option 4...'})
        self.fields['ans'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter answer...'})
        self.fields['chapter'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter chapter...'})

class addQuestionform2(ModelForm):
    class Meta:
        model=QuesModel
        fields= ('question', 'op1', 'op2', 'op3', 'op4', 'ans')
    def __init__(self, *args, **kwargs):
        super(addQuestionform2, self).__init__(*args, **kwargs)
        self.fields['question'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter question...'})
        self.fields['op1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter option 1...'})
        self.fields['op2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter option 2...'})
        self.fields['op3'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter option 3...'})
        self.fields['op4'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter option 4...'})
        self.fields['ans'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter answer...'})

class ILS_Form(ModelForm):
    class Meta:
        model = ILSmodel
        fields = ('question', 'option1', 'option2')
    def __init__(self, *args, **kwargs):
        super(ILS_Form, self).__init__(*args, **kwargs)
        self.fields['question'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter question...'})
        self.fields['option1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter option 1...'})
        self.fields['option2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter option 2...'})


#Chapter form
class ChapterForm(ModelForm):
    class Meta:
        model = Chapter
        fields = ('title', 'description')
    def __init__(self, *args, **kwargs):
        super(ChapterForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description...'})
class ChapterForm2(ModelForm):
    class Meta:
        model = Chapter
        fields = ('title', 'description', 'classroom')
    def __init__(self, *args, **kwargs):
        super(ChapterForm2, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class':'form-control','placeholder':'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control','placeholder':'Enter description...'})
        self.fields['classroom'].widget.attrs.update({'class': 'form-control','placeholder':'...'})

class chapt_result(ModelForm):
    class Meta:
        model = ChapterResult
        fields = ('status',)

class pretest_result(ModelForm):
    class Meta:
        model = Pretest_Result
        fields = ('status',)

class LessonForm2(ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(LessonForm2, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description...'})
        self.fields['chapter'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter chapter...'})
class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'description', 'vid',)
    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description...'})
        self.fields['vid'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Upload video...'})
class VideoForm2(ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'description', 'vid', 'lesson')
    def __init__(self, *args, **kwargs):
        super(VideoForm2, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description...'})
        self.fields['vid'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Upload video...'})
        self.fields['lesson'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter lesson...'})

class PDFForm(ModelForm):
    class Meta:
        model = PDFs
        fields = ('title', 'description', 'pdf')
    def __init__(self, *args, **kwargs):
        super(PDFForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description...'})
        self.fields['pdf'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Upload pdf...'})

class PDFForm2(ModelForm):
    class Meta:
        model = PDFs
        fields = ('title', 'description', 'pdf', 'lesson')
    def __init__(self, *args, **kwargs):
        super(PDFForm2, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description...'})
        self.fields['pdf'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Upload video...'})
        self.fields['lesson'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter lesson...'})
class ImageForm2(ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'description', 'img', 'lesson')

    def __init__(self, *args, **kwargs):
        super(ImageForm2, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description...'})
        self.fields['img'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Upload image...'})
        self.fields['lesson'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter lesson...'})
class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'description', 'img')
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description...'})
        self.fields['img'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Upload image...'})

class AudioForm(ModelForm):
    class Meta:
        model = Audio
        fields = ('title', 'description', 'aud')
    def __init__(self, *args, **kwargs):
        super(AudioForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description...'})
        self.fields['aud'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Upload audio...'})


class AudioForm2(ModelForm):
    class Meta:
        model = Audio
        fields = ('title', 'description', 'aud', 'lesson')
    def __init__(self, *args, **kwargs):
        super(AudioForm2, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description...'})
        self.fields['aud'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Upload audio...'})
        self.fields['lesson'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter lesson...'})

class PPTForm(ModelForm):
    class Meta:
        model = PPT
        fields = ('title', 'description', 'ppt',)
    def __init__(self, *args, **kwargs):
        super(PPTForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description...'})
        self.fields['ppt'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Upload ppt...'})

class PPTForm2(ModelForm):
    class Meta:
        model = PPT
        fields = ('title', 'description', 'ppt', 'lesson')
    def __init__(self, *args, **kwargs):
        super(PPTForm2, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description...'})
        self.fields['ppt'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Upload ppt...'})
        self.fields['lesson'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter lesson...'})

class GIFForm(ModelForm):
    class Meta:
        model = GIF
        fields = ('title', 'description', 'gif')
    def __init__(self, *args, **kwargs):
        super(GIFForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description...'})
        self.fields['gif'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Upload gif...'})

class GIFForm2(ModelForm):
    class Meta:
        model = GIF
        fields = ('title', 'description', 'gif', 'lesson')
    def __init__(self, *args, **kwargs):
        super(GIFForm2, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description...'})
        self.fields['gif'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Upload gif...'})
        self.fields['lesson'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter lesson...'})

class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = ('title', 'description', 'exercise')
    def __init__(self, *args, **kwargs):
        super(ExerciseForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description...'})
        self.fields['exercise'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Upload exercise...'})

class ExerciseForm2(ModelForm):
    class Meta:
        model = Exercise
        fields = ('title', 'description', 'exercise', 'lesson')
    def __init__(self, *args, **kwargs):
        super(ExerciseForm2, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description...'})
        self.fields['exercise'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Upload exercise...'})
        self.fields['lesson'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter lesson...'})

class ExampleForm(ModelForm):
    class Meta:
        model = Example
        fields = ('title', 'description', 'example')
    def __init__(self, *args, **kwargs):
        super(ExampleForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description...'})
        self.fields['example'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Upload example...'})

class ExampleForm2(ModelForm):
    class Meta:
        model = Example
        fields = ('title', 'description', 'example', 'lesson')
    def __init__(self, *args, **kwargs):
        super(ExampleForm2, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description...'})
        self.fields['example'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Upload example...'})
        self.fields['lesson'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter lesson...'})

class ToreForm(ModelForm):
    class Meta:
        model = Topic_Reference
        fields = ('title', 'description', 'tore')
    def __init__(self, *args, **kwargs):
        super(ToreForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description...'})
        self.fields['tore'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Link...'})

class ToreForm2(ModelForm):
    class Meta:
        model = Topic_Reference
        fields = ('title', 'description', 'tore', 'lesson')
    def __init__(self, *args, **kwargs):
        super(ToreForm2, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter title...'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description...'})
        self.fields['tore'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Link...'})
        self.fields['lesson'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter lesson...'})