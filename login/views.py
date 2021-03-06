from django.shortcuts import render, redirect

from .models import User
from django.contrib import messages
import student


# Create your views here.


def login(request):

    if request.method == 'POST':
        username1 = request.POST.get('username')
        password1 = request.POST.get('password')

        try:
            user = User.objects.get(username=username1, password=password1)
            if user.password == password1 and user.is_hod == True and user.is_active == True:
                #  print(i.username, i.password)
                first_name = user.first_name
                last_name = user.last_name
                full_name = first_name +" "+ last_name
                request.session['name'] = full_name
                request.session['status'] = 1
                request.session['hod_username'] = username1
                
                return redirect('hod_index')

            elif user.password == password1 and user.is_staff == True and user.is_active == True:
                first_name = user.first_name
                last_name = user.last_name
                full_name = first_name + " " + last_name

                request.session['id'] = username1
                request.session['staff_name'] = full_name
                # request.session['username'] = username1
                
                return redirect('staff_index')

            elif user.password == password1 and user.is_student == True and user.is_active == True:
                first_name = user.first_name
                last_name = user.last_name
                full_name = first_name + " " + last_name

                request.session['student_id'] = username1
                request.session['student_name'] = full_name
                
                return redirect('student_index')
            
            else:
                messages.error(request, 'Invalid username or password')
                return render(request, 'login.html')

        except:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')

    return render(request, 'login.html')
