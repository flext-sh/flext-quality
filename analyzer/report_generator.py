"""Web-based report generator for Django Code Analyzer."""

from __future__ import annotations

import io
from typing import TYPE_CHECKING

from django.template.loader import get_template
from django.utils import timezone
from flext_core import get_logger
from xhtml2pdf import pisa

from analyzer.models import AnalysisReport

if TYPE_CHECKING:
    from analyzer.models import AnalysisSession, QualityMetrics

logger = get_logger(__name__)


class WebReportGenerator:
    """Web-based report generator for analysis results."""

    def __init__(self, session: AnalysisSession) -> None:
        """Initialize the report generator with an analysis session.

        Args:
            session: The analysis session to generate reports for.

        """
        self.session = session
        self.flx_project = session.flx_project

    def generate_summary_report(self, output_format: str = "html") -> AnalysisReport:
        """Generate a summary report for the analysis session."""
        try:
            # Get quality metrics
            quality_metrics = getattr(self.session, "quality_metrics", None)
            if not quality_metrics:
                content = self._generate_no_metrics_content()
            else:
                content = self._generate_summary_content(quality_metrics)

            # Convert to requested format
            if output_format == "html":
                final_content = self._render_html_template("summary", content)
            elif output_format == "pdf":
                final_content = self._generate_pdf_content(content)
            else:
                final_content = content

            # Create report record
            return AnalysisReport.objects.create(
                session=self.session,
                report_type="summary",
                format=output_format,
                content=final_content,
                generated_at=timezone.now(),
            )

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Error generating summary report: %s", e)
            raise

    def generate_detailed_report(self, output_format: str = "html") -> AnalysisReport:
        """Generate a detailed report for the analysis session."""
        try:
            content = self._generate_detailed_content()

            # Convert to requested format
            if output_format == "html":
                final_content = self._render_html_template("detailed", content)
            elif output_format == "pdf":
                final_content = self._generate_pdf_content(content)
            else:
                final_content = content

            # Create report record
            return AnalysisReport.objects.create(
                session=self.session,
                report_type="detailed",
                format=output_format,
                content=final_content,
                generated_at=timezone.now(),
            )

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Error generating detailed report: %s", e)
            raise

    def generate_security_report(self, output_format: str = "html") -> AnalysisReport:
        """Generate a security report for the analysis session."""
        try:
            content = self._generate_security_content()

            # Convert to requested format
            if output_format == "html":
                final_content = self._render_html_template("security", content)
            elif output_format == "pdf":
                final_content = self._generate_pdf_content(content)
            else:
                final_content = content

            # Create report record
            return AnalysisReport.objects.create(
                session=self.session,
                report_type="security",
                format=output_format,
                content=final_content,
                generated_at=timezone.now(),
            )

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Error generating security report: %s", e)
            raise

    def _generate_no_metrics_content(self) -> str:
        """Generate content when no metrics are available."""
        return "<p>No quality metrics available for this session.</p>"

    def _generate_summary_content(self, quality_metrics: QualityMetrics) -> str:
        """Generate summary content from quality metrics."""
        return f"""
        <h1>Analysis Summary</h1>
        <p>Overall Score: {quality_metrics.overall_score}</p>
        <p>Total Files: {quality_metrics.total_files}</p>
        <p>Total Lines: {quality_metrics.total_lines}</p>
        """

    def _generate_detailed_content(self) -> str:
        """Generate detailed content from analysis session."""
        return f"""
        <h1>Detailed Analysis Report</h1>
        <p>Project: {self.flx_project.name}</p>
        <p>Session: {self.session.name}</p>
        <p>Status: {self.session.status}</p>
        <p>Created: {self.session.created_at}</p>
        """

    def _generate_security_content(self) -> str:
        """Generate security content from analysis session."""
        return f"""
        <h1>Security Analysis Report</h1>
        <p>Project: {self.flx_project.name}</p>
        <p>Session: {self.session.name}</p>
        <p>Security issues will be listed here.</p>
        """

    def _render_html_template(self, template_name: str, content: str) -> str:
        """Render content using HTML template."""
        template = get_template(f"analyzer/reports/{template_name}.html")
        return template.render({"content": content})

    def _generate_pdf_content(self, content: str) -> str:
        """Generate PDF content from HTML content."""
        result = io.BytesIO()
        pdf = pisa.pisaDocument(io.BytesIO(content.encode("utf-8")), result)
        if not pdf.err:
            return result.getvalue().decode("utf-8")
        return content
