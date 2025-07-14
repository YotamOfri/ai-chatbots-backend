from typing import TypedDict, List, Optional, Literal, Union
from datetime import datetime


class ConversationData(TypedDict):
    id: str
    origin: dict  # Can be further typed if needed


class PricingData(TypedDict):
    billable: bool
    pricing_model: str
    category: str
    type: str


class StatusData(TypedDict):
    id: str
    status: Literal["delivered", "read", "sent", "failed"]
    timestamp: str
    recipient_id: str
    conversation: ConversationData
    pricing: PricingData


class MetadataData(TypedDict):
    display_phone_number: str
    phone_number_id: str


class TextData(TypedDict):
    body: str


class MessageData(TypedDict):
    id: str
    # The 'from' field in the incoming data is mapped to 'from_' here due to Python keyword restrictions.
    from_: str
    timestamp: str
    text: TextData
    type: Literal["text", "image", "document", "audio", "video"]


# For TypedDict, we need to handle 'from' field differently
class MessageDataTypedDict(TypedDict):
    id: str
    timestamp: str
    text: TextData
    type: Literal["text", "image", "document", "audio", "video"]
    # Note: 'from' field will be accessed as whatsapp_data["messages"][0]["from"]


class ProfileData(TypedDict):
    name: str


class ContactData(TypedDict):
    profile: ProfileData
    wa_id: str


class ValueData(TypedDict):
    messaging_product: Literal["whatsapp"]
    metadata: MetadataData
    statuses: Optional[List[StatusData]]
    messages: Optional[List[MessageDataTypedDict]]
    contacts: Optional[List[ContactData]]


class ChangeData(TypedDict):
    value: ValueData
    field: Literal["messages"]


class EntryData(TypedDict):
    id: str
    changes: List[ChangeData]


class WhatsAppWebhookData(TypedDict):
    object: Literal["whatsapp_business_account"]
    entry: List[EntryData]
