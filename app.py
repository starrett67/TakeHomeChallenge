from flask import Flask, request, jsonify
from exception_handler import RestfulException
import data

app = Flask(__name__)
data = data.PhoneDataLayer()


@app.errorhandler(RestfulException)
def handle_restful_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def get_results(count=None, area_code=None):
    entries = data.get_entries(count, area_code)
    if len(entries) == 0:
        raise RestfulException('No results found', status_code=404)
    return u'[' + u', '.join(map(unicode, data.get_entries(count, area_code))) + u']'


@app.route('/interview/api/v1.0/results', methods=['GET'])
def results():
    count = request.args.get('count')
    area_code = request.args.get('area_code')
    if count is not None:
        try:
            count = int(count)
        except:
            raise RestfulException('Invalid count given', status_code=400)
    return get_results(count, area_code)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
