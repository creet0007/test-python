import pytest # Import pytest for writing and running tests
from app import app # Import the Flask app from the app module

# Create a mock response class to simulate HTTP responses
class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data # Store the JSON data to return
        self.status_code = status_code  # Store the HTTP status code

    def json(self):
        return self.json_data # Method to return the JSON data

# Define a pytest fixture to create a test client for the Flask app
@pytest.fixture
def client():
    with app.test_client() as client: # Create a test client for the app
        yield client # Provide the client to the test functions

# Test the homepage route
def test_homepage(client):
    response = client.get('/') # Make a GET request to the homepage
    assert response.status_code == 200 # Check that the response status code is 200 (OK)
    assert response.data == b'This app is used to get gists of any Github User, to get info about any user use /gists/username path in url' # Check that the response data matches the expected message

def test_get_user_gists_success(client, monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse([
        {"id": "123", "description": "First Test gist"},
        {"id": "456", "description": "Second Test gist"}
    ], 200) # Return multiple gists

    monkeypatch.setattr("requests.get", mock_get) # Replace requests.get with the mock function

    response = client.get('/gists/octocat') # Make a GET request to the gists endpoint
    assert response.status_code == 200 # Check that the response status code is 200 (OK)
    assert response.json == [  {"id": "123", "description": "First Test gist"},
        {"id": "456", "description": "Second Test gist"}
    ]  # Check that the JSON response matches the mock data

# Test getting user gists with a failure (user not found)
def test_get_user_gists_failure(client, monkeypatch):
    # Define a mock function to simulate a failed API call
    def mock_get(*args, **kwargs):
        return MockResponse([], 404) # Return a mock response with an empty list and status code 404

    monkeypatch.setattr("requests.get", mock_get) # Replace requests.get with the mock function

    response = client.get('/gists/invaliduser')  # Make a GET request to the gists endpoint with an invalid user
    assert response.status_code == 404 # Check that the response status code is 404 (Not Found)
    assert response.json == {"error": "please pass a existing user"} # Check that the JSON error message matches

# Test an invalid path
def test_invalid_path(client, monkeypatch): 
    response = client.get('/auth/')  # Make a GET request to an invalid path
    assert response.status_code == 404 # Check that the response status code is 404 (Not Found)
    assert response.json == None # Check that there is no JSON data returned for invalid paths

