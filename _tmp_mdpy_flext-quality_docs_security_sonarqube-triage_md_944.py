# from flext-quality_docs/security/sonarqube-triage.md:944
       31              return []
       32
       33          @staticmethod
       34          def _empty_dict_str_str() -> t.StrMapping:
>>>    35              return dict[str, str]()
       36
       37          @staticmethod
       38          def _empty_list_dict_str_str() -> MutableSequence[t.MutableStrMapping]:
       39              return []
