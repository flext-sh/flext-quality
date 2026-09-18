# from flext-quality/docs/security/sonarqube-triage.md:222
       90          lines = content.split("\n")
       91          fixed_lines: MutableSequence[str] = []
       92          for i, line in enumerate(lines):
       93              if (
>>>    94                  u.Quality.compile_pattern(r"^#{1,6}\\s").match(line)
       95                  and i > 0
       96                  and lines[i - 1].strip()
       97              ):
       98                  fixed_lines.append("")
