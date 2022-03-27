import login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import messages

from hod.models import scheme, subject, subject_to_staff, batch
from staff.models import profile
from login.models import User


def staff_index(request):
    user_id = request.session['id']
    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}


    return render(request, 'staff_index.html', {'context': context})


# Staff profile

def staff_profile(request):
    # name = request.session['staff_name']
    user_id = request.session['id']

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name

    context = {'name': fullname}

    date = str(staff_details.Date_of_Joining)
    dob = str(staff_details.Date_of_Birth)

    # Please check the gender is valid or not

    if 'edit_profile' in request.POST:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # faculty_unique_id = request.POST.get('faulty_unique_id')
        # print(faculty_unique_id)
        gender = request.POST.get('gender')

        if gender == '0':
            messages.error(request, 'Please select the valid gender')

        else:

            dob = request.POST.get('date_of_birth')
            phone_no = request.POST.get('phone_no')
            email = request.POST.get('email')
            aadhaar_no = request.POST.get('aadhaar_no')
            caste = request.POST.get('caste')
            religion = request.POST.get('religion')
            category = request.POST.get('category')
            pan = request.POST.get('pan')

            # date_of_joining = request.POST.get('date_of_joining')
            # aicte_unique_id = request.POST.get('aicte_unique_id')

            appointment_type = request.POST.get('appointment_type')
            cadre = request.POST.get('cadre')
            designation = request.POST.get('designation')
            specialisation = request.POST.get('specialisation')
            department_of_program = request.POST.get('department_of_program')
            examiner_institution = request.POST.get('examiner_institution')
            area_of_research = request.POST.get('area_of_research')

            # print(name, gender,faculty_unique_id, dob, phone_no,email, aadhaar_no, caste, religion, category, cadre)

            staff_details.First_name = first_name
            staff_details.Last_name = last_name
            staff_details.Gender = gender
            staff_details.Date_of_Birth = dob
            staff_details.Aadhar_No = aadhaar_no
            staff_details.Caste = caste
            staff_details.Religion = religion
            staff_details.category = category
            staff_details.PAN = pan

            #   staff.Date_of_Joining = date_of_joining
            #   staff.AICTE_unique_Id = aicte_unique_id

            staff_details.Appointment_type = appointment_type
            staff_details.Cadre = cadre
            staff_details.Designation = designation
            staff_details.Specialisation = specialisation
            staff_details.Department_of_program = department_of_program
            staff_details.Examiner_institution = examiner_institution
            staff_details.Area_of_Research = area_of_research
            staff_details.email = email
            staff_details.phone_no = phone_no
            staff_details.save()
            messages.error(request, "Successfully updated profile")

    if 'change_password' in request.POST:
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        renew_password = request.POST.get('renew_password')

        user_data = User.objects.get(username=user_id)
        user_password = user_data.password

        if new_password != renew_password:
            messages.error(request, "Password mismatch")

        elif current_password != user_password:
            messages.error(request, "incorrect old password")

        else:
            user_data.password = new_password
            user_data.save()
            messages.error(request, "Successfully changed password")

    return render(request, 'staff_profile.html',
                  {'context': context, 'staff_details': staff_details, 'date': date, 'date_dob': dob})


def view_subjects(request):
    user_id = request.session['id']
    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    scheme_data = scheme.objects.all()
    view_subject_all = subject.objects.all()
    assign_subject_data = subject_to_staff.objects.all()
    none = "None"
    staff_data = profile.objects.all()
    batch_data = batch.objects.all()


    assigned_subject_to_this_staff = subject_to_staff.objects.filter(staff_id=staff_details.id)


    return render(request, 'view_subjects.html',
                  {
    'scheme_data': scheme_data,
    "view_subject": view_subject_all,
    'assign_subject_data': assign_subject_data,
    'none': none,
    'staff_data': staff_data,
    'batch_data': batch_data,
    'context': context,
    'subject_to_this_staff': assigned_subject_to_this_staff
    })

# logout
def log_out(request):
    logout(request)
    return redirect(login.views.login)
