class SFMCError(Exception):
    """Base class for SFMC exceptions."""
    pass

class AuthenticationError(SFMCError):
    """Raised when authentication fails."""
    pass

class APIRequestError(SFMCError):
    """Raised when an API request fails."""
    pass