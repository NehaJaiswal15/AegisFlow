class AegisFlowException(Exception):
    """Base exception for all AegisFlow errors."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ModelNotLoadedError(AegisFlowException):
    """Raised when the ML model hasn't been loaded yet."""

    def __init__(self):
        super().__init__(
            message="ML model is not loaded. Server is still starting up.",
            status_code=503,
        )


class ModerationNotFoundError(AegisFlowException):
    """Raised when a moderation ID doesn't exist."""

    def __init__(self, moderation_id: str):
        super().__init__(
            message=f"Moderation ID '{moderation_id}' not found.",
            status_code=404,
        )


class TextTooLongError(AegisFlowException):
    """Raised when input text exceeds the limit."""

    def __init__(self, length: int, max_length: int = 5000):
        super().__init__(
            message=f"Text length ({length}) exceeds maximum ({max_length}).",
            status_code=422,
        )
