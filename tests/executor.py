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
from typing import List


class MyExecutor:

    def __init__(
        self,
        entry_point,
        timeout=60,  # reasonable timeout?
    ):
        self.entry_point = entry_point
        self.timeout = timeout

    def execute(
        self,
        input_str,
    ):
        """
        Main method to call application and collect metrics

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

        print(output)

        if output:
            response["output"] = output.strip()

        response = response | {
            "terminated": terminated,
            "running_time": running_time,
            "response_code": process.returncode,
            "errors": errors,
        }

        return response
