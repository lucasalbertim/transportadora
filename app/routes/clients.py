from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from routes.auth import get_current_user
from models.user import User
from models.client import Client
from schemas.client import ClientCreate, ClientUpdate, Client as ClientSchema

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("/", response_model=ClientSchema)
def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verificar se CNPJ/CPF já existe
    db_client = db.query(Client).filter(Client.document == client.document).first()
    if db_client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document already registered"
        )
    
    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


@router.get("/", response_model=List[ClientSchema])
def read_clients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    clients = db.query(Client).offset(skip).limit(limit).all()
    return clients


@router.get("/{client_id}", response_model=ClientSchema)
def read_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.put("/{client_id}", response_model=ClientSchema)
def update_client(
    client_id: int,
    client: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    
    update_data = client.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_client, field, value)
    
    db.commit()
    db.refresh(db_client)
    return db_client


@router.delete("/{client_id}")
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    
    db.delete(client)
    db.commit()
    return {"message": "Client deleted successfully"}