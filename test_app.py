import os
import pytest
from unittest.mock import patch, MagicMock
from app import app as flask_app

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def mock_groq():
    """Mock the Groq client for testing."""
    with patch('app.client') as mock_client:
        # Create a mock for chat.completions.create
        mock_completion = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        
        # Set up the mock return values
        mock_message.content = "Mocked response"
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        
        # Set up the chat.completions.create method
        mock_client.chat.completions.create.return_value = mock_completion
        
        yield mock_client

def test_home_route(client):
    """Test the home route returns 200 status code."""
    response = client.get('/')
    assert response.status_code == 200

def test_generate_story_missing_word(client):
    """Test story generation with missing word parameter."""
    response = client.post('/generate_story', json={})
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_generate_story_success(client, mock_groq):
    """Test successful story generation."""
    test_word = "adventure"
    response = client.post(
        '/generate_story',
        json={'word': test_word},
        content_type='application/json'
    )
    
    assert response.status_code == 200
    assert 'result' in response.get_json()
    
    # Verify the Groq client was called with expected arguments
    mock_groq.chat.completions.create.assert_called_once()
    call_args = mock_groq.chat.completions.create.call_args[1]
    assert call_args['model'] == "llama3-8b-8192"
    assert call_args['messages'][0]['content'] == f"Write a creative short story (100-150 words) based on this word: {test_word}"

def test_generate_poem_missing_topic(client):
    """Test poem generation with missing topic."""
    response = client.post('/generate_poem', json={})
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_generate_poem_success(client, mock_groq):
    """Test successful poem generation."""
    test_topic = "nature"
    test_style = "haiku"
    response = client.post(
        '/generate_poem',
        json={'topic': test_topic, 'style': test_style},
        content_type='application/json'
    )
    
    assert response.status_code == 200
    assert 'result' in response.get_json()
    
    # Verify the Groq client was called with expected arguments
    mock_groq.chat.completions.create.assert_called_once()
    call_args = mock_groq.chat.completions.create.call_args[1]
    assert call_args['model'] == "llama3-8b-8192"
    assert f"Write a {test_style} poem about {test_topic}" in call_args['messages'][0]['content']

def test_generate_joke_success(client, mock_groq):
    """Test successful joke generation."""
    test_topic = "programmers"
    response = client.post(
        '/generate_joke',
        json={'topic': test_topic},
        content_type='application/json'
    )
    
    assert response.status_code == 200
    assert 'result' in response.get_json()
    
    # Verify the Groq client was called with expected arguments
    mock_groq.chat.completions.create.assert_called_once()
    call_args = mock_groq.chat.completions.create.call_args[1]
    assert call_args['model'] == "llama3-8b-8192"
    assert f"Tell me a funny, clean joke about {test_topic}" in call_args['messages'][0]['content']

def test_generate_joke_default_topic(client, mock_groq):
    """Test joke generation with default topic."""
    response = client.post(
        '/generate_joke',
        json={},
        content_type='application/json'
    )
    
    assert response.status_code == 200
    assert 'result' in response.get_json()
    
    # Verify the Groq client was called with expected arguments
    mock_groq.chat.completions.create.assert_called_once()
    call_args = mock_groq.chat.completions.create.call_args[1]
    assert call_args['model'] == "llama3-8b-8192"
    assert "Tell me a funny, clean joke about general" in call_args['messages'][0]['content']