from rdkit import Chem
from fastapi import FastAPI, HTTPException, Depends
from typing import List

import logging

from src.repositories import MoleculeRepository
from src.schemas import Molecule
from src.dependencies import get_molecule_repository

app = FastAPI()

logging.basicConfig(level=logging.INFO, filename="myPythonApp.log", format="%(asctime)s %(levelname)s %(message)s")



@app.get("/molecules", response_model=List[Molecule])
def get_molecules(
        repo: MoleculeRepository = Depends(get_molecule_repository)
):
    logging.info("GET /molecules")   
    try:
        return repo.get_all()
    except Exception as e:
        logging.error("Error getting all molecules from database", exc_info=e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/molecules/{molecule_id}", response_model=Molecule)
def get_molecule(
        molecule_id: int,
        repo: MoleculeRepository = Depends(get_molecule_repository)
):
    molecule = repo.get_by_id(molecule_id)
    if molecule is None:
        logging.error("Molecule by id is not found")
        raise HTTPException(status_code=400, detail="Molecule not found")
    logging.info("Getting molecule by id from database")
    return molecule


@app.post("/molecules", response_model=Molecule, status_code=201)
def create_molecule(
        molecule: Molecule,
        repo: MoleculeRepository = Depends(get_molecule_repository)
):
    logging.info(f"Creating molecule in database with id={molecule.id} and name={molecule.name}")
    return repo.create(mid=molecule.id, name=molecule.name)


@app.patch("/molecules/{molecule_id}", response_model=Molecule)
def update_molecule(
        molecule_id: int,
        molecule_update: Molecule,
        repo: MoleculeRepository = Depends(get_molecule_repository)
):
    existing_molecule = repo.get_by_id(molecule_id)
    if existing_molecule is None:
        logging.error(f"No molecule to update by id={molecule_id}")
        raise HTTPException(status_code=404, detail="Molecule not found")

    for field, value in molecule_update.model_dump(exclude_unset=True).items():
        setattr(existing_molecule, field, value)
    try:
        return repo.update(existing_molecule)
    except Exception as e:
        logging.error(f"Error updating molecule by id={molecule_id}. Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/molecules/{molecule_id}", status_code=204)
def delete_molecule(
        molecule_id: int,
        repo: MoleculeRepository = Depends(get_molecule_repository)
):
    molecule = repo.get_by_id(molecule_id)
    if molecule is None:
        logging.error(f"No molecule to delete by id={molecule_id}")
        raise HTTPException(status_code=404, detail="Molecule not found")
    try:
        repo.delete(molecule)
    except Exception as e:
        logging.error(f"Error deleting molecule by id={molecule_id}. Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    return None


@app.get("/search", response_model=List[str])
def search_substructure(
        substructure: str,
        repo: MoleculeRepository = Depends(get_molecule_repository)):
    molecules = repo.get_all()
    molecules_name = [molecule.name for molecule in molecules]
    logging.INFO(f"Finding molecules for search: {molecules_name} with substructure: {substructure}")
    result = substructure_search(molecules_name, substructure)
    logging.INFO(f"Found molecules: {result}")
    if result:
        return result
    else:
        logging.ERROR("No matches")
        raise HTTPException(status_code=400, detail="No matches")


def substructure_search(smiles_list: List[str], substructure: str):
    molecules = [Chem.MolFromSmiles(smiles) for smiles in smiles_list]
    substructure_mol = Chem.MolFromSmiles(substructure)
    result = []
    for molecule in molecules:
        if molecule.HasSubstructMatch(substructure_mol):
            result.append(Chem.MolToSmiles(molecule))
    return result
