class PolyStringError(Exception): ...


class UnsupportedLanguageError(PolyStringError):
    def __init__(self, code: str) -> None:
        super().__init__(
            f"'{code}' is not a supported language code. "
            f"Call polystring.supported_languages() for the full list."
        )


class InputTooShortError(PolyStringError):
    def __init__(
        self,
        message: str = "Input too short: need at least 2 tokens.",
    ) -> None:
        super().__init__(message)
