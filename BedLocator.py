from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://suryanshroy.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Hospital(BaseModel):
    id: int
    name: str

class BedType(BaseModel):
    id: int
    name: str

class BedAvailability(BaseModel):
    total_beds: int
    available_beds: int

class BedAvailabilityRequest(BaseModel):
    hospitalName: str
    bedType: str

hospitals = {
    1: Hospital(id=1, name="AIIMS"),
    2: Hospital(id=2, name="IGIMS"),
    3: Hospital(id=3, name="PMCH"),
    4: Hospital(id=4, name='Paras')
}

bed_types = {
    1: BedType(id=1, name="ICU"),
    2: BedType(id=2, name="Ventillator"),
    3: BedType(id=3, name="General"),
}

bed_availabilities = {
    # AIIMS
    ('AIIMS', "ICU"): BedAvailability(total_beds=100, available_beds=82),
    ('AIIMS', "Ventillator"): BedAvailability(total_beds=118, available_beds=56),
    ('AIIMS', "General"): BedAvailability(total_beds=85, available_beds=70),
    # IGIMS
    ('IGIMS', "ICU"): BedAvailability(total_beds=50, available_beds=38),
    ('IGIMS', "Ventillator"): BedAvailability(total_beds=37, available_beds=29),
    ('IGIMS', "General"): BedAvailability(total_beds=42, available_beds=40),
    # PMCH
    ('PMCH', "ICU"): BedAvailability(total_beds=88, available_beds=60),
    ('PMCH', "Ventillator"): BedAvailability(total_beds=49, available_beds=38),
    ('PMCH', "General"): BedAvailability(total_beds=75, available_beds=68),
    #Paras
    ('Paras', "ICU"): BedAvailability(total_beds=90, available_beds=68),
    ('Paras', "Ventillator"): BedAvailability(total_beds=66, available_beds=55),
    ('Paras', "General"): BedAvailability(total_beds=106, available_beds=83),
}

@app.post("/bedavailability")
async def check_bed_Availability(request: BedAvailabilityRequest):
    hospital_name = request.hospitalName
    bed_type = request.bedType

    bed_availability_key = (hospital_name, bed_type)
    return bed_availabilities[bed_availability_key]

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
