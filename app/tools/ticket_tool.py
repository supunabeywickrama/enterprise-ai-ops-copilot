"""ServiceNow ticket tool — implemented in Phase 7."""
from app.schemas.ticket_schema import TicketCreate, TicketResponse, TicketUpdate


class TicketTool:
    async def create_ticket(self, ticket: TicketCreate) -> TicketResponse:
        raise NotImplementedError("TicketTool.create_ticket — implement in Phase 7")

    async def list_tickets(self, status=None, priority=None, limit=20) -> list[TicketResponse]:
        raise NotImplementedError("TicketTool.list_tickets — implement in Phase 7")

    async def get_ticket(self, ticket_id: str) -> TicketResponse | None:
        raise NotImplementedError("TicketTool.get_ticket — implement in Phase 7")

    async def update_ticket(self, ticket_id: str, update: TicketUpdate) -> TicketResponse | None:
        raise NotImplementedError("TicketTool.update_ticket — implement in Phase 7")
