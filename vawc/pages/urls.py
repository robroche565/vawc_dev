from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login-with-otp/', views.login_with_otp, name='login_with_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('logout/', views.logout_view, name='logout'),

    #anonymouse side
    path('report_violence/', views.report_violence_view, name='report violence'),
    path('impact-victim-survivor/', views.impact_victim_view, name='impact victim'),
    path('behalf-victim-survivor/', views.behalf_victim_view, name='behalf impact victim'),
    path('add-case/', views.add_case, name='add_case'),

    #super admin side
    path('admin-vawc/dashboard/', views.admin_dashboard_view, name='admin dashboard'),
    path('admin-vawc/graph-report/', views.admin_graph_view, name='admin graph'),

    #barangay admin side
    path('admin-barangay-vawc/dashboard/', views.barangay_dashboard_view, name='barangay dashboard'),
    path('admin-barangay-vawc/settings/', views.barangay_settings_view, name='barangay settings'),

    path('admin-barangay-vawc/case/', views.barangay_case_view, name='barangay case'),
    path('admin-barangay-vawc/view-case/<int:case_id>/', views.view_case, name='barangay case view'),
    
    path('update_status/', views.update_status, name='update_status'),
    path('update_status_case/', views.update_status_case, name='update_status_case'),

    path('save_victim_data/<int:victim_id>/', views.save_victim_data, name='save_victim_data'),
    path('save_perpetrator_data/<int:perpetrator_id>/', views.save_perpetrator_data, name='save_perpetrator_data'),

    path('add_parent/<int:case_id>/<int:victim_id>/', views.add_parent_view, name='add_parent'),


]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)