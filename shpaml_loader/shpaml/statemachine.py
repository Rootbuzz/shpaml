from string import upper

class StateMachine(object):
    start_state = None
    end_states = []
    _handlers = {}
    
    def __init__(self):
        self.end_states = set(self.end_states)
        
        for attr, val in self.__dict__.items():
            if attr.startswith("state_") and callable(val):
                self._init_handler(attr, val)
        
        

    def _get_handler(self, handler_name):
        return getattr(self, "state_%s" % handler_name)
    
    def _init_handler(self, handler_name, handler):
        self._handlers[handler_name] = handler
        handler.end_states = set(getattr(handler, 'end_states', ()))
    
    def hander(self, handler_name):
        handler_name = "state_%s" % handler_name
        def decorator(fn):
            setattr(self, handler_name, fn)
            self._init_handler(handler_name, fn)
        return decorator

    def run(self, cargo):
        try:
            handler = self._get_handler(self.startState)
        except:
            raise "InitializationError", "Must set \"start_state\" attribute before calling .run()"
        if not self.endStates:
            raise "InitializationError", "Must specify at least one end_state (either self.end_states or using the end_states() decorator on a handler)"

        while True:
            new_state, cargo = handler(cargo)
            if new_state in self.end_states + handler.end_states:
                break
            else:
                handler = self._get_handler(new_state)


def end_states(*end_states):
    def decorator(fn):
        fn.end_states = end_states
        return fn
    return decorator
