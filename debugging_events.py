from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from dataclasses import dataclass
import datetime


logs = [
    {
        "id": "0",
        "timestamp": "2025-01-01T00:00:00Z",
        "event": "EV Turned On",
    },
    {
        "id": "1",
        "timestamp": "2025-01-02T00:00:00Z",
        "event": "EV Turned Off",
    },
    {
        "id": "2",
        "timestamp": "2025-01-03T00:00:00Z",
        "event": "EV Turned On",
    },
    {
        "id": "3",
        "timestamp": "2025-01-04T00:00:00Z",
        "event": "EV Registered",
    },
    {
        "id": "4",
        "timestamp": "2025-01-05T00:00:00Z",
        "event": "EV Registration Failed",
        "meta": {
            "failure_reason": "Network Error",
        },
    },
    {
        "id": "5",
        "timestamp": "2025-01-06T00:00:00Z",
        "event": "EV Registration Re-Attempted",
    },
    {
        "id": "6",
        "timestamp": "2025-01-07T00:00:00Z",
        "event": "EV Registration Aborted",
    },
]


class EventQueryResult(BaseModel):
    timestamp: datetime.datetime


class DeviceRegistrationFailureReasons(BaseModel):
    event_ids: list[str]
    start_time: datetime.datetime
    end_time: datetime.datetime
    failure_reason: str


@dataclass
class Params:
    logs: list[dict]


agent = Agent(
    "google-gla:gemini-1.5-flash",
    deps_type=Params,
    output_type=DeviceRegistrationFailureReasons,
)


@agent.system_prompt
def get_system_prompt(ctx: RunContext[Params]) -> str:
    return f"You are a knowledge base for the following events: {ctx.deps.logs}"


result = agent.run_sync(
    "What was the failure reason for the EV registration to fail?",
    deps=Params(logs=logs),
)
print(f"reason for failure: {result.output.failure_reason}")
print(f"offending events:")
for event_id in result.output.event_ids:
    event = next((e for e in logs if e["id"] == event_id), None)
    if event:
        print(f"event {event_id} details: {event}")
