"""
report-template: A Python-based solution for generating standardized, professional project reports.

This package provides tools for creating consistent documentation across feature development,
program management, and engineering initiatives.
"""

__version__ = "0.1.0"

from report_template.generator import ReportGenerator
from report_template.models import (
    ReportType,
    ReportData,
    FeatureDevReport,
    ProgramMgmtReport,
    EngineeringInitReport,
)

__all__ = [
    "ReportGenerator",
    "ReportType",
    "ReportData",
    "FeatureDevReport",
    "ProgramMgmtReport",
    "EngineeringInitReport",
]
