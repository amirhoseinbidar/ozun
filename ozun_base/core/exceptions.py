from django.core.exceptions import ValidationError


class membershipException(ValidationError):
    def __init__(self, *args, **kwargs):
        self.code = 'membershipException'
        super(membershipException, self).__init__(*args, **kwargs)


class duplicationException(ValidationError):
    def __init__(self, *args, **kwargs):
        self.code = 'duplicationException'
        super(duplicationException, self).__init__(*args, **kwargs)


class unequalityException(ValidationError):
    def __init__(self, *args, **kwargs):
        self.code = 'unequalityException'
        super(unequalityException, self).__init__(*args, **kwargs)


class overDepthException(ValidationError):
    def __init__(self, *args, **kwargs):
        self.code = 'overDepthException'
        super(overDepthException, self).__init__(*args, **kwargs)
