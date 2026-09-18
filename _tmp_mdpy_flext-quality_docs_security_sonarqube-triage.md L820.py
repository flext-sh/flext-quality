# from flext-quality/docs/security/sonarqube-triage.md:820
      330              """Validate image references."""
      331              images = [link for link in links if link.type == "image"]
      332              for image in images:
      333                  src = image.url
>>>   334                  if src.startswith(("http://", "https://")):
      335                      self.results.valid_links += 1
      336                      continue
      337                  image_path = Path(src)
      338                  if not image_path.is_absolute():
