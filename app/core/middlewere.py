import time
from typing import Callable
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from .logging import logger

from starlette.responses import Response

class loggin_middlewere (BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next ):
        start_time = time.time()
        
        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        format_process_time = '{0:.2f}'.format(process_time)
 
        logger.info(
            f'[{request.method} {request.url.path}]'
            f'{response.status_code}'
            f'{format_process_time}ms'
        )
        return response
