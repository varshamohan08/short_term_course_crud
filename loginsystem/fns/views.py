from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import user_data, ShortTermCourse
from .serializers import userSeralizer
from .forms import LoginForm, ShortTermCourseForm
from django.contrib.auth import logout, update_session_auth_hash
from rest_framework import permissions
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib import messages

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

class userLogout(APIView):
    def get(self, request):
        logout(request)
        return redirect('/login')
    
class userLogin(APIView):
    def get(self, request):
        return render(request, "login.html")
    
    def post(self,request):
        data = request.data

        username = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/fns')
        else:
            return render(request, "login.html")
        

class UserActions(APIView):
    def get(self, request):
        course_count = ShortTermCourse.objects.count()
        user_count = User.objects.count()
        return render(request, "index.html", {'course_count': course_count, 'user_count': user_count})
    
    def post(self,request):
        data = request.data

        username = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/reg')
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)  
        

class ShortCourseAPI(APIView):
    def get(self, request):
        all_courses = ShortTermCourse.objects.all()
        paginator = Paginator(all_courses, 2)  # Display 2 records per page
        page_number = request.GET.get('page')
        courses = paginator.get_page(page_number)
        return render(request, "short-course-view.html", {'courses': courses})
    
    def post(self,request):
        data = request.data

        username = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/reg')
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)  
        
    def delete(self, request, id):

        # id = request.GET.get('id')
        ShortTermCourse.objects.filter(id = id).delete()
        return Response(status = status.HTTP_200_OK)

class AddShortCourseAPI(APIView):
    def get(self, request):
        return render(request, "short-course-create.html")
    
    def post(self,request):

        form = ShortTermCourseForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new ShortTermCourse object and save it to the database
            course = ShortTermCourse(
                title=form.cleaned_data['title'],
                subtitle=form.cleaned_data['subtitle'],
                description=form.cleaned_data['description'],
                amount=form.cleaned_data['amount'],
                additional_information=form.cleaned_data['additional_information'],
                status=form.cleaned_data['status'],
                image=form.cleaned_data['image']
            )
            course.save()
            return redirect('short_course')
        return render(request, "short-course-create.html")
    def delete(self, request):

        id = request.GET.get('id')
        ShortTermCourse.objects.filter(id = id).delete()
        return Response(status = status.HTTP_200_OK)
    
# class UpdateShortCourseAPI(APIView):
#     def get(self, request,id):

#         course = ShortTermCourse.objects.filter(id=id).values()
#         # form = ShortTermCourseForm(instance=course)
#         return render(request, "short-course-create.html", {'form': course})

class UpdateShortCourseAPI(APIView):
    def get(self, request, id):
        course = get_object_or_404(ShortTermCourse, id=id)
        form = ShortTermCourseForm(initial={
            'title': course.title,
            'subtitle': course.subtitle,
            'description': course.description,
            'amount' : course.amount,
            'additional_information' : course.additional_information,
            'status' : course.status,
            'image' : course.image
        })
        return render(request, "short-course-edit.html", {'course': course})
    def post(self, request, id):

        form = ShortTermCourseForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new ShortTermCourse object and save it to the database
            if form.cleaned_data['image'] and form.cleaned_data['image'] != "":
                course = ShortTermCourse.objects.get(id=id)
                course.title=form.cleaned_data['title']
                course.subtitle=form.cleaned_data['subtitle']
                course.description=form.cleaned_data['description']
                course.amount=form.cleaned_data['amount']
                course.additional_information=form.cleaned_data['additional_information']
                course.status=form.cleaned_data['status']
                course.image=form.cleaned_data['image']
                
                course.save()
            else:
                course = ShortTermCourse.objects.get(id=id)
                course.title=form.cleaned_data['title']
                course.subtitle=form.cleaned_data['subtitle']
                course.description=form.cleaned_data['description']
                course.amount=form.cleaned_data['amount']
                course.additional_information=form.cleaned_data['additional_information']
                course.status=form.cleaned_data['status']
                
                course.save()

            return redirect('short_course')
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class userProfile(APIView):
    def get(self, request):
        user_details = User.objects.get(id = request.user.id)
        return render(request, "profile.html", {'details': user_details})
    
    def post(self,request):
        username = request.user.email
        password = request.POST.get('current-password')
        user = authenticate(username=username, password=password)

        if user is not None:
            new_password = request.POST.get('new-password')
            confirm_password = request.POST.get('confirm-new-password')
            
            if new_password == confirm_password:
                user = request.user
                user.set_password(new_password)  # Set the new password
                user.save()
                
                # Update the user's session to prevent logging out
                update_session_auth_hash(request, user)
                
                messages.success(request, 'Password changed successfully.')
                return redirect('logout')
            else:
                messages.error(request, 'Passwords do not match.')
        else:
            messages.error(request, 'Current password not corrects')
    
    def put(self,request):
        data = request.data

        username = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/reg')
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)  