from fastapi import APIRouter
from api.schemas.sanpo import FacilityTagWithCoordinate, Facility
from api.routers.serch_facilities import serch_facilities, get_nearest_facility

router = APIRouter()

@router.post("/search")
async def get_facilities(request: FacilityTagWithCoordinate) -> Facility:
    candidate_facilities = serch_facilities(request.lat, request.lon, request.facility_type)
    response = get_nearest_facility(request.lat, request.lon, candidate_facilities)
    return {"facility": response}