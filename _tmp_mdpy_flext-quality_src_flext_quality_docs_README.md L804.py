# from flext-quality/src/flext_quality/docs/README.md:804
from docs import DocumentationAuditor

auditor = DocumentationAuditor(config_path="docs/maintenance/settings/")
results = auditor.run_comprehensive_audit()
report = auditor.generate_report(format="json")
