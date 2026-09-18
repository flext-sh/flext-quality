# from flext-quality/docs/security/sonarqube-triage.md:677
      336          # Webhook notification
      337          if self.config.channels.webhook.enabled:
      338              try:
      339                  self._send_webhook_notification(title, message, priority)
>>>   340              except (requests.RequestException, ConnectionError, OSError) as e:
      341                  self.results.errors.append(f"Webhook notification failed: {e}")
      342                  success = False
      343
      344          if success:
