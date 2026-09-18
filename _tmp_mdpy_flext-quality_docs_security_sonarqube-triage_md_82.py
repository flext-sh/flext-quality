# from flext-quality_docs/security/sonarqube-triage.md:82
      182
      183      def get_validation_config(self) -> FlextQualityConfigManager.ValidationSettings:
      184          """Get validation configuration."""
      185          if self._validation_config is None:
>>>   186              data = self._load_config_file("validation_config.yaml")
      187              self._validation_config = (
      188                  FlextQualityConfigManager.ValidationSettings.model_validate(data)
      189              )
      190          return self._validation_config
