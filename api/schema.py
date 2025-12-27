from typing import Any, Dict, List, Optional, Literal
from pydantic import BaseModel, Field

SourceType = Literal["hosted", "git", "path", "sdk", "unknown"]

class Dependency(BaseModel):
    name: str
    source_type: SourceType
    constraint: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)

class Environment(BaseModel):
    sdk: Optional[str] = None
    flutter: Optional[str] = None

class PubspecMeta(BaseModel):
    name: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    homepage: Optional[str] = None
    repository: Optional[str] = None
    issue_tracker: Optional[str] = None
    publish_to: Optional[str] = None

    environment: Environment = Field(default_factory=Environment)

    dependencies: List[Dependency] = Field(default_factory=list)
    dev_dependencies: List[Dependency] = Field(default_factory=list)
    dependency_overrides: List[Dependency] = Field(default_factory=list)
