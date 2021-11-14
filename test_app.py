import pytest 
from app import app


@pytest.fixture
def client():
    return app.test_client()


def test_activities_json_with_proper_mimetype(client):
    response = client.get('/api/activities')
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_activities_returns_two_activities(client):
    response = client.get('/api/activities')
    activities_dict = response.get_json()
    assert len(activities_dict) == 2


def test_activities_returns_id(client):
    response = client.get('/api/activities/1')
    activities_dict = response.get_json()
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_new_activities_returns_id(client):
    doing_stuff = {"user_id": 3, "username": "Derek", "details": "Doing stuff related to this assignment"}
    response = client.post('/api/activities', json=doing_stuff)
    activities_response = response.get_json()
    assert isinstance(activities_response['user_id'], int)
    assert response.status_code == 201


def test_bad_id_will_return_404(client):
    response = client.get('/api/activities/5')
    assert response.status_code == 404



