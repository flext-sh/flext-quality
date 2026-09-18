# from flext-quality_docs/security/sonarqube-triage.md:718
      484              internal_links = u.Quality.compile_pattern(
      485                  r"\\[([^\\]]+)\\]\\(([^)]+)\\)"
      486              ).findall(content)
      487              for text, link in internal_links:
>>>   488                  if not link.startswith(("http://", "https://", "#", "mailto:")):
      489                      all_links.append({
      490                          "url": link,
      491                          "text": text,
      492                          "file": str(file_path.relative_to(self.project_root)),
