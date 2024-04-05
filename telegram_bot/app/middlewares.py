from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable


class TestMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str,Any]],Awaitable],
                       event: TelegramObject,
                       data: Dict[str,Any]) -> Any:
        print('Действие до обработчика')
        result = await handler(event, data)
        print('Действия после обработчика')
        return result
