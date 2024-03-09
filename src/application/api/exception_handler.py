from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.exceptions.exceptions import (BalanceLimitExceededException,
                                       ClientNotFoundException)


def client_not_found_exception_handler(request, exc):
    return JSONResponse(content={"detail": f"Cliente não encontrado"}, status_code=404)


def balance_limit_exceeded_exception_handler(request, exc):
    return JSONResponse(content={"detail": f"Limite atingido"}, status_code=402)


def init_exception_handler(app: FastAPI):
    app.add_exception_handler(
        exc_class_or_status_code=BalanceLimitExceededException,
        handler=balance_limit_exceeded_exception_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=ClientNotFoundException,
        handler=client_not_found_exception_handler,
    )
