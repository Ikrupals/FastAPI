from pydantic import BaseModel, ConfigDict


class Device(BaseModel):
    model_config = ConfigDict(extra="forbid")
    device_id: int
    device_name: str
    optional: str | None = None
