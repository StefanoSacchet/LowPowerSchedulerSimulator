from pydantic import BaseModel, field_validator

from src.config.Config import ConfigParams


class Capacitor(BaseModel):
    """Model for MCU capacitor"""

    energy: float
    max_energy: int

    class Config:
        validate_assignment = True

    @field_validator("energy")
    def check_energy(cls, value):
        assert value >= 0, "Energy must be greater than or equal to 0"
        return value

    @field_validator("max_energy")
    def check_max_energy(cls, value):
        assert value > 0, "Max energy must be greater than 0"
        return value

    def __init__(
        self,
        energy: float = ConfigParams.ENERGY.value,
        max_energy: int = ConfigParams.MAX_ENERGY.value,
    ):
        super().__init__(energy=energy, max_energy=max_energy)
        self.energy = energy
        self.max_energy = max_energy

    # Charge energy to the capacitor if there is enough space
    def charge(self, energy_input: int) -> None:
        self.energy = min(self.max_energy, self.energy + energy_input)

    # Discharge energy from the capacitor if there is enough energy available
    def discharge(self, energy_required: float) -> bool:
        if self.energy >= energy_required:
            self.energy -= energy_required
            return True
        self.energy = 0
        return False
