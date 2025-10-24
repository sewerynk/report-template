"""Tests for data models."""

from datetime import date

import pytest
from pydantic import ValidationError

from report_template.models import (
    FeatureDevReport,
    Milestone,
    Priority,
    Risk,
    Status,
    Task,
    TeamMember,
)


def test_team_member_creation():
    """Test TeamMember model creation."""
    member = TeamMember(
        name="John Doe",
        role="Developer",
        email="john@example.com"
    )
    assert member.name == "John Doe"
    assert member.role == "Developer"
    assert member.email == "john@example.com"


def test_team_member_without_email():
    """Test TeamMember creation without email."""
    member = TeamMember(name="Jane Doe", role="Manager")
    assert member.name == "Jane Doe"
    assert member.email is None


def test_task_creation():
    """Test Task model creation."""
    task = Task(
        title="Implement feature",
        assignee="John Doe",
        status=Status.IN_PROGRESS,
        priority=Priority.HIGH,
        due_date=date(2024, 12, 31)
    )
    assert task.title == "Implement feature"
    assert task.status == Status.IN_PROGRESS
    assert task.priority == Priority.HIGH


def test_task_default_priority():
    """Test Task default priority is MEDIUM."""
    task = Task(
        title="Test task",
        status=Status.NOT_STARTED
    )
    assert task.priority == Priority.MEDIUM


def test_milestone_completion_validation():
    """Test Milestone completion percentage validation."""
    # Valid percentages
    milestone = Milestone(
        name="Release 1.0",
        target_date=date(2024, 12, 31),
        status=Status.IN_PROGRESS,
        completion_percentage=50
    )
    assert milestone.completion_percentage == 50

    # Invalid percentage (> 100)
    with pytest.raises(ValidationError):
        Milestone(
            name="Release 1.0",
            target_date=date(2024, 12, 31),
            status=Status.IN_PROGRESS,
            completion_percentage=150
        )

    # Invalid percentage (< 0)
    with pytest.raises(ValidationError):
        Milestone(
            name="Release 1.0",
            target_date=date(2024, 12, 31),
            status=Status.IN_PROGRESS,
            completion_percentage=-10
        )


def test_risk_creation():
    """Test Risk model creation."""
    risk = Risk(
        description="API downtime",
        impact=Priority.HIGH,
        likelihood=Priority.LOW,
        mitigation="Use fallback service",
        owner="DevOps Team"
    )
    assert risk.description == "API downtime"
    assert risk.impact == Priority.HIGH
    assert risk.likelihood == Priority.LOW


def test_feature_dev_report_minimal():
    """Test FeatureDevReport with minimal required fields."""
    report = FeatureDevReport(
        title="Test Report",
        project_name="Test Project",
        author="Test Author",
        feature_name="Test Feature",
        summary="Test summary"
    )
    assert report.title == "Test Report"
    assert report.feature_name == "Test Feature"
    assert report.date == date.today()
    assert report.version == "1.0"
    assert len(report.team_members) == 0
    assert len(report.tasks) == 0


def test_feature_dev_report_complete():
    """Test FeatureDevReport with all fields."""
    report = FeatureDevReport(
        title="Feature Report",
        project_name="My Project",
        author="John Doe",
        feature_name="OAuth2 Auth",
        summary="OAuth2 implementation",
        repository="https://github.com/org/repo",
        branch="feature/oauth",
        sprint="Sprint 5",
        team_members=[
            TeamMember(name="John Doe", role="Developer")
        ],
        objectives=["Implement OAuth2", "Add security"],
        tasks=[
            Task(
                title="Design flow",
                status=Status.COMPLETED,
                priority=Priority.HIGH
            )
        ],
        milestones=[
            Milestone(
                name="MVP",
                target_date=date(2024, 12, 31),
                status=Status.IN_PROGRESS,
                completion_percentage=75
            )
        ],
        risks=[
            Risk(
                description="Provider downtime",
                impact=Priority.HIGH,
                likelihood=Priority.LOW,
                mitigation="Use fallback"
            )
        ]
    )
    assert report.feature_name == "OAuth2 Auth"
    assert len(report.team_members) == 1
    assert len(report.tasks) == 1
    assert len(report.milestones) == 1
    assert len(report.risks) == 1


def test_custom_fields():
    """Test custom_fields dictionary."""
    report = FeatureDevReport(
        title="Test",
        project_name="Test",
        author="Test",
        feature_name="Test",
        summary="Test",
        custom_fields={
            "jira_epic": "PROJ-123",
            "estimated_hours": 40,
            "tech_stack": "Python, FastAPI"
        }
    )
    assert report.custom_fields["jira_epic"] == "PROJ-123"
    assert report.custom_fields["estimated_hours"] == 40


def test_date_parsing():
    """Test date field parsing from various formats."""
    # Date object
    report1 = FeatureDevReport(
        title="Test",
        project_name="Test",
        author="Test",
        feature_name="Test",
        summary="Test",
        date=date(2024, 10, 24)
    )
    assert report1.date == date(2024, 10, 24)

    # ISO string
    report2 = FeatureDevReport(
        title="Test",
        project_name="Test",
        author="Test",
        feature_name="Test",
        summary="Test",
        date="2024-10-24"
    )
    assert report2.date == date(2024, 10, 24)


def test_model_serialization():
    """Test model can be serialized to dict."""
    report = FeatureDevReport(
        title="Test",
        project_name="Test",
        author="Test",
        feature_name="Test",
        summary="Test"
    )
    data = report.model_dump()
    assert isinstance(data, dict)
    assert data["title"] == "Test"
    assert data["feature_name"] == "Test"
