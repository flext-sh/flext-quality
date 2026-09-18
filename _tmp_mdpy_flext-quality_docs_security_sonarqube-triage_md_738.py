# from flext-quality_docs/security/sonarqube-triage.md:738
      567
      568      def _validate_images(self, images: t.SequenceOf[t.StrMapping]) -> None:
      569          """Validate image references."""
      570          for image in images:
>>>   571              if image["src"].startswith(("http://", "https://")):
      572                  continue
      573              image_path = Path(image["src"])
      574              if not image_path.is_absolute():
      575                  file_dir = Path(image["file"]).parent
