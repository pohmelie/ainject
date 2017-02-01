import pytest

import ainject


def test_already_binded(binded_injector):

    with pytest.raises(ainject.AInjectorError):

        binded_injector.bind(lambda: 1, name="singleton_value")


@pytest.mark.asyncio
async def test_no_such_name(binded_injector):

    with pytest.raises(ainject.AInjectorError):

        await binded_injector.instance("no_such_name")
