# from flext-quality/docs/security/sonarqube-triage.md:635
      328          # Slack notification
      329          if self.config.channels.slack.enabled:
      330              try:
      331                  self._send_slack_notification(title, message, priority)
>>>   332              except (requests.RequestException, ConnectionError, OSError) as e:
      333                  self.results.errors.append(f"Slack notification failed: {e}")
      334                  success = False
      335
      336          # Webhook notification
