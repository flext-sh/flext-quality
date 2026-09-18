# from flext-quality_docs/security/sonarqube-triage.md:142
       89          self.results: m.Quality.NotifierResults = m.Quality.NotifierResults(
       90              timestamp=u.now().isoformat()
       91          )
       92
>>>    93      def _load_user_config(self, loaded: t.JsonMapping) -> _NotifierConfig:
       94          cfg = self.get_default_config()
       95
       96          channels = loaded.get("channels")
       97          if isinstance(channels, dict):
