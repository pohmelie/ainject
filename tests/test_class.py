import pytest


@pytest.mark.asyncio
async def test_init_calling_count(binded_injector):

    @binded_injector.inject(value="singleton_value")
    class A:

        count = 0

        def __init__(self, value):

            self.value = value
            A.count += 1

    @binded_injector.inject(value="singleton_value")
    class B:

        count = 0

        def __init__(self, value):

            self.value = value
            B.count += 1

    a = await A()
    b = await B()
    assert a.value is b.value
    assert A.count == 1
    assert B.count == 1


@pytest.mark.asyncio
async def test_new(binded_injector):

    @binded_injector.inject(value="singleton_value")
    class MyInt(int):

        count = 0

        def __new__(cls, x, value):

            return super().__new__(cls, x, base=2)

        def __init__(self, x, value):

            MyInt.count += 1
            self.value = value

    myint = await MyInt("101")
    assert myint == 5
    assert myint.count == 1
    assert myint.value is await binded_injector.instance("singleton_value")


@pytest.mark.asyncio
async def test_async_init(binded_injector):

    @binded_injector.inject(value="singleton_value")
    class A:

        async def __init__(self, value):

            self.value = value

    a = await A()
    assert a.value is (await binded_injector.instance("singleton_value"))


@pytest.mark.asyncio
async def test_function_to_class_to_function_injection(binded_injector):

    async def foo():

        return []

    @binded_injector.inject(x="foo")
    class A:
        def __init__(self, x):
            self.x = x

    @binded_injector.inject(a=A)
    def bar(a):
        return a

    binded_injector.bind(foo, name="foo")
    binded_injector.bind(A)
    assert (await bar()).x == []
