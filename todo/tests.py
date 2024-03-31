from django.test import TestCase
from .models import *
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from django.urls import reverse
from rest_framework import status
from accounts.models import User

class TaskAPITestCase(APITestCase):

    def setUp(self):
        self.tester = User.objects.create(
            username="이진욱",
            password="1q2w3e4r!!",
            team="단비"
        )
        self.client = APIClient()
        self.client.login(username='이진욱', password='1q2w3e4r!!')
        self.client.force_authenticate(user=self.tester)


    # 업무 조회
    def test_get_task(self):

        uri = reverse('Todo:task')
        response = self.client.get(uri)
        self.assertEqual(response.status_code,200)

    # 업무 생성
    def test_post_task(self):

        uri = reverse('Todo:task')

        input_data = {
            "title":"title",
            "content":"content",
            "completed_date":"",
            "choice_subtask":["단비", "블라블라"],
        }

        response = self.client.post(uri,input_data)

        self.assertEqual(response.status_code,201)

    # 업무 수정
    def test_update_task(self):

        uri = reverse('Todo:task')
        input_data = {
            "title":"title",
            "content":"content",
            "completed_date":"",
            "choice_subtask":["단비", "블라블라"],
        }

        self.client.post(uri,input_data)
        task_id = Task.objects.first().id

        modified_data = {
            "title":"modified_title",
            "content":"modified_content",
            "completed_date":"",
            "choice_subtask":["단비", "블라블라"],
        }

        response = self.client.put(reverse("Todo:task_detail",  kwargs={'pk':task_id}),modified_data)

        self.assertEqual(response.status_code,200)

    # 업무(Task)의 모든 하위업무(SubTask)가 완료되면 해당 상위업무(Task)는 자동으로 완료처리가 되어야합니다 
    def test_action_complete_task(self):

        uri = reverse('Todo:task')
        input_data = {
            "title":"title",
            "content":"content",
            "completed_date":"",
            "choice_subtask":["단비", "블라블라"],
        }
        self.client.post(uri,input_data)

        task_id = Task.objects.first().id
        subtask_id = SubTask.objects.get(team="단비").id
        subtask_id2 = SubTask.objects.get(team="블라블라").id
        modified_data = {
            "team":"단비",
            "is_complete":True,
            "completed_date":"2023-11-14T23:05:00Z",
        }
        modified_data2 = {
            "team":"블라블라",
            "is_complete":True,
            "completed_date":"2023-11-14T23:05:00Z",
        }

        self.client.put(reverse("Todo:subtask_detail",  kwargs={'Task_id':task_id,'pk':subtask_id}),modified_data)
        self.client2.put(reverse("Todo:subtask_detail",  kwargs={'Task_id':task_id,'pk':subtask_id2}),modified_data2)

        self.assertEqual(Task.objects.first().is_complete,True)

    # 작성자 이외 다른 사람이 업무를 수정하려고 할 때
    def test_update_otheruser_task(self):

        uri = reverse('Todo:task')
        input_data = {
            "title":"title",
            "content":"content",
            "completed_date":"",
            "choice_subtask":["단비", "블라블라"],
        }

        self.client.post(uri,input_data)
        task_id = Task.objects.first().id

        modified_data = {
            "title":"modified_title",
            "content":"modified_content",
            "completed_date":"",
            "choice_subtask":["단비", "블라블라"],
        }

        response = self.client2.put(reverse("Todo:task_detail",  kwargs={'pk':task_id}),modified_data)

        self.assertEqual(response.data.get('detail'),'You do not have permission to perform this action.')




class SubTaskAPITestCase(APITestCase):

    def setUp(self):
        self.tester = USER.objects.create(
            username="이진욱",
            password="1q2w3e4r!!",
            team="단비"
        )
        self.client = APIClient()
        self.client.login(username='이진욱', password='1q2w3e4r!!')
        self.client.force_authenticate(user=self.tester)

        self.tester2 = USER.objects.create(
            username="김재후",
            password="1q2w3e4r!!",
            team="블라블라"
        )
        self.client2 = APIClient()
        self.client2.login(username='김재후', password='1q2w3e4r!!')
        self.client2.force_authenticate(user=self.tester2)

        uri = reverse('Todo:task')
        input_data = {
            "title":"title",
            "content":"content",
            "completed_date":"",
            "choice_subtask":["단비", "블라블라"],
        }

        self.client.post(uri,input_data)
        self.task_id = Task.objects.first().id

    # 하위업무 수정
    def test_update_subtask(self):

        subtask_id = SubTask.objects.get(team="단비").id
        modified_data = {
            "team":"블라블라",
            "completed_date":"2023-11-14T23:05:00Z",
        }

        response = self.client.put(reverse("Todo:subtask_detail",  kwargs={'Task_id':self.task_id,'pk':subtask_id}),modified_data)
        self.assertEqual(response.data.get('team'),"블라블라")

    # 다른 팀의 하위업무를 완료처리할 때
    def test_update_otherteam_subtask(self):

        subtask_id = SubTask.objects.get(team="블라블라").id
        modified_data = {
            "team":"블라블라",
            "is_complete":True,
            "completed_date":"2023-11-14T23:05:00Z",
        }

        response = self.client.put(reverse("Todo:subtask_detail",  kwargs={'Task_id':self.task_id,'pk':subtask_id}),modified_data)
        self.assertEqual(response.data.get('detail'),'소속이 달라 완료 처리할 수 없습니다.')

    # 완료된 하위 업무를 삭제하려고 할 때
    def test_delete_completed_subtask(self):

        subtask_id = SubTask.objects.get(team="단비").id
        modified_data = {
            "team":"단비",
            "is_complete":True,
            "completed_date":"2023-11-14T23:05:00Z",
        }

        self.client.put(reverse("Todo:subtask_detail",  kwargs={'Task_id':self.task_id,'pk':subtask_id}),modified_data)
        response = self.client.delete(reverse("Todo:subtask_detail",  kwargs={'Task_id':self.task_id,'pk':subtask_id}))
        self.assertEqual(response.data.get('detail'),'완료된 하위 업무는 삭제할 수 없습니다.')


    # 하위 업무에 정해진 7개의 팀 이외의 다른 팀
    def test_post_task_error_data(self):

        uri = reverse('Todo:task')

        error_data = {
            "title":"title",
            "content":"content",
            "completed_date":"",
            "choice_subtask":["잘못", "입력"],
        }

        response = self.client.post(uri,error_data)

        self.assertEqual(response.status_code,400)

