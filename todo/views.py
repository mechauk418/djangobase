from django.shortcuts import render
from django.db.models import Q
from .models import *
from accounts.models import User
from .serializers import *
from .permissions import *
from rest_framework import exceptions
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
import requests


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # 업무(Task)는 작성자 이외에 수정이 불가합니다.
    permission_classes = [IsOwnerOrReadOnly]
    
    def list(self, request, *args, **kwargs):
        try:
            inner_qs = SubTask.objects.filter(team=self.request.user.team)
            queryset = Task.objects.filter(Q(id__in = inner_qs)|Q(team=self.request.user.team))
        except:
            raise exceptions.PermissionDenied("권한이 없습니다. 로그인 해주세요.")
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        
        serializer.save(
            create_user=self.request.user,
        )

class SubTaskViewSet(ModelViewSet):

    queryset=SubTask.objects.all()
    serializer_class=SubTaskSerializer
    
    def get_queryset(self):
        return super().get_queryset().filter(task=self.kwargs.get("Task_id"))

    def perform_create(self, serializer):
        serializer.save(
            task = Task.objects.get(id=self.kwargs.get('Task_id')),
        )
    
    def destroy(self, request, *args, **kwargs):
        
        complete_check = self.get_object()
        if complete_check.is_complete:
            raise exceptions.PermissionDenied("완료된 하위 업무는 삭제할 수 없습니다.")
        
        else:
            return super().destroy(request, *args, **kwargs)
        
    def perform_update(self, serializer):

        subpk = self.kwargs.get('pk')
        task = Task.objects.get(id=self.kwargs.get('Task_id'))

        # 하위업무(SubTask) 완료 처리는 소속된 팀만 처리 가능합니다.
        if self.request.data['team'] != self.request.user.team:
            if 'is_complete' in self.request.data:
                raise exceptions.PermissionDenied("소속이 달라 완료 처리할 수 없습니다.")
        
        # 업무(Task)의 모든 하위업무(SubTask)가 완료되면 해당 상위업무(Task)는 자동으로 완료처리가 되어야합니다.
        try:
            checkdata = self.request.data['is_complete']
        except:
            checkdata = False
        remain = task.subtasks.exclude(id=subpk)
        alltruecheck = True
        for r in remain:
            if not r.is_complete:
                alltruecheck = False

        if checkdata and alltruecheck:
            task.is_complete = True
            task.save()
        else:
            task.is_complete = False
            task.save()
        
        return super().perform_update(serializer)
    