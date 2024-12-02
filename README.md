

# Alex Polovinko test runner

Validated test runner on the MacOS Sonoma Apple M3.

### Using local runtime

```
git clone https://github.com/polovinko1980/fetch_test_repo.git
cd fetch_test_repo

pip3 install -r requirements.txt

```

To run application:

```
python3 geolocator.py "Madison, WI" "12345" "Chicago, IL" "10001"

 ./entry_point.sh "Madison, WI" "12345" "Chicago, IL" "10001"

```

To run tests:

```
pytest

pytest -sv

```


### Using dockerized container

```
# To build on Mac OS ARM
# docker buildx build --platform linux/amd64 -t my_docker:develop.latest -f dockerFile .
#
# To build on other platforms
# docker build -t my_docker:develop.latest -f dockerFile .
#
# To start
# docker run -d --name my_container my_docker:develop.latest
#
# To clean up
# docker stop my_container
# docker rm my_container
# docker rmi my_docker:develop.latest
```

### To run application

```
docker exec my_container python geolocator.py "Madison, WI" "12345" "Chicago, IL" "10001"

docker exec my_container  ./entry_point.sh "Madison, WI" "12345" "Chicago, IL" "10001"


```

Sample output:

```
2024-12-02 19:36:17,579 - GeoLocatorProcessor - INFO - Start processing 4 geo locations
2024-12-02 19:36:17,917 - GeoLocatorProcessor - INFO - Finished processing 4 geo locations. Elapsed time: 0.3364778329851106
2024-12-02 19:36:17,918 - GeoLocatorProcessor - INFO - ############################## Results ##############################

Madison, WI:=>latitude=43.074761,longitude=-89.3837613,place name=Madison,country=US
12345:=>latitude=42.8142,longitude=-73.9396,place name=Schenectady,country=US
Chicago, IL:=>latitude=41.8755616,longitude=-87.6244212,place name=Chicago,country=US
10001:=>latitude=40.7484,longitude=-73.9967,place name=New York,country=US

```

### To run tests

```

docker exec my_container pytest

docker exec my_container pytest -sv

```

Sample output:

```
============================= test session starts ==============================
platform linux -- Python 3.11.10, pytest-8.3.4, pluggy-1.5.0 -- /usr/local/bin/python3.11
cachedir: .pytest_cache
rootdir: /app
collecting ... collected 4 items

tests/test_sanity.py::test_smoke 2024-12-02 21:44:49,343 - GeoLocatorProcessor - INFO - Start processing 4 geo locations
2024-12-02 21:44:49,645 - GeoLocatorProcessor - INFO - Finished processing 4 geo locations. Elapsed time: 0.30018775002099574
2024-12-02 21:44:49,645 - GeoLocatorProcessor - INFO - ############################## Results ##############################
Madison, WI:=>latitude=43.074761,longitude=-89.3837613,place name=Madison,country=US
12345:=>latitude=42.8142,longitude=-73.9396,place name=Schenectady,country=US
Chicago, IL:=>latitude=41.8755616,longitude=-87.6244212,place name=Chicago,country=US
10001:=>latitude=40.7484,longitude=-73.9967,place name=New York,country=US

PASSED
tests/test_sanity.py::test_invalid_zip 2024-12-02 21:44:49,883 - GeoLocatorProcessor - INFO - Start processing 1 geo locations
2024-12-02 21:44:49,884 - GeoLocatorProcessor - INFO - Finished processing 1 geo locations. Elapsed time: 9.087496437132359e-05
2024-12-02 21:44:49,884 - GeoLocatorProcessor - INFO - ############################## Results ##############################
1000:=>unable to get geo code. Exception: Invalid location: 1000

PASSED
tests/test_sanity.py::test_invalid_location 2024-12-02 21:44:50,086 - GeoLocatorProcessor - INFO - Start processing 1 geo locations
2024-12-02 21:44:50,088 - GeoLocatorProcessor - INFO - Finished processing 1 geo locations. Elapsed time: 2.5165965780615807e-05
2024-12-02 21:44:50,088 - GeoLocatorProcessor - INFO - ############################## Results ##############################
Three, Words, Invalid:=>unable to get geo code. Exception: Invalid location: Three, Words, Invalid

PASSED
tests/test_sanity.py::test_unknown_zip 2024-12-02 21:44:50,289 - GeoLocatorProcessor - INFO - Start processing 1 geo locations
2024-12-02 21:44:50,366 - GeoLocatorProcessor - INFO - Finished processing 1 geo locations. Elapsed time: 0.07535558298695832
2024-12-02 21:44:50,366 - GeoLocatorProcessor - INFO - ############################## Results ##############################
99999:=>unable to get geo code. Exception: 404 Client Error: Not Found for url: http://api.openweathermap.org/geo/1.0/zip?zip=99999,US&appid=f897a99d971b5eef57be6fafa0d83239

PASSED

```