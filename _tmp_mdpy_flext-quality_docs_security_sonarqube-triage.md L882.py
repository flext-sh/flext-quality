# from flext-quality/docs/security/sonarqube-triage.md:882
      437              rp.set_url(f"https://{domain}/robots.txt")
      438              rp.read()
      439
      440              return rp.can_fetch(self.settings.user_agent, "/")
>>>   441          except (OSError, ConnectionError, TimeoutError, UnicodeDecodeError):
      442              # If robots.txt can't be read, assume crawling is allowed
      443              return True
      444
      445      def validate_github_links(
