from django.contrib import admin
from .models import QuesModel, style1, style2, ChapterResult, ILSmodel, Student, Classroom, Chapter, Lesson,\
    Video, Image, Audio, PDFs, PPT, GIF, Exercise, Example, Topic_Reference, ChapterResult2, Pretest_Model, \
    Pretest_Result, Pretest_Result2
# Register your models here.
admin.site.register(QuesModel)
admin.site.register(ILSmodel)
admin.site.register(style1)
admin.site.register(style2)
admin.site.register(ChapterResult)
admin.site.register(ChapterResult2)
admin.site.register(Pretest_Result)
admin.site.register(Pretest_Result2)
admin.site.register(Pretest_Model)
admin.site.register(Student)
admin.site.register(Classroom)
admin.site.register(Chapter)
admin.site.register(Lesson)
admin.site.register(Video)
admin.site.register(Image)
admin.site.register(Audio)
admin.site.register(PDFs)
admin.site.register(PPT)
admin.site.register(GIF)
admin.site.register(Exercise)
admin.site.register(Example)
admin.site.register(Topic_Reference)