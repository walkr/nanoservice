"""NanoService Exceptions"""


class NanoServiceError(Exception):
    """Base exception for Nanoservice"""
    pass


class ServiceError(NanoServiceError):
    """Service Generic Exception"""
    pass


class ClientError(NanoServiceError):
    """Client Generic Exception"""
    pass


class ConfigError(NanoServiceError):
    """Config Generic Exception"""
    pass


class AuthenticatorInvalidSignature(NanoServiceError):
    """ Message could not be authenticated """
    pass


class RequestParseError(NanoServiceError):
    """ Message from client could not be parsed """
    pass


class PublisherError(NanoServiceError):
    """Publisher Generic Exception"""
    pass


class SubscriberError(NameError):
    """Subscriber Generic Exception"""
    pass


class DecodeError(ServiceError):
    """ Cannot decode request """
    pass


class EncodeError(ServiceError):
    """ Cannot encode request """
    pass


class AuthenticateError(ServiceError):
    """ Cannot authenticate request """
    pass


class EndpointError(ServiceError):
    """ Endpoint Error """
    pass
