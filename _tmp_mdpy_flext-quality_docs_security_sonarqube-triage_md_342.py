# from flext-quality_docs/security/sonarqube-triage.md:342
      737                      self.filename or f"monthly_trends_{u.now().strftime('%Y%m%d')}"
      738                  )
      739                  save_result = reporter.save_report(trend_report, filename, "md")
      740                  if save_result.failure:
>>>   741                      return r[bool].fail(save_result.error or "report write failed")
      742              elif self.weekly_trends:
      743                  trend_report = reporter.generate_trend_report(days=7)
      744                  filename = (
      745                      self.filename or f"weekly_trends_{u.now().strftime('%Y%m%d')}"
