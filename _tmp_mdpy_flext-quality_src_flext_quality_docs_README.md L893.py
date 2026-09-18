# from flext-quality/src/flext_quality/docs/README.md:893
from __future__ import annotations
# Extend audit_rules.yaml with custom checks
custom_checks:
  - name: "company_branding"
    pattern: "\\bincorrect\\b|\\bwrong\\b"
    severity: "medium"
    message: "Use approved company terminology"

# Create custom validator
from docs import  BaseValidator

class CustomValidator(BaseValidator):
    def validate(self, content: str, file_path: Path) -> List[Dict]:
        # Your custom validation logic
        return issues
