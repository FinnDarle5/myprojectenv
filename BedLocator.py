from fastapi import FastAPI, Query
from pydantic import BaseModel
from corsheaders import corsheadrs

app = FastAPI()

app = corsheaders(app)

class Hospital(BaseModel):
    id: int
    name: str

class BedType(BaseModel):
    id: int
    name: str

class BedAvailability(BaseModel):
    total_beds: int
    available_beds: int

hospitals = {
    1: Hospital(id=1, name="AIIMS"),
    2: Hospital(id=2, name="IGIMS"),
    3: Hospital(id=3, name="PMCH"),
}

bed_types = {
    1: BedType(id=1, name="ICU"),
    2: BedType(id=2, name="Ventillator"),
    3: BedType(id=3, name="General"),
}

bed_availabilities = {
    # AIIMS
    (1, 1): BedAvailability(total_beds=100, available_beds=82),
    (1, 2): BedAvailability(total_beds=118, available_beds=56),
    (1, 3): BedAvailability(total_beds=85, available_beds=70),
    # IGIMS
    (2, 1): BedAvailability(total_beds=50, available_beds=38),
    (2, 2): BedAvailability(total_beds=37, available_beds=29),
    (2, 3): BedAvailability(total_beds=42, available_beds=40),
    # PMCH
    (3, 1): BedAvailability(total_beds=88, available_beds=60),
    (3, 2): BedAvailability(total_beds=49, available_beds=38),
    (3, 3): BedAvailability(total_beds=75, available_beds=68),
}
@app.get("/")
def root():
    return {"message": "Hello World!"}

@app.get("/protected")
def protected():
    return {"message": "This is a protected route"}

@app.get("/hospitals")
async def get_all_hospitals():
    return list(hospitals.values())

@app.get("/hospitals/{hospital_id}")
async def get_hospital(hospital_id: int):
    if hospital_id not in hospitals:
        return {"message": "Hospital not found"}
    return hospitals[hospital_id]

@app.get("/bedtypes")
async def get_all_bed_types():
    return list(bed_types.values())

@app.get("/hospitals/{hospital_id}/beds")
async def get_all_bed_availability(hospital_id: int):
    available_beds = {}
    for (hospital_id_, bed_type_id), bed_availability in bed_availabilities.items():
        if hospital_id_ == hospital_id:
            available_beds[bed_types[bed_type_id].name] = bed_availability
    return available_beds if available_beds else {"message": "Bed information not available"}

@app.get("/hospitals/{hospital_id}/beds/{bed_type_name}")
async def get_bed_availability_by_type(hospital_id: int, bed_type_name: str):
    for bed_type_id, bed_type in bed_types.items():
        if bed_type.name == bed_type_name:
            bed_availability_key = (hospital_id, bed_type_id)
            if bed_availability_key in bed_availabilities:
                return bed_availabilities[bed_availability_key]
    return {"message": "Bed information not available"}

app.config["CORS_ORIGINS"] = ["https://suryanshroy.github.io"]
app.config["CORS_METHODS"] = ["GET", "POST"]
app.config["CORS_HEADERS"] = ["Content-Type", "Authorization"]
