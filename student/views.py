from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from hod.models import batch, scheme
from student.models import profile_student
from login.models import User
import login


# Create your views here.
def student_index(request):
    name = request.session['student_name']
    # id = request.session['student_id']
    context = {'name': name}

    return render(request, 'student_index.html', {'context': context})


def student_profile(request):
    # name = request.session['student_name']
    id = request.session['student_id']
    student_data = profile_student.objects.filter(register_no=id)
    for i in student_data:
        batch_id = i.batch
        date_of_birth = i.date_of_birth
        name_first = i.first_name
        name_last = i.last_name

    name = name_first + " " + name_last
    context = {'name': name}  # display the name

    batch_data = batch.objects.get(id=batch_id)
    scheme_id = batch_data.scheme
    scheme_data = scheme.objects.get(id=scheme_id)

    date_dob = str(date_of_birth)  # dob can only display in html only as string type

    if 'edit_profile' in request.POST:

        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        dob = request.POST.get('date_of_birth')
        ph_no = request.POST.get('phone_no')
        email = request.POST.get('email')
        address = request.POST.get('address')
        aadhaar_no = request.POST.get('aadhaar_no')
        caste = request.POST.get('caste')
        religion = request.POST.get('religion')
        nationality = request.POST.get('nationality')
        native_place = request.POST.get('native_place')
        blood_group = request.POST.get('blood_group')

        if gender == '0':
            messages.error(request, "Please select a valid Gender")
        elif blood_group == '0':
            messages.error(request, "Please select a valid blood Group")
        else:

            student_data1 = profile_student.objects.get(register_no=id)
            user_data = User.objects.get(username=id)

            user_data.first_name = f_name
            user_data.last_name = l_name
            user_data.save()  # update the first and second name in login table

            student_data1.first_name = f_name
            student_data1.first_name = f_name
            student_data1.last_name = l_name
            student_data1.aadhar_no = aadhaar_no
            student_data1.address = address
            student_data1.phone_no = ph_no
            student_data1.email = email
            student_data1.sex = gender
            student_data1.date_of_birth = dob
            student_data1.nationality = nationality
            student_data1.religion = religion
            student_data1.caste = caste
            student_data1.native_place = native_place
            student_data1.blood_group = blood_group

            student_data1.save()

            messages.error(request, "Successfully updated")
            return render(request, 'student_profile.html',
                          {'student_data': student_data, 'scheme_data': scheme_data, 'batch_data': batch_data,
                           'date_dob': date_dob, 'context': context})

    if 'change_password' in request.POST:
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        renew_password = request.POST.get('renew_password')

        user_data = User.objects.get(username=id)
        user_password = user_data.password

        if new_password != renew_password:
            messages.error(request, "Password mismatch")
        elif current_password != user_password:
            messages.error(request, "incorrect old password")
        else:
            user_data.password = new_password
            user_data.save()
            messages.error(request, "Successfully changed password")
            return render(request, 'student_profile.html',
                          {'student_data': student_data, 'scheme_data': scheme_data, 'batch_data': batch_data,
                           'date_dob': date_dob, 'context': context})

    return render(request, 'student_profile.html',
                  {'student_data': student_data, 'scheme_data': scheme_data, 'batch_data': batch_data,
                   'date_dob': date_dob, 'context': context})


# logout
def log_out(request):
    logout(request)
    return redirect(login.views.login)
