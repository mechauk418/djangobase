from django.urls import path, include
from .views import TaskViewSet, SubTaskViewSet

app_name = "todo"

urlpatterns = [
    path("task/", TaskViewSet.as_view({'get':'list', 'post':'create'}), name='task'),
    path("task/<int:pk>/", TaskViewSet.as_view({'get':'retrieve', "delete": "destroy", "put": "update", "patch": "partial_update"}), name='task_detail'),
    path("task/<int:Task_id>/subtask/", SubTaskViewSet.as_view({'get':'list', 'post':'create'}), name='subtask'),
    path("task/<int:Task_id>/subtask/<int:pk>/", SubTaskViewSet.as_view({"put": "update", "patch": "partial_update", "delete": "destroy", "get": 'retrieve'}),name='subtask_detail'),
]