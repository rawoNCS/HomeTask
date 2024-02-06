import pytest
import requests
import logging
from requests.exceptions import ConnectionError

LOGGER = logging.getLogger(__name__)


def is_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


@pytest.fixture(scope="session")
def http_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""
    port = docker_services.port_for("app", 5000)
    url = "http://{}:{}".format(docker_ip, port)
    LOGGER.info("Running tests on {}".format(url))
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url


def test_restore_empty(http_service):
    """
    Given: Service is responsive
    When: "/restore" is asked before "/reverse"
    Then: Status 200 is received with empty item in JSON result
    """
    status = 200
    result = ''
    response = requests.get(http_service + '/restore')
    LOGGER.info("Response:{}".format(response.text))

    assert response.status_code == status
    if response.status_code == status:
        assert response.json() == {'result': result}


def test_reverse(http_service):
    """
    Given: Service is responsive
    When: "/reverse" is asked properly
    Then: Status 200 is received with reversed input string in JSON result
    """
    sentence = "The quick brown fox jumps over the lazy dog"
    result = 'dog lazy the over jumps fox brown quick The'
    status = 200

    response = requests.get(http_service + '/reverse', {'in': '{}'.format(sentence)})
    LOGGER.info("Response:{}".format(response.text))

    assert response.status_code == status
    if response.status_code == status:
        assert response.json() == {'result': result}


def test_restore(http_service):
    """
    Given: Service is responsive
    When: "/restore" is requested
    Then: Status 200 is received with last output in JSON result
    """
    status = 200
    result = 'dog lazy the over jumps fox brown quick The'
    response = requests.get(http_service + '/restore')
    LOGGER.info("Response:{}".format(response.text))

    assert response.status_code == status
    if response.status_code == status:
        assert response.json() == {'result': result}


def test_reverse_multiple_reverse(http_service):
    """
    Given: Service is responsive
    When: "/reverse" is asked properly two times and "/restore" is requested afterward
    Then: Status 200 is received with reversed input string in JSON result after each "/reverse" request
    Finally: Status 200 is received with last output in JSON result
    """
    sentence1 = "Lorem ipsum dolor sit amet"
    sentence2 = "The quick brown fox jumps over the lazy dog"
    result1 = 'amet sit dolor ipsum Lorem'
    result2 = 'dog lazy the over jumps fox brown quick The'
    status = 200

    response = requests.get(http_service + '/reverse', {'in': '{}'.format(sentence1)})
    LOGGER.info("Response:{}".format(response.text))

    assert response.status_code == status
    if response.status_code == status:
        assert response.json() == {'result': result1}

    response = requests.get(http_service + '/reverse', {'in': '{}'.format(sentence2)})
    LOGGER.info("Response:{}".format(response.text))

    assert response.status_code == status
    if response.status_code == status:
        assert response.json() == {'result': result2}

    response = requests.get(http_service + '/restore')
    LOGGER.info("Response:{}".format(response.text))

    assert response.status_code == status
    if response.status_code == status:
        assert response.json() == {'result': result2}


def test_multiple_restore(http_service):
    """
    Given: Service is responsive
    When: "/restore" is requested 5 times
    Then: Status 200 is received with last output in JSON result
    """
    status = 200
    result = 'dog lazy the over jumps fox brown quick The'
    for i in range(5):
        response = requests.get(http_service + '/restore')
        LOGGER.info("Response:{}".format(response.text))

        assert response.status_code == status
        if response.status_code == status:
            assert response.json() == {'result': result}


def test_reverse_int(http_service):
    """
    Given: Service is responsive
    When: "/reverse" is asked with a number
    Then: Status 200 is received with input number string in JSON result
    """
    sentence = 123
    result = '123'
    status = 200

    response = requests.get(http_service + '/reverse', {'in': '{}'.format(sentence)})
    LOGGER.info("Response:{}".format(response.text))

    assert response.status_code == status
    if response.status_code == status:
        assert response.json() == {'result': result}


def test_reverse_wrong_querry(http_service):
    """
    Given: Service is responsive
    When: "/reverse" is asked with a "data" query
    Then: Status 400 is received
    """
    sentence = "The quick brown fox jumps over the lazy dog"
    status = 400

    response = requests.get(http_service + '/reverse', {'data': '{}'.format(sentence)})
    LOGGER.info("Response:{}".format(response.text))
    # This test will fail to check logging and reporting
    assert response.status_code == status
