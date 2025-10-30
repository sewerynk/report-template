"""
Example: Generating a Feature Development Report
"""

from datetime import date, timedelta
from pathlib import Path

from report_template import (
    FeatureDevReport,
    ReportGenerator,
    ReportType,
)
from report_template.models import ActionPoint, Milestone, Priority, Status, Task, TeamMember


def main():
    """Generate a sample feature development report."""

    # Create report data
    report = FeatureDevReport(
        title="User Authentication Feature - Development Report",
        project_name="MyApp Platform",
        author="John Doe",
        feature_name="OAuth2 Authentication System",
        repository="https://github.com/myorg/myapp",
        branch="feature/oauth2-auth",
        sprint="Sprint 12",
        summary="Implementation of a comprehensive OAuth2 authentication system with support "
        "for multiple providers including Google, GitHub, and Microsoft.",
        team_members=[
            TeamMember(name="John Doe", role="Lead Developer", email="john@example.com"),
            TeamMember(name="Jane Smith", role="Backend Developer", email="jane@example.com"),
            TeamMember(name="Bob Johnson", role="Security Engineer", email="bob@example.com"),
        ],
        objectives=[
            "Implement OAuth2 authentication flow",
            "Support multiple OAuth providers (Google, GitHub, Microsoft)",
            "Add session management with Redis",
            "Implement rate limiting and security measures",
            "Create comprehensive test coverage",
        ],
        requirements=[
            "Password must be at least 12 characters with complexity requirements",
            "Support multi-factor authentication (MFA)",
            "Implement rate limiting (5 requests per minute)",
            "Session timeout after 30 minutes of inactivity",
            "All authentication endpoints must use HTTPS",
        ],
        technical_approach="""
We are using FastAPI for the backend framework with the following components:

- **OAuth2 Library**: Authlib for OAuth2 client implementation
- **Token Management**: JWT tokens with RS256 signing
- **Session Storage**: Redis for distributed session management
- **Database**: PostgreSQL for user data and OAuth credentials
- **Security**: Argon2 for password hashing

The authentication flow follows the OAuth2 Authorization Code Grant pattern.
        """,
        architecture_notes="""
The system follows a microservices architecture:

1. Auth Service: Handles OAuth flows and token generation
2. User Service: Manages user profiles and permissions
3. Session Service: Redis-based session management
4. API Gateway: Routes requests and validates tokens

All services communicate via REST APIs with JWT authentication.
        """,
        tasks=[
            Task(
                title="Design OAuth2 flow and database schema",
                assignee="John Doe",
                status=Status.COMPLETED,
                priority=Priority.HIGH,
                jira_id="AUTH-101",
                target_start_date=date.today() - timedelta(days=10),
                target_end_date=date.today() - timedelta(days=5),
            ),
            Task(
                title="Implement OAuth2 provider integrations",
                assignee="Jane Smith",
                status=Status.IN_PROGRESS,
                priority=Priority.HIGH,
                jira_id="AUTH-102",
                target_start_date=date.today() - timedelta(days=3),
                target_end_date=date.today() + timedelta(days=4),
                due_date=date.today() + timedelta(days=7),
            ),
            Task(
                title="Set up Redis session management",
                assignee="John Doe",
                status=Status.IN_PROGRESS,
                priority=Priority.MEDIUM,
                jira_id="AUTH-103",
                target_start_date=date.today() - timedelta(days=2),
                target_end_date=date.today() + timedelta(days=3),
                due_date=date.today() + timedelta(days=5),
            ),
            Task(
                title="Implement rate limiting middleware",
                assignee="Bob Johnson",
                status=Status.NOT_STARTED,
                priority=Priority.MEDIUM,
                jira_id="AUTH-104",
                target_start_date=date.today() + timedelta(days=3),
                target_end_date=date.today() + timedelta(days=8),
                due_date=date.today() + timedelta(days=10),
            ),
            Task(
                title="Security audit and penetration testing",
                assignee="Bob Johnson",
                status=Status.NOT_STARTED,
                priority=Priority.CRITICAL,
                jira_id="AUTH-105",
                target_start_date=date.today() + timedelta(days=10),
                target_end_date=date.today() + timedelta(days=13),
                due_date=date.today() + timedelta(days=14),
            ),
        ],
        milestones=[
            Milestone(
                name="MVP - Basic OAuth Flow",
                target_date=date.today() + timedelta(days=7),
                status=Status.IN_PROGRESS,
                completion_percentage=75,
                description="Basic OAuth2 authentication with Google provider",
            ),
            Milestone(
                name="Multi-Provider Support",
                target_date=date.today() + timedelta(days=14),
                status=Status.NOT_STARTED,
                completion_percentage=0,
                description="Support for GitHub and Microsoft OAuth providers",
            ),
            Milestone(
                name="Production Ready",
                target_date=date.today() + timedelta(days=21),
                status=Status.NOT_STARTED,
                completion_percentage=0,
                description="Security audit complete, all tests passing, documentation done",
            ),
        ],
        testing_strategy="""
Comprehensive testing approach:

1. **Unit Tests**: 80%+ coverage for all authentication logic
2. **Integration Tests**: Test OAuth flows with mock providers
3. **Security Tests**: SQL injection, XSS, CSRF protection
4. **Load Tests**: 1000 concurrent users authentication
5. **E2E Tests**: Complete user registration and login flows

Using pytest, pytest-asyncio, and locust for load testing.
        """,
        deployment_plan="""
Phased rollout strategy:

1. **Week 1**: Deploy to development environment
2. **Week 2**: Internal beta testing with team
3. **Week 3**: Deploy to staging, QA validation
4. **Week 4**: Production deployment with feature flag
5. **Week 5**: Gradual rollout (10% -> 50% -> 100%)

Rollback plan: Feature flag can instantly disable new auth system.
        """,
        action_points=[
            ActionPoint(
                description="Complete security audit of authentication flow",
                priority=Priority.CRITICAL,
                status=Status.IN_PROGRESS,
                owner="Bob Johnson",
                due_date=date.today() + timedelta(days=7),
            ),
            ActionPoint(
                description="Set up Redis cluster with replication for production",
                priority=Priority.HIGH,
                status=Status.NOT_STARTED,
                owner="DevOps Team",
                due_date=date.today() + timedelta(days=14),
            ),
            ActionPoint(
                description="Implement monitoring for OAuth provider status",
                priority=Priority.MEDIUM,
                status=Status.NOT_STARTED,
                owner="John Doe",
                due_date=date.today() + timedelta(days=21),
            ),
        ],
        dependencies=[
            "Redis cluster setup (DevOps)",
            "SSL certificates for OAuth callbacks",
            "OAuth app registration with Google, GitHub, Microsoft",
            "Database migration for user schema changes",
        ],
        progress_notes="""
**Week 1 Progress:**
- Completed database schema design
- Set up development OAuth apps with Google
- Initial implementation of OAuth flow in progress
- Redis integration 80% complete

**Blockers:**
- Waiting for OAuth app approval from Microsoft (submitted 3 days ago)

**Next Week:**
- Complete Google OAuth integration
- Start GitHub provider integration
- Begin rate limiting implementation
        """,
    )

    # Initialize generator
    generator = ReportGenerator()

    # Generate reports in different formats
    output_dir = Path("examples/output")
    output_dir.mkdir(exist_ok=True)

    print("Generating reports...")

    # Markdown
    md_path = generator.generate_to_file(
        report, ReportType.FEATURE_DEV, output_dir / "feature_dev_report.md"
    )
    print(f"✓ Markdown report: {md_path}")

    # HTML
    html_path = generator.generate_to_file(
        report, ReportType.FEATURE_DEV, output_dir / "feature_dev_report.html"
    )
    print(f"✓ HTML report: {html_path}")

    # PDF (requires weasyprint)
    try:
        pdf_path = generator.generate_to_file(
            report, ReportType.FEATURE_DEV, output_dir / "feature_dev_report.pdf"
        )
        print(f"✓ PDF report: {pdf_path}")
    except ImportError:
        print("⚠ PDF generation skipped (install weasyprint to enable)")

    print("\nReports generated successfully!")


if __name__ == "__main__":
    main()
