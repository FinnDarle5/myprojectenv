from fastapi import FastAPI, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust allowed origins based on your security needs
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
