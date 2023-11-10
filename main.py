import time
import uuid
import structlog
import uvicorn
from fastapi import FastAPI, Request, Response
from custom_logger.logger import setup_logger
from api.api_v1 import api

setup_logger()

logger = structlog.get_logger("elastic_logger")
app = FastAPI()
app.include_router(api.router, prefix='/api')


@app.get("/")
async def root():
    """
    The root function returns a JSON object with the message &quot;Hello World&quot;.

    :return: A dictionary
    :doc-author: Trelent
    """
    return {"message": "Hello World"}


@app.middleware("http")
async def logging_middleware(request: Request, call_next) -> Response:
    correlation_id = request.headers.get("correlation-id")
    if not correlation_id:
        correlation_id = uuid.uuid4().hex

    setattr(request.state, 'correlation_id', correlation_id)

    status_code = None
    response = None
    message = "Request processed successfully"
    has_exception = False
    event = f"Account/middleware{request.url.path}"

    start_time = time.perf_counter_ns()
    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception as e:
        status_code = 500
        message = f"Internal Server Error: {str(e)}"
        has_exception = True
    finally:
        process_time = time.perf_counter_ns() - start_time
        log_dict = {
            "remote_host": request.client.host,
            "request_method": f"{request.method}",
            "url": f" {request.url.path}",
            "status_code": status_code,
            "referer": request.headers.get("referer", ""),
            "user_agent": request.headers.get("user-agent", ""),
            "elapsed_time": process_time,
            "message": message,
            'correlation_id': correlation_id,
        }
    if has_exception:
        await logger.error(event=event, **log_dict)
    else:
        await logger.info(event=event, **log_dict)

    return response


if __name__ == '__main__':
    uvicorn.run('__main__:app', host='0.0.0.0', port=8001, reload=True, log_level="debug", access_log=True)
