# from flext-quality/docs/security/sonarqube-triage.md:182
      578              None, description="Monthly report JSON file", validate_default=True
      579          )
      580
      581          @override
>>>   582          def execute(self) -> p.Result[bool]:
      583              """Dispatch to the appropriate notification action."""
      584              notifier = FlextQualityDocumentationNotifier(self.settings_path)
      585              if self.test:
      586                  notifier.send_notification(
