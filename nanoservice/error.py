class NanoServiceError(Exception):
    pass


class ServiceError(NanoServiceError):
    pass


class ClientError(NanoServiceError):
    pass


class ConfigError(NanoServiceError):
    pass


class AuthenticatorInvalidSignature(NanoServiceError):
    """ Message could not be authenticated """
    pass


class RequestParseError(NanoServiceError):
    """ Message from client could not be parsed """
    pass


class PublisherError(NanoServiceError):
    pass


class SubscriberError(NameError):
    pass


class DecodeError(ServiceError):
    """ Service cannot decode request """
    pass


class AuthenticateError(ServiceError):
    """ Service cannot authenticate request """
    pass
