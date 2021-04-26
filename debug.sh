# to make executable:
# chmod +x debug.sh

export FLASK_APP=homeserver
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000