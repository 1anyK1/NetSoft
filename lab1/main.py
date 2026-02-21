from fastapi import FastAPI, HTTPException
from typing import List
from schemas import Car, CarCreate
from pydantic import ValidationError

app = FastAPI(title = "Car Catalog")

id_counter = 1
cars_db = []

@app.on_event("startup")
async def startup_event():
    print("Applicaton is running")

@app.on_event("shutdown")
async def shutdown_event():
    print("Applicaton is stopped")

@app.get("/")
async def get_ownPage():
    return {"message": "You're on own page of our Cars Catalog!"}

@app.get("/cars/", response_model=List[Car])
async def get_cars():
    return cars_db

@app.get("/cars/{car_id}", response_model=Car)
async def get_car(car_id: int):
    car = next((c for c in cars_db if c.id == car_id), None)
    if not car:
        raise HTTPException(status_code=404, detail = "Car not found")
    return car

@app.post("/cars/", response_model=Car, status_code=201)
async def create_car(car: CarCreate):
    global id_counter
    try:
        new_car = Car(id = id_counter, **car.model_dump())
    except ValidationError as e:
        raise HTTPException(status_code=422, detail="Validate error")
    
    cars_db.append(new_car)
    id_counter += 1
    return new_car