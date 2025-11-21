"""
Base API class with common functionality.
"""

import asyncio
import random
import logging
from abc import ABC
from datetime import datetime
from typing import Any, Dict, Optional, TypeVar, Generic
from pydantic import BaseModel

logger = logging.getLogger(__name__)

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    timestamp: datetime = datetime.now()
    request_id: str = ""
    latency_ms: int = 0


class BaseAPI(ABC):
    """
    Base class for all data APIs.
    Provides common functionality like latency simulation, logging, and error handling.
    """

    def __init__(
        self,
        name: str,
        min_latency_ms: int = 50,
        max_latency_ms: int = 200,
        failure_rate: float = 0.0  # 0-1, probability of simulated failure
    ):
        self.name = name
        self.min_latency_ms = min_latency_ms
        self.max_latency_ms = max_latency_ms
        self.failure_rate = failure_rate
        self.request_count = 0
        self.logger = logging.getLogger(f"api.{name}")

    async def _simulate_latency(self) -> int:
        """Simulate network latency."""
        latency = random.randint(self.min_latency_ms, self.max_latency_ms)
        await asyncio.sleep(latency / 1000)  # Convert to seconds
        return latency

    def _generate_request_id(self) -> str:
        """Generate a unique request ID."""
        self.request_count += 1
        return f"{self.name}-{datetime.now().strftime('%Y%m%d%H%M%S')}-{self.request_count:06d}"

    def _should_fail(self) -> bool:
        """Check if request should fail (for testing resilience)."""
        return random.random() < self.failure_rate

    async def _execute_request(
        self,
        operation: str,
        handler: callable,
        **kwargs
    ) -> APIResponse:
        """
        Execute an API request with latency simulation and error handling.
        """
        request_id = self._generate_request_id()
        start_time = datetime.now()

        self.logger.info(f"[{request_id}] Starting {operation}")

        try:
            # Simulate latency
            latency = await self._simulate_latency()

            # Check for simulated failure
            if self._should_fail():
                raise Exception("Simulated API failure for testing")

            # Execute the actual handler
            result = handler(**kwargs)

            end_time = datetime.now()
            total_latency = int((end_time - start_time).total_seconds() * 1000)

            self.logger.info(f"[{request_id}] Completed {operation} in {total_latency}ms")

            return APIResponse(
                success=True,
                data=result,
                request_id=request_id,
                latency_ms=total_latency,
                timestamp=end_time
            )

        except Exception as e:
            end_time = datetime.now()
            total_latency = int((end_time - start_time).total_seconds() * 1000)

            self.logger.error(f"[{request_id}] Failed {operation}: {str(e)}")

            return APIResponse(
                success=False,
                error=str(e),
                error_code="API_ERROR",
                request_id=request_id,
                latency_ms=total_latency,
                timestamp=end_time
            )

    def get_stats(self) -> Dict[str, Any]:
        """Get API statistics."""
        return {
            "name": self.name,
            "total_requests": self.request_count,
            "min_latency_ms": self.min_latency_ms,
            "max_latency_ms": self.max_latency_ms,
            "failure_rate": self.failure_rate
        }
