from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from repositories import MoleculeRepository

def get_molecule_repository(db: Session = Depends(get_db)) -> MoleculeRepository:
    return MoleculeRepository(db)