from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class IngestResponse(BaseModel):
    status: str
    indexed: int


class DbIngestRequest(BaseModel):
    connection_string: str
    query: str
    columns: list[str]


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    status: str
    answer: str
    steps: list[dict]


class ResetResponse(BaseModel):
    status: str


class CacheResetResponse(BaseModel):
    status: str
