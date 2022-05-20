from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.HomeView, name='home'),
    path('about/', views.AboutLang, name='about'),
    path('ILS', views.index , name='index'),
    path('ILS/add_question/', views.Add_ILS_Question, name='ils_add'),
    path('chapter/pre-test/<int:pk>', views.PreTest, name='pre-test'),
    path('chapter/quiz/<int:pk>', views.ChapterQuiz,name='chapter-quiz'),
    path('dummy/', views.CreateResult.as_view(), name='dummy-result'),
    path('profile/create/', views.ProfileCreateView.as_view(), name='profile-create'),
    path('addQuestion/<int:pk>/', views.addQuestion,name='addQuestion'),
    path('add_pretest/<int:chapter_id>', views.Add_Pretest_Question, name='add-pretest'),
    path('delete_pretest/<int:pk>', views.PretestDeleteView.as_view(), name='delete-pretest'),
    path('add_question/<int:chapter_id>', views.Add_Question, name='add-question'),
    #path('add_question/<int:pk>', views.AddQuestionView.as_view(), name='add-question'),
    path('edit_question/<int:pk>/', views.QuizUpdateView.as_view(), name='edit-question'),
    path('edit_pretest/<int:pk>', views.PretestUpdateView.as_view(), name='edit-pretest'),
    path('delete_question/<int:pk>', views.QuizDeleteView.as_view(), name='delete-question'),
    #path('profile/<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:id>', views.ProfileViewdin, name='profile'),
    path('profile/<int:pk>/edit/', views.EditProfile.as_view(), name='edit-profile'),
    path('student_lists/', views.student_lists, name='student-list'),
    path('', views.LoginUser, name='login'),
    path('logout/', views.LogOutUser, name='logout'),
    path('register/', views.RegisterUser, name='register'),

    #Favorites
    path('favorite/<int:id>', views.favourite_add1, name='favourite_add1'),
    path('favorite2/<int:id>', views.favourite_add2, name='favourite_add2'),
    path('favorite3/<int:id>', views.favourite_add3, name='favourite_add3'),
    path('favorite4/<int:id>', views.favourite_add4, name='favourite_add4'),
    path('favorite5/<int:id>', views.favourite_add5, name='favourite_add5'),
    path('favorite6/<int:id>', views.favourite_add6, name='favourite_add6'),
    path('favorite7/<int:id>', views.favourite_add7, name='favourite_add7'),
    path('favorite8/<int:id>', views.favourite_add8, name='favourite_add8'),
    path('favorite9/<int:id>', views.favourite_add9, name='favourite_add9'),
    path('favourites_list/', views.favourites_list, name='favourites_list'),

    #CLASSROOM URLS(class-based)
    #path('', views.HomeView.as_view(), name='home'),
    #path('class/<int:pk>', views.ClassDetailView.as_view(), name='class-details'),
    #path('create_class/', views.AddClassView.as_view(), name='class-create'),
    path('class/edit/<int:pk>', views.UpdateClassView.as_view(), name='class-edit'),
    path('class/<int:pk>/delete', views.DeleteClassView.as_view(), name='class-delete'),
    path('add_classroom/', views.Add_Classroom, name='classroom-create'),
    path('class/list/', views.ClassListView.as_view(), name='class-list'),

    #CHAPTER URLS
    path('chapter/<int:pk>', views.Chapter_Detail, name='chapter-details'),
    path('chapter/create_chapter/<int:classroom_id>', views.Add_Chapter, name='chapter-create2'),
    path('chapter/<int:pk>/create_chapter/', views.ChapterCreateView.as_view(), name='chapter-create'),
    #path('chapter/<int:pk>', views.ChapterDetailView.as_view(), name='chapter-details'),
    path('chapter/edit/<int:pk>', views.ChapterUpdateView.as_view(), name='chapter-edit'),
    path('chapter/<int:pk>/delete', views.ChapterDeleteView.as_view(), name='chapter-delete'),
    #path('chapter/<int:pk>', views.ChapterListView.as_view(), name='chapter-list'),

    #LESSONS - BAYESIAN FILTER ATTACHED
    path('lesson/<int:pk>', views.Lesson_Detail, name='lesson-details'),
    #path('lesson/<int:pk>', views.LessonDetailView.as_view(), name='lesson-details'),
    path('lesson/edit/<int:pk>', views.LessonUpdateView.as_view(), name='lesson-edit'),
    path('lesson/<int:pk>/delete', views.LessonDeleteView.as_view(), name='lesson-delete'),
    path('lesson/<int:pk>/create_lesson/', views.LessonCreateView.as_view(), name='lesson-create'),
    path('lesson/create_lesson/<int:chapter_id>', views.Add_Lesson, name='lesson-create2'),

    #VIDEO
    path('video/<int:pk>', views.VideoDetailView.as_view(), name='video-detail'),
    path('video/list/', views.VideoListView.as_view(), name='video-list'),
    path('video/edit/<int:pk>', views.VideoUpdateView.as_view(), name='video-edit'),
    path('video/<int:pk>/delete', views.VideoDeleteView.as_view(), name='video-delete'),
    path('video/<int:pk>/create_video', views.VideoCreateView.as_view(), name='video-create'),
    #path('video/create_video/<int:pk>', views.VideoCreateView2.as_view(), name='video-create3'),
    path('video/create_video/<int:lesson_id>', views.Add_Video, name='video-create2'),

    #IMAGE
    path('image/list/', views.ImageListView.as_view(), name='image-list'),
    path('image/<int:pk>', views.ImageDetailView.as_view(), name='image-detail'),
    path('image/edit/<int:pk>', views.ImageUpdateView.as_view(), name='image-edit'),
    path('image/<int:pk>/delete', views.ImageDeleteView.as_view(), name='image-delete'),
    path('image/<int:pk>/create_image', views.ImageCreateView.as_view(), name='image-create'),
    #path('image/create_image/<int:pk>', views.ImageCreateView2.as_view(), name='image-create2'),
    path('image/create_image/<int:lesson_id>', views.Add_Image, name='image-create2'),

    #PDFS
    path('pdf/list/', views.PDFListView.as_view(), name='pdf-list'),
    path('pdf/<int:pk>', views.PDFDetailView.as_view(), name='pdf-detail'),
    path('pdf/edit/<int:pk>', views.PDFUpdateView.as_view(), name='pdf-edit'),
    path('pdf/<int:pk>/delete', views.PDFDeleteView.as_view(), name='pdf-delete'),
    path('pdf/<int:pk>/create_pdf', views.PDFCreateView.as_view(), name='pdf-create'),
    #path('pdf/create_pdf/<int:pk>', views.PDFCreateView2.as_view(), name='pdf-create3'),
    path('pdf/create_pdf/<int:lesson_id>', views.Add_PDF, name='pdf-create3'),

    #AUDIO
    path('audio/list/', views.AudioListView.as_view(), name='audio-list'),
    path('audio/<int:pk>', views.AudioDetailView.as_view(), name='audio-detail'),
    path('audio/edit/<int:pk>', views.AudioUpdateView.as_view(), name='audio-edit'),
    path('audio/<int:pk>/delete', views.AudioDeleteView.as_view(), name='audio-delete'),
    path('audio/<int:pk>/create_audio', views.AudioCreateView.as_view(), name='audio-create'),
    #path('audio/create_audio/<int:pk>', views.AudiCreateView2.as_view(), name='audio-create2'),
    path('audio/create_audio/<int:lesson_id>', views.Add_Audio, name='audio-create2'),

    #PPT
    path('ppt/list/', views.PPTListView.as_view(), name='ppt-list'),
    path('ppt/<int:pk>', views.PPTDetailView.as_view(), name='ppt-detail'),
    path('ppt/edit/<int:pk>', views.PPTUpdateView.as_view(), name='ppt-edit'),
    path('ppt/<int:pk>/delete', views.PPTDeleteView.as_view(), name='ppt-delete'),
    path('ppt/<int:pk>/create_ppt', views.PPTCreateView.as_view(), name='ppt-create'),
    #path('ppt/create_ppt/<int:pk>', views.PPTCreateView2.as_view(), name='ppt-create2'),
    path('ppt/create_ppt/<int:lesson_id>', views.Add_PPT, name='ppt-create2'),

    #GIF
    path('gif/list', views.GIFListView.as_view(), name='gif-list'),
    path('gif/<int:pk>', views.GIFDetailView.as_view(), name='gif-detail'),
    path('gif/edit/<int:pk>', views.GIFUpdateView.as_view(), name='gif-edit'),
    path('gif/<int:pk>/delete', views.GIFDeleteView.as_view(), name='gif-delete'),
    path('gif/<int:pk>/create_gif', views.GIFCreateView.as_view(), name='gif-create'),
    #path('gif/create_gif/<int:pk>', views.GIFCreateView2.as_view(), name='gif-create2'),
    path('gif/create_gif/<int:lesson_id>', views.Add_GIF, name='gif-create2'),

    #Exercise
    path('exercise/list/', views.ExerciseListView.as_view(), name='exercise-list'),
    path('exercise/<int:pk>', views.ExerciseDetailView.as_view(), name='exercise-detail'),
    path('exercise/edit/<int:pk>', views.ExerciseUpdateView.as_view(), name='exercise-edit'),
    path('exercise/<int:pk>/delete', views.ExerciseDeleteView.as_view(), name='exercise-delete'),
    path('exercise/<int:pk>/create_exercise', views.ExericeCreateView.as_view(), name='exercise-create'),
    #path('exercise/create_exercise/<int:pk>', views.ExerciseCreateView2.as_view(), name='exercise-create2'),
    path('exercise/create_exercise/<int:lesson_id>', views.Add_Exercise, name='exercise-create2'),

    #Examples
    path('example/list/', views.ExampleListView.as_view(), name='example-list'),
    path('example/<int:pk>', views.ExampleDetailView.as_view(), name='example-detail'),
    path('example/edit/<int:pk>', views.ExampleUpdateView.as_view(), name='example-edit'),
    path('example/<int:pk>/delete', views.ExampleDeleteView.as_view(), name='example-delete'),
    path('example/<int:pk>/create_example', views.ExampleCreateView.as_view(), name='example-create'),
    #path('example/create_example/<int:pk>', views.ExampleCreateView2.as_view(), name='example-create2'),
    path('example/create_example/<int:lesson_id>', views.Add_Example, name='example-create2'),

    #Topic_References
    path('tore/list/', views.ToreListView.as_view(), name='tore-list'),
    path('tore/<int:pk>', views.ToreDetailView.as_view(), name='tore-detail'),
    path('tore/edit/<int:pk>', views.ToreUpdateView.as_view(), name='tore-edit'),
    path('tore/<int:pk>/delete', views.ToreDeleteView.as_view(), name='tore-delete'),
    path('tore/<int:pk>/create_tore', views.ToreCreateView.as_view(), name='tore-create'),
    #path('tore/create_tore/<int:pk>', views.ToreCreateView2.as_view(), name='tore-create2'),
    path('tore/create_tore/<int:lesson_id>', views.Add_Tore, name='tore-create2'),

    #experiment
    path('exp_class_chapter_create/<int:classroom_id>', views.new_class, name='new-class'),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)