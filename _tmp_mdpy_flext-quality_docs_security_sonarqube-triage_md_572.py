# from flext-quality_docs/security/sonarqube-triage.md:572
      205                  self._as_config_data(raw) if raw else self._get_default_config(filename)
      206              )
      207          except FileNotFoundError:
      208              return self._get_default_config(filename)
>>>   209          except (OSError, PermissionError, UnicodeDecodeError) as exc:
      210              _ = exc
      211              return self._get_default_config(filename)
      212
      213      def _get_default_config(
