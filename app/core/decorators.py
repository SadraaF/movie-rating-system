import time
import logging
import functools
from typing import Any, Callable

logger = logging.getLogger("app.performance")

def log_execution_time(func: Callable) -> Callable:
    """
    Decorator that logs the start, end, and duration of a function.
    Addresses Latency and Observability requirements.
    """
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        func_name = func.__name__
        
        # eaningful Events (Start)
        logger.debug(f"Starting {func_name}")
        
        try:
            result = await func(*args, **kwargs)
            end_time = time.perf_counter()
            duration = (end_time - start_time) * 1000  # Convert to ms
            
            # Latency Metric
            logger.info(f"Finished {func_name} - Duration: {duration:.2f}ms")
            return result
        except Exception as e:
            end_time = time.perf_counter()
            duration = (end_time - start_time) * 1000
            logger.error(f"Error in {func_name} after {duration:.2f}ms: {str(e)}")
            raise

    return wrapper