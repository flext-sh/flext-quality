# from flext-quality/docs/security/sonarqube-triage.md:262
      314              ):
      315                  enhanced_lines.extend(("", "---", ""))
      316          return "\n".join(enhanced_lines)
      317
>>>   318      def update_metadata(
      319          self, doc_files: t.SequenceOf[Path]
      320      ) -> m.Quality.OptimizerResults:
      321          """Update frontmatter metadata and timestamps."""
      322          for file_path in doc_files:
