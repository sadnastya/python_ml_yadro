from pydantic import BaseModel

class Molecule(BaseModel):
    id: int
    name: str

class MoleculeUpdate(BaseModel):
    name: str