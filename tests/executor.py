#!/usr/local/bin/python

"""
Python wrapper on subprocess to interact with geolocator utility

It will take input,
execute subprocess command,
wait for process completion
and keep some test metadata:

- response code
- raw stderr stream
- raw output str
- execution time


Wrapper should also be non-blocking and should
be terminated if it can not get response from
subprocess in the reasonable time (60s)

We can extend wrapper to add other non-functional characteristics
like process memory usage monitoring or CPU usage (future enhancement)

"""

import subprocess
import time
from typing import Dict


class MyExecutor:

    def __init__(
        self,
        entry_point: str,
        timeout=60,  # reasonable timeout?
    ):
        """
        Initialize MyExecutor instance

        Args:
            entry_point (str): application/utility to invoke
            timeout (int): max time to wait till application response

        """

        self.entry_point = entry_point
        self.timeout = timeout

    def execute(
        self,
        input_str: str,
    ) -> Dict[str, str]:
        """
        Main method to call application and collect metrics

        Args:
            input_str (str): String of quoted locations as is, i.e. '"Madison, WI" "12345" "Chicago, IL" "10001"'

        Returns:
            (Dist): Dictionary with test metadata like stdout, stderr, response code, running time

        """

        terminated = False

        cmd = f"{self.entry_point} {input_str}"

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
        )

        output, errors = None, None

        starting_time = time.perf_counter()

        # not allowing infinite time run
        try:
            output, errors = process.communicate(
                timeout=self.timeout,
            )

        except subprocess.TimeoutExpired:
            process.kill()
            terminated = True

        running_time = time.perf_counter() - starting_time

        response = {"input": input_str}

        if output:
            response["output"] = output.strip()

        response = response | {
            "terminated": terminated,
            "running_time": running_time,
            "response_code": process.returncode,
            "errors": errors,
        }

        return response
