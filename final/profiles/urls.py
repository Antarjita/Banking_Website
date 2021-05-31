from django.conf.urls import url
from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    #path(r"account_status", views.show_account_status, name = "account_status"),
    #url(r"^login/$", views.sign_in, name = "signin"),
    #url(r"^logout/$", views.logout_view, name = "logout"),
    #url(r"^test/$", views.test_classes, name = "test_class"),
    path(r"dashboard", views.display_menu, name = "dashboard"),
    path(r"redirect_from_dashboard", views.get_function_chosen, name = "get_function_chosen"),
    path(r"account_management", views.account_management, name='account_management'),
    path(r"process_account_action", views.get_account_action, name='get_account_action'),
    path(r"withdraw", views.withdraw, name='withdraw'),
    path(r"deposit", views.deposit, name='deposit'),
    path(r"stat_gen", views.stat_gen, name='stat_gen'),
    path(r"get_stat_gen", views.get_transaction_action, name='get_transaction_action'),
    path(r"show_ecs_options", views.show_ecs_options, name='show_ecs_options'),
    path(r"redirect_ecs", views.redirect_ecs, name='redirect_ecs'),
    path(r"start_ecs", views.start_ecs, name='start_ecs'),
    path(r"store_new_ecs_data", views.store_new_ecs_data, name='store_new_ecs_data'),
    path(r"show_due_bills", views.show_due_bills, name='show_due_bills'),
    path(r"pay_bill", views.pay_bill, name='pay_bill'),
]

