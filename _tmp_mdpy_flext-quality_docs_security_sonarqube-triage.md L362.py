# from flext-quality/docs/security/sonarqube-triage.md:362
      271                  })
      272              )
      273              return max_retry_result
      274
>>>   275          def validate_internal_links(
      276              self,
      277              links: t.SequenceOf[m.Quality.LinkRecord],
      278              doc_files: t.SequenceOf[Path],
      279          ) -> m.Quality.LinkValidatorResults:
