# from flext-quality/docs/security/sonarqube-triage.md:242
      248
      249      def _improve_link_text(self, content: str) -> str:
      250          """Improve generic link text for better accessibility."""
      251          improvements = {
>>>   252              "\\[here\\]\\(([^)]+)\\)": "[learn more](\\1)",
      253              "\\[click here\\]\\(([^)]+)\\)": "[learn more](\\1)",
      254              "\\[link\\]\\(([^)]+)\\)": "[learn more](\\1)",
      255              "\\[read more\\]\\(([^)]+)\\)": "[continue reading](\\1)",
      256          }
