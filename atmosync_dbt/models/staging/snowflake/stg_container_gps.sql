WITH source_data AS (

    SELECT *
    FROM {{ source('atmosync_raw', 'container_gps_raw') }}

),

extracted_data AS (

    SELECT
        TRIM(EVENT_ID) AS EVENT_ID,
        RAW_PAYLOAD:route_id::VARCHAR AS ROUTE_ID,
        RAW_PAYLOAD:leg_id::VARCHAR AS LEG_ID,
        RAW_PAYLOAD:container_id::VARCHAR AS CONTAINER_ID,
        UPPER(TRIM(RAW_PAYLOAD:transport_mode::VARCHAR)) AS TRANSPORT_MODE,
        RAW_PAYLOAD:latitude::FLOAT AS LATITUDE,
        RAW_PAYLOAD:longitude::FLOAT AS LONGITUDE,
        RAW_PAYLOAD:speed_kmh::FLOAT AS SPEED_KMH,
        RAW_PAYLOAD:heading::FLOAT AS HEADING,
        TRY_TO_TIMESTAMP_TZ(
            RAW_PAYLOAD:location_timestamp::VARCHAR
        ) AS LOCATION_TIMESTAMP,
        INGESTED_AT,

        ROW_NUMBER() OVER (
            PARTITION BY EVENT_ID
            ORDER BY INGESTED_AT DESC
        ) AS ROW_NUM

    FROM source_data

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

FROM extracted_data

WHERE ROW_NUM = 1
  AND EVENT_ID IS NOT NULL
  AND EVENT_ID != ''
  AND CONTAINER_ID IS NOT NULL
  AND CONTAINER_ID != ''
  AND LATITUDE BETWEEN -90 AND 90
  AND LONGITUDE BETWEEN -180 AND 180
