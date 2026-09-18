# from flext-quality/docs/security/sonarqube-triage.md:511
      291                      link_file_dir = Path(link.file).parent
      292                      relative_target = (
      293                          link_file_dir / target[2:]
      294                          if target.startswith("./")
>>>   295                          else link_file_dir.parent / target[3:]
      296                          if target.startswith("../")
      297                          else Path(target)
      298                      )
      299                      search_root = Path(link.file).parent.parent.parent
