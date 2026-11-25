
WITH source_data AS (
    SELECT
        TRIM(EVENT_ID) AS EVENT_ID,
        EVENT_TIMESTAMP,
        TRIM(CONTAINER_ID) AS CONTAINER_ID,
        TEMPERATURE,
        HUMIDITY,
        VIBRATION,
        INITCAP(TRIM(COMMODITY)) AS COMMODITY,
        QUANTITY_KG,
        INGESTED_AT
    FROM {{ source('atmosync_raw', 'container_sensor_view') }}
),

cleaned_data AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY EVENT_ID
            ORDER BY
                INGESTED_AT DESC NULLS LAST,
                EVENT_TIMESTAMP DESC NULLS LAST
        ) AS ROW_NUM
    FROM source_data
)

SELECT
    EVENT_ID,
    EVENT_TIMESTAMP,
    CONTAINER_ID,
    TEMPERATURE,
    HUMIDITY,
    VIBRATION,
    COMMODITY,
    QUANTITY_KG,
    INGESTED_AT
FROM cleaned_data
WHERE ROW_NUM = 1
  AND EVENT_ID IS NOT NULL
  AND EVENT_ID != ''
  AND CONTAINER_ID IS NOT NULL
  AND CONTAINER_ID != ''
  AND LOWER(COMMODITY) = 'avocados'
