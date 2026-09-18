# from flext-quality/docs/security/sonarqube-triage.md:491
      178          total_issues = 0
      179          files_analyzed = 0
      180          links_checked = 0
      181          optimizations_applied = 0
>>>   182          quality_trend = "unknown"
      183
      184          if self.audit_data and isinstance(self.audit_data, dict):
      185              metrics = self.audit_data.get("metrics")
      186              if isinstance(metrics, dict):
