from app.domain.models import Vehicle


class FakeServiceCenter:
    def __init__(self, decision: bool) -> None:
        self.decision = decision
        self.inspected: list[Vehicle] = []

    def accepts(self, vehicle: Vehicle) -> bool:
        self.inspected.append(vehicle)
        return self.decision
