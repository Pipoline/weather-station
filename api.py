import subprocess

from flask import Flask, jsonify, request
from prometheus_client import CollectorRegistry, Gauge, pushadd_to_gateway

app = Flask(__name__)
GATEWAY_ADDRESS = "pushgateway:9091"


@app.route('/api', methods=['POST'])
def home():
    registry = CollectorRegistry()
    Gauge('job_last_success_unixtime', 'Last time the weather job ran', registry=registry).set_to_current_time()
    
    sensor = request.form.get('sensor')
    print(sensor)
    if not sensor:
        sensor = 'test'

    temperature = request.form.get('temperature')
    print("temperature: {} *C".format(temperature))
    gtemerature = Gauge('temperature', '', registry=registry, labelnames=['sensor'])
    gtemerature.labels(sensor).set(temperature)

    humidity = request.form.get('humidity')
    print("humidity: {} %".format(humidity))
    ghumidity = Gauge('humidity', '', registry=registry, labelnames=['sensor'])
    ghumidity.labels(sensor).set(humidity)

    heat_index = request.form.get('heat_index')
    print("heat_index: {} *C".format(heat_index))
    gheat_index = Gauge('heat_index', '', registry=registry, labelnames=['sensor'])
    gheat_index.labels(sensor).set(heat_index)
    pushadd_to_gateway(GATEWAY_ADDRESS, job='weather', registry=registry, grouping_key={'sensor': sensor})
    
    pressure = request.form.get('pressure')
    if pressure:
        print("pressure: {} hPa".format(pressure))
        gpressure = Gauge('pressure', '', registry=registry, labelnames=['sensor'])
        gpressure.labels(sensor).set(pressure)

    altitude = request.form.get('altitude')
    if altitude:
        print("altitude: {} m".format(altitude))
        galtitude = Gauge('altitude', '', registry=registry, labelnames=['sensor'])
        galtitude.labels(sensor).set(altitude)
    print("\n\n")
    pushadd_to_gateway(GATEWAY_ADDRESS, job='weather', registry=registry, grouping_key={'sensor': sensor})
    return 'OK'


@app.route('/api/cron', methods=['GET'])
def cron():
    return 'CRON'


@app.route('/api/create_ssl/<string:domain>', methods=['POST'])
def create_ssl(domain):
    try:
        output = subprocess.check_output(["/root/ssl-registrator.sh", domain])
    except subprocess.CalledProcessError as ex:
        return jsonify({'status': 0, 'msg': ex.output})

    return jsonify({'status': 1, 'msg': output})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
