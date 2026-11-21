WITH sensor_data AS (

    SELECT *
    FROM {{ ref('stg_container_sensors') }}

),

commodity_prices AS (

    SELECT
        INITCAP(TRIM(COMMODITY)) AS COMMODITY,
        PRICE_PER_KG
    FROM {{ ref('commodity_prices') }}

)

SELECT
    sensor_data.EVENT_ID,
    sensor_data.EVENT_TIMESTAMP,
    sensor_data.CONTAINER_ID,
    sensor_data.COMMODITY,
    sensor_data.QUANTITY_KG,
    commodity_prices.PRICE_PER_KG,

    ROUND(
        sensor_data.QUANTITY_KG * commodity_prices.PRICE_PER_KG,
        2
    ) AS ESTIMATED_CARGO_VALUE_INR

FROM sensor_data

LEFT JOIN commodity_prices
    ON sensor_data.COMMODITY = commodity_prices.COMMODITY
