from flask import Flask, request, jsonify
from exception_handler import RestfulException
from traceback import print_exc
import data

app = Flask(__name__)
data = data.PhoneDataLayer()


@app.errorhandler(RestfulException)
def handle_restful_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def get_results(n=None):
    return u'[' + u', '.join(map(unicode, data.get_entries(n))) + u']'


def get_results_by_area(area_code, n=None):
    d = filter(lambda entry: entry.area_code ==
               area_code, data.get_all_entries())
    if len(d) == 0:
        raise RestfulException('No results found', status_code=404)
    else:
        try:
            return u'[' + u', '.join(map(unicode, d[:n])) + u']'
        except Exception, e:
            if (len(d) < n):
                return u'[' + u', '.join(map(unicode, d)) + u']'
            else:
                raise RestfulException('Invalid count given', status_code=400)


@app.route('/interview/api/v1.0/results', methods=['GET'])
def results():
    count = request.args.get('count')
    return get_results(count)


@app.route('/interview/api/v1.0/resultsForArea/<string:area_code>', methods=['GET'])
def results_by_area_with_limit(area_code):
    count = request.args.get('count')
    return get_results_by_area(area_code, count)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
