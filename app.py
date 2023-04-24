from flask import Flask

app = Flask(__name__)

@app.route("/test-route")
def test_route(): 
    return 'Route is working as expected'

if __name__ == '__main__':
    app.run()