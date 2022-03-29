from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from app.models import Workflow


WORKFLOW_ADD_URL = reverse("workspace-list")


def create_user(data):
    return get_user_model().objects.create_user(**data)


class WorkflowTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user(data={
            "username": "testuser",
            "email": "test@gmail.com",
            "password": "testuser@123"
        })
        self.client.force_authenticate(self.user)

    def test_workflow_create_successfully(self):
        """
        Test to check the workflow create api
        endpoint.
        """
        payload = {
            "name": "workflow1",
            "description": "short fake description",
            "type": Workflow.TypeChoices.PROJECT
        }
        res = self.client.post(WORKFLOW_ADD_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
