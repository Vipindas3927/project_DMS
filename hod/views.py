from ast import For
import code
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout

import login
from hod.models import batch, scheme, subject, subject_to_staff
from login.models import User
from staff.models import profile
from student.models import profile_student
from hod.models import batch
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
import hod


# Create your views here.
# print(make_password('123'))
# print(check_password('1', '1'))


def hod_index(request):
    status = 0
    try:
        status_new = request.session['status']
    except:
        status += 1

    # print(user_name)
    # full_name = request.session['full_name']
    # if 'user_name' == user_name:
    #  return redirect(login.views.login)
    # else:

    if status == 0:
        # name = request.session['name']
        staff_id = request.session['hod_username']
        staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
        name = staff_details_1.First_name + " " + staff_details_1.Last_name
        context = {'name': name}
        staff_count = profile.objects.all().count()
        student_count = profile_student.objects.all().count()

        return render(request, 'hod_index.html',
                      {"staff_count": staff_count, "student_count": student_count, "context": context,
                       "data_for_self_profile": staff_details_1})
    else:
        return redirect(login.views.login)


# staff code

def add_staff(request):
    # name = request.session['name']

    staff_id = request.session['hod_username']
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_joining = request.POST.get('date_of_joining')
        full_name = first_name + " " + last_name
        password1 = request.POST.get('password_1')
        password2 = request.POST.get('password_2')

        if password1 != password2:
            messages.error(request, 'Password mismatch')
        else:
            user = User.objects.filter(username=username)
            if user:
                messages.error(request, 'User already exist')
            else:
                # enc_pswrd = make_password(password1)
                User.objects.create(username=username,
                                    first_name=first_name,
                                    last_name=last_name,
                                    password=password1,
                                    is_staff=True,
                                    is_active=True,
                                    is_student=False,
                                    is_hod=False,
                                    is_superuser=False

                                    )

                profile.objects.create(Faculty_unique_id=username, First_name=first_name, Last_name=last_name,
                                       Date_of_Joining=date_of_joining)
                messages.error(request, 'Faculty ' + full_name + ' successfully added')

    return render(request, 'add_staff.html', {"context": context, "data_for_self_profile": staff_details_1})


def view_faculty(request):
    # name = request.session['name']
    staff_id = request.session['hod_username']
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    staff_details = profile.objects.all()
    batch_data = batch.objects.all()

    return render(request, 'view_faculty.html',
                  {"staff_data": staff_details, "context": context, "data_for_self_profile": staff_details_1,
                  'batch_data': batch_data
                  })


def delete_faculty(request, f_id):
    # check the faculty for delete is hod or not
    login_data = User.objects.get(username=f_id)
    f_data = profile.objects.get(Faculty_unique_id=f_id)

    if login_data.is_hod:
        messages.error(request, 'Cannot delete your account ' + f_data.First_name + f_data.Last_name)
        return redirect(view_faculty)
    else:
        f_data.delete()
        login_delete = User.objects.get(username=f_id)
        login_delete.delete()
        messages.error(request, 'Successfully deleted the faculty ' + f_data.First_name + f_data.Last_name)
        return redirect(view_faculty)


def faculty_profile(request, f_id):
    # name = request.session['name']
    staff_id = request.session['hod_username']
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    staff_details = profile.objects.get(Faculty_unique_id=f_id)
    date = str(staff_details.Date_of_Joining)
    dob = str(staff_details.Date_of_Birth)

    print(staff_details.Profile_photo)

    if 'edit_profile' in request.POST:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        faculty_unique_id = request.POST.get('faulty_unique_id')
        gender = request.POST.get('gender')

        if gender == '0':
            messages.error(request, 'Please select the valid gender')
        else:

            # please validate gender

            dob = request.POST.get('date_of_birth')
            phone_no = request.POST.get('phone_no')
            email = request.POST.get('email')
            aadhaar_no = request.POST.get('aadhaar_no')
            caste = request.POST.get('caste')
            religion = request.POST.get('religion')
            category = request.POST.get('category')
            pan = request.POST.get('pan')
            date_of_joining = request.POST.get('date_of_joining')
            aicte_unique_id = request.POST.get('aicte_unique_id')
            appointment_type = request.POST.get('appointment_type')
            cadre = request.POST.get('cadre')
            designation = request.POST.get('designation')
            specialisation = request.POST.get('specialisation')
            department_of_program = request.POST.get('department_of_program')
            examiner_institution = request.POST.get('examiner_institution')
            area_of_research = request.POST.get('area_of_research')

            # print(name, gender,faculty_unique_id, dob, phone_no,email, aadhaar_no, caste, religion, category, cadre)

            #  staff_details.Faculty_unique_id = faculty_unique_id
            staff_details.First_name = first_name
            staff_details.Last_name = last_name
            staff_details.Gender = gender
            staff_details.Date_of_Birth = dob
            staff_details.Aadhar_No = aadhaar_no
            staff_details.Caste = caste
            staff_details.Religion = religion
            staff_details.category = category
            staff_details.PAN = pan

            staff_details.Date_of_Joining = date_of_joining
            staff_details.AICTE_unique_Id = aicte_unique_id

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

    if 'change_password' in request.POST:
        new_password = request.POST.get('new_password')
        renew_password = request.POST.get('renew_password')

        user_data = User.objects.get(username=f_id)
        if new_password != renew_password:
            messages.error(request, "Password mismatch")
        else:
            user_data.password = new_password
            user_data.save()
            messages.error(request, "Successfully changed password")

    return render(request, 'faculty_profile.html',
                  {'context': context, 'staff_details': staff_details, 'date': date, 'date_dob': dob,
                   "data_for_self_profile": staff_details_1})


