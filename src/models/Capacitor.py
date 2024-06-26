from pydantic import BaseModel


class Capacitor(BaseModel):
    """Model for MCU capacitor"""

    energy: int = 0
    max_energy: int = 100

    def __init__(self, energy: int = 0, max_energy: int = 100):
        super().__init__(energy=energy, max_energy=max_energy)
        self.energy = energy
        self.max_energy = max_energy

    # Charge energy to the capacitor if there is enough space
    def charge(self, energy_input: int) -> None:
        self.energy = min(self.max_energy, self.energy + energy_input)

    # Discharge energy from the capacitor if there is enough energy available
    def discharge(self, energy_required: int) -> bool:
        if self.energy >= energy_required:
            self.energy -= energy_required
            return True
        self.energy = 0
        return False
