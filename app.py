import logging
from flask import Flask, jsonify
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Key Vault configurations
VAULT_URL = "https://mykeyvaultv1.vault.azure.net/"  # Replace with your Key Vault's URL
logging.info("Initializing Key Vault Client")
credential = DefaultAzureCredential()
client = SecretClient(vault_url=VAULT_URL, credential=credential)

@app.route('/secret')
def get_secret():
    try:
        logging.info("Attempting to retrieve secret: WelcomeMessage")
        secret = client.get_secret("WelcomeMessage")  # Secret name should be within double quotes
        logging.info("Successfully retrieved secret")
        return jsonify(message=secret.value)
    except ResourceNotFoundError:
        logging.error("Secret not found: WelcomeMessage")
        return jsonify(error="Secret not found"), 404
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify(error=str(e)), 500

@app.route('/power/<int:x>/<int:y>')
def power(x, y):
    result = x ** y
    logging.info(f"Calculated power: {x}^{y} = {result}")
    return jsonify(result=result)

@app.route('/health_v2')
def health_check():
    logging.info("Health check accessed")
    return jsonify(status='ok')

if __name__ == "__main__":
    logging.info("Starting Flask application")
    app.run(host='127.0.0.1', port=5000, debug=True)