# student view
@csrf_exempt
def check_user_exist(request):
    username = request.POST.get('username')
    subject_exist = User.objects.filter(username=username).exists()
    if subject_exist:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def add_student(request):
    # name = request.session['name']
    staff_id = request.session['hod_username']
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    batch_data_class = batch.objects.all()  # for display the existing batch details
    # batch_data_year = batch.objects.all().distinct('date_of_join')
    scheme_data = scheme.objects.all()

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        batch_id_str = request.POST.get('batch_id')
        batch_id_int = int(batch_id_str)

        full_name = first_name + " " + last_name

        password1 = request.POST.get('password_1')
        password2 = request.POST.get('password_2')

        if batch_id_int == 0:
            messages.error(request, 'Please select Class')
        else:

            batch_data = batch.objects.get(id=batch_id_int)
            class_name = batch_data.class_name
            batch_year = batch_data.date_of_join
            semester = batch_data.semester

            if password1 != password2:
                messages.error(request, 'Password mismatch')
            else:

                user = User.objects.filter(username=username)
                if user:
                    messages.error(request, 'User already exist')
                else:
                    # insert only the year in student profile (column : year_of_join)

                    User.objects.create(username=username,
                                        first_name=first_name,
                                        last_name=last_name,
                                        password=password1,
                                        is_staff=False,
                                        is_active=True,
                                        is_student=True,
                                        is_hod=False,
                                        is_superuser=False
                                        )

                    profile_student.objects.create(
                        register_no=username,
                        first_name=first_name,
                        last_name=last_name,
                        batch=batch_id_int,
                        scheme_id=batch_data.scheme
                    )

                    messages.error(request, 'Student ' + full_name + ' successfully added in ' + batch_data.class_name)

    return render(request, 'add_student.html',
                  {
                      "batch_class": batch_data_class,
                      "context": context,
                      "scheme_data": scheme_data,
                      "data_for_self_profile": staff_details_1
                  }
                  )


def view_student(request):
    # name = request.session['name']
    staff_id = request.session['hod_username']
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    batch_data = batch.objects.all()
    scheme_data = scheme.objects.all()

    if request.method == 'POST':

        batch_id = request.POST.get('batch_select')
        # print(batch_id)
        batch_id_int = int(batch_id)

        if batch_id == '0':

            messages.error(request, 'Please select Batch')

        else:

            batch_id = batch_id_int

            data = profile_student.objects.filter(batch=batch_id)

            batch_data1 = batch.objects.get(id=batch_id)
            scheme_data1 = scheme.objects.get(id=batch_data1.scheme)

            batch_data = batch.objects.all()
            scheme_data = scheme.objects.all()

            return render(request, 'view_student.html',
                          {"student_data": data, "scheme_data1": scheme_data1, 'batch_data1': batch_data1,
                           "context": context,
                           "scheme_data": scheme_data,
                           'batch': batch_data,
                           "data_for_self_profile": staff_details_1
                           })

    return render(request, 'view_student.html',

                  {
                      "batch": batch_data,
                      "scheme_data": scheme_data,
                      "context": context,
                      "data_for_self_profile": staff_details_1

                  }

                  )


