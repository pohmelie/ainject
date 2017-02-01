import pytest

import ainject


@pytest.fixture
def binded_injector():

    async def value():

        return []

    injector = ainject.Injector()
    injector.bind(value, name="singleton_value")
    injector.bind(value, name="multiple_value", singleton=False)
    return injector
