# from flext-quality_docs/security/sonarqube-triage.md:800
      124              # NOTE (multi-agent, mro-f8vk / kimi): match-with-guards was
      125              # non-exhaustive by construction (reportMatchNotExhaustive); the
      126              # if-chain keeps identical first-match semantics and an explicit
      127              # default without a dummy `case _: pass`.
>>>   128              if url.startswith(("http://", "https://")):
      129                  return "external"
      130              if url.startswith("mailto:"):
      131                  return "email"
      132              if url.startswith("#"):
