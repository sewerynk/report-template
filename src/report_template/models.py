"""
Data models for different report types using Pydantic for validation.
"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class ReportType(str, Enum):
    """Supported report types."""

    FEATURE_DEV = "feature_dev"
    PROGRAM_MGMT = "program_mgmt"
    ENGINEERING_INIT = "engineering_init"


class OutputFormat(str, Enum):
    """Supported output formats."""

    MARKDOWN = "markdown"
    HTML = "html"
    PDF = "pdf"
    DOCX = "docx"


class Status(str, Enum):
    """Project/task status options."""

    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    BLOCKED = "Blocked"
    ON_HOLD = "On Hold"


class Priority(str, Enum):
    """Priority levels."""

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class Milestone(BaseModel):
    """Represents a project milestone."""

    name: str
    target_date: date
    status: Status
    completion_percentage: int = Field(ge=0, le=100, default=0)
    description: Optional[str] = None


class Task(BaseModel):
    """Represents a task or work item."""

    title: str
    assignee: Optional[str] = None
    status: Status
    priority: Priority = Priority.MEDIUM
    due_date: Optional[date] = None
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class TeamMember(BaseModel):
    """Represents a team member."""

    name: str
    role: str
    email: Optional[str] = None


class Risk(BaseModel):
    """Represents a project risk."""

    description: str
    impact: Priority
    likelihood: Priority
    mitigation: str
    owner: Optional[str] = None


class ReportData(BaseModel):
    """Base model for all reports."""

    title: str
    project_name: str
    author: str
    date: date = Field(default_factory=date.today)
    version: str = "1.0"
    summary: str
    custom_fields: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("date", mode="before")
    @classmethod
    def parse_date(cls, v: Any) -> date:
        """Parse date from various formats."""
        if isinstance(v, date):
            return v
        if isinstance(v, datetime):
            return v.date()
        if isinstance(v, str):
            return datetime.fromisoformat(v).date()
        return v


class FeatureDevReport(ReportData):
    """Model for feature development reports."""

    feature_name: str
    repository: Optional[str] = None
    branch: Optional[str] = None
    sprint: Optional[str] = None
    team_members: List[TeamMember] = Field(default_factory=list)
    objectives: List[str] = Field(default_factory=list)
    requirements: List[str] = Field(default_factory=list)
    technical_approach: str = ""
    architecture_notes: str = ""
    tasks: List[Task] = Field(default_factory=list)
    testing_strategy: str = ""
    deployment_plan: str = ""
    risks: List[Risk] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    milestones: List[Milestone] = Field(default_factory=list)
    progress_notes: str = ""


class ProgramMgmtReport(ReportData):
    """Model for program management reports."""

    program_name: str
    stakeholders: List[str] = Field(default_factory=list)
    reporting_period: str
    executive_summary: str = ""
    status: Status
    budget_summary: str = ""
    team_members: List[TeamMember] = Field(default_factory=list)
    milestones: List[Milestone] = Field(default_factory=list)
    key_achievements: List[str] = Field(default_factory=list)
    challenges: List[str] = Field(default_factory=list)
    risks: List[Risk] = Field(default_factory=list)
    upcoming_activities: List[str] = Field(default_factory=list)
    decisions_needed: List[str] = Field(default_factory=list)
    kpis: Dict[str, Any] = Field(default_factory=dict)


class EngineeringInitReport(ReportData):
    """Model for engineering initiative reports."""

    initiative_name: str
    initiative_type: str  # e.g., "Infrastructure", "Architecture", "Process Improvement"
    sponsors: List[str] = Field(default_factory=list)
    team_members: List[TeamMember] = Field(default_factory=list)
    start_date: Optional[date] = None
    target_completion_date: Optional[date] = None
    status: Status
    objectives: List[str] = Field(default_factory=list)
    scope: str = ""
    technical_details: str = ""
    architecture_diagrams: List[str] = Field(default_factory=list)  # File paths or URLs
    implementation_phases: List[Dict[str, Any]] = Field(default_factory=list)
    success_criteria: List[str] = Field(default_factory=list)
    milestones: List[Milestone] = Field(default_factory=list)
    risks: List[Risk] = Field(default_factory=list)
    resources_required: str = ""
    impact_analysis: str = ""
    rollout_strategy: str = ""
