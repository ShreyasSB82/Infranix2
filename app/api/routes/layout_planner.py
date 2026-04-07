# API routes for layout planning, providing endpoints to generate multiple site layout options.

from fastapi import APIRouter, HTTPException

from app.models.layout_planner import MultiLayoutRequest, MultiLayoutResponse
from app.services.generative_engine import generate_multiple_layouts, list_strategies

router = APIRouter(tags=["layout-planner"])


@router.get("/strategies")
async def get_strategies():
    """Return metadata about all available layout strategies."""
    return {"strategies": list_strategies()}


@router.post("/generate", response_model=MultiLayoutResponse)
async def generate_layouts(body: MultiLayoutRequest):
    """
    Generate multiple diverse site layout options.

    Accepts a GeoJSON plot polygon, percentage-based zone preferences,
    and site constraints. Returns top N scored layouts.
    """
    prefs_fractions = body.preferences.as_fractions()

    try:
        layouts = generate_multiple_layouts(
            plot_geojson=body.plot_geojson,
            preferences=prefs_fractions,
            constraints=body.constraints.model_dump(),
            n_layouts=body.n_layouts,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Engine error: {e}")

    plot_area = layouts[0]["stats"]["plot_area_sqm"] if layouts else 0.0

    return MultiLayoutResponse(
        layouts=layouts,
        plot_area_sqm=plot_area,
        preferences_used=prefs_fractions,
        n_generated=len(layouts),
    )
