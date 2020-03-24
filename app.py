from flask_cors import CORS
from flask_restful import Api
from controller import create_app
import os

app = create_app()
app.config['SECRET_KEY'] = 'IsBLK8lCfYOF7VHNflxkSg'
api = Api(app)
port = int(os.environ.get('PORT', 5000))
CORS(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
