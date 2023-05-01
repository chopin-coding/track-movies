from starlette.middleware.base import BaseHTTPMiddleware


class CustomHeaderMiddleware(BaseHTTPMiddleware):
    """
    Exemplary custom middleware provided by Starlette.
    """

    def __init__(self, app, test_option: bool = False):
        super().__init__(app)
        self._test_option = test_option

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Custom"] = "KeepingThisInForNow"
        return response
