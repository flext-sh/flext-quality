# from flext-quality_docs/security/sonarqube-triage.md:41
      164
      165      def get_audit_rules(self) -> FlextQualityConfigManager.AuditRules:
      166          """Get audit rules configuration."""
      167          if self._audit_rules is None:
>>>   168              data = self._load_config_file("audit_rules.yaml")
      169              self._audit_rules = FlextQualityConfigManager.AuditRules.model_validate(
      170                  data
      171              )
      172          return self._audit_rules
