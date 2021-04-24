# rpi-server2

## IoT Architecture
Python + Flask + SQLite + Bokeh plots
![Homeserver IoT updated](https://user-images.githubusercontent.com/11139566/115975632-56518e80-a534-11eb-88a2-ded63e1244db.png)

## Shower temperature plot
![shower2](https://user-images.githubusercontent.com/11139566/115975003-1e941800-a52f-11eb-9693-f396d3428f5a.png)

## Todos
Deploy to production
Dark mode
Derivatives and current average temperature
Add start/stop record
Save shower session? 

## Helpful Things
### Test POST in Linux
curl -X POST -F 'temperature=50' localhost:5000/shower

### Debug server commands
export FLASK_APP=homeserver
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
