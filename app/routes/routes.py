from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from routes.auth import get_current_user
from models.user import User
from models.route import Route
from schemas.route import RouteCreate, RouteUpdate, Route as RouteSchema

router = APIRouter(prefix="/routes", tags=["routes"])


@router.post("/", response_model=RouteSchema)
def create_route(
    route: RouteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_route = Route(**route.dict())
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route


@router.get("/", response_model=List[RouteSchema])
def read_routes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    routes = db.query(Route).offset(skip).limit(limit).all()
    return routes


@router.get("/{route_id}", response_model=RouteSchema)
def read_route(
    route_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    route = db.query(Route).filter(Route.id == route_id).first()
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return route


@router.put("/{route_id}", response_model=RouteSchema)
def update_route(
    route_id: int,
    route: RouteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_route = db.query(Route).filter(Route.id == route_id).first()
    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    
    update_data = route.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_route, field, value)
    
    db.commit()
    db.refresh(db_route)
    return db_route


@router.delete("/{route_id}")
def delete_route(
    route_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    route = db.query(Route).filter(Route.id == route_id).first()
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    
    db.delete(route)
    db.commit()
    return {"message": "Route deleted successfully"}