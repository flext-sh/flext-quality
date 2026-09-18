# from flext-quality_docs/security/sonarqube-triage.md:759
      848                  metrics = results.metrics
      849                  if self._should_fail(metrics):
      850                      return r[bool].fail("Audit failed quality threshold")
      851              except (
>>>   852                  FileNotFoundError,
      853                  PermissionError,
      854                  OSError,
      855                  KeyError,
      856                  ValueError,
