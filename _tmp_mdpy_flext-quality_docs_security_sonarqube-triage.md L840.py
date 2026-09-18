# from flext-quality/docs/security/sonarqube-triage.md:840
      172          return all_links
      173
      174      def _classify_link(self, url: str) -> str:
      175          """Classify link type based on URL."""
>>>   176          if url.startswith(("http://", "https://")):
      177              return "external"
      178          if url.startswith("#"):
      179              return "anchor"
      180          if url.startswith(("mailto:", "tel:")):
