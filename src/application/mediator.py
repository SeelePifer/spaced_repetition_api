from abc import ABC, abstractmethod
from typing import Any, Dict, Type, TypeVar
from .commands.study_commands import Command
from .queries.study_queries import Query
from .handlers.command_handlers import CommandHandler
from .handlers.query_handlers import QueryHandler

TCommand = TypeVar('TCommand', bound=Command)
TQuery = TypeVar('TQuery', bound=Query)
TCommandHandler = TypeVar('TCommandHandler', bound=CommandHandler)
TQueryHandler = TypeVar('TQueryHandler', bound=QueryHandler)


class Mediator(ABC):
    """Base interface for CQRS mediator"""
    
    @abstractmethod
    async def send_command(self, command: Command) -> Any:
        """Sends a command to be processed"""
        pass
    
    @abstractmethod
    async def send_query(self, query: Query) -> Any:
        """Sends a query to be processed"""
        pass


class CQRSMediator(Mediator):
    """CQRS Mediator implementation"""
    
    def __init__(self):
        self._command_handlers: Dict[Type[Command], CommandHandler] = {}
        self._query_handlers: Dict[Type[Query], QueryHandler] = {}
    
    def register_command_handler(self, command_type: Type[TCommand], handler: TCommandHandler):
        """Registers a handler for a command type"""
        self._command_handlers[command_type] = handler
    
    def register_query_handler(self, query_type: Type[TQuery], handler: TQueryHandler):
        """Registers a handler for a query type"""
        self._query_handlers[query_type] = handler
    
    async def send_command(self, command: Command) -> Any:
        """Sends a command to be processed"""
        command_type = type(command)
        handler = self._command_handlers.get(command_type)
        
        if not handler:
            raise ValueError(f"No handler registered for command {command_type.__name__}")
        
        return await handler.handle(command)
    
    async def send_query(self, query: Query) -> Any:
        """Sends a query to be processed"""
        query_type = type(query)
        handler = self._query_handlers.get(query_type)
        
        if not handler:
            raise ValueError(f"No handler registered for query {query_type.__name__}")
        
        return await handler.handle(query)