'''def student_list(request):
    name = request.session['name']
    context = {'name': name}

    batch_id = request.session['batch_id']
    
    data = profile_student.objects.filter(batch=batch_id)


    batch_data = batch.objects.get(id=batch_id)
    scheme_data = scheme.objects.get(id=batch_data.scheme)
    return render(request, 'student_list.html', {"student_data": data, "scheme_data":scheme_data, 'batch_data': batch_data, "context": context})
'''


# batch details 

def create_batch(request):
    # name = request.session['name']
    staff_id = request.session['hod_username']
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}
    scheme_data = scheme.objects.all()

    tutor_data = profile.objects.all()

    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        date_of_join = request.POST.get('date_of_join')
        semester = request.POST.get('semester')
        scheme_input = request.POST.get('scheme')
        tutor_id = request.POST.get('tutor')
        scheme_input_int = int(scheme_input)
        tutor = int(tutor_id)

        if class_name == '0':
            messages.error(request, 'Please select class')
        elif semester == '0':
            messages.error(request, 'Please select Semester')
        elif scheme_input == '0':
            messages.error(request, 'Please select Scheme')
        elif tutor_id == '0':
            messages.error(request, 'Please select Tutor')
        else:
            data = batch.objects.filter(class_name=class_name, date_of_join=date_of_join, semester=semester,
                                        scheme=scheme_input_int, tutor_id=tutor)

            if data:
                messages.error(request, 'The class already exist')
            else:
                batch.objects.create(class_name=class_name, date_of_join=date_of_join, semester=semester,
                                     scheme=scheme_input_int, tutor_id=tutor)
                messages.error(request, 'Successfully added the class ' + class_name + ' year ' + date_of_join)

    return render(request, 'create_batch.html',
                  {"context": context, "scheme_data": scheme_data, "data_for_self_profile": staff_details_1, "tutor_data": tutor_data})


def view_batch(request):
    # name = request.session['name']
    staff_id = request.session['hod_username']
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    data = batch.objects.all()
    scheme_data = scheme.objects.all()
    tutor_data = profile.objects.all()
    return render(request, 'view_batch.html', {"batch_data": data, "scheme_data": scheme_data, "context": context,
                                               "data_for_self_profile": staff_details_1, "tutor_data": tutor_data})


def edit_batch(request, b_id):
    # name = request.session['name']
    staff_id = request.session['hod_username']
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}


    edit_data = batch.objects.get(id=b_id)
    join_date = str(edit_data.date_of_join)
    edit_scheme_id = edit_data.scheme
    scheme_data = scheme.objects.all()
    tutor_data = profile.objects.all()

    edit_scheme_data = scheme.objects.get(id=edit_scheme_id)
    student_data = profile_student.objects.filter(batch=b_id)

    subject_data = subject.objects.all()
    assign_subject_data = subject_to_staff.objects.filter(batch_id=b_id)
    
    if request.method == 'POST':
        # class_name = request.POST.get('class_name')
        # date_of_join = request.POST.get('date_of_join')
        semester = request.POST.get('semester')
        tutor = request.POST.get('tutor')
        # scheme_input = request.POST.get('scheme')

        ''' 
        if class_name == '0':
            messages.error(request, 'Please select class')
        elif semester == '0':
            messages.error(request, 'Please select semester')
        elif scheme_input == '0':
            messages.error(request, 'Please select Scheme')
        '''

        if semester == '0':
            messages.error(request, 'Please select semester')
        else:
            edit_data1 = batch.objects.get(id=b_id)
            edit_data1.semester = str(semester)
            edit_data1.tutor_id = int(tutor)
            # print(semester)
            edit_data1.save()
            messages.error(request, 'Successfully Updated')
            return redirect(hod.views.view_batch)
            '''
            sh_data = int(scheme_input)
            data = batch.objects.filter(class_name=class_name, date_of_join=date_of_join, semester=semester, scheme=sh_data)

            if data:

                messages.error(request, 'The class already exist')

            else:

                edit_data.class_name = class_name
                edit_data.date_of_join = date_of_join
                edit_data.semester = semester
                edit_data.scheme = sh_data
                edit_data.save()

                # update_student = profile_student.objects.filter(class_name=class_name1, year_of_join=year_only)
                messages.error(request, 'Successfully added the class ' + class_name + ' year ' + date_of_join)
                return redirect(hod.views.view_batch)
            '''

    return render(request, 'edit_batch.html',
                  {'edit_data': edit_data, 'context': context, 'scheme_data': scheme_data, 'date': join_date,
                   "data_for_self_profile": staff_details_1
                      , 'present_scheme': edit_scheme_data,
                      'tutor_data':tutor_data,
                      'student_data':student_data,
                      'subject_data': subject_data,
                      'assign_subject_data': assign_subject_data

                   })


