from django.test import Client
from django.urls import reverse

from .test_users_and_quiz import BaseAPITest 

from qa.models import Question, Answer
from json import loads

class QAViewsTest(BaseAPITest):
    def setUp(self):
        self.user = self.setup_user("first_user" , 'test' , 'first_user@test.com')
        self.other_user = self.setup_user("second_user" , 'test2' , 'second_user@test.com')
        self.client = Client()
        self.other_client = Client()
        self.client.login(username="first_user", password="test")
        self.other_client.login(username="second_user", password="test2")
        self.question_one = Question.objects.create(
            user=self.user, title="This is a sample question",
            content="This is a sample question content",
            tags="test1, test2"
        )
        self.question_two = Question.objects.create(
            user=self.user,
            title="A Short Title",
            content="""This is a really good content, just if somebody
            published it, that would be awesome, but no, nobody wants to
            publish it, because they know this is just a test, and you
            know than nobody wants to publish a test, just a test;
            everybody always wants the real deal.""",
            has_answer=True,
            tags="test1, test2"
        )
        self.answer = Answer.objects.create(
            user=self.user,
            question=self.question_two,
            content="A reaaaaally loooong content",
            is_answer=True
        )

    def test_index_questions(self):
        response = self.client.get(reverse("api:index_all"))
        assert response.status_code == 200
        title = loads(response.content.decode())[0]['title']
        assert "A Short Title" in title

    def test_create_question_view(self):
        current_count = Question.objects.count()
        response = self.client.post(reverse("api:ask_question"),
                                    {
                                    "user" : self.user.pk ,
                                    "title": "Not much of a title",
                                    "content": "bablababla bablababla",
                                    "status": "O",
                                    "tags": "test, tag"})
        assert response.status_code == 201
        new_question = Question.objects.first()
        assert new_question.title == "Not much of a title"
        assert Question.objects.count() == current_count + 1

    def test_answered_questions(self):
        response = self.client.get(reverse("api:index_ans"))
        self.assertEqual(response.status_code, 200)
        title = loads(response.content.decode())[0]['title']
        self.assertTrue("A Short Title" in title)

    def test_unanswered_questions(self):
        response = self.client.get(reverse("api:index_noans"))
        assert response.status_code == 200
        title = loads(response.content.decode())[0]['title']
        assert "This is a sample question" in title

    def test_answer_question(self):
        current_answer_count = Answer.objects.count()
        response = self.client.post(
            reverse("api:propose_answer"),
            {
                'user' : self.user.pk ,
                'question' :  self.question_one.id ,
                "content": "A reaaaaally loooong content",
            }
        )
        assert response.status_code == 201
        assert Answer.objects.count() == current_answer_count + 1

    def test_question_upvote(self):
        url = reverse("api:question_vote")
        param = {"feedback_type": "U", "question": self.question_one.id}
        response_one = self.client.post( url , data = param ,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert response_one.status_code == 200

    def test_question_downvote(self):
        response_one = self.client.post(
            reverse("api:question_vote"),
            {"feedback_type": "D", "question": self.question_one.id},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert response_one.status_code == 200

    def test_answer_upvote(self):
        url =  reverse("api:answer_vote")
        response_one = self.client.post(
            url, {"feedback_type": "U", "answer": self.answer.id},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert response_one.status_code == 200

    def test_answer_downvote(self):
        response_one = self.client.post(
            reverse("api:answer_vote"),
            {"feedback_type": "D", "answer": self.answer.id},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert response_one.status_code == 200

    def test_accept_answer(self):
        url = reverse("api:accept_answer")
        params = {"answer": self.answer.id}

        response_one = self.client.post(url , params,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        
        assert response_one.status_code == 200
