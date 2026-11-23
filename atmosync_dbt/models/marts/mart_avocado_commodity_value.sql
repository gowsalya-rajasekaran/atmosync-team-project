WITH avocado_sensors AS (
    SELECT *
    FROM {{ ref('stg_avocado_sensors') }}
),

avocado_prices AS (
    SELECT
        INITCAP(TRIM(COMMODITY)) AS COMMODITY,
        PRICE_PER_KG
    FROM {{ ref('commodity_prices_avocado_test') }}
)

SELECT
    sensors.EVENT_ID,
    sensors.EVENT_TIMESTAMP,
    sensors.CONTAINER_ID,
    sensors.COMMODITY,
    sensors.QUANTITY_KG,
    prices.PRICE_PER_KG,

    sensors.QUANTITY_KG * prices.PRICE_PER_KG
        AS TOTAL_COMMODITY_VALUE,

    sensors.TEMPERATURE,
    sensors.HUMIDITY,
    sensors.VIBRATION

FROM avocado_sensors AS sensors

LEFT JOIN avocado_prices AS prices
    ON LOWER(sensors.COMMODITY) = LOWER(prices.COMMODITY)

