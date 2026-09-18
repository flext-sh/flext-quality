# from flext-quality/examples/basic/simple_analysis/README.md:285
from flext_quality import QualityReport

# Generate detailed quality report
report = QualityReport.from_analysis_results(results)
html_report = report.generate_html_report()
pdf_report = report.generate_pdf_report()
