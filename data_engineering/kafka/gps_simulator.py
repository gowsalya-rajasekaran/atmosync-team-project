import json
import uuid
import math
from datetime import datetime, timezone, timedelta

# AtmoSync GPS Route Simulator

CONTAINER_ID = "CONT001"
ROUTE_ID = "ROUTE-MOM-CHE-001"

# Illustrative sea route: Mombasa to Chennai
SEA_ROUTE = [
    (-4.0435, 39.6682),    # Port of Mombasa
    (-2.0000, 43.0000),    # Indian Ocean
    (0.5000, 65.0000),     # Indian Ocean
    (5.0000, 78.0000),     # Near Sri Lanka
    (10.0000, 80.0000),    # Near Chennai
    (13.0827, 80.2707)     # Chennai Port
]

# Illustrative road route: Chennai to Coimbatore
ROAD_ROUTE = [
    (13.0827, 80.2707),    # Chennai Port
    (11.9400, 79.4900),    # Villupuram area
    (11.6643, 78.1460),    # Salem
    (11.3410, 77.7172),    # Erode
    (11.0168, 76.9558)     # Coimbatore Market
]


def calculate_heading(point1, point2):
    """Calculate direction of travel in degrees."""
    lat1, lon1 = map(math.radians, point1)
    lat2, lon2 = map(math.radians, point2)

    difference = lon2 - lon1

    x = math.sin(difference) * math.cos(lat2)
    y = (
        math.cos(lat1) * math.sin(lat2)
        - math.sin(lat1) * math.cos(lat2) * math.cos(difference)
    )

    heading = math.degrees(math.atan2(x, y))
    return round((heading + 360) % 360, 2)


def generate_gps_events():
    events = []

    current_time = datetime.now(timezone.utc)

    routes = [
        {
            "leg_id": "LEG001",
            "transport_mode": "SEA",
            "waypoints": SEA_ROUTE,
            "speed_kmh": 30,
            "time_gap_hours": 12
        },
        {
            "leg_id": "LEG002",
            "transport_mode": "ROAD",
            "waypoints": ROAD_ROUTE,
            "speed_kmh": 55,
            "time_gap_hours": 2
        }
    ]

    for route in routes:
        waypoints = route["waypoints"]

        for index, point in enumerate(waypoints):

            if index < len(waypoints) - 1:
                heading = calculate_heading(
                    point, waypoints[index + 1]
                )
            else:
                heading = 0.0

            event = {
                "event_id": str(uuid.uuid4()),
                "route_id": ROUTE_ID,
                "leg_id": route["leg_id"],
                "container_id": CONTAINER_ID,
                "transport_mode": route["transport_mode"],
                "latitude": point[0],
                "longitude": point[1],
                "speed_kmh": route["speed_kmh"],
                "heading": heading,
                "location_timestamp": current_time.isoformat()
            }

            events.append(event)

            current_time += timedelta(
                hours=route["time_gap_hours"]
            )

    return events


if __name__ == "__main__":
    print("Starting AtmoSync GPS Simulator...")

    gps_events = generate_gps_events()

    for event in gps_events:
        print(json.dumps(event))

    print("\nTotal GPS events generated:", len(gps_events))
    print("GPS simulation completed.")