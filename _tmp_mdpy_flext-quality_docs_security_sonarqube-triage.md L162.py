# from flext-quality/docs/security/sonarqube-triage.md:162
      438              webhook_config.url, json=payload, headers=headers, timeout=timeout
      439          )
      440          response.raise_for_status()
      441
>>>   442      def _format_critical_issues_message(self, audit_data: t.JsonMapping) -> str:
      443          """Format message for critical issues notification."""
      444          metrics_val = audit_data.get("metrics")
      445          metrics: t.JsonMapping = (
      446              t.Quality.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_python(metrics_val)
