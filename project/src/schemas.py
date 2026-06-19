from pydantic import BaseModel


class Molecule(BaseModel):
    id: int
    name: str

    def __repr__(self):
        return f"Molecule(id={self.id}, name='{self.name}')"

    def __eq__(self, other):
        if isinstance(other, Molecule):
            return (self.name == other.name and self.id == other.id)
        return False


class MoleculeUpdate(BaseModel):
    name: str
