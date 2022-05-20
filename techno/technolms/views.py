from django.template.context_processors import csrf
from .models import ILSmodel
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404, HttpResponse
from .models import (Classroom, style1, style2, ChapterResult, QuesModel, Student, Chapter,
                     Lesson, Video, Audio, Image, PDFs, PPT, GIF, Exercise, Example, Topic_Reference,
                     ChapterResult2, Pretest_Model, Pretest_Result, Pretest_Result2)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import (CustomUserCreationForm, ClassroomForm, addQuestionform,
                    StudentForm, ChapterForm, ChapterForm2, LessonForm2, VideoForm2, ImageForm2, AudioForm2, PDFForm2,
                    PPTForm2, ExampleForm2, ExerciseForm2, ToreForm2, GIFForm2, addQuestionform2,
                    TestChapter, TestClassroom, TestLesson, VideoForm, ImageForm, PDFForm, PPTForm, GIFForm,
                    AudioForm, ExampleForm, ExerciseForm, ToreForm, chapt_result, ILS_Form, PretestForm,
                    pretest_result)
from django.views.generic import (View, TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView)
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from pybbn.causality.ace import Ace
from pybbn.graph.dag import Bbn
from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable

def new_class(request, classroom_id):
    if request.method == 'POST':
        class_form = TestClassroom(request.POST)
        chapter_form = TestChapter(request.POST)
        if chapter_form.is_valid():
            chapt = chapter_form.save(False)
            chapt.classroom = Classroom.objects.get(pk=classroom_id)
            chapt.save()
            return redirect(reverse('home'))
    else:
        class_form = TestClassroom()
        chapter_form = TestChapter()
    args = {}
    args.update(csrf(request))
    args['class_form']= class_form
    args['chapter_form']= chapter_form
    return render(request, 'list/test_class.html', args)

def PreTest(request, pk):
    chapter = Chapter.objects.get(pk=pk)
    if request.method == 'POST':
        print(request.POST)
        questions = Pretest_Model.objects.filter(chapter=chapter.id)
        score=0
        wrong=0
        correct=0
        total=0
        for q in questions:
            total+=1
            print(request.POST.get(q.question))
            print(q.ans)
            if q.ans ==  request.POST.get(q.question):
                score+=10
                correct+=1
            else:
                wrong+=1
        percent = score/(total*10)*100
        pre_test_score = Pretest_Result(pre_test_result=percent, id=request.user.id, student=Student.objects.get(pk=request.user.id))
        quiz_score2 = Pretest_Result2(pre_test_result=percent, student=Student.objects.get(pk=request.user.id))
        quiz_score2.save()
        print(pre_test_score.pre_test_result)
        print(percent)
        pre_test_score.save()
        context = {
            'chapter':chapter,
            'score':score,
            'time': request.POST.get('timer'),
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total
        }
        return render(request,'Quiz/chapter_quiz_results.html',context)
    else:
        questions=Pretest_Model.objects.all()
        context = {
            'questions':questions, 'chapter':chapter,
        }
        return render(request,'Quiz/Pre_Test.html',context)

def ChapterQuiz(request, pk):
    chapter = Chapter.objects.get(pk=pk)
    if request.method == 'POST':
        print(request.POST)
        questions = QuesModel.objects.filter(chapter=chapter.id)
        score=0
        wrong=0
        correct=0
        total=0
        for q in questions:
            total+=1
            print(request.POST.get(q.question))
            print(q.ans)
            if q.ans ==  request.POST.get(q.question):
                score+=10
                correct+=1
            else:
                wrong+=1
        percent = score/(total*10)*100
        quiz_score = ChapterResult(Quiz_Score=percent, id=request.user.id, student=Student.objects.get(pk=request.user.id))
        quiz_score2 = ChapterResult2(Quiz_Score=percent, student=Student.objects.get(pk=request.user.id))
        quiz_score2.save()
        print(quiz_score.Quiz_Score)
        print(percent)
        quiz_score.save()
        context = {
            'chapter':chapter,
            'score':score,
            'time': request.POST.get('timer'),
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total
        }
        return render(request,'Quiz/chapter_quiz_results.html',context)
    else:
        questions=QuesModel.objects.all()
        context = {
            'questions':questions, 'chapter':chapter,
        }
        return render(request,'Quiz/Chapter Quiz.html',context)
