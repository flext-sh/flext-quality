# from flext-quality/src/flext_quality/docs/README.md:913
from __future__ import annotations

# Add new validation tools to the pipeline
from docs import DocumentationAuditor


class ExtendedAuditor(DocumentationAuditor):
    def run_custom_checks(self, doc_files: List[Path]):
        # Integrate your custom tools
        custom_results = self.custom_validator.validate_files(doc_files)
        _ = self.results["custom_checks"] = custom_results
