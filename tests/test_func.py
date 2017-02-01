import pytest


@pytest.mark.asyncio
async def test_coroutine(binded_injector):

    @binded_injector.inject(value="singleton_value")
    async def foo(value):

        return value

    a = await foo()
    b = await foo()
    assert a is b


@pytest.mark.asyncio
async def test_function(binded_injector):

    @binded_injector.inject(value="singleton_value")
    def foo(value):

        return value

    a = await foo()
    b = await foo()
    assert a is b


@pytest.mark.asyncio
async def test_multiple(binded_injector):

    @binded_injector.inject(value="multiple_value")
    async def foo(value):

        return value

    a = await foo()
    b = await foo()
    assert a is not b
    assert a == b


@pytest.mark.asyncio
async def test_custom(binded_injector):

    class A:

        pass

    @binded_injector.inject(a=A)
    def foo(a):

        return a

    binded_injector.bind(A)
    assert isinstance(await foo(), A)


@pytest.mark.asyncio
async def test_chain(binded_injector):

    @binded_injector.inject(x="singleton_value")
    def a(x):

        return x

    @binded_injector.inject(a=a)
    def b(a):

        return a

    @binded_injector.inject(b=b)
    def c(b):

        return b

    binded_injector.bind(a)
    binded_injector.bind(b)
    r1 = await c()
    r2 = await binded_injector.instance("singleton_value")
    assert r1 is r2
