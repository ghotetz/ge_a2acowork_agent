#MCP svr framework
from mcp.server.fastmcp import FastMCP
#MCP svr name
mcp = FastMCP("expense-rules")

#test rules
LIMITS = {
    "A" : {"lodging": 250_000, "per_diem": 80_000},
    "B" : {"lodging": 180_000, "per_diem": 60_000},
    "C" : {"lodging": 120_000, "per_diem": 40_000}
}

CITY_GRADE = {"뉴욕": "A", "도쿄": "A", "런던": "A", "싱가포르": "B", "하노이": "B", "부산": "C", "대전": "C"}

#mcp tool1 max limit check
@mcp.tool()
def get_travel_limit(city: str) -> dict:
    """출장 도시와 1박 숙박비, 일당 한도를 원단위로 반환한다"""
    #not inlucded in CITY_GRADE all B
    grade = CITY_GRADE.get(city, "B")
    #return grade, limit, standard grade written in note
    return {"city": city, "grade": grade, **LIMITS[grade],
            "note": "목록에 없는 도시는 B등급 적용" if city not in CITY_GRADE else ""}

#mcp tool 2 whole trip budget check
@mcp.tool()
def estimate_trip_bedget(city: str, nights: int) -> dict:
    """도시와 숙박 일수로 출장 예산 한도를 계산한다. 일당은 숙박일+1일"""
    limit = get_travel_limit(city)
    #lodging * days
    lodging = limit["lodging"] * nights
    #per_diem * days
    per_diem = limit["per_diem"] * nights
    #budget cap return
    return {"city": city, "nights": nights, "lodging_total": lodging, "per_diem_total": per_diem, "budget_cap": lodging + per_diem}

#server rusn
if __name__ == "__main__":
    mcp.run()