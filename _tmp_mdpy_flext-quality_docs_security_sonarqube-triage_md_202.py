# from flext-quality_docs/security/sonarqube-triage.md:202
      263          ).search(content):
      264              indicators.append("potentially inconsistent status")
      265          return indicators
      266
>>>   267      def check_content_completeness(self, doc_files: t.SequenceOf[Path]) -> None:
      268          """Check documentation completeness and identify missing sections."""
      269          min_word_count = self.audit_rules.quality_thresholds.min_word_count
      270          required_sections = self.validation_config.content_analysis.required_sections
      271          check_todos = self.validation_config.content_analysis.check_todos
