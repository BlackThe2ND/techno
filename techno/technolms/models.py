from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class ILSmodel(models.Model):
    question = models.CharField(max_length=400, null=True)
    option1 = models.CharField(max_length=200, null=True)
    option2 = models.CharField(max_length=200, null=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.question

class Classroom(models.Model):
    section = models.CharField(max_length=300, blank=False)
    subject = models.CharField(max_length=200, blank=False)
    status = models.BooleanField(default=False, null=True)
    def __str__(self):
        return self.section
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('home')


class Student(models.Model):
    first_name = models.CharField(max_length=200, null=True, blank=False)
    last_name = models.CharField(max_length=200, null=True, blank=False)
    img = models.ImageField(upload_to='uploads/', null=True, blank=False)
    age = models.IntegerField(null=True)
    section = models.CharField(max_length=200, null=True)
    student = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=False)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.first_name
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('home')

class style1(models.Model):
    username = models.CharField(max_length=200, null=True)
    LO1 = models.CharField(max_length=100, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.username

class style2(models.Model):
    LO2 = models.CharField(max_length=100, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)

class ChapterResult(models.Model):
    Quiz_Score = models.IntegerField(default=0.0, null=True)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)

class ChapterResult2(models.Model):
    Quiz_Score = models.IntegerField(default=0.0, null=True)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)

class Chapter(models.Model):
    title = models.CharField(max_length=300, null=True, blank=False)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('home', args=[str(self.pk)])
        #return reverse('home')

class QuesModel(models.Model):
    question = models.CharField(max_length=400, null=True, unique=True)
    op1 = models.CharField(max_length=200, null=True)
    op2 = models.CharField(max_length=200, null=True)
    op3 = models.CharField(max_length=200, null=True)
    op4 = models.CharField(max_length=200, null=True)
    ans = models.CharField(max_length=200, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.question
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('chapter-quiz', args=[str(self.pk)])

class Pretest_Model(models.Model):
    question = models.CharField(max_length=400, null=True, unique=True)
    op1 = models.CharField(max_length=200, null=True)
    op2 = models.CharField(max_length=200, null=True)
    op3 = models.CharField(max_length=200, null=True)
    op4 = models.CharField(max_length=200, null=True)
    ans = models.CharField(max_length=200, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.question
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('pre-test', args=[str(self.pk)])

class Pretest_Result(models.Model):
    pre_test_result = models.IntegerField(default=0.0, null=True)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)

class Pretest_Result2(models.Model):
    pre_test_result = models.IntegerField(default=0.0, null=True)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)

class Lesson(models.Model):
    title = models.CharField(max_length=300, null=True, blank=False)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('lesson-details', args=[str(self.pk)])

class Video(models.Model):
    title = models.CharField(max_length=300, null=True, blank=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    vid = models.FileField(upload_to='uploads/', blank=False)
    description = models.TextField(blank=True)
    favourites = models.ManyToManyField(User, related_name='favourites1', default=None, blank=True)
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='draft')
    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    status = models.CharField(max_length=100, choices=options, default='draft')
    newmanager = NewManager()
    objects = models.Manager()
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('video-detail', args=[str(self.pk)])

class Image(models.Model):
    title = models.CharField(max_length=300, null=True, blank=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='uploads/', null=True, blank=False)
    description = models.TextField(blank=True)
    favourites = models.ManyToManyField(User, related_name='favourites2', default=None, blank=True)
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='draft')
    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    status = models.CharField(max_length=100, choices=options, default='draft')
    newmanager = NewManager()
    objects = models.Manager()
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('image-detail', args=[str(self.pk)])
class PDFs(models.Model):
    title = models.CharField(max_length=300, null=True, blank=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='uploads/', null=True, blank=False)
    description = models.TextField(blank=True)
    favourites = models.ManyToManyField(User, related_name='favourites3', default=None, blank=True)
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='draft')
    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    status = models.CharField(max_length=100, choices=options, default='draft')
    newmanager = NewManager()
    objects = models.Manager()
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('pdf-detail', args=[str(self.pk)])
class Audio(models.Model):
    title = models.CharField(max_length=300, null=True, blank=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    aud = models.FileField(upload_to='uploads/')
    description = models.TextField(blank=True)
    favourites = models.ManyToManyField(User, related_name='favourites4', default=None, blank=True)
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='draft')
    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    status = models.CharField(max_length=100, choices=options, default='draft')
    newmanager = NewManager()
    objects = models.Manager()
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('audio-detail', args=[str(self.pk)])

class PPT(models.Model):
    title = models.CharField(max_length=300, null=True, blank=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    ppt = models.FileField(upload_to='uploads/')
    description = models.TextField(blank=True)
    favourites = models.ManyToManyField(User, related_name='favourites5', default=None, blank=True)
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='draft')
    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    status = models.CharField(max_length=100, choices=options, default='draft')
    newmanager = NewManager()
    objects = models.Manager()
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('ppt-detail', args=[str(self.pk)])

class GIF(models.Model):
    title = models.CharField(max_length=300, null=True, blank=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    gif = models.FileField(upload_to='uploads/')
    description = models.TextField(blank=True)
    favourites = models.ManyToManyField(User, related_name='favourites6', default=None, blank=True)
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='draft')
    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    status = models.CharField(max_length=100, choices=options, default='draft')
    newmanager = NewManager()
    objects = models.Manager()
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('gif-detail', args=[str(self.pk)])
class Exercise(models.Model):
    title = models.CharField(max_length=300, null=True, blank=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    exercise = models.FileField(upload_to='uploads/')
    description = models.TextField(blank=True)
    favourites = models.ManyToManyField(User, related_name='favourites7', default=None, blank=True)
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='draft')
    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    status = models.CharField(max_length=100, choices=options, default='draft')
    newmanager = NewManager()
    objects = models.Manager()
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('exercise-detail', args=[str(self.pk)])

class Example(models.Model):
    title = models.CharField(max_length=300, null=True, blank=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    example = models.FileField(upload_to='uploads/')
    description = models.TextField(blank=True)
    favourites = models.ManyToManyField(User, related_name='favourites8', default=None, blank=True)
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='draft')
    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    status = models.CharField(max_length=100, choices=options, default='draft')
    newmanager = NewManager()
    objects = models.Manager()
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('example-detail', args=[str(self.pk)])

class Topic_Reference(models.Model):
    title = models.CharField(max_length=300, null=True, blank=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    tore = models.URLField()
    description = models.TextField(blank=True)
    favourites = models.ManyToManyField(User, related_name='favourites9', default=None, blank=True)
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='draft')
    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    status = models.CharField(max_length=100, choices=options, default='draft')
    newmanager = NewManager()
    objects = models.Manager()
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('tore-detail', args=[str(self.pk)])