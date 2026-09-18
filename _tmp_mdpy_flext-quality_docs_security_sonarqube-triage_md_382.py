# from flext-quality_docs/security/sonarqube-triage.md:382
      251                  self.results.performance.slowest_response, response_time
      252              )
      253              return result
      254
>>>   255      def check_link_sync(
      256          self, url: str, context: t.JsonMapping | None = None
      257      ) -> FlextQualityLinkChecker.LinkResult:
      258          """Check a single link synchronously (fallback method)."""
      259          start_time = time.time()
