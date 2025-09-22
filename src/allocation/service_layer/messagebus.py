# src/allocation/service_layer/messagebus.py
import logging
from typing import Callable, Dict, List, Type, Union

from allocation.domain import commands, events
from allocation.service_layer import handlers, ports

Message = Union[commands.Command, events.Event]

# --- Handler Registries --- #

COMMAND_HANDLERS: Dict[Type[commands.Command], Callable] = {
    commands.CreateBatch: handlers.add_batch,
    commands.Allocate: handlers.allocate,
    commands.ChangeBatchQuantity: handlers.change_batch_quantity,
}

EVENT_HANDLERS: Dict[Type[events.Event], List[Callable]] = {
    events.Allocated: [handlers.publish_allocated_event],
    events.OutOfStock: [handlers.send_out_of_stock_notification],
}


# --- Dispatch Logic --- #

def handle_event(event: events.Event, queue: List[Message], uow: ports.AbstractUnitOfWork):
    for handler in EVENT_HANDLERS.get(type(event), []):
        try:
            logging.debug("handling event %s with handler %s", event, handler)
            handler(event, uow=uow)
            queue.extend(uow.collect_new_events())
        except Exception:
            logging.exception("Exception handling event %s", event)
            continue


def handle_command(command: commands.Command, queue: List[Message], uow: ports.AbstractUnitOfWork):
    handler = COMMAND_HANDLERS[type(command)]
    logging.debug("handling command %s with handler %s", command, handler)
    try:
        result = handler(command, uow=uow)
        queue.extend(uow.collect_new_events())
        return result
    except Exception:
        logging.exception("Exception handling command %s", command)
        raise


def handle(message: Message, uow: ports.AbstractUnitOfWork):
    results = []
    queue = [message]

    while queue:
        msg = queue.pop(0)

        if isinstance(msg, events.Event):
            handle_event(msg, queue, uow)
        elif isinstance(msg, commands.Command):
            result = handle_command(msg, queue, uow)
            results.append(result)
        else:
            raise Exception(f"Unknown message type: {msg}")

    return results
