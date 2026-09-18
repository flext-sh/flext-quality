# from flext-quality_docs/security/sonarqube-triage.md:282
      169              return self._generate_markdown_report(report_data)
      170          msg = f"Unsupported format: {report_format}"
      171          raise ValueError(msg)
      172
>>>   173      def _calculate_summary_metrics(
      174          self,
      175      ) -> FlextQualityDocumentationReporter.SummaryMetrics:
      176          """Calculate summary metrics from all available data."""
      177          overall_score = 0
