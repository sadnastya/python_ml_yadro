from sqlalchemy.orm import Session
from models import Molecule

class MoleculeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Molecule).all()

    def get_by_id(self, molecule_id: int):
        return self.db.query(Molecule).filter(Molecule.id == molecule_id).first()

    def create(self, mid: int, name: str):
        molecule = Molecule(id=mid, name=name)
        self.db.add(molecule)
        self.db.commit()
        self.db.refresh(molecule)
        return molecule

    def update(self, molecule: Molecule):
        self.db.commit()
        self.db.refresh(molecule)
        return molecule

    def delete(self, molecule: Molecule):
        self.db.delete(molecule)
        self.db.commit()