class AbstractRegister(object):
    def __init__(self):
        self.registered = {}

    def register(self, i):
        assert (
            i.REGISTER_ID is not None
        ), "REGISTER_ID is required for registration"
        self.registered[i.REGISTER_ID] = i

    def get(self, i):
        return self.registered.get(i)

    def get_instance(self, i, **kwargs):
        return self.get(i=i)(**kwargs)

    def get_or_raise(self, i):
        try:
            return self.registered[i]
        except KeyError:
            raise RuntimeError("No instance registered for %s" % i)

    def get_instance_or_raise(self, i, **kwargs):
        try:
            return self.registered[i](**kwargs)
        except KeyError:
            available = ", ".join(self.registered.keys())
            raise RuntimeError(
                "No instance registered under the id %s. Available instances are %s"
                % (i, available)
            )

    def iter(self):
        for i in self.registered.keys():
            yield self.get_instance_or_raise(i)
