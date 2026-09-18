# from flext-quality_docs/security/sonarqube-triage.md:471
       57                      check_value = bool(self.style_checks.get(check_name, False))
       58                  case "accessibility":
       59                      check_value = bool(self.accessibility_checks.get(check_name, False))
       60                  case _:
>>>    61                      pass
       62              return check_value
       63
       64      class StyleGuide(FlextQualityModels.Quality.StyleGuideConfig):
       65          """Configuration for style and formatting guidelines."""
