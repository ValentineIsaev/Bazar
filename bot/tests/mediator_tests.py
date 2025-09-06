from dataclasses import dataclass

from asyncio import run

from pathlib import Path
from bot.configs.constants import UserTypes

from bot.services.buyer_chat.services import BuyerChatService
from bot.services.buyer_chat.dto import ChatMessage
from bot.database.repository import MediatorRepository

from bot.database.core import SessionLocal

@dataclass
class TestSendData:
    send_message: ChatMessage
    chat_name: str
    chat_id: int

async def test_send_messages():
    repository = MediatorRepository(SessionLocal)
    chat = BuyerChatService(repository)

    send_messages_tests: tuple[TestSendData, ...] = (
        TestSendData(ChatMessage(123456, UserTypes.BUYER, 98761, UserTypes.SELLER,
                                 text='Добрый день, каков размер товара?'),
                     'Car',
                     12),
        TestSendData(ChatMessage(98761, UserTypes.SELLER, 123456, UserTypes.BUYER, text='23x23'),
                     'Car',
                     12),
        TestSendData(ChatMessage(76456456, UserTypes.BUYER, 98761, UserTypes.SELLER, text='Добрый день, вы меня обманываете'),
                     'Parliament',
                     11),
        TestSendData(ChatMessage(98761, UserTypes.SELLER, 76456456, UserTypes.BUYER, text='Здравствуйте, такого не может быть.'),
                     'Parliament',
                     11)
    )

    # for test in send_messages_tests:
    #     await chat.send_message(test.send_message,
    #                       test.chat_name, test.chat_id)

    all_data = await repository.get_all()
    print(*list(map(repr, all_data)), sep='\n', end=f'\n{5*'='}\n')

    data_seller = await chat.get_updates(UserTypes.SELLER, 98761)
    print(data_seller, end=f'\n{"="*5}\n')

    chat_ = await chat.get_chat(data_seller[1].chat_id)
    print('\n'.join((message.text for message in chat_)), end=f'\n{"="*5}\n')

    data_buyer = await chat.get_updates(UserTypes.BUYER, 123456)
    print(data_buyer, end=f'\n{"="*5}\n')

    chat_ = await chat.get_chat(data_buyer[0].chat_id)
    print('\n'.join((message.text for message in chat_)))


run(test_send_messages())