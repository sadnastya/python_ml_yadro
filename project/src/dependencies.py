from fastapi import Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.repositories import MoleculeRepository


def get_molecule_repository(
        db: Session = Depends(get_db)) -> MoleculeRepository:
    return MoleculeRepository(db)


def get_test_molecule_repository(db: Session = get_db()) -> MoleculeRepository:
    return MoleculeRepository(db)
