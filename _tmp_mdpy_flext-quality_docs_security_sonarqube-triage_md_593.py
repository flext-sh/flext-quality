# from flext-quality_docs/security/sonarqube-triage.md:593
      320          # Email notification
      321          if self.config.channels.email.enabled:
      322              try:
      323                  self._send_email_notification(title, message, priority)
>>>   324              except (smtplib.SMTPException, ConnectionError, OSError) as e:
      325                  self.results.errors.append(f"Email notification failed: {e}")
      326                  success = False
      327
      328          # Slack notification
