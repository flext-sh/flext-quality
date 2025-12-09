# Simple Analysis Example

This example demonstrates the fundamental usage of FLEXT Quality for analyzing a Python project and generating quality reports. It showcases the core functionality and basic integration patterns that form the foundation of quality analysis workflows.

## Overview

The simple analysis example covers:

- **Basic CodeAnalyzer Usage**: Initialize and execute project analysis
- **Quality Metrics Processing**: Extract and interpret quality scores
- **Issue Detection**: Identify and categorize quality issues
- **Result Interpretation**: Understand analysis outputs and recommendations
- **Error Handling**: Proper error handling and user feedback

## Features Demonstrated

### Core Analysis Capabilities

- **Multi-Backend Analysis**: Security, complexity, dead code, and duplication detection
- **Quality Scoring**: Comprehensive scoring algorithm with letter grades
- **Issue Categorization**: Organized issue reporting by analysis type
- **Progress Feedback**: Real-time analysis progress and status updates

### FLEXT Integration Patterns

- **FlextResult Usage**: Consistent error handling patterns
- **QualityMetrics Integration**: Working with quality value objects
- **Type Safety**: Comprehensive type hints and validation
- **Enterprise Standards**: Professional code structure and documentation

## Usage

### Basic Execution

```bash

# Analyze current directory
python example.py

# Analyze specific project
python example.py /path/to/your/project

# Analyze FLEXT Quality itself
python example.py ../../../src
```

### Expected Output

```
🚀 FLEXT Quality - Basic Analysis Example
============================================================
🔍 Starting quality analysis for: /path/to/project
============================================================
📊 Executing comprehensive analysis...

📈 Analysis Results:
----------------------------------------
Files analyzed: 15
Total lines of code: 2,847
Python files found: 15

🎯 Quality Assessment:
----------------------------------------
Overall Score: 87.3/100
Quality Grade: B+

📋 Quality Metrics Summary:
----------------------------------------
Quality Grade: B+ (87.3/100)
Files: 15, Lines: 2,847
Functions: 89, Classes: 12
Issues: Security(0), Complexity(3), DeadCode(1), Duplicates(0)

🚨 Issues Detection:
----------------------------------------
Security: No issues found ✅
Complexity: 3 issues
  - src/analyzer.py: High complexity: 12.0
  - src/metrics.py: High complexity: 11.0
  - src/reports.py: High complexity: 15.0
DeadCode: 1 issues
  - src/utils.py: Potentially unused import: import unused_module
Duplicates: No issues found ✅

💡 Recommendations:
----------------------------------------
👍 Good quality. Consider addressing high-priority issues.
🔄 Reduce complexity in 3 locations

✅ Analysis completed successfully!
📊 Final Quality Grade: B+ (87.3/100)
```

## Code Structure

### Main Components

#### `analyze_project(project_path: str)`

Core analysis function that orchestrates the complete quality assessment workflow:

- Initializes CodeAnalyzer with project path
- Executes comprehensive analysis with all backends enabled
- Processes results and calculates quality metrics
- Provides detailed output and recommendations

#### `validate_project_path(path: str)`

Input validation function ensuring robust error handling:

- Validates path existence and accessibility
- Verifies directory structure
- Checks for Python file presence
- Provides helpful error messages

#### `main()`

Entry point handling command-line interface and execution flow:

- Processes command-line arguments
- Provides default behavior for demonstration
- Handles user interruption and unexpected errors
- Returns appropriate exit codes

### Quality Assessment Logic

The example demonstrates FLEXT Quality's comprehensive scoring system:

```python

# Basic analysis execution
results = analyzer.analyze_project(
    include_security=True,      # Security vulnerability detection
    include_complexity=True,    # Cyclomatic complexity analysis
    include_dead_code=True,     # Unused code detection
    include_duplicates=True     # Code duplication analysis
)

# Quality score calculation
score = analyzer.get_quality_score()  # 0-100 numeric score
grade = analyzer.get_quality_grade()  # A+ to F letter grade

# Comprehensive metrics
metrics = QualityMetrics.from_analysis_results(results)
```

### Issue Processing

The example shows how to process and interpret different types of quality issues:

```python
issues = results.get('issues', {})

for category, issue_list in issues.items():
    if isinstance(issue_list, list) and issue_list:
        print(f"{category.title()}: {len(issue_list)} issues")

        for issue in issue_list[:3]:  # Show first 3 issues
            file_path = issue.get('file', 'unknown')
            message = issue.get('message', 'No description')
            print(f"  - {file_path}: {message}")
```