def delete_batch(request, b_id):
    # Print(join_date, class_name1)

    batch_data = batch.objects.get(id=b_id)
    student_data = profile_student.objects.filter(batch=b_id)

    # print(student_data)
    # print(student_data == [])

    if not student_data:
        a = batch.objects.get(id=b_id)
        a.delete()
        messages.error(request, 'Successfully deleted')
        return redirect(view_batch)

    else:
        messages.error(request,
                       'Some students have the class '
                       + batch_data.class_name +
                       ' So can not delete without changing their class'
                       )
        return redirect(view_batch)


# Manage scheme

def create_scheme(request):
    # name = request.session['name']
    staff_id = request.session['hod_username']
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    if request.method == 'POST':
        scheme_input = request.POST.get('scheme')
        scheme_count = scheme.objects.filter(scheme=scheme_input)
        if scheme_count:
            messages.error(request,
                           'Already exist ' + scheme_input)

        else:
            scheme.objects.create(scheme=scheme_input)
            messages.error(request,
                           'Successfully created ' + scheme_input)

    return render(request, 'create_scheme.html', {'context': context, "data_for_self_profile": staff_details_1})


def view_scheme(request):
    # name = request.session['name']
    staff_id = request.session['hod_username']
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    scheme_data = scheme.objects.all()

    return render(request, 'view_scheme.html',
                  {'context': context, "scheme_data": scheme_data, "data_for_self_profile": staff_details_1})


# Manage Subject

def create_subject(request):
    # name = request.session['name']
    staff_id = request.session['hod_username']
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    scheme_data = scheme.objects.all()
    if 'create_subject' in request.POST:
        subject_code_input = request.POST.get('subject_code')
        subject_name_input = request.POST.get('subject_name')
        subject_credit = request.POST.get('subject_credit')
        scheme_id = request.POST.get('scheme')
        scheme_id_int = int(scheme_id)

        subject_code = subject_code_input.upper()
        subject_name = subject_name_input.upper()

        # check the subject already exist
        subject_exist = subject.objects.filter(code=subject_code, scheme=scheme_id_int).count()
        if subject_exist == 0:
            subject.objects.create(code=subject_code, subject_name=subject_name, credit=subject_credit,
                                   scheme=scheme_id_int)
            messages.error(request, "The Subject " + subject_name + " successfully added")

            return render(request, 'create_subject.html',
                          {'context': context, 'scheme_data': scheme_data, "data_for_self_profile": staff_details_1})

        else:
            messages.error(request, "The Subject code already exist!")
            return render(request, 'create_subject.html',
                          {'context': context, 'scheme_data': scheme_data, "data_for_self_profile": staff_details_1})

    return render(request, 'create_subject.html',
                  {'context': context, 'scheme_data': scheme_data, "data_for_self_profile": staff_details_1})


@csrf_exempt
def check_subject_exist(request):
    subject_code = request.POST.get('subject_code')
    scheme_id = request.POST.get('scheme_id')
    subject_exist = subject.objects.filter(code=subject_code, scheme=scheme_id).exists()
    if subject_exist:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def view_subject(request):
    # name = request.session['name']
    staff_id = request.session['hod_username']
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    scheme_data = scheme.objects.all()
    view_subject_all = subject.objects.all()
    assign_subject_data = subject_to_staff.objects.all()
    none = "None"
    staff_data = profile.objects.all()
    batch_data = batch.objects.all()
    
    if 'view_subject' in request.POST:
        scheme_id = request.POST.get('scheme_id')
        scheme_id_int = int(scheme_id)
        print(scheme_id_int)

        if scheme_id_int == 0:
            messages.error(request, "Please select scheme")
            return render(request, 'view_subject.html',
                          {'context': context, 'scheme_data': scheme_data, "data_for_self_profile": staff_details_1})

        else:

            scheme_details = scheme.objects.filter(id=scheme_id_int)

            # for subject and scheme details
            for i in scheme_details:
                scheme_name = i.scheme
                scheme_input_id = i.id

            view_subject = subject.objects.filter(scheme=scheme_id_int)
            return render(request, 'view_subject.html',
                          {'context': context, 'scheme_data': scheme_data, 'view_subject': view_subject,
                           'scheme_input_id': scheme_input_id,
                           'scheme_name': scheme_name, "data_for_self_profile": staff_details_1,
                           'assign_subject_data':assign_subject_data,
                           'none': none,
                           'staff_data': staff_data,
                           'batch_data': batch_data
                           })

    return render(request, 'view_subject.html',
                  {'context': context, 'scheme_data': scheme_data, "data_for_self_profile": staff_details_1,
                   "view_subject": view_subject_all, 
                   'assign_subject_data':assign_subject_data,
                   'none': none,
                   'staff_data': staff_data,
                   'batch_data': batch_data
                   })


