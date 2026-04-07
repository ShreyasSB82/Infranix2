from fastapi import APIRouter, HTTPException
from interior_backend.models import InteriorRequest, InteriorResponse
from interior_backend.floorplan_engine import generate_floor_plan

router = APIRouter(tags=["interior"])


@router.post("/generate", response_model=InteriorResponse)
async def generate_interior(body: InteriorRequest):
    """
    Generate a floor plan with rectangular rooms + triangular corner rooms.

    Accepts the building footprint (GeoJSON Polygon geometry) extracted from
    the site plan's building zone, plus user preferences.
    """
    try:
        result = generate_floor_plan(
            building_geojson=body.building_geojson,
            num_floors=body.num_floors,
            bedrooms=body.bedrooms,
            bathrooms=body.bathrooms,
            has_study=body.has_study,
            style=body.style,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Floor plan engine error: {e}")

    return result
