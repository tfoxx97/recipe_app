import os
from recipe_app import app

cert_path = os.path.abspath("recipe_app/certificates/cert.pem")
key_path = os.path.abspath("recipe_app/certificates/key.pem")

if __name__ == '__main__':
    app.run(ssl_context=(cert_path, key_path), host='0.0.0.0', debug=True)