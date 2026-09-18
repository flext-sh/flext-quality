# from flext-quality_docs/security/sonarqube-triage.md:322
      553              str, t.Quality.DocumentationReportValue | datetime
      554          ] = {**report_data_raw, "date": report_date}
      555          return report_data_dict
      556
>>>   557      def _analyze_trend_data(
      558          self,
      559          reports: t.SequenceOf[
      560              Mapping[str, t.Quality.DocumentationReportValue | datetime]
      561          ],
