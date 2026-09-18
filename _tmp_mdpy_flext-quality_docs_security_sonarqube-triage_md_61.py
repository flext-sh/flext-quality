# from flext-quality_docs/security/sonarqube-triage.md:61
      173
      174      def get_style_guide(self) -> FlextQualityConfigManager.StyleGuide:
      175          """Get style guide configuration."""
      176          if self._style_guide is None:
>>>   177              data = self._load_config_file("style_guide.yaml")
      178              self._style_guide = FlextQualityConfigManager.StyleGuide.model_validate(
      179                  data
      180              )
      181          return self._style_guide
