import pytest
from app import app, client
from unittest.mock import patch, MagicMock
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_generate_story_no_input(client):
    response = client.post('/generate_story', json={})
    assert response.status_code == 400
    assert 'error' in json.loads(response.data)

@patch('app.client')
def test_generate_story_success(mock_groq, client):
    test_word = "adventure"
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Once upon a time..."
    mock_groq.chat.completions.create.return_value = mock_response

    response = client.post('/generate_story', json={'word': test_word})
    
    assert response.status_code == 200
    assert 'result' in json.loads(response.data)
    
    call_args = mock_groq.chat.completions.create.call_args[1]
    assert call_args['model'] == "llama3-8b-8192"
    assert f"Write a creative short story (100-150 words) based on this word: {test_word}" in call_args['messages'][0]['content']

def test_generate_poem_no_input(client):
    response = client.post('/generate_poem', json={})
    assert response.status_code == 400
    assert 'error' in json.loads(response.data)

@patch('app.client')
def test_generate_poem_success(mock_groq, client):
    test_topic = "nature"
    test_style = "haiku"
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Gentle breeze whispers..."
    mock_groq.chat.completions.create.return_value = mock_response

    response = client.post('/generate_poem', json={'topic': test_topic, 'style': test_style})
    
    assert response.status_code == 200
    assert 'result' in json.loads(response.data)
    
    call_args = mock_groq.chat.completions.create.call_args[1]
    assert call_args['model'] == "llama3-8b-8192"
    assert f"Write a {test_style} poem about {test_topic}" in call_args['messages'][0]['content']

def test_generate_joke_no_input(client):
    response = client.post('/generate_joke', json={})
    assert response.status_code == 200
    assert 'result' in json.loads(response.data)

@patch('app.client')
def test_generate_joke_success(mock_groq, client):
    test_topic = "programmers"
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Why do programmers prefer dark mode? Because light attracts bugs!"
    mock_groq.chat.completions.create.return_value = mock_response

    response = client.post('/generate_joke', json={'topic': test_topic})
    
    assert response.status_code == 200
    assert 'result' in json.loads(response.data)
    
    call_args = mock_groq.chat.completions.create.call_args[1]
    assert call_args['model'] == "llama3-8b-8192"
    assert f"Tell me a funny, clean joke about {test_topic}" in call_args['messages'][0]['content']

@patch('app.client')
def test_generate_joke_default_topic(mock_groq, client):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Here's a general joke!"
    mock_groq.chat.completions.create.return_value = mock_response

    response = client.post('/generate_joke', json={})
    
    assert response.status_code == 200
    assert 'result' in json.loads(response.data)
    
    call_args = mock_groq.chat.completions.create.call_args[1]
    assert call_args['model'] == "llama3-8b-8192"
    assert "Tell me a funny, clean joke about general" in call_args['messages'][0]['content']