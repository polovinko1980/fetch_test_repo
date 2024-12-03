#!/usr/bin/env python3

"""
Module with classes to interact with
https://openweathermap.org/api/geocoding-api site

"""

import os
import re
import time
from re import Match
from typing import List, Any
import requests
import logging
import sys


# Set up logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)],
)

# Create a logger
logger = logging.getLogger("GeoLocatorProcessor")


class GeoLocatorProcessor:
    """
    Class to process multiple locations strings
    """

    LOCATION_CODE_SEPARATOR = ":=>"

    def __init__(self):
        self._geo_codes = []
        self.geolocator_client = GeoLocatorApiClient(
            api_key=os.getenv("API_KEY") or "f897a99d971b5eef57be6fafa0d83239"
        )


    def get_geocodes(
        self,
        locations: tuple[Any, ...],
    ) -> List[str]:

        """
        Method to process multiple locations in sequence. If required, can be parallelized

        Args:
            locations (List) list of strings representing locations in the form of "city, state" or "zip"

        Returns:
            List: list of strings with locations and results of getting location geocodes

        """

        for location in locations:
            result = self.geolocator_client.get_code(location)

            self._geo_codes.append(
                f"{location}{GeoLocatorProcessor.LOCATION_CODE_SEPARATOR}{result}"
            )

        return self._geo_codes


class GeoLocatorApiClient:
    """
    Wrapper on openweathermap api

    """

    def __init__(
        self,
        api_key: str,
    ):

        """
        Initiates GeoLocatorApiClient instance

        Args:
           api_key (str): Api key to use in authorization

        """

        self._api_key = api_key

        # Some constants
        self._API_BASE_URL = "http://api.openweathermap.org/geo/1.0"
        self._REQUEST_LIMIT = 1 # no need to spam api; increase, if required

        # Response formatting
        self._SUCCESS_RESPONSE = (
            "latitude={latitude},"
            "longitude={longitude},"
            "place name={place_name},"
            "country={country}"
        )
        self._ERROR_RESPONSE = (
            "unable to get geo code. "
            "Exception: {exception}"
        )


    def get_code(
        self,
        location: str,
    ) -> str:

        """
        Method to get response from openweathermap service.

        Args:
           location (str): String representing location. Valid strings "city, state" or "zip"

        Returns:
             (str) Result of api call. Either normalized api response or exception message

        """

        try:
            endpoint = self.get_api_endpoint_from_location(location=location)
        except ValueError:
            return self._ERROR_RESPONSE.format(
                exception=f"Invalid location: {location}",
            )

        try:
            response = requests.get(url=endpoint)
            response.raise_for_status()


            response_json = response.json()

            # api might return either list or single object
            if type(response_json) == list:

                if len(response_json) < 1:
                    return self._ERROR_RESPONSE.format(
                        exception="location not found",
                    )

                response_json = response_json[0]

            if not response_json.get("lat") or not response_json.get("lon"):
                return self._ERROR_RESPONSE.format(
                        exception="api not returning latitude or longitude",
                    )

            return self._SUCCESS_RESPONSE.format(
                latitude = response_json.get("lat"),
                longitude = response_json.get("lon"),
                place_name = response_json.get("name"),
                country=response_json.get("country"),
            )

        except Exception as e:
            return self._ERROR_RESPONSE.format(
                exception=str(e),
            )

    def get_api_endpoint_from_location(
        self,
        location: str,
    ) -> str:
        """
        Constructs and returns api endpoint to call.

        Supporting 2 endpoints for now:

        https://openweathermap.org/api/geocoding-api#direct_name

        https://openweathermap.org/api/geocoding-api#direct_zip

        Args:
           location (str): String representing location. Valid strings "city, state" or "zip"

        Raises:
            ValueError: if location input can not be used to determine endpoint url.

        Returns:
            (str): endpoint url

        """


        validator = LocationValidator(location=location)

        if validator.is_valid_zip():

            endpoint_url = f"{self._API_BASE_URL}/zip?zip={location},US&appid={self._api_key}"

        elif validator.is_valid_direct_location():

            # need to normalize inputs
            normalized_locations = ",".join([word.strip() for word in location.split(",")])

            endpoint_url = f"{self._API_BASE_URL}/direct?q={normalized_locations},US&limit={self._REQUEST_LIMIT}&appid={self._api_key}"
        else:

            raise ValueError("Invalid location, unable to define api endpoint")

        return endpoint_url


class LocationValidator:
    """
    Class responsible to validate
    inputs against business requirements

    """

    def __init__(
        self,
        location: str,
    ):

        """
        Initiates GeoLocatorValidator instance

        Args:
           location (str): String representing location. Valid strings "city, state" or "zip"

        """

        self._location = location


    def is_valid_zip(self) -> Match[str] | None:
        """
        Considering location is valid zip
        if it is a single word and passing US zip regex

        """

        # checking if zip code the single word
        if len(self._location.split(",")) > 1:
            return None

        # checking if zip code is valid
        zip_pattern = re.compile(r"^\d{5}(?:[-\s]\d{4})?$")
        return zip_pattern.match(self._location)

    def is_valid_direct_location(self) -> Match[str] | None:
        """
        Considering direct location is valid if it is two comma separated words and
        second word is passing state regex.

        """

        # checking that exactly 2 words are passed
        all_words = self._location.split(",")
        all_words = [word.strip() for word in all_words]

        if len(all_words) != 2:
            return None

        # checking if state is valid
        state_pattern = re.compile(
            r'\b(?:AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY)\b'
        )

        return state_pattern.match(all_words[1])


def main(*args):


    logger.info(f"Start processing {len(args)} geo locations")
    start_time = time.perf_counter()

    geo_locator_processor = GeoLocatorProcessor()
    results = geo_locator_processor.get_geocodes(args)

    logger.info(
        f"Finished processing {len(args)} geo locations. "
        f"Elapsed time: {time.perf_counter() - start_time}"
    )
    logger.info("#"*30 + " Results " + "#"*30)

    # As output format not outlined, just printing to stdout
    [print(result) for result in results]


if __name__ == "__main__":
    main(*sys.argv[1:])