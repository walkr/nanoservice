class NanoServiceError(Exception):
    pass

class ServiceError(NanoServiceError):
    pass

class ClientError(NanoServiceError):
    pass