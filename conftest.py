import pytest

from tests.executor import MyExecutor


@pytest.fixture(scope="session")
def my_executor(
    request,
):
    """
    Fixture to return the
    executor agent for the
    convenience

    Caller is responsible to pass valid
    entry point to execute commands

    """

    my_executor = MyExecutor(
        entry_point="./entry_point.sh",
    )

    return my_executor

