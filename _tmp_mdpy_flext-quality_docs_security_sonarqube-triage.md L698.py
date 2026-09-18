# from flext-quality/docs/security/sonarqube-triage.md:698
      358          email_config = self.config.email
      359
      360          msg = MIMEMultipart()
      361          msg["From"] = email_config.from_address
>>>   362          msg["To"] = ", ".join(x for x in (email_config.to_addresses or []))
      363          msg["Subject"] = f"[{priority.upper()}] {title}"
      364
      365          body = f"""
      366  FLEXT Quality Documentation Alert