## Configuration

### Analysis Configuration

The example uses default analysis settings, but can be customized:

```python

# Custom analysis configuration
results = analyzer.analyze_project(
    include_security=True,       # Enable security analysis
    include_complexity=True,     # Enable complexity analysis
    include_dead_code=False,     # Disable dead code detection
    include_duplicates=True      # Enable duplication detection
)
```

### Quality Thresholds

Quality assessment uses standard thresholds:

- **A+ Grade**: 97-100 points (Exceptional)
- **A Grade**: 93-96 points (Excellent)
- **B+ Grade**: 87-92 points (Very Good)
- **B Grade**: 83-86 points (Good)
- **C+ Grade**: 77-82 points (Satisfactory)
- **C Grade**: 73-76 points (Needs Improvement)
- **D+ Grade**: 67-72 points (Poor)
- **D Grade**: 60-66 points (Very Poor)
- **F Grade**: Below 60 points (Failing)

## Understanding Results

### Quality Metrics Interpretation

**Files and Code Statistics:**

- **Files analyzed**: Number of Python files processed
- **Total lines of code**: Non-comment, non-blank lines
- **Functions/Classes**: Code structure complexity indicators

**Quality Scores:**

- **Overall Score**: Weighted combination of all quality factors
- **Category Scores**: Individual scores for security, complexity, maintainability
- **Quality Grade**: Letter grade based on overall score

**Issue Categories:**

- **Security**: Vulnerabilities and dangerous patterns
- **Complexity**: High cyclomatic complexity functions
- **Dead Code**: Unused imports, variables, and functions
- **Duplicates**: Similar or identical code blocks

### Recommendations System

The example provides contextual recommendations based on analysis results:

- **Score-Based Recommendations**: General guidance based on overall quality
- **Category-Specific Recommendations**: Targeted advice for specific issue types
- **Priority Guidance**: Focus areas for maximum quality improvement impact

## Extending the Example

### Custom Analysis Backends

```python

# Add custom analysis configuration
analyzer = CodeAnalyzer(project_path)
analyzer.configure_backends({
    'security': {'confidence': 'high'},
    'complexity': {'threshold': 8},
    'duplicates': {'similarity': 0.9}
})
```

### Integration with FLEXT Services

```python
from flext_observability import create_metric

# Publish quality metrics to observability stack
create_metric(
    name="project_quality_score",
    value=score,
    tags={"project": project_name, "grade": grade}
)
```

### Report Generation

```python
from flext_quality import QualityReport

# Generate detailed quality report
report = QualityReport.from_analysis_results(results)
html_report = report.generate_html_report()
pdf_report = report.generate_pdf_report()
```

## Troubleshooting

### Common Issues

**No Python Files Found:**

```bash
⚠️  Warning: No Python files found in: /path/to/project
```

- Verify the path contains `.py` files
- Check subdirectories for Python code
- Ensure proper file permissions

**Analysis Timeout:**

```bash
❌ Analysis failed: Analysis timeout after 300 seconds
```

- Large projects may require timeout configuration
- Consider analyzing subdirectories separately
- Check system resources and availability

**Permission Errors:**

```bash
❌ Error: Path does not exist: /path/to/project
```

- Verify path exists and is accessible
- Check file and directory permissions
- Use absolute paths for clarity

### Getting Help

For additional support:

- Review the **API Documentation** (*Documentation coming soon*)
- Check **Integration Examples** (*Documentation coming soon*)
- Consult **Troubleshooting Guide** (*Documentation coming soon*)

## Next Steps

After mastering this basic example:

1. **Explore Advanced Examples** - (*Documentation coming soon*)
2. **Learn Integration Patterns** - (*Documentation coming soon*)
3. **Implement CI/CD** - (*Documentation coming soon*)
4. **Create Custom Reports** - (*Documentation coming soon*)

## Related Resources

- **[FLEXT Quality Documentation](../../../docs/README.md)** - Complete system documentation
- **CodeAnalyzer API** - Detailed API reference (*Documentation coming soon*)
- **Quality Metrics Guide** - Understanding quality scoring (*Documentation coming soon*)
- **Integration Patterns** - FLEXT ecosystem integration (*Documentation coming soon*)