def edit_subject(request, subject_id):
    # name = request.session['name']
    staff_id = request.session['hod_username']
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    scheme_data = scheme.objects.all()

    previous_subject_data = subject.objects.get(id=subject_id)
    previous_scheme_id = previous_subject_data.scheme
    previous_scheme_data = scheme.objects.get(id=previous_scheme_id)

    if 'edit_subject' in request.POST:
        subject_code = request.POST.get('subject_code')
        subject_name = request.POST.get('subject_name')
        subject_credit = request.POST.get('subject_credit')
        scheme_id = request.POST.get('scheme')
        scheme_id_int = int(scheme_id)

        # check the subject already exist
        subject_exist = subject.objects.filter(code=subject_code, scheme=scheme_id_int).count()

        if subject_exist == 0:
            update_subject = subject.objects.get(id=subject_id)
            update_subject.code = subject_code
            update_subject.subject_name = subject_name
            update_subject.credit = subject_credit
            update_subject.scheme = scheme_id_int
            update_subject.save()

            messages.error(request, "The Subject " + subject_name + " successfully Updated")

            return render(request, 'create_subject.html',
                          {'context': context, 'scheme_data': scheme_data, "data_for_self_profile": staff_details_1})

        else:
            messages.error(request, "The Subject code already exist!")
            return render(request, 'create_subject.html',
                          {'context': context, 'scheme_data': scheme_data, "data_for_self_profile": staff_details_1})

    return render(request, 'edit_subject.html',
                  {'context': context, 'scheme_data': scheme_data, 'previous_subject_data': previous_subject_data,
                   'previous_scheme_data': previous_scheme_data, "data_for_self_profile": staff_details_1
                   })


def assign_subject_to_staff(request):
    staff_id = request.session['hod_username']
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    batch_data_class = batch.objects.all()
    scheme_data = scheme.objects.all()
    subject_data = subject.objects.all()
    faculty = profile.objects.all()

    if request.method == 'POST':
        batch_id   = int(request.POST.get('batch_id'))
        subject_id = int(request.POST.get('subject_id'))
        faculty_id = int(request.POST.get('faculty_id'))
        sem = int(request.POST.get('semester'))

        batch_id_data = batch.objects.filter(id=batch_id)
        subject_id_data = subject.objects.filter(id=subject_id)
        valid_scheme = False

        for i in batch_id_data:
            for j in subject_id_data:
                if i.scheme == j.scheme:
                    valid_scheme = True
        
        if batch_id == 0:
            messages.error(request, "Select Class")
        elif subject_id == 0:
            messages.error(request, "Select Subject")
        elif valid_scheme == False:
            messages.error(request, "Select Subject with same scheme")
        elif sem == 0:
            messages.error(request, "Select Semester")
        elif faculty_id == 0:
            messages.error(request, "Select Faculty")
        else:

            check_exist = subject_to_staff.objects.filter(subject_id=subject_id, batch_id=batch_id)
            if check_exist:
                messages.error(request, "Subject Exist")
            else:
                subject_to_staff.objects.create(subject_id=subject_id, batch_id=batch_id, staff_id=faculty_id, semester=sem)
                messages.error(request, "Successfully added")
        
        

    return render(request, 'assign_subject_to_staff.html', {'context': context, "data_for_self_profile": staff_details_1,
                'batch_class': batch_data_class,
                'scheme_data': scheme_data,
                'subject_data': subject_data,
                'faculty': faculty
                })


def delete_subject(request, subject_id):
    subject_for_delete = subject.objects.get(id=subject_id)
    subject_for_delete.delete()

    return redirect(hod.views.view_subject)


# manage all batch data 

def batch_details(request, b_id):
    staff_id = request.session['hod_username']
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}
    return render(request, 'batch_details.html', {'context': context, "data_for_self_profile": staff_details_1})
# manage tutors

def view_tutor(request):
    staff_id = request.session['hod_username']
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}
    return render(request, 'view_tutor.html', {'context': context, "data_for_self_profile": staff_details_1})
# logout
def log_out(request):
    logout(request)

    return redirect(login.views.login)
