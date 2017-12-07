import inspect
import functools


__all__ = (
    "AInjectorError",
    "Injector",
    "bind",
    "instance",
    "inject",
    "_injector",
)


class AInjectorError(Exception):
    pass


class AInjectorNoName:
    pass


class Injector:

    def __init__(self):
        self._bindings = {}
        self._instances = {}

    def bind(self, function, *, name=AInjectorNoName, singleton=True):
        if name is AInjectorNoName:
            name = function
        if name in self._bindings:
            raise AInjectorError("Name {!r} is binded already".format(name))
        self._bindings[name] = singleton, function

    async def _evaluate(self, function, *args, **kwargs):
        if inspect.iscoroutinefunction(function) or \
                inspect.isclass(function) and \
                inspect.iscoroutinefunction(function.__new__):
            return await function(*args, **kwargs)
        else:
            return function(*args, **kwargs)

    async def instance(self, name):
        if name not in self._bindings:
            raise AInjectorError("Name {!r} is not binded".format(name))
        singleton, function = self._bindings[name]
        if singleton:
            if name not in self._instances:
                self._instances[name] = await self._evaluate(function)
            return self._instances[name]
        else:
            return await self._evaluate(function)

    def _class_wrapper(self, class_, parameters):
        original_new = class_.__new__

        @functools.wraps(original_new)
        async def new(cls, *args, **kwargs):
            for parameter, name in parameters.items():
                if parameter not in kwargs:
                    kwargs[parameter] = await self.instance(name)
            if inspect.isbuiltin(original_new):
                obj = await self._evaluate(original_new, cls)
            else:
                obj = await self._evaluate(original_new, cls, *args, **kwargs)
            await self._evaluate(obj.__init__, *args, **kwargs)
            return obj

        class_.__new__ = new
        return class_

    def _function_wrapper(self, function, parameters):

        @functools.wraps(function)
        async def wrapper(*args, **kwargs):
            for parameter, name in parameters.items():
                if parameter not in kwargs:
                    kwargs[parameter] = await self.instance(name)
            return await self._evaluate(function, *args, **kwargs)
        return wrapper

    def inject(self, **parameters):

        def decorator(function_or_class):
            if inspect.isclass(function_or_class):
                return self._class_wrapper(function_or_class, parameters)
            else:
                return self._function_wrapper(function_or_class, parameters)

        return decorator


_injector = Injector()
bind = _injector.bind
instance = _injector.instance
inject = _injector.inject
