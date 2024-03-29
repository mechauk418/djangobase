from rest_framework import serializers, fields
from .models import *
from rest_framework.serializers import ModelSerializer
from rest_framework import exceptions
from accounts.models import User

class SubTaskSerializer(serializers.ModelSerializer):

    task = serializers.ReadOnlyField(source="task.title")
    
    class Meta:
        model = SubTask
        fields = [
            'id',
            'team',
            'is_complete',
            'compleated_date',
            'task'
        ]


team_list = (
        ('단비','단비'),
        ('다래','다래'),
        ('블라블라','블라블라'),
        ('철로','철로'),
        ('땅이','땅이'),
        ('해태','해태'),
        ('수피','수피'),
    )

class TaskSerializer(serializers.ModelSerializer):
    subtask_list = serializers.SerializerMethodField()
    choice_subtask = serializers.MultipleChoiceField(choices = team_list, write_only=True)
    
    def get_subtask_list(self,obj):
        sub = obj.subtasks.all()
        return SubTaskSerializer(instance=sub, many=True, context = self.context).data

    class Meta:
        model = Task
        fields = [
            'id',
            'create_user',
            'team',
            'title',
            'content',
            'is_complete',
            'completed_date',
            'subtask_list',
            'choice_subtask',
        ]
        read_only_fields = ['is_complete','team','create_user']
        

    def create(self, validated_data):
        print(validated_data)
        validated_data['team'] = validated_data['create_user'].team
        ch_list = self.context['request'].data.getlist('choice_subtask')

        # 업무 생성 시, 한 개 이상의 팀을 설정해야합니다.
        if not ch_list:
            raise exceptions.ValidationError('한 개 이상의 팀을 설정해주세요.')
        instance = Task.objects.create(**validated_data)
        
        for team in ch_list:
            
            SubTask.objects.create(team=team, task =instance)

        return instance