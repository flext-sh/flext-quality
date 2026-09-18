# from flext-quality/docs/security/sonarqube-triage.md:102
       23
       24      def __init__(self, reports_dir: str = "docs/maintenance/reports/") -> None:
       25          """Initialize documentation dashboard with reports directory."""
       26          self.reports_dir = Path(reports_dir)
>>>    27          self.app = Flask(__name__)
       28          self._logger_instance: p.Logger = u.fetch_logger(__name__)
       29          self.setup_routes()
       30
       31      @property
