# from flext-quality_docs/security/sonarqube-triage.md:861
      405              try:
      406                  async with ClientSession() as session:
      407                      self.session = session
      408                      results = await self.check_links_batch_async(links)
>>>   409              except (OSError, ClientError, TimeoutError, RuntimeError):
      410                  results = self.check_links_batch_sync(links)
      411          else:
      412              results = self.check_links_batch_sync(links)
      413
