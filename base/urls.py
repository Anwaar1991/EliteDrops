from django.urls import path, include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin
from .views import *

urlpatterns = [
    # Home page + User Registration
    path('', views.home, name='home'), 
    path('register/', views.register, name='register'), 
    path('register_business/', views.register_business, name='register_business'), 
    path('signin/', views.signin, name='signin'),
    path('contactus/', views.contactus, name='contactus'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('hireus/', views.hireus, name='hireus'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('faqs/', views.faqs, name='faqs'),
    path('guide/', views.guide, name='guide'),
    path('no_link/', views.no_link, name='no_link'),
    path('image-conversion/', views.image_conversion, name='image-conversion'),



    # Reset Password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_email_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_select_new.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'), name='password_reset_complete'),


    path('dashboard/', views.dashboard, name='dashboard'), 
    path('product_details/<int:id>', views.prodcut_details, name='product_details'),
    path('pay-now/<int:id>', views.pay_now, name='pay-now'),
    path('pay-now-business/<int:id>', views.pay_now_business, name='pay-now-business'),
    path('signout/', views.signout, name='signout'), 
    path('success/<int:id>', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('past_two_weeks_products/', views.past_two_weeks_products, name='past_two_weeks_products'),
    path('past_three_weeks_products/', views.past_three_weeks_products, name='past_three_weeks_products'),
    path('past_four_weeks_products/', views.past_four_weeks_products, name='past_four_weeks_products'),

    # ADMIN PANEL URLS
    path('add_products/', views.add_products, name='add_products'),
    path('all_products/', views.all_products, name='all_products'),
    path('edit_products/<int:id>', views.edit_products, name='edit_products'),
    path('confirm_delete/<int:id>', views.confirm_delete, name='confirm_delete'),
    path('redistered_users/', views.redistered_users, name='redistered_users'),
    path('subscribers/', views.subscribers, name='subscribers'),
    path('old_subscribers/', views.old_subscribers, name='old_subscribers'),

    # TOOLS
    
    path('privacy_policy_generator/', views.privacy_policy_generator, name='privacy_policy_generator'),
    path('refund_policy_generator/', views.refund_policy_generator, name='refund_policy_generator'),
    path('return_policy_generator/', views.return_policy_generator, name='return_policy_generator'),
    path('shipping_policy_generator/', views.shipping_policy_generator, name='shipping_policy_generator'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
