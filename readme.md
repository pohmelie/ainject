# ainject
Simple asynchronous dependency injector for python.

## Reasons
* No asynchronous DI with `async`/`await` support.
* Simplifying things.

## Features
* Asynchronous instance factories.
* Asynchronous `__init__` and `__new__` support.
* Damn simple api.

## Requirements
* Python 3.5+
* setuptools >= 30.3.0 (installation only)

## Usage
All you have to do is `bind` some factories with some names and
`inject`/`instance` them where you want.
``` python
>>> import ainject
```
### Bind and instance
Simple bind with name:
``` python
>>> async def async_factory():
...     return "async_value"
...
>>> def sync_factory():
...     return "sync_value"
>>> ainject.bind(async_factory, name="async")
>>> await ainject.instance("async")
'async_value'
>>> ainject.bind(sync_factory, name="sync")
>>> await ainject.instance("sync")
'sync_value'
>>>
```
As you can see you should always `await` your result, even if factory is actually synchronous.

Bind without name:
``` python
>>> ainject.bind(async_factory)
>>> await ainject.instance(async_factory)
'async_value'
>>> ainject.bind(sync_factory)
>>> await ainject.instance(sync_factory)
'sync_value'
>>>
```
In this case `name` is `factory` itself. This is equivalent to:
``` python
>>> ainject.bind(async_factory, name=async_factory)
>>>
```
So, you can use any hashable value for name, or even omit it for auto naming.

By default binding is done in «singleton» mode. This means, that first time instance is accessed it will be cashed and for every next instance request cashed version will be used:
``` python
>>> def factory():
...     return []
...
>>> ainject.bind(factory)
>>> a = await ainject.instance(factory)
>>> b = await ainject.instance(factory)
>>> a, b
([], [])
>>> a is b
True
>>>
```
For non-singleton usage pass `singleton=False` to bind method. In this case every instantiation will actually execute factory function:
``` python
>>> def factory():
...     return []
...
>>> ainject.bind(factory, singleton=False)
>>> a = await ainject.instance(factory)
>>> b = await ainject.instance(factory)
>>> a, b
([], [])
>>> a is b
False
>>>
```
### Inject
Injecting is done via `inject` decorator:
``` python
>>> @ainject.inject(x=factory)
... def foo(x):
...     print(x)
...
...
>>> await foo()
[]
>>>
```
Keep in mind that «name» should be defined before decorator, or just use strings for names. Also, remember, that everything you wrap with `inject` decorator became awaitable:
``` python
>>> @ainject.inject(x="async")
... class A:
...     def __init__(self, x):
...         self.x = x
...
...
...
>>> a = await A()
>>>
```
Even class instantiation. Side-effect of this «magic» is that you can use `async` `__init__` and `async` `__new__`:
``` python
>>> @ainject.inject()
... class A:
...     async def __new__(self, x):
...         ...
...         return super().__new__(self)
...     async def __init__(self, x):
...         self.x = x
...
...
...
>>> a = await A(3)
```
As you can see you can even inject nothing.

## Advanced usage
Most of time you only need above scenarios, but if you need low-level access to injector, or use more than one injector you should instantiate `Injector` class and use its `bind`, `inject` and `instance` methods. Default injector is global for ainject module and can be accessed as `ainject._injector`. Bindings are stored as dictionary with name-factory pairs in `Injector._bindings`. Instances (singletons) stored as name-instance pairs in `Injector._instances`.