#UNUSED BUT STANDBY
def addQuestion(request, pk):
    if request.user.is_staff:
        chapter = Chapter.objects.get(pk=pk)
        form=addQuestionform()
        if(request.method=='POST'):
            form=addQuestionform(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('home')
        context={'form':form, 'chapter':chapter}
        return render(request,'Quiz/addQuestion.html',context)
    else:
        return redirect('chapter-details')

class AddQuestionView(CreateView):
    form_class = addQuestionform2
    model = QuesModel
    context_object_name = 'add-question'
    template_name = 'Quiz/addQuestion.html'
    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.chapter = self.object.chapter
        fm.save()
        return redirect('home')
def Add_Question(request, chapter_id):
    if request.method == "POST":
        form = addQuestionform2(request.POST)
        if form.is_valid():
            fm = form.save(False)
            fm.chapter = Chapter.objects.get(pk=chapter_id)
            fm.save()
            return redirect(reverse('home'))
    else:
        form = addQuestionform2()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render(request, 'Quiz/addQuestion.html', args)

def Add_Pretest_Question(request, chapter_id):
    if request.method == "POST":
        form = PretestForm(request.POST)
        if form.is_valid():
            fm = form.save(False)
            fm.chapter = Chapter.objects.get(pk=chapter_id)
            fm.save()
            return redirect(reverse('home'))
    else:
        form = PretestForm()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render(request, 'Quiz/add_pre_test.html', args)

class PretestUpdateView(UpdateView):
    model = Pretest_Model
    context_object_name = 'pretest-chapter'
    form_class = PretestForm
    template_name = 'Quiz/edit_pretest.html'
    success_url = reverse_lazy('home')

class PretestDeleteView(DeleteView):
    model = Pretest_Model
    context_object_name = 'delete_question'
    template_name = 'Quiz/delete_pretest.html'
    success_url = reverse_lazy('home')



def Add_ILS_Question(request):
    if request.method == "POST":
        form = ILS_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
    else:
        form = ILS_Form()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render(request, 'Quiz/add_ils_question.html', args)

class QuizUpdateView(UpdateView):
    model = QuesModel
    context_object_name = 'quiz-chapter'
    form_class = addQuestionform2
    template_name = 'Quiz/Edit_Quiz.html'
    success_url = reverse_lazy('home')

class QuizDeleteView(DeleteView):
    model = QuesModel
    context_object_name = 'delete_question'
    template_name = 'Quiz/delete_question.html'
    success_url = reverse_lazy('home')



def index(request):
    if request.method == 'POST':
        questions = ILSmodel.objects.all()
        chapt_results = ChapterResult(status=True)
        chapt_results.save()
        pretest = Pretest_Result(status=True)
        pretest.save()
        a1 = 0
        b1 = 0
        a2 = 2
        b2 = 0
        a3 = 0
        b3 = 2
        a4 = 0
        b4 = 0
        total1 = 0
        total2 = 0
        total3 = 0
        total4 = 0
        for q in questions[0:11]:
            total1 += 1
            if 'a' == request.POST.get(q.question):
                a1 += 1
            elif 'b' == request.POST.get(q.question):
                b1 += 1
        for q in questions[11:22]:
            total2 +=1
            if 'a' ==  request.POST.get(q.question):
                a2 += 1
            elif 'b' == request.POST.get(q.question):
                b2 += 1
        for q in questions[22:33]:
            total3 += 1
            #print(request.POST.get(q.question))
            if 'a' ==  request.POST.get(q.question):
                a3 += 1
            elif 'b' == request.POST.get(q.question):
                b3 += 1
        for q in questions[33:44]:
            total4 += 1
            if 'a' ==  request.POST.get(q.question):
                a4 += 1
            elif 'b' == request.POST.get(q.question):
                b4 += 1

        rank1 = [a1, a2 , a3, a4, b1 , b2, b3, b4] #This will save the score per learning styles
        rank2 = [a1, a2 , a3, a4, b1 , b2, b3, b4]
        R1 = max(rank1)  #It will get the 1 highest values in the list
        rank2.remove(max(rank2)) #tinatanggal ung first highest
        R2 = max(rank2) #Kinukuha ung 2nd highest
        print(rank2)
        if R1 == rank1[0]:
            print('LO1 = Active')
            print(rank1)
            ranking1 = style1(username=request.user.username, LO1='Active', id=request.user.id, student=Student.objects.get(pk=request.user.id))
            ranking1.save()
            if R2 == rank2[0]:
                print('LO2 = Sensing')
                ranking2 = style2(LO2='Sensing', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[1]:
                print('LO2 = Visual')
                ranking2 = style2(LO2='Visual', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[2]:
                print('LO2 = Sequential')
                ranking2 = style2(LO2='Sequential', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[3]:
                print('LO2 = Reflective')
                ranking2 = style2(LO2='Reflective', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[4]:
                print('LO2 = Intuitive')
                ranking2 = style2(LO2='Intuitive', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[5]:
                print('LO2 = Verbal')
                ranking2 = style2(LO2='Verbal', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[6]:
                print('LO2 = Global')
                ranking2 = style2(LO2='Global', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
        elif R1 == rank1[1]:
            print('LO1 = Sensing')
            ranking1 = style1(username=request.user.username, LO1='Sensing', id=request.user.id, student=Student.objects.get(pk=request.user.id))
            ranking1.save()
            if R2 == rank2[0]:
                print('LO2 = Active')
                ranking2 = style2(LO2='Active', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[1]:
                print('LO2 = Visual')
                ranking2 = style2(LO2='Visual', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[2]:
                print('LO2 = Sequential')
                ranking2 = style2(LO2='Sequential', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[3]:
                print('LO2 = Reflective')
                ranking2 = style2(LO2='Reflective', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[4]:
                print('LO2 = Intuitive')
                ranking2 = style2(LO2='Intuitive', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[5]:
                print('LO2 = Verbal')
                ranking2 = style2(LO2='Verbal', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[6]:
                print('LO2 = Global')
                ranking2 = style2(LO2='Global', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
        elif R1 == rank1[2]:
            print('LO1 = Visual')
            ranking1 = style1(username=request.user.username, LO1='Visual', id=request.user.id, student=Student.objects.get(pk=request.user.id))
            ranking1.save()
            if R2 == rank2[0]:
                print('LO2 = Active')
                ranking2 = style2(LO2='Active', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[1]:
                print('LO2 = Sensing')
                ranking2 = style2(LO2='Sensing', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[2]:
                print('LO2 = Sequential')
                ranking2 = style2(LO2='Sequential', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[3]:
                print('LO2 = Reflective')
                ranking2 = style2(LO2='Reflective', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[4]:
                print('LO2 = Intuitive')
                ranking2 = style2(LO2='Intuitive', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[5]:
                print('LO2 = Verbal')
                ranking2 = style2(LO2='Verbal', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[6]:
                print('LO2 = Global')
                ranking2 = style2(LO2='Global', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
        elif R1 == rank1[3]:
            print('LO1 = Sequential')
            ranking1 = style1(username=request.user.username, LO1='Sequential', id=request.user.id, student=Student.objects.get(pk=request.user.id))
            ranking1.save()
            if R2 == rank2[0]:
                print('LO2 = Active')
                ranking2 = style2(LO2='Active', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[1]:
                print('LO2 = Sensing')
                ranking2 = style2(LO2='Sensing', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[2]:
                print('LO2 = Visual')
                ranking2 = style2(LO2='Visual', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[3]:
                print('LO2 = Reflective')
                ranking2 = style2(LO2='Reflective', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[4]:
                print('LO2 = Intuitive')
                ranking2 = style2(LO2='Intuitive', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[5]:
                print('LO2 = Verbal')
                ranking2 = style2(LO2='Verbal', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[6]:
                print('LO2 = Global')
                ranking2 = style2(LO2='Global', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
        elif R1 == rank1[4]:
            print('LO1 = Reflective')
            ranking1 = style1(username=request.user.username, LO1='Reflective', id=request.user.id, student=Student.objects.get(pk=request.user.id))
            ranking1.save()
            if R2 == rank2[0]:
                print('LO2 = Active')
                ranking2 = style2(LO2='Active', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[1]:
                print('LO2 = Sensing')
                ranking2 = style2(LO2='Sensing', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[2]:
                print('LO2 = Visual')
                ranking2 = style2(LO2='Visual', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[3]:
                print('LO2 = Sequential')
                ranking2 = style2(LO2='Sequential', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[4]:
                print('LO2 = Intuitive')
                ranking2 = style2(LO2='Intuitive', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[5]:
                print('LO2 = Verbal')
                ranking2 = style2(LO2='Verbal', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[6]:
                print('LO2 = Global')
                ranking2 = style2(LO2='Global', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
        elif R1 == rank1[5]:
            print('LO1 = Intuitive')
            ranking1 = style1(username=request.user.username, LO1='Intuitive', id=request.user.id, student=Student.objects.get(pk=request.user.id))
            ranking1.save()
            if R2 == rank2[0]:
                print('LO2 = Active')
                ranking2 = style2(LO2='Active', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[1]:
                print('LO2 = Sensing')
                ranking2 = style2(LO2='Sensing', id=request.user.id)
                ranking2.save()
            elif R2 == rank2[2]:
                print('LO2 = Visual')
                ranking2 = style2(LO2='Visual', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[3]:
                print('LO2 = Sequential')
                ranking2 = style2(LO2='Sequential', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[4]:
                print('LO2 = Reflective')
                ranking2 = style2(LO2='Reflective', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[5]:
                print('LO2 = Verbal')
                ranking2 = style2(LO2='Verbal', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[6]:
                print('LO2 = Global')
                ranking2 = style2(LO2='Global', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
        elif R1 == rank1[6]:
            print('LO1 = Verbal')
            ranking1 = style1(username=request.user.username, LO1='Verbal', id=request.user.id, student=Student.objects.get(pk=request.user.id))
            ranking1.save()
            if R2 == rank2[0]:
                print('LO2 = Active')
                ranking2 = style2(LO2='Active', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[1]:
                print('LO2 = Sensing')
                ranking2 = style2(LO2='Sensing', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[2]:
                print('LO2 = Visual')
                ranking2 = style2(LO2='Visual', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[3]:
                print('LO2 = Sequential')
                ranking2 = style2(LO2='Sequential', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[4]:
                print('LO2 = Reflective')
                ranking2 = style2(LO2='Reflective', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[5]:
                print('LO2 = Intuitive')
                ranking2 = style2(LO2='Intuitive', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[6]:
                print('LO2 = Global')
                ranking2 = style2(LO2='Global', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
        elif R1 == rank1[7]:
            print('LO1 = Global')
            ranking1 = style1(username=request.user.username, LO1='Global', id=request.user.id)
            ranking1.save()
            if R2 == rank2[0]:
                print('LO2 = Active')
                ranking2 = style2(LO2='Active', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[1]:
                print('LO2 = Sensing')
                ranking2 = style2(LO2='Sensing', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[2]:
                print('LO2 = Visual')
                ranking2 = style2(LO2='Visual', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[3]:
                print('LO2 = Sequential')
                ranking2 = style2(LO2='Sequential', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[4]:
                print('LO2 = Reflective')
                ranking2 = style2(LO2='Reflective', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[5]:
                print('LO2 = Intuitive')
                ranking2 = style2(LO2='Intuitive', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()
            elif R2 == rank2[6]:
                print('LO2 = Verbal')
                ranking2 = style2(LO2='Verbal', id=request.user.id, student=Student.objects.get(pk=request.user.id))
                ranking2.save()

        context = {
            'a1': a1,
            'a2': a2,
            'a3': a3,
            'a4': a4,
            'time': request.POST.get('timer'),
            'b1': b1,
            'b2': b2,
            'b3': b3,
            'b4': b4,
            'total1': total1,
            'total2': total2,
            'total3': total3,
            'total4': total4,
        }
        return render(request,'Quiz/Results.html', context)
    else:
        questions= ILSmodel.objects.all()
        chapt_results = chapt_result()
        pretest = pretest_result()
        context = {
            'questions':questions, 'chapt_results':chapt_results, 'pretest':pretest,
        }
        return render(request,'Quiz/ILS.html',context)



def ProfileViewdin(request, id):
    student = Student.objects.filter(pk=request.user.id)
    if student.exists():
        profile = Student.objects.get(id=request.user.id)
        chapter_result = ChapterResult.objects.get(id=request.user.id)
        pre_test = Pretest_Result.objects.get(id=request.user.id)
        ls1 = style1.objects.get(id=request.user.id)
        ls2 = style2.objects.get(id=request.user.id)
        return render(request, 'newapp/profile.html', context={'profile':profile,
                                                           'chapter_result':chapter_result,
                                                           'ls1':ls1, 'ls2':ls2, 'pre_test':pre_test})
    else:
        return redirect('profile-create')
class ProfileCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'newapp/create_profile.html'
    context_object_name = 'profile'
    def form_valid(self, form, *args, **kwargs):
        form.save()
        return redirect('index')

class EditProfile(UpdateView):
    form_class = StudentForm
    model = Student
    template_name = 'newapp/profile_edit.html'

def student_lists(request):
    students = Student.objects.all()
    context = {'students': students}
    return render(request, 'list/student_list.html', context)

class CreateResult(CreateView):
    model = ChapterResult
    fields = ('Quiz_Score',)
    template_name = 'dummy/dummy_result.html'
    def form_valid(self, form, *args, **kwargs):
        form.save()
        return redirect('index')


@login_required
def favourite_add1(request, id):
    post = get_object_or_404(Video, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return redirect('favourites_list')
@login_required
def favourite_add2(request, id):
    post = get_object_or_404(Image, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return redirect('home')
@login_required
def favourite_add3(request, id):
    post = get_object_or_404(PDFs, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return redirect('home')
@login_required
def favourite_add4(request, id):
    post = get_object_or_404(Audio, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return redirect('home')
@login_required
def favourite_add5(request, id):
    post = get_object_or_404(PPT, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return redirect('home')
@login_required
def favourite_add6(request, id):
    post = get_object_or_404(GIF, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return redirect('home')
@login_required
def favourite_add7(request, id):
    post = get_object_or_404(Exercise, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return redirect('home')
@login_required
def favourite_add8(request, id):
    post = get_object_or_404(Example, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return redirect('home')
@login_required
def favourite_add9(request, id):
    post = get_object_or_404(Topic_Reference, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return redirect('home')
@login_required
def favourites_list(request):
    new = Video.newmanager.filter(favourites=request.user)
    new2 = Image.newmanager.filter(favourites=request.user)
    new3 = PDFs.newmanager.filter(favourites=request.user)
    new4 = Audio.newmanager.filter(favourites=request.user)
    new5 = PPT.newmanager.filter(favourites=request.user)
    new6 = GIF.newmanager.filter(favourites=request.user)
    new7 = Exercise.newmanager.filter(favourites=request.user)
    new8 = Example.newmanager.filter(favourites=request.user)
    new9 = Topic_Reference.newmanager.filter(favourites=request.user)
    return render(request, 'favourites/favourites_list.html', {'new':new, 'new2':new2, 'new3':new3, 'new4':new4,
                                                               'new5':new5, 'new6':new6, 'new7':new7, 'new8':new8,
                                                               'new9':new9})

class UpdateClassView(UpdateView):
    model = Classroom
    template_name = 'newapp/update_class.html'
    fields = ('section', 'subject')
class DeleteClassView(DeleteView):
    model = Classroom
    template_name = 'newapp/delete_class.html'
    success_url = reverse_lazy('home')

class ClassListView(ListView):
    model = Classroom
    template_name = 'newapp/class_list.html'
    context_object_name = 'class_list'

#CLASSROOOM (FUNCTION-BASED)
@login_required()
def Add_Classroom(request):
    submitted = False
    if request.method == "POST":
        form = ClassroomForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_classroom?submitted=True')
    else:
        form = ClassroomForm
        if 'submitted' in request.GET:
            submitted = True
    form = ClassroomForm
    return render(request, 'newapp/add_classes.html', {'form': form, 'submitted': submitted})

@login_required()
def HomeView(request):
    classroom_list = Classroom.objects.all()
    result = ChapterResult.objects.filter(pk=request.user.id)
    student = Student.objects.filter(pk=request.user.id)
    style_1 = style1.objects.filter(pk=request.user.id)
    style_2 = style2.objects.filter(pk=request.user.id)
    if student.exists():
        if result.exists():
            result1 = ChapterResult.objects.get(pk=request.user.id)
            chapt_result = result1.Quiz_Score
            print(chapt_result)
            if style_1.exists() and style_2.exists():
                print('nice one')
            else:
                redirect('index')
        else:
            return redirect('index')
        return render(request, 'newapp/home.html', {'classroom':classroom_list, 'chapt_result': float(chapt_result)})
    else:
        return redirect('profile-create')

#NOT USED (BACK UP)
class ChapterDetailView(DetailView):
    model = Chapter
    allow_empty = True
    context_object_name = 'chapter_details'
    template_name = 'newapp/chapter_detail.html'

def Chapter_Detail(request, pk):
    chapters = Chapter.objects.get(pk=pk)
    #result = ChapterResult.objects.get(pk=pk)
    #print(result.Quiz_Score)
    result1 = ChapterResult.objects.get(pk=request.user.id)
    chapt_result = result1.Quiz_Score
    context = {
        'chapt_result': float(chapt_result), 'chapter_details':chapters,
    }
    return render(request, 'newapp/chapter_detail.html', context)

class ChapterUpdateView(UpdateView):
    model = Chapter
    form_class = TestChapter
    template_name = 'newapp/update_chapter.html'
    success_url = reverse_lazy('home')
class ChapterCreateView(CreateView):
    allow_empty = True
    model = Chapter
    template_name = 'newapp/create_chapter.html'
    form_class = TestChapter
    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.classroom = self.object.classroom
        fm.save()
        return redirect('home')
@login_required()
def Add_Chapter(request, classroom_id):
    if request.method == "POST":
        class_form = TestClassroom(request.POST)
        form = TestChapter(request.POST)
        if form.is_valid():
            fm = form.save(False)
            fm.classroom = Classroom.objects.get(pk=classroom_id)
            fm.save()
            return redirect(reverse('home'))
    else:
        class_form = TestClassroom()
        form = TestChapter()
    args = {'form':form,}
    args.update(csrf(request))
    args['class_form'] = class_form
    args['form'] = TestChapter
    return render(request, 'newapp/create_chapter.html', args)


class ChapterDeleteView(DeleteView):
    model = Chapter
    context_object_name = 'chapters'
    template_name = 'newapp/delete_chapter.html'
    success_url = reverse_lazy('home')

def Lesson_Detail(request, pk):
    lessons = Lesson.objects.get(pk=pk)
    students = style1.objects.get(pk=request.user.id)
    result = ChapterResult.objects.get(pk=request.user.id)
    result1 = ChapterResult.objects.get(pk=request.user.id)
    print(result.Quiz_Score)
    chapt_result = result1.Quiz_Score

    fav = 0.5
    post1 = lessons.video_set.all()
    for post in post1:
        if post.favourites.exists():
            fav += 0.01
    post2 = lessons.image_set.all()
    for post in post2:
        if post.favourites.exists():
            fav += 0.01
    post3 = lessons.pdfs_set.all()
    for post in post3:
        if post.favourites.exists():
            fav += 0.01
    post4 = lessons.audio_set.all()
    for post in post4:
        if post.favourites.exists():
            fav += 0.01
    post5 = lessons.ppt_set.all()
    for post in post5:
        if post.favourites.exists():
            fav += 0.01
    post6 = lessons.gif_set.all()
    for post in post6:
        if post.favourites.exists():
            fav += 0.01
    post7 = lessons.exercise_set.all()
    for post in post7:
        if post.favourites.exists():
            fav += 0.01
    post8 = lessons.example_set.all()
    for post in post8:
        if post.favourites.exists():
            fav += 0.01
    post9 = lessons.topic_reference_set.all()
    for post in post9:
        if post.favourites.exists():
            fav += 0.01

    print(fav)
    fav2 = (1 - float(fav))
    print(fav2)
    # dont forget to also include the code idea for first time taking the LMS (no chat. quiz yet)
    if (float(result1.Quiz_Score) < 70.0) and (float(result1.Quiz_Score) != 0.0):
        print('Failed')
        LS1 = []
        LS2 = []
        style_1 = style1.objects.get(pk=request.user.id)
        style_2 = style2.objects.get(pk=request.user.id)
        student_1 = []
        # FOR STYLE_1...
        if style_1.LO1 == 'Active':
            item = ['video', 'diagram', 'demo', 'ppt', 'exercises']
            LS1.append(item)
        elif style_1.LO1 == 'Sensing':
            item = ['video', 'example', 'diagram', 'demo']
            LS1.append(item)
        elif style_1.LO1 == 'Visual':
            item = ['video', 'example', 'diagram', 'demo', 'ppt']
            LS1.append(item)
        elif style_1.LO1 == 'Sequential':
            item = ['video', 'example', 'exercises', 'pdf', 'audio']
            LS1.append(item)
        elif style_1.LO1 == 'Reflective':
            item = ['pdf', 'exercises', 'diagram', 'audio']
            LS1.append(item)
        elif style_1.LO1 == 'Intuitive':
            item = ['tore', 'ppt', 'diagram', 'pdf']
            LS1.append(item)
        elif style_1.LO1 == 'Verbal':
            item = ['pdf', 'exercises', 'diagram', 'demo']
            LS1.append(item)
        elif style_1.LO1 == 'Global':
            item = ['video', 'ppt', 'pdf', 'diagram', 'audio']
            LS1.append(item)

        # FOR STYLE_2...
        if style_2.LO2 == 'Active':
            item = ['video', 'diagram', 'demo', 'ppt', 'exercises']
            LS2.append(item)
        elif style_2.LO2 == 'Sensing':
            item = ['video', 'example', 'diagram', 'demo']
            LS2.append(item)
        elif style_2.LO2 == 'Visual':
            item = ['video', 'example', 'diagram', 'demo', 'ppt']
            LS2.append(item)
        elif style_2.LO2 == 'Sequential':
            item = ['video', 'example', 'exercises', 'pdf', 'audio']
            LS2.append(item)
        elif style_2.LO2 == 'Reflective':
            item = ['pdf', 'exercises', 'diagram', 'audio']
            LS2.append(item)
        elif style_2.LO2 == 'Intuitive':
            item = ['tore', 'ppt', 'diagram', 'pdf']
            LS2.append(item)
        elif style_2.LO2 == 'Verbal':
            item = ['pdf', 'exercises', 'diagram', 'demo']
            LS2.append(item)
        elif style_2.LO2 == 'Global':
            item = ['video', 'ppt', 'pdf', 'diagram', 'audio']
            LS2.append(item)
        # BAYESIAN FILTERING!!!
        students2 = style2.objects.get(pk=request.user.id)

        for LS_1 in LS1:
            x = []
            xx = []
            if LS_1 not in LS2:
                xx.append(LS_1)
                xx.append(LS1[0])
                xyz = LS1[0] + LS2[0]
                xxx = len(xx[1])
                yyy = len(LS1[0] + LS2[0])
                prob2 = ((xxx + 3) / yyy)
                prob1 = (1 - prob2)
                x.append(prob1)
                x.append(prob2)
                print(LS1[0])
                print(LS2[0])
                print(x)
                print(xxx)
                print(yyy)
                # gawa ko ito, tas nagEdit din me sa gender_probs by adding float function sa loob.
                # Palitan ang variable names ng Duplicates, Bookmarks and other variables depende sa gusto natin
                DUP = [x[0], x[1]]
                favourites = [fav2, fav,
                              fav2, fav]
                acceptance = [0.31000000000000005, 0.69,
                              0.27, 0.73,
                              0.13, 0.87,
                              0.06999999999999995, 0.93]

                X = BbnNode(Variable(1, 'fav', ['false', 'true']), favourites)
                Y = BbnNode(Variable(2, 'accept', ['false', 'true']), acceptance)
                Z = BbnNode(Variable(0, 'duplicate', ['false', 'true']), DUP)

                bbn = Bbn() \
                    .add_node(X) \
                    .add_node(Y) \
                    .add_node(Z) \
                    .add_edge(Edge(Z, X, EdgeType.DIRECTED)) \
                    .add_edge(Edge(Z, Y, EdgeType.DIRECTED)) \
                    .add_edge(Edge(X, Y, EdgeType.DIRECTED))

                # compute the ACE
                ace = Ace(bbn)
                results = ace.get_ace('accept', 'duplicate', 'true')
                t = results['true']  # gawan ng if/else function base sa status ng files na i-filter sa ating LMS system
                f = results['false']
                average_causal_impact = t - f
                print(average_causal_impact)
                print(t)
                print('The Probability of the object to be accepted is: ' + str(f * 100) + ' %')
                if f > 0.55:
                    # maybe gawa ng boolean function here to make the style1.LO1 to be included
                    # in the new_learning_path
                    students1 = style1.objects.get(pk=request.user.id)
                    print(xyz)
                    print(students2.LO2)
                    print(students1.LO1)
                    print('The Object is ACCEPTED in the filtering')

                else:
                    students1 = None
                    print(xx)
                    print(students2.LO2)
                    print('The Object is REJECTED in the filtering')

        a = ['Active', 'Sensing', 'Visual', 'Sequential', 'Global']
        b = ['Active', 'Reflective', 'Sensing', 'Intuitive', 'Visual', 'Verbal', 'Global']
        c = ['Reflective', 'Intuitive', 'Verbal', 'Sequential', 'Global']
        d = ['Reflective', 'Sequential', 'Global']
        e = ['Active', 'Intuitive', 'Visual', 'Global']
        f = ['Active', 'Sensing', 'Visual', 'Verbal']
        g = ['Active', 'Reflective', 'Verbal', 'Sequential']
        h = ['Sensing', 'Visual', 'Sequential']
        i = ['Intuitive']
        context = {'lesson_details': lessons, 'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f, 'g': g,
                   'h': h, 'i': i, 'students2': students2, 'students1': students1, 'chapt_result': float(chapt_result)}
        return render(request, 'newapp/lesson_detail.html', context)
    elif float(result.Quiz_Score) == 0:
        print(students.LO1)
        a = ['Active', 'Sensing', 'Visual', 'Sequential', 'Global']
        b = ['Active', 'Reflective', 'Sensing', 'Intuitive', 'Visual', 'Verbal', 'Global']
        c = ['Reflective', 'Intuitive', 'Verbal', 'Sequential', 'Global']
        d = ['Reflective', 'Sequential', 'Global']
        e = ['Active', 'Intuitive', 'Visual', 'Global']
        f = ['Active', 'Sensing', 'Visual', 'Verbal']
        g = ['Active', 'Reflective', 'Verbal', 'Sequential']
        h = ['Sensing', 'Visual', 'Sequential']
        i = ['Intuitive']
        context = {'lesson_details':lessons, 'a':a, 'b':b, 'c':c, 'd':d, 'e':e, 'f':f, 'g':g,
                'h':h, 'i':i, 'students':students, 'chapt_result': float(chapt_result)}
        return render(request, 'newapp/lesson_detail.html', context)
    print(students.LO1)
    a = ['Active', 'Sensing', 'Visual', 'Sequential', 'Global']
    b = ['Active', 'Reflective', 'Sensing', 'Intuitive', 'Visual', 'Verbal', 'Global']
    c = ['Reflective', 'Intuitive', 'Verbal', 'Sequential', 'Global']
    d = ['Reflective', 'Sequential', 'Global']
    e = ['Active', 'Intuitive', 'Visual', 'Global']
    f = ['Active', 'Sensing', 'Visual', 'Verbal']
    g = ['Active', 'Reflective', 'Verbal', 'Sequential']
    h = ['Sensing', 'Visual', 'Sequential']
    i = ['Intuitive']
    context = {'lesson_details': lessons, 'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f, 'g': g,
               'h': h, 'i': i, 'students': students, 'chapt_result': float(result.Quiz_Score)}
    return render(request, 'newapp/lesson_detail.html', context)
class LessonUpdateView(UpdateView):
    model = Lesson
    template_name = 'newapp/update_lesson.html'
    form_class = TestLesson
    success_url = reverse_lazy('home')
class LessonDeleteView(DeleteView):
    model = Lesson
    context_object_name = 'lessons'
    template_name = 'newapp/delete_lesson.html'
    success_url = reverse_lazy('home')
class LessonCreateView(CreateView):
    allow_empty = True
    model = Lesson
    template_name = 'newapp/create_lesson.html'
    fields = ('title', 'description',)
    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.chapter = self.object.chapter
        fm.save()
        return redirect('home')
@login_required()
def Add_Lesson(request, chapter_id):
    if request.method == "POST":
        form = TestLesson(request.POST)
        chapter_form = TestChapter(request.POST)
        if form.is_valid():
            fm = form.save(False)
            fm.chapter = Chapter.objects.get(pk=chapter_id)
            fm.save()
            return redirect(reverse('home'))
    else:
        form = TestLesson()
        chapter_form = TestChapter()
    args = {}
    args.update(csrf(request))
    args['chapter_form'] = chapter_form
    args['form'] = TestLesson
    return render(request, 'newapp/create_lesson.html', args)

#Video Content
class VideoDetailView(DetailView):
    model = Video
    context_object_name = 'videos'
    template_name = 'video/video_detail.html'
class VideoListView(ListView):
    model = Video
    context_object_name = 'videos'
    template_name = 'video/video_list.html'
class VideoUpdateView(UpdateView):
    model = Video
    template_name = 'video/update_video.html'
    form_class = VideoForm
    success_url = reverse_lazy('home')
class VideoDeleteView(DeleteView):
    model = Video
    context_object_name = 'videos'
    template_name = 'video/delete_video.html'
    success_url = reverse_lazy('home')
class VideoCreateView(CreateView):
    model = Video
    template_name = 'video/create_video.html'
    context_object_name = 'vid'
    form_class = VideoForm
    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.lesson = self.object.lesson
        fm.save()
        return redirect('home')
class VideoCreateView2(CreateView):
    model = Video
    form_class = VideoForm2
    #fields = ('first_name', 'last_name', 'student','img', 'age', 'section', 'status')
    template_name = 'video/create_video.html'
    context_object_name = 'vid'
    def form_valid(self, form, *args, **kwargs):
        form.save()
        return redirect('home')
def Add_Video(request, lesson_id):
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        lesson_form = TestLesson(request.POST)
        if form.is_valid():
            fm = form.save(False)
            fm.lesson = Lesson.objects.get(pk=lesson_id)
            fm.save()
            return redirect(reverse('home'))
    else:
        form = VideoForm()
        lesson_form = TestLesson()
    args = {}
    args.update(csrf(request))
    args['lesson_form'] = lesson_form
    args['form'] = form
    return render(request, 'video/create_video.html', args)
#Image Content
class ImageDetailView(DetailView):
    model = Image
    context_object_name = 'images'
    template_name = 'image/image_detail.html'
class ImageListView(ListView):
    model = Image
    context_object_name = 'images'
    template_name = 'image/image_list.html'
class ImageUpdateView(UpdateView):
    model = Image
    template_name = 'image/update_image.html'
    form_class = ImageForm
    success_url = reverse_lazy('home')
class ImageDeleteView(DeleteView):
    model = Image
    context_object_name = 'images'
    template_name = 'image/delete_image.html'
    success_url = reverse_lazy('home')
class ImageCreateView(CreateView):
    model = Image
    template_name = 'image/create_image.html'
    context_object_name = 'img'
    form_class = ImageForm
    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.lesson = self.object.lesson
        fm.save()
        return redirect('home')
class ImageCreateView2(CreateView):
    model = Image
    form_class = ImageForm2
    template_name = 'image/create_image.html'
    context_object_name = 'img'
    def form_valid(self, form, *args, **kwargs):
        form.save()
        return redirect('home')
def Add_Image(request, lesson_id):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        lesson_form = TestLesson(request.POST)
        if form.is_valid():
            fm = form.save(False)
            fm.lesson = Lesson.objects.get(pk=lesson_id)
            fm.save()
            return redirect(reverse('home'))
    else:
        form = ImageForm()
        lesson_form = TestLesson()
    args = {}
    args.update(csrf(request))
    args['lesson_form'] = lesson_form
    args['form'] = form
    return render(request, 'image/create_image.html', args)

#PDF content
class PDFDetailView(DetailView):
    model = PDFs
    context_object_name = 'pdfs'
    template_name = 'pdf/pdf_detail.html'
class PDFListView(ListView):
    model = PDFs
    context_object_name = 'pdfs'
    template_name = 'pdf/pdf_list.html'
class PDFUpdateView(UpdateView):
    model = PDFs
    template_name = 'pdf/update_pdf.html'
    form_class = PDFForm
    success_url = reverse_lazy('home')
class PDFDeleteView(DeleteView):
    model = PDFs
    context_object_name = 'pdfs'
    template_name = 'pdf/delete_pdf.html'
    success_url = reverse_lazy('home')
class PDFCreateView(CreateView):
    model = PDFs
    template_name = 'pdf/create_pdf.html'
    context_object_name = 'pdfs'
    form_class = PDFForm
    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.lesson = self.object.lesson
        fm.save()
        return redirect('home')
class PDFCreateView2(CreateView):
    model = PDFs
    form_class = PDFForm2
    template_name = 'pdf/create_pdf.html'
    context_object_name = 'pdf'
    def form_valid(self, form, *args, **kwargs):
        form.save()
        return redirect('home')

def Add_PDF(request, lesson_id):
    if request.method == "POST":
        form = PDFForm(request.POST, request.FILES)
        lesson_form = TestLesson(request.POST)
        if form.is_valid():
            fm = form.save(False)
            fm.lesson = Lesson.objects.get(pk=lesson_id)
            fm.save()
            return redirect(reverse('home'))
    else:
        form = PDFForm()
        lesson_form = TestLesson()
    args = {}
    args.update(csrf(request))
    args['lesson_form'] = lesson_form
    args['form'] = form
    return render(request, 'pdf/create_pdf.html', args)

#Audio Content
class AudioDetailView(DetailView):
    model = Audio
    context_object_name = 'audios'
    template_name = 'audio/audio_detail.html'
class AudioListView(ListView):
    model = Video
    context_object_name = 'audios'
    template_name = 'audio/audio_list.html'
class AudioUpdateView(UpdateView):
    model = Audio
    template_name = 'audio/update_audio.html'
    form_class = AudioForm
    success_url = reverse_lazy('home')
class AudioDeleteView(DeleteView):
    model = Audio
    context_object_name = 'audios'
    template_name = 'audio/delete_audio.html'
    success_url = reverse_lazy('home')
class AudioCreateView(CreateView):
    model = Audio
    template_name = 'audio/create_audio.html'
    context_object_name = 'audios'
    form_class = AudioForm
    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.lesson = self.object.lesson
        fm.save()
        return redirect('home')
class AudiCreateView2(CreateView):
    model = Audio
    form_class = AudioForm2
    template_name = 'audio/create_audio.html'
    context_object_name = 'audio'
    def form_valid(self, form, *args, **kwargs):
        form.save()
        return redirect('home')

def Add_Audio(request, lesson_id):
    if request.method == "POST":
        form = AudioForm(request.POST, request.FILES)
        lesson_form = TestLesson(request.POST)
        if form.is_valid():
            fm = form.save(False)
            fm.lesson = Lesson.objects.get(pk=lesson_id)
            fm.save()
            return redirect(reverse('home'))
    else:
        form = AudioForm()
        lesson_form = TestLesson()
    args = {}
    args.update(csrf(request))
    args['lesson_form'] = lesson_form
    args['form'] = form
    return render(request, 'audio/create_audio.html', args)

#PPT content
class PPTDetailView(DetailView):
    model = PPT
    context_object_name = 'ppts'
    template_name = 'ppt/ppt_detail.html'
class PPTListView(ListView):
    model = PPT
    context_object_name = 'ppts'
    template_name = 'ppt/ppt_list.html'
class PPTUpdateView(UpdateView):
    model = PPT
    template_name = 'ppt/update_ppt.html'
    form_class = PPTForm
    success_url = reverse_lazy('home')
class PPTDeleteView(DeleteView):
    model = PPT
    context_object_name = 'ppts'
    template_name = 'ppt/delete_ppt.html'
    success_url = reverse_lazy('home')
class PPTCreateView(CreateView):
    model = PPT
    template_name = 'ppt/create_ppt.html'
    context_object_name = 'ppts'
    form_class = PPTForm
    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.lesson = self.object.lesson
        fm.save()
        return redirect('home')
class PPTCreateView2(CreateView):
    model = PPT
    form_class = PPTForm2
    template_name = 'ppt/create_ppt.html'
    context_object_name = 'ppt'
    def form_valid(self, form, *args, **kwargs):
        form.save()
        return redirect('home')

def Add_PPT(request, lesson_id):
    if request.method == "POST":
        form = PPTForm(request.POST, request.FILES)
        lesson_form = TestLesson(request.POST)
        if form.is_valid():
            fm = form.save(False)
            fm.lesson = Lesson.objects.get(pk=lesson_id)
            fm.save()
            return redirect(reverse('home'))
    else:
        form = PPTForm()
        lesson_form = TestLesson()
    args = {}
    args.update(csrf(request))
    args['lesson_form'] = lesson_form
    args['form'] = form
    return render(request, 'ppt/create_ppt.html', args)

#GIF content
class GIFDetailView(DetailView):
    model = GIF
    context_object_name = 'gifs'
    template_name = 'gif/gif_detail.html'
class GIFListView(ListView):
    model = GIF
    context_object_name = 'gifs'
    template_name = 'gif/gif_list.html'
class GIFUpdateView(UpdateView):
    model = GIF
    template_name = 'gif/update_gif.html'
    form_class = GIFForm
    success_url = reverse_lazy('home')
class GIFDeleteView(DeleteView):
    model = GIF
    context_object_name = 'gifs'
    template_name = 'gif/delete_gif.html'
    success_url = reverse_lazy('home')
class GIFCreateView(CreateView):
    model = GIF
    template_name = 'gif/create_gif.html'
    context_object_name = 'gifs'
    form_class = GIFForm
    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.lesson = self.object.lesson
        fm.save()
        return redirect('home')
class GIFCreateView2(CreateView):
    model = GIF
    form_class = GIFForm2
    template_name = 'gif/create_gif.html'
    context_object_name = 'gif'
    def form_valid(self, form, *args, **kwargs):
        form.save()
        return redirect('home')

def Add_GIF(request, lesson_id):
    if request.method == "POST":
        form = GIFForm(request.POST, request.FILES)
        lesson_form = TestLesson(request.POST)
        if form.is_valid():
            fm = form.save(False)
            fm.lesson = Lesson.objects.get(pk=lesson_id)
            fm.save()
            return redirect(reverse('home'))
    else:
        form = GIFForm()
        lesson_form = TestLesson()
    args = {}
    args.update(csrf(request))
    args['lesson_form'] = lesson_form
    args['form'] = form
    return render(request, 'gif/create_gif.html', args)

#Exercise content
class ExerciseDetailView(DetailView):
    model = Exercise
    context_object_name = 'exercises'
    template_name = 'exercise/exercise_detail.html'
class ExerciseListView(ListView):
    model = Exercise
    context_object_name = 'exercises'
    template_name = 'exercise/exercise_list.html'
class ExerciseUpdateView(UpdateView):
    model = Exercise
    template_name = 'exercise/update_exercise.html'
    form_class = ExerciseForm
    success_url = reverse_lazy('home')
class ExerciseDeleteView(DeleteView):
    model = Exercise
    context_object_name = 'exercises'
    template_name = 'exercise/delete_exercise.html'
    success_url = reverse_lazy('home')
class ExericeCreateView(CreateView):
    model = Exercise
    template_name = 'exercise/create_exercise.html'
    context_object_name = 'exercises'
    form_class = ExerciseForm
    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.lesson = self.object.lesson
        fm.save()
        return redirect('home')
class ExerciseCreateView2(CreateView):
    model = Exercise
    form_class = ExerciseForm2
    template_name = 'exercise/create_exercise.html'
    context_object_name = 'exercise'
    def form_valid(self, form, *args, **kwargs):
        form.save()
        return redirect('home')

def Add_Exercise(request, lesson_id):
    if request.method == "POST":
        form = ExerciseForm(request.POST, request.FILES)
        lesson_form = TestLesson(request.POST)
        if form.is_valid():
            fm = form.save(False)
            fm.lesson = Lesson.objects.get(pk=lesson_id)
            fm.save()
            return redirect(reverse('home'))
    else:
        form = ExerciseForm()
        lesson_form = TestLesson()
    args = {}
    args.update(csrf(request))
    args['lesson_form'] = lesson_form
    args['form'] = form
    return render(request, 'exercise/create_exercise.html', args)

#Example content
class ExampleDetailView(DetailView):
    model = Example
    context_object_name = 'examples'
    template_name = 'example/example_detail.html'
class ExampleListView(ListView):
    model = Example
    context_object_name = 'examples'
    template_name = 'example/example_list.html'
class ExampleUpdateView(UpdateView):
    model = Example
    template_name = 'example/update_example.html'
    form_class = ExampleForm
    success_url = reverse_lazy('home')
class ExampleDeleteView(DeleteView):
    model = Example
    context_object_name = 'examples'
    template_name = 'example/delete_example.html'
    success_url = reverse_lazy('home')
class ExampleCreateView(CreateView):
    model = Example
    template_name = 'example/create_example.html'
    context_object_name = 'examples'
    form_class = ExampleForm
    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.lesson = self.object.lesson
        fm.save()
        return redirect('home')
class ExampleCreateView2(CreateView):
    model = Example
    form_class = ExampleForm2
    template_name = 'example/create_example.html'
    context_object_name = 'example'
    def form_valid(self, form, *args, **kwargs):
        form.save()
        return redirect('home')

def Add_Example(request, lesson_id):
    if request.method == "POST":
        form = ExampleForm(request.POST, request.FILES)
        lesson_form = TestLesson(request.POST)
        if form.is_valid():
            fm = form.save(False)
            fm.lesson = Lesson.objects.get(pk=lesson_id)
            fm.save()
            return redirect(reverse('home'))
    else:
        form = ExampleForm()
        lesson_form = TestLesson()
    args = {}
    args.update(csrf(request))
    args['lesson_form'] = lesson_form
    args['form'] = form
    return render(request, 'example/create_example.html', args)

#Topic/Reference content
class ToreDetailView(DetailView):
    model = Topic_Reference
    context_object_name = 'tores'
    template_name = 'tore/tore_detail.html'
class ToreListView(ListView):
    model = Topic_Reference
    context_object_name = 'tores'
    template_name = 'tore/tore_list.html'
class ToreUpdateView(UpdateView):
    model = Topic_Reference
    template_name = 'tore/update_tore.html'
    form_class = ToreForm
    success_url = reverse_lazy('home')
class ToreDeleteView(DeleteView):
    model = Topic_Reference
    context_object_name = 'tores'
    template_name = 'tore/delete_tore.html'
    success_url = reverse_lazy('home')
class ToreCreateView(CreateView):
    model = Topic_Reference
    template_name = 'tore/create_tore.html'
    context_object_name = 'tores'
    form_class = ToreForm
    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.lesson = self.object.lesson
        fm.save()
        return redirect('home')
class ToreCreateView2(CreateView):
    model = Topic_Reference
    form_class = ToreForm2
    template_name = 'tore/create_tore.html'
    context_object_name = 'tore'
    def form_valid(self, form, *args, **kwargs):
        form.save()
        return redirect('home')

def Add_Tore(request, lesson_id):
    if request.method == "POST":
        form = ToreForm(request.POST, request.FILES)
        lesson_form = TestLesson(request.POST)
        if form.is_valid():
            fm = form.save(False)
            fm.lesson = Lesson.objects.get(pk=lesson_id)
            fm.save()
            return redirect(reverse('home'))
    else:
        form = ToreForm()
        lesson_form = TestLesson()
    args = {}
    args.update(csrf(request))
    args['lesson_form'] = lesson_form
    args['form'] = form
    return render(request, 'tore/create_tore.html', args)

#LOGIN/REGISTER STUFF
def LoginUser(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login_register.html', {'page':page})

def RegisterUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            user = authenticate(request, username=user.username, password=request.POST['password1'])
            if user is not None:
                login(request, user)
                return redirect('profile-create')
    context = {
        'form':form, 'page':page
    }
    return render(request, 'login_register.html', context)

def LogOutUser(request):
    logout(request)
    return redirect('login')

def AboutLang(request):
    return render(request, 'newapp/about.html')