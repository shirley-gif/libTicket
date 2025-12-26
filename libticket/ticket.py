from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


@dataclass
class Ticket:
    """Simple in-memory ticket record."""

    id: int
    question: str
    requested_details: List[str]
    created_at: str = field(default_factory=_now)
    status: str = "pending"

    def to_dict(self) -> Dict[str, str]:
        return {
            "id": self.id,
            "question": self.question,
            "requested_details": self.requested_details,
            "created_at": self.created_at,
            "status": self.status,
        }


class TicketStore:
    """Minimal ticket storage for demo purposes."""

    def __init__(self):
        self._tickets: List[Ticket] = []

    def create(self, question: str, requested_details: List[str]) -> Ticket:
        ticket_id = len(self._tickets) + 1
        ticket = Ticket(id=ticket_id, question=question, requested_details=requested_details)
        self._tickets.append(ticket)
        return ticket

    def all(self) -> List[Ticket]:
        return list(self._tickets)


__all__ = ["Ticket", "TicketStore"]
