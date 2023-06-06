from django.urls import path
from . import views
app_name = 'main'

urlpatterns = [
    path('procedure/category', views.ProcedureCategoryView.as_view(),
     name='procedure_category'),
    path('procedure/list/<int:category>', views.ProcedureListView.as_view(),
     name='procedure_list'),
    path('procedure/detail/<int:pk>', views.ProcedureDetailView.as_view(),
     name='procedure_detail'),
    path('procedure/schedule/list/<int:pk>', views.ScheduleView.as_view(),
     name='schedule_list'),
    path('procedure/my/schedule/list', views.MyScheduleView.as_view(),
     name='my_schedule'),
    path('procedure/record/save/', views.RecordSaveView.as_view(),
     name='record_save'),
    path('procedure/record/cancel/<pk>', views.RecordCancelView.as_view(),
         name='record_cancel'),
    path('favorite/', views.AddRemoveFavoriteProcedure.as_view(),name='favorite'),
    path('category/filter/', views.ProcedureCategoryFilterView.as_view(),name='category_filter'),
    path('substruction/', views.SubstructionView.as_view(),name='substruction'),
    path('profile/', views.ProfileView.as_view(),name='profile'),
    path('register/', views.RegistrationView.as_view(),name='register'),
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),

]