from __future__ import annotations

from fastapi.middleware import Middleware
from starlette.types import ASGIApp, Receive, Scope, Send

from apscheduler import AsyncScheduler
from apscheduler.datastores.sqlalchemy import SQLAlchemyDataStore
from apscheduler.eventbrokers.asyncpg import AsyncpgEventBroker
from apscheduler.triggers.interval import IntervalTrigger

from db.engine import async_engine
from tasks import print_expired_certificates, remove_expired_certificates


class SchedulerMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        scheduler: AsyncScheduler,
    ) -> None:
        self.app = app
        self.scheduler = scheduler

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "lifespan":
            async with self.scheduler:
                await self.scheduler.add_schedule(
                    print_expired_certificates, IntervalTrigger(seconds=30), id="expired_cert_print"
                )
                await self.scheduler.add_schedule(
                    remove_expired_certificates, IntervalTrigger(minutes=1), id="expired_cert_remove"
                )
                await self.scheduler.start_in_background()
                await self.app(scope, receive, send)
        else:
            await self.app(scope, receive, send)


data_store = SQLAlchemyDataStore(async_engine)
event_broker = AsyncpgEventBroker.from_async_sqla_engine(async_engine)
scheduler = AsyncScheduler(data_store, event_broker)
middleware = [Middleware(SchedulerMiddleware, scheduler=scheduler)]
