# from flext-quality_src/flext_quality/docs/README.md:814
from docs import LinkValidator

validator = LinkValidator(timeout=10, retries=3)
results = validator.check_external_links(doc_files)
broken_links = validator.get_broken_links()
