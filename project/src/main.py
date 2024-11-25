from rdkit import Chem
from fastapi import FastAPI, HTTPException, Depends
from typing import List

from repositories import MoleculeRepository
from schemas import Molecule
from dependencies import get_molecule_repository

app = FastAPI()

# GET    /molecules
# GET    /molecules/{molecule_id}
# POST   /molecules
# PATCH  /molecules/{molecule_id}
# DELETE /molecules/{molecule_id}

# GET    /search?substructure

@app.get("/molecules", response_model=List[Molecule])
def get_molecules(
        repo: MoleculeRepository = Depends(get_molecule_repository)
):
    return repo.get_all()


@app.get("/molecules/{molecule_id}", response_model=Molecule)
def get_molecule(
        molecule_id: int,
        repo: MoleculeRepository = Depends(get_molecule_repository)
):
    molecule = repo.get_by_id(molecule_id)
    if molecule is None:
        raise HTTPException(status_code=400, detail="Molecule not found")
    return molecule


@app.post("/molecules", response_model=Molecule, status_code=201)
def create_molecule(
        molecule: Molecule,
        repo: MoleculeRepository = Depends(get_molecule_repository)
):
    return repo.create(mid=molecule.id, name=molecule.name)


@app.patch("/molecules/{molecule_id}", response_model=Molecule)
def update_molecule(
        molecule_id: int,
        molecule_update: Molecule,
        repo: MoleculeRepository = Depends(get_molecule_repository)
):
    existing_molecule = repo.get_by_id(molecule_id)
    if existing_molecule is None:
        raise HTTPException(status_code=404, detail="Molecule not found")

    for field, value in molecule_update.dict(exclude_unset=True).items():
        setattr(existing_molecule, field, value)

    return repo.update(existing_molecule)


@app.delete("/molecules/{molecule_id}", status_code=204)
def delete_molecule(
        molecule_id: int,
        repo: MoleculeRepository = Depends(get_molecule_repository)
):
    molecule = repo.get_by_id(molecule_id)
    if molecule is None:
        raise HTTPException(status_code=404, detail="Molecule not found")
    repo.delete(molecule)
    return None

@app.get("/search", response_model=List[str])
def search_substructure(
        substructure: str,
        repo: MoleculeRepository = Depends(get_molecule_repository)):
    molecules = repo.get_all()
    print(molecules)
    molecules_name = [molecule.name for molecule in molecules]
    print(molecules_name)
    result = searching(molecules_name, substructure)
    if result:
        return result
    else:
        raise HTTPException(status_code=400, detail="No matches")


def searching(smiles_list: List[str], substructure: str):
    molecules = [Chem.MolFromSmiles(smiles) for smiles in smiles_list]
    substructure_mol = Chem.MolFromSmiles(substructure)
    result=[]
    for molecule in molecules:
        if molecule.HasSubstructMatch(substructure_mol):
            result.append(Chem.MolToSmiles(molecule))
    return result


