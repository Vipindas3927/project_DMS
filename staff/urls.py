from django.urls import path, include
from staff.views import staff_index, log_out, staff_profile, view_subjects

urlpatterns = [
    path('', staff_index, name='staff_index'),
    path('log_out/', log_out, name='log_out'),
    path('staff_profile/', staff_profile, name='staff_profile' ),
    path('view_subjects/', view_subjects, name='view_subjects' ),

]