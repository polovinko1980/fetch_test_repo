"""
Test module to run sanity tests
to make sure basic functionality is working:

Input is a basic sanity example from spec,
basic validation and non-functional attributes like

running time, stderr and response code

"""
from geolocator import GeoLocatorProcessor


def test_smoke(my_executor):

    input_str = '"Madison, WI" "12345" "Chicago, IL" "10001"'

    expected_results = {
        "Madison, WI": "latitude=43.074761,longitude=-89.3837613,place name=Madison,country=US",
        "12345": "latitude=42.8142,longitude=-73.9396,place name=Schenectady,country=US",
        "Chicago, IL": "latitude=41.8755616,longitude=-87.6244212,place name=Chicago,country=US",
        "10001": "latitude=40.7484,longitude=-73.9967,place name=New York,country=US",
    }

    response = my_executor.execute(
        input_str=input_str
    )

    assert response.get("response_code") == 0

    assert response.get("errors") == ""

    assert response.get("running_time") < 5

    # skipping first 3 lines, they have metadata only
    results = response.get("output").split("\n")[3:]

    for result in results:
        location, geo_code = result.split(GeoLocatorProcessor.LOCATION_CODE_SEPARATOR)

        assert expected_results[location] == geo_code


def test_invalid_zip(my_executor):

    input_str = '"1000"'

    expected_results = {
        "1000": "unable to get geo code. Exception: Invalid location: 1000",
    }

    response = my_executor.execute(
        input_str=input_str
    )

    # skipping first 3 lines, they have metadata only
    results = response.get("output").split("\n")[3:]

    for result in results:
        location, geo_code = result.split(GeoLocatorProcessor.LOCATION_CODE_SEPARATOR)
        assert expected_results[location] == geo_code


def test_invalid_location(my_executor):

    input_str = '"Three, Words, Invalid"'

    expected_results = {
        "Three, Words, Invalid": "unable to get geo code. Exception: Invalid location: Three, Words, Invalid",
    }

    response = my_executor.execute(
        input_str=input_str
    )

    # skipping first 3 lines, they have metadata only
    results = response.get("output").split("\n")[3:]

    for result in results:
        location, geo_code = result.split(GeoLocatorProcessor.LOCATION_CODE_SEPARATOR)
        assert expected_results[location] == geo_code


def test_unknown_zip(my_executor):

    input_str = '"99999"'

    expected_results = {
        "99999": (
            "unable to get geo code. Exception: 404 Client Error: Not Found for url: "
            "http://api.openweathermap.org/geo/1.0/zip?zip=99999,US&appid=f897a99d971b5eef57be6fafa0d83239"
        ),
    }

    response = my_executor.execute(
        input_str=input_str
    )

    # skipping first 3 lines, they have metadata only
    results = response.get("output").split("\n")[3:]

    for result in results:
        location, geo_code = result.split(GeoLocatorProcessor.LOCATION_CODE_SEPARATOR)
        assert expected_results[location] == geo_code
