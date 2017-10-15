import requests
import pytest
import os
import json

host = os.getenv('HOST', 'localhost')
port = os.getenv('PORT', '5000')


@pytest.fixture
def get():
    def get_request(endpoint):
        url = "http://{0}:{1}/interview/api/v1.0/{2}".format(
            host, port, endpoint)
        response = requests.get(url)
        return response
    return get_request


status_tests = [
    ("results", 200),
    ("results?count=1", 200),
    ("results?count=99", 200),
    ("results?count=abc", 400),
    ("results?count=0", 200),
    ("resultsForArea/770", 200),
    ("resultsForArea/555", 404),
    ("resultsForArea/770?count=1", 200),
    ("resultsForArea/770?count=99", 200),
    ("resultsForArea/770?count=0", 200),
    ("asdfasldfasdlfk", 404)
]


@pytest.mark.parametrize("endpoint,status", status_tests)
def test_validate_status_code(get, endpoint, status):
    response = get(endpoint)
    assert response.status_code == status

def test_validate_json_types(get):
    response = get("results")
    reported_numbers = response.json()
    for number in reported_numbers:
        area_code = number['area_code']
        phone_number = number['phone_number']
        report_count = number['report_count']
        comment = number['comment']
        assert type(area_code) is unicode
        assert type(phone_number) is unicode
        assert type(report_count) is unicode
        assert type(comment) is unicode
