# Complete Django Mental Health Project

# Step 1: Set Up Django Environment
# ==================================
# Install Django
# ```bash
# pip install django
# ```

# Start a new project
# ```bash
# django-admin startproject mental_health_app
# cd mental_health_app
# ```

# Create a new app
# ```bash
# python manage.py startapp mental_test
# ```

# Add the app to INSTALLED_APPS in settings.py
INSTALLED_APPS = [
    ...,
    'mental_test',
]

# Run the development server
# ```bash
# python manage.py runserver
# ```

# Step 2: User Authentication and Registration
# =============================================
# Create a registration view
# mental_test/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('start_test')
    else:
        form = UserCreationForm()
    return render(request, 'mental_test/register.html', {'form': form})

# Add login/logout and register URLs
# mental_health_app/urls.py
from django.contrib import admin
from django.urls import path, include
from mental_test import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Login/Logout
    path('register/', views.register, name='register'),  # User Registration
    path('', include('mental_test.urls')),  # Mental Test App
]

# Create registration template
# templates/mental_test/register.html
# ```html
# <h2>Register</h2>
# <form method="post">
#     {% csrf_token %}
#     {{ form.as_p }}
#     <button type="submit">Register</button>
# </form>
# ```

# Step 3: Create Models for Questions and Results
# =================================================
# mental_test/models.py
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    text = models.TextField()
    option_1 = models.CharField(max_length=100)
    option_2 = models.CharField(max_length=100)
    option_3 = models.CharField(max_length=100)
    option_4 = models.CharField(max_length=100)
    correct_option = models.IntegerField()  # Store 1, 2, 3, or 4

    def __str__(self):
        return self.text

class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}"

# Run migrations
# ```bash
# python manage.py makemigrations
# python manage.py migrate
# ```

# Step 4: Admin Panel for Managing Questions
# ===========================================
# mental_test/admin.py
from django.contrib import admin
from .models import Question, TestResult

admin.site.register(Question)
admin.site.register(TestResult)

# Step 5: Implement Test Flow
# ============================
# mental_test/views.py
@login_required
def start_test(request):
    questions = Question.objects.all()
    return render(request, 'mental_test/start_test.html', {'questions': questions})

@login_required
def submit_test(request):
    if request.method == 'POST':
        questions = Question.objects.all()
        score = 0
        for question in questions:
            selected = int(request.POST.get(str(question.id)))
            if selected == question.correct_option:
                score += 1
        TestResult.objects.create(user=request.user, score=score)
        return redirect('test_result', score=score)

@login_required
def test_result(request, score):
    return render(request, 'mental_test/test_result.html', {'score': score})

@login_required
def suggestions(request):
    return render(request, 'mental_test/suggestions.html')

# mental_test/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('start-test/', views.start_test, name='start_test'),
    path('submit-test/', views.submit_test, name='submit_test'),
    path('result/<int:score>/', views.test_result, name='test_result'),
    path('suggestions/', views.suggestions, name='suggestions'),
]

# Step 6: Templates
# ==================
# start_test.html
# ```html
# <h2>Start Test</h2>
# <form method="post" action="{% url 'submit_test' %}">
#     {% csrf_token %}
#     {% for question in questions %}
#         <p>{{ question.text }}</p>
#         <input type="radio" name="{{ question.id }}" value="1"> {{ question.option_1 }}<br>
#         <input type="radio" name="{{ question.id }}" value="2"> {{ question.option_2 }}<br>
#         <input type="radio" name="{{ question.id }}" value="3"> {{ question.option_3 }}<br>
#         <input type="radio" name="{{ question.id }}" value="4"> {{ question.option_4 }}<br>
#     {% endfor %}
#     <button type="submit">Submit</button>
# </form>
# ```

# test_result.html
# ```html
# <h2>Your Score: {{ score }}</h2>
# <a href="{% url 'start_test' %}">Retake Test</a>
# <a href="{% url 'suggestions' %}">Get Suggestions</a>
# ```

# suggestions.html
# ```html
# <h2>Mental Health Suggestions</h2>
# <ul>
#     <li>Medication: Consult a certified psychologist.</li>
#     <li>Diet: Include omega-3 rich foods and avoid caffeine.</li>
#     <li>Consultation: Schedule a session with a doctor.</li>
# </ul>
# 
