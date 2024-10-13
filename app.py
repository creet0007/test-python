from flask import Flask, jsonify  # Import Flask and jsonify to create web routes and send JSON responses
import requests # Import requests to make HTTP requests

# Create a new Flask app
app = Flask(__name__)

# Set up the homepage routes that show a welcome message
@app.route('/')
@app.route('/home')
@app.route('/home/')
def homepage():
        # Return a message explaining how to use the app and a status code of 200
    return 'This app is used to get gists of any Github User, to get info about any user use /gists/username path in url', 200

# Set up a route to get gists for a specific GitHub username
@app.route('/gists/<username>')
def get_user_gists(username):    # Return a message explaining how to use the app and a status code of 200
    # Create the URL for the GitHub API using the provided username
      url = f'https://api.github.com/users/{username}/gists'
      try:
        # Make a GET request to the GitHub API
        response = requests.get(url)
        print(response.status_code) # Print the status code for debugging
                # If the request was successful, return the gists as JSON
        if response.status_code == 200:
           gists = response.json() # Convert the response to JSON
           return jsonify(gists) # Send back the gists as a JSON 
        else:
            # If the user doesn't exist, return an error message with status code 404
            return jsonify({"error": "please pass a existing user"}), 404
      except Exception as e:
         # If something goes wrong, return an error message with status code 500
        return jsonify({"error": "Internal Server error"}), 500
      #gists = response.json()
      #return jsonify(gists)

# Uncomment this section if you want to handle invalid paths with a custom message

#@app.route('/<path:invalid_path>')
#def handle_invalid_path(invalid_path):

#    return 'Invalid path. Please use /gists/username path in URL.', 404

if __name__ == '__main__':
    app.run(debug=True,  host='0.0.0.0', port=8080)
