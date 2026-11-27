
WITH ranked_locations AS (

    SELECT
        EVENT_ID,
        ROUTE_ID,
        LEG_ID,
        CONTAINER_ID,
        TRANSPORT_MODE,
        LATITUDE,
        LONGITUDE,
        SPEED_KMH,
        HEADING,
        LOCATION_TIMESTAMP,
        INGESTED_AT,

        ROW_NUMBER() OVER (
            PARTITION BY ROUTE_ID, CONTAINER_ID
            ORDER BY LOCATION_TIMESTAMP DESC, INGESTED_AT DESC
        ) AS ROW_NUM

    FROM {{ ref('stg_container_gps') }}

)

SELECT
    EVENT_ID,
    ROUTE_ID,
    LEG_ID,
    CONTAINER_ID,
    TRANSPORT_MODE,
    LATITUDE,
    LONGITUDE,
    SPEED_KMH,
    HEADING,
    LOCATION_TIMESTAMP,
    INGESTED_AT

FROM ranked_locations

WHERE ROW_NUM = 1
