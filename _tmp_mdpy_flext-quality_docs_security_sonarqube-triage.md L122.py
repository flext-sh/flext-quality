# from flext-quality/docs/security/sonarqube-triage.md:122
       49              return Response(
       50                  t.Quality.RELAXED_CONTAINER_MAPPING_ADAPTER.dump_json(
       51                      self.get_current_metrics()
       52                  ).decode(),
>>>    53                  mimetype="application/json",
       54              )
       55
       56          _ = api_metrics
       57
