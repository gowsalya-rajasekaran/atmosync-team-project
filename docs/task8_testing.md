# Task 8 – Continuous Ingestion, Duplicate Prevention, Restart Recovery and Invalid-Message Handling

## 1. Objective

To implement and validate reliable Kafka-to-Snowflake ingestion for the AtmoSync IoT Container Sensor Data Pipeline.

The implementation covers continuous ingestion, duplicate prevention, consumer restart recovery, invalid-message handling through a Dead Letter Queue (DLQ), and recovery after a failed Snowflake write.

## 2. Implementation Details

### 2.1 Continuous Kafka Ingestion

- Kafka topic: `atmosync-sensor-data`
- Kafka broker: `localhost:9092`
- Consumer group: `atmosync-snowflake-consumer`
- Consumer reads sensor events continuously.
- Sensor events are validated before being inserted into Snowflake.
- Automatic offset commits are disabled.
- Kafka offsets are committed only after successful Snowflake writes.

### 2.2 Duplicate Prevention

Snowflake `MERGE` is used to prevent duplicate event IDs.

The consumer matches incoming events against existing records using `EVENT_ID`.

- Existing event ID: No additional record is inserted.
- New event ID: A new record is inserted.

The duplicate replay test confirmed that replaying an existing event did not create another Snowflake record.

### 2.3 Consumer Restart Recovery

The consumer was stopped and restarted.

New sensor events were published after restarting the consumer.

The consumer successfully processed the new events and stored them in Snowflake.

### 2.4 Invalid-Message Handling

The consumer validates incoming JSON messages and checks the required event fields.

Invalid messages are sent to the Dead Letter Queue.

DLQ topic:

`atmosync-sensor-data-dlq`

The DLQ record includes:
- Original message
- Error description
- Failure timestamp
- Source topic

The consumer commits the invalid message's offset only after successful DLQ delivery.

An isolated malformed JSON test confirmed that the invalid message was routed to the DLQ.

### 2.5 Snowflake Write Failure and Recovery

A separate test topic and consumer group were created:

- Topic: `atmosync-failure-test`
- Consumer group: `atmosync-failure-test-group`

A valid test event was published:

`FAILURE-TEST-001`

A temporary consumer copy was used with an intentionally invalid Snowflake table name.

The test confirmed:
1. Kafka delivered the event.
2. Python validation succeeded.
3. Snowflake rejected the write.
4. The consumer logged that the offset was not committed.
5. The consumer stopped without committing the failed message.
6. The test topic retained the message.

The correct Snowflake table name and target alias were then restored in the temporary consumer.

The same event was retried using the same consumer group.

The consumer successfully stored and committed the event.

Final verification:
- Kafka current offset: 1
- Kafka log-end offset: 1
- Kafka lag: 0
- Snowflake records matching `FAILURE-TEST-001`: 1

This confirms successful retry after a failed Snowflake write without creating duplicate records.

## 3. Test Results

| Test Case | Result |
|---|---|
| Kafka broker restart | Passed |
| Existing topic preservation | Passed |
| Continuous event ingestion | Passed |
| Duplicate event replay | Passed |
| Consumer restart recovery | Passed |
| Invalid JSON handling | Passed |
| DLQ message delivery | Passed |
| Offset commit after successful Snowflake write | Passed |
| Snowflake write failure handling | Passed |
| Offset remains uncommitted after failed write | Passed |
| Retry after Snowflake recovery | Passed |
| Exactly one Snowflake record after retry | Passed |

## 4. Snowflake Data Validation

The raw Snowflake table:

`ATMOSYNC_DB.RAW_DATA.CONTAINER_EVENTS_RAW`

At the time of validation:

- Total records: 77
- Unique event IDs: 77
- Records with NULL `INGESTED_AT`: 20

The 20 records with NULL ingestion timestamps were older records from before the ingestion timestamp fix. They were not artificially backfilled.

The failure-recovery test event was separately verified to have exactly one matching record.

## 5. Kafka Consumer Configuration

The production consumer uses:

- `enable_auto_commit=False`
- Configurable Kafka input topic
- Configurable consumer group
- Configurable offset reset behaviour
- Manual offset commits after successful processing

For invalid messages, the offset is committed only after successful DLQ delivery.

For Snowflake or other processing failures, the exception is raised and the offset is not committed.

## 6. Limitations and Pending Validation

The following scenario has not yet been tested:

A hard process crash occurring specifically after a successful Snowflake write but before the Kafka offset commit.

The current implementation uses Snowflake `MERGE` to protect against duplicate records if an event is replayed, but this exact crash window still requires a separate runtime test.

## 7. Conclusion

Task 8 was functionally implemented and tested.

The tests demonstrated continuous Kafka-to-Snowflake ingestion, duplicate prevention, consumer restart recovery, invalid-message routing to the DLQ, and recovery after a failed Snowflake write.

The isolated failure-recovery test confirmed that a failed Snowflake write did not commit the Kafka offset and that the original event could be retried successfully, resulting in exactly one Snowflake record.
