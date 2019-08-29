from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

from .models import Classroom , Student
from .forms import ClassroomForm , SigninForm, SignupForm, StudentForm

def classroom_list(request):
    classrooms = Classroom.objects.all()
    context = {
        "classrooms": classrooms,
    }
    return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    context = {
        "classroom": classroom,
    }
    return render(request, 'classroom_detail.html', context)


def classroom_create(request):
    if request.user.is_anonymous:
        messages.warning(request, "You are not a user please login")
        return redirect('signin')
    form = ClassroomForm()
    if request.method == "POST":
        form = ClassroomForm(request.POST, request.FILES or None)
        if form.is_valid():
            classroom_obj = form.save(commit=False)
            classroom_obj.teacher = request.user
            classroom_obj.save()
            messages.success(request, "Successfully Created!")
            return redirect('classroom-list')
        print (form.errors)
    context = {
    "form": form,

    }
    return render(request, 'create_classroom.html', context)

def student_create(request, classroom_id):
    classroom_obj = Classroom.objects.get(id = classroom_id)
    if request.user != classroom_obj.teacher:
        messages.warning(request, "You are not the teacher for this classroom")
        return redirect('classroom-list')
    form = StudentForm()
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES or None)
        if form.is_valid():
            student = form.save(commit=False)
            student.classroom = classroom_obj
            student.save()
            messages.success(request, "Successfully Added a student!")
            return redirect('classroom-detail', classroom_id)
        print (form.errors)
    context = {
    "form": form,
    'classroom': classroom_obj,
    }
    return render(request, 'create_student.html', context)


def classroom_update(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    if request.user != classroom.teacher:
        messages.warning(request, "You are not the teacher for this classroom")
        return redirect('classroom-list')
    form = ClassroomForm(instance=classroom)
    if request.method == "POST":
        form = ClassroomForm(request.POST, request.FILES or None, instance=classroom)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Edited!")
            return redirect('classroom-list')
        print (form.errors)
    context = {
    "form": form,
    "classroom": classroom,
    }
    return render(request, 'update_classroom.html', context)


def student_update(request, student_id):
    student = Student.objects.get(id=student_id)
    if request.user != student.classroom.teacher:
        messages.warning(request, "You are not the teacher for this classroom")
        return redirect('classroom-list')
    form = StudentForm(instance=student)
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES or None, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Edited!")
            return redirect('classroom-detail', student.classroom.id)
        print (form.errors)
    context = {
    "form": form,
    "student": student,
    }
    return render(request, 'update_student.html', context)


def classroom_delete(request, classroom_id):
    classroom_obj = Classroom.objects.get(id=classroom_id)
    if request.user != classroom_obj.teacher:
        messages.warning(request, "You are not the teacher for this classroom")
        return redirect('signin')
    classroom_obj.delete()
    messages.success(request, "Successfully Deleted!")
    return redirect('classroom-list')


def student_delete(request, student_id):
    student_obj = Student.objects.get(id=student_id)
    if request.user != student_obj.classroom.teacher:
        messages.warning(request, "You are not the teacher for this classroom")
        return redirect('classroom-list')
    student_obj.delete()
    messages.success(request, "Successfully Deleted!")
    return redirect('classroom-detail', student_obj.classroom.id )


def signup(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()

            login(request ,user)
            return redirect('classroom-list')
    context = {
        'form': form,
    }
    return render(request,'singup.html',context)

def signin(request):
    form = SigninForm()
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('classroom-list')
    context = {
        "form":form
    }
    return render(request, 'signin.html', context)

def signout(request):
    logout(request)
    return redirect('signin')

