# from flext-quality_docs/security/sonarqube-triage.md:924
      142              if loaded_obj:
      143                  self.settings = self._normalize_config(loaded_obj)
      144              else:
      145                  self._set_default_config()
>>>   146          except (FileNotFoundError, KeyError, OSError):
      147              self._set_default_config()
      148
      149      def _normalize_config(
      150          self, raw: t.JsonMapping
