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
        timeout: int = 60,  # reasonable timeout?
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
            Dict[str, str]: Dictionary with test metadata like stdout, stderr, response code, running time

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

        starting_time = time.perf_counter()

        # not allowing infinite time run
        try:
            output, errors = process.communicate(
                timeout=self.timeout,
            )
            response_code = process.returncode

        except subprocess.TimeoutExpired:
            process.kill()
            terminated = True
            output, errors = None, None
            response_code = -1  # Indicate that the process was terminated due to timeout

        running_time = time.perf_counter() - starting_time

        response = {
            "input": input_str,
            "output": output.strip() if output else None,
            "terminated": terminated,
            "running_time": running_time,
            "response_code": response_code,
            "errors": errors.strip() if errors else None,
        }

        return response
