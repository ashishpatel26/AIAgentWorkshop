from typing import Optional, Literal
from pydantic import BaseModel, Field
from openai import OpenAI
import os
import logging

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4o"

# --------------------------------------------------------------
# Step 1: Define the data models for routing and responses
# --------------------------------------------------------------


class CalendarRequestType(BaseModel):
    """Router LLM call: Determine the type of calendar request"""

    request_type: Literal["new_event", "modify_event", "other"] = Field(
        description="Type of calendar request being made"
    )
    confidence_score: float = Field(description="Confidence score between 0 and 1")
    description: str = Field(description="Cleaned description of the request")


class NewEventDetails(BaseModel):
    """Details for creating a new event"""

    name: str = Field(description="Name of the event")
    date: str = Field(description="Date and time of the event (ISO 8601)")
    duration_minutes: int = Field(description="Duration in minutes")
    participants: list[str] = Field(description="List of participants")


class Change(BaseModel):
    """Details for changing an existing event"""

    field: str = Field(description="Field to change")
    new_value: str = Field(description="New value for the field")


class ModifyEventDetails(BaseModel):
    """Details for modifying an existing event"""

    event_identifier: str = Field(
        description="Description to identify the existing event"
    )
    changes: list[Change] = Field(description="List of changes to make")
    participants_to_add: list[str] = Field(description="New participants to add")
    participants_to_remove: list[str] = Field(description="Participants to remove")


class CalendarResponse(BaseModel):
    """Final response format"""

    success: bool = Field(description="Whether the operation was successful")
    message: str = Field(description="User-friendly response message")
    calendar_link: Optional[str] = Field(description="Calendar link if applicable")


# --------------------------------------------------------------
# Step 2: Define the routing and processing functions
# --------------------------------------------------------------


def route_calendar_request(user_input: str) -> CalendarRequestType:
    """Router LLM call to determine the type of calendar request"""
    logger.info("Routing calendar request")

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Determine if this is a request to create a new calendar event or modify an existing one.",
            },
            {"role": "user", "content": user_input},
        ],
        response_format=CalendarRequestType,
    )
    result = completion.choices[0].message.parsed
    logger.info(
        f"Request routed as: {result.request_type} with confidence: {result.confidence_score}"
    )
    return result


def handle_new_event(description: str) -> CalendarResponse:
    """Process a new event request"""
    logger.info("Processing new event request")

    # Get event details
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Extract details for creating a new calendar event.",
            },
            {"role": "user", "content": description},
        ],
        response_format=NewEventDetails,
    )
    details = completion.choices[0].message.parsed

    logger.info(f"New event: {details.model_dump_json(indent=2)}")

    # Generate response
    return CalendarResponse(
        success=True,
        message=f"Created new event '{details.name}' for {details.date} with {', '.join(details.participants)}",
        calendar_link=f"calendar://new?event={details.name}",
    )


def handle_modify_event(description: str) -> CalendarResponse:
    """Process an event modification request"""
    logger.info("Processing event modification request")

    # Get modification details
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Extract details for modifying an existing calendar event.",
            },
            {"role": "user", "content": description},
        ],
        response_format=ModifyEventDetails,
    )
    details = completion.choices[0].message.parsed

    logger.info(f"Modified event: {details.model_dump_json(indent=2)}")

    # Generate response
    return CalendarResponse(
        success=True,
        message=f"Modified event '{details.event_identifier}' with the requested changes",
        calendar_link=f"calendar://modify?event={details.event_identifier}",
    )


def process_calendar_request(user_input: str) -> Optional[CalendarResponse]:
    """Main function implementing the routing workflow"""
    logger.info("Processing calendar request")

    # Route the request
    route_result = route_calendar_request(user_input)

    # Check confidence threshold
    if route_result.confidence_score < 0.7:
        logger.warning(f"Low confidence score: {route_result.confidence_score}")
        return None

    # Route to appropriate handler
    if route_result.request_type == "new_event":
        return handle_new_event(route_result.description)
    elif route_result.request_type == "modify_event":
        return handle_modify_event(route_result.description)
    else:
        logger.warning("Request type not supported")
        return None


# --------------------------------------------------------------
# Step 3: Test with new event
# --------------------------------------------------------------

new_event_input = "Let's schedule a team meeting next Tuesday at 2pm with Alice and Bob"
result = process_calendar_request(new_event_input)
if result:
    print(f"Response: {result.message}")

# --------------------------------------------------------------
# Step 4: Test with modify event
# --------------------------------------------------------------

modify_event_input = (
    "Can you move the team meeting with Alice and Bob to Wednesday at 3pm instead?"
)
result = process_calendar_request(modify_event_input)
if result:
    print(f"Response: {result.message}")

# --------------------------------------------------------------
# Step 5: Test with invalid request
# --------------------------------------------------------------

invalid_input = "What's the weather like today?"
result = process_calendar_request(invalid_input)
if not result:
    print("Request not recognized as a calendar operation")