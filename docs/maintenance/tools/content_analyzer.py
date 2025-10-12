#!/usr/bin/env python3
"""FLEXT Quality Content Analysis Tool.

Advanced content quality analysis including readability assessment,
completeness checking, and structural validation for documentation.
"""

import re
from collections import Counter
from pathlib import Path
from typing import Any

import yaml
from flext_core import FlextCore


class ContentAnalyzer:
    """Advanced content quality analysis system."""

    def __init__(
        self, config_path: str = "docs/maintenance/config/audit_rules.yaml"
    ) -> None:
        self.load_config(config_path)
        self.results = {
            "files_analyzed": 0,
            "quality_metrics": {},
            "content_scores": {},
            "readability_stats": {},
            "completeness_checks": {},
            "recommendations": [],
        }

    def load_config(self, config_path: str) -> None:
        """Load content analysis configuration."""
        try:
            with Path(config_path).open(encoding="utf-8") as f:
                self.config = yaml.safe_load(f)
        except (FileNotFoundError, KeyError):
            self.config = {
                "content_checks": {
                    "check_freshness": True,
                    "check_completeness": True,
                    "check_readability": False,
                },
                "quality_thresholds": {
                    "min_word_count": 100,
                    "min_readability_score": 60,
                    "max_age_days": 90,
                },
            }

    def analyze_file(self, file_path: Path) -> dict[str, Any]:
        """Perform comprehensive content analysis on a single file."""
        try:
            content = file_path.read_text(encoding="utf-8")
            filename = str(file_path.relative_to(file_path.parents[2]))

            analysis = {
                "file": filename,
                "metrics": self._calculate_content_metrics(content),
                "readability": self._analyze_readability(content),
                "structure": self._analyze_structure(content),
                "completeness": self._check_completeness(content, filename),
                "quality_score": 0,
                "issues": [],
                "suggestions": [],
            }

            # Calculate overall quality score
            analysis["quality_score"] = self._calculate_quality_score(analysis)

            # Generate issues and suggestions
            analysis["issues"] = self._identify_issues(analysis)
            analysis["suggestions"] = self._generate_suggestions(analysis)

            # Update global results
            self.results["files_analyzed"] += 1
            self.results["quality_metrics"][filename] = analysis["metrics"]
            self.results["content_scores"][filename] = analysis["quality_score"]
            self.results["readability_stats"][filename] = analysis["readability"]
            self.results["completeness_checks"][filename] = analysis["completeness"]

            return analysis

        except Exception as e:
            return {
                "file": str(file_path),
                "error": str(e),
                "quality_score": 0,
                "issues": [{"type": "analysis_error", "message": str(e)}],
                "suggestions": [],
            }

    def _calculate_content_metrics(self, content: str) -> dict[str, Any]:
        """Calculate basic content metrics."""
        # Word analysis
        words = re.findall(r"\b\w+\b", content)
        word_count = len(words)

        # Sentence analysis
        sentences = re.split(r"[.!?]+", content)
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_count = len(sentences)

        # Character analysis
        char_count = len(content)
        char_count_no_spaces = len(re.sub(r"\s", "", content))

        # Line analysis
        lines = content.split("\n")
        total_lines = len(lines)
        code_lines = len([
            line for line in lines if line.strip().startswith(("```", "    ", "\t"))
        ])
        empty_lines = len([line for line in lines if line.strip() == ""])

        # Heading analysis
        headings = re.findall(r"^#{1,6}\s+.+", content, re.MULTILINE)
        heading_count = len(headings)

        # List analysis
        list_items = re.findall(r"^[\s]*[-\*\+]\s+", content, re.MULTILINE)
        list_count = len(list_items)

        # Link analysis
        links = re.findall(r"\[([^\]]+)\]\([^\)]+\)", content)
        link_count = len(links)

        # Image analysis
        images = re.findall(r"!\[([^\]]*)\]\([^\)]+\)", content)
        image_count = len(images)

        # Code block analysis
        code_blocks = re.findall(r"```[\s\S]*?```", content)
        code_block_count = len(code_blocks)

        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "character_count": char_count,
            "character_count_no_spaces": char_count_no_spaces,
            "line_count": total_lines,
            "code_lines": code_lines,
            "empty_lines": empty_lines,
            "heading_count": heading_count,
            "list_count": list_count,
            "link_count": link_count,
            "image_count": image_count,
            "code_block_count": code_block_count,
            "avg_words_per_sentence": word_count / sentence_count
            if sentence_count > 0
            else 0,
            "avg_sentence_length": char_count / sentence_count
            if sentence_count > 0
            else 0,
            "code_to_content_ratio": code_lines / total_lines if total_lines > 0 else 0,
        }

    def _analyze_readability(self, content: str) -> dict[str, Any]:
        """Analyze content readability using various metrics."""
        words = re.findall(r"\b\w+\b", content)
        sentences = re.split(r"[.!?]+", content)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not words or not sentences:
            return {"readability_score": 0, "grade_level": "N/A", "reading_ease": 0}

        # Average words per sentence
        avg_words_per_sentence = len(words) / len(sentences)

        # Average syllables per word (simplified)
        syllable_count = sum(self._count_syllables(word) for word in words)
        avg_syllables_per_word = syllable_count / len(words)

        # Flesch Reading Ease Score
        reading_ease = (
            206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)
        )
        reading_ease = max(0, min(100, reading_ease))  # Clamp to 0-100

        # Automated Readability Index (simplified)
        grade_level = (
            (0.5 * avg_words_per_sentence) + (8.5 * avg_syllables_per_word) - 15.59
        )

        # Determine readability level
        if reading_ease >= 90:
            level = "Very Easy"
        elif reading_ease >= 80:
            level = "Easy"
        elif reading_ease >= 70:
            level = "Fairly Easy"
        elif reading_ease >= 60:
            level = "Standard"
        elif reading_ease >= 50:
            level = "Fairly Difficult"
        elif reading_ease >= 30:
            level = "Difficult"
        else:
            level = "Very Difficult"

        return {
            "readability_score": round(reading_ease, 1),
            "grade_level": round(grade_level, 1),
            "reading_level": level,
            "avg_words_per_sentence": round(avg_words_per_sentence, 1),
            "avg_syllables_per_word": round(avg_syllables_per_word, 2),
        }

    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word (simplified algorithm)."""
        word = word.lower()
        count = 0
        vowels = "aeiouy"

        if word[0] in vowels:
            count += 1

        for i in range(1, len(word)):
            if word[i] in vowels and word[i - 1] not in vowels:
                count += 1

        if word.endswith("e"):
            count -= 1

        if count == 0:
            count += 1

        return count

    def _analyze_structure(self, content: str) -> dict[str, Any]:
        """Analyze document structure and organization."""
        structure = {
            "has_table_of_contents": False,
            "toc_position": None,
            "heading_hierarchy_valid": True,
            "sections": [],
            "depth_analysis": {},
        }

        # Check for table of contents
        toc_patterns = [
            r"^#{1,6}.*\b[tT]able of [cC]ontents\b",
            r"^#{1,6}.*\b[cC]ontents?\b",
            r"^#{1,6}.*\b[tT]OC\b",
        ]

        for pattern in toc_patterns:
            toc_match = re.search(pattern, content, re.MULTILINE)
            if toc_match:
                structure["has_table_of_contents"] = True
                structure["toc_position"] = content[: toc_match.start()].count("\n") + 1
                break

        # Analyze heading hierarchy
        headings = []
        for match in re.finditer(r"^(#{1,6})\s+(.+)$", content, re.MULTILINE):
            level = len(match.group(1))
            title = match.group(2).strip()
            line_num = content[: match.start()].count("\n") + 1
            headings.append({"level": level, "title": title, "line": line_num})

        structure["sections"] = headings

        # Check heading hierarchy
        if len(headings) > 1:
            for i in range(1, len(headings)):
                if headings[i]["level"] > headings[i - 1]["level"] + 1:
                    structure["heading_hierarchy_valid"] = False
                    break

        # Analyze heading depth distribution
        depths = [h["level"] for h in headings]
        structure["depth_analysis"] = {
            "max_depth": max(depths) if depths else 0,
            "avg_depth": sum(depths) / len(depths) if depths else 0,
            "depth_distribution": dict(Counter(depths)),
        }

        return structure

    def _check_completeness(self, content: str, filename: str) -> dict[str, Any]:
        """Check documentation completeness based on file type and content."""
        completeness = {
            "score": 100,
            "missing_elements": [],
            "required_sections_present": [],
            "optional_sections_present": [],
            "word_count_sufficient": True,
        }

        # Basic word count check
        word_count = len(re.findall(r"\b\w+\b", content))
        min_words = self.config["quality_thresholds"]["min_word_count"]

        if word_count < min_words:
            completeness["word_count_sufficient"] = False
            completeness["missing_elements"].append(f"Minimum word count ({min_words})")
            completeness["score"] -= 20

        # File-specific completeness checks
        if filename.endswith("README.md"):
            required_sections = [
                "Purpose|Overview|Introduction",
                "Installation|Setup",
                "Usage",
            ]
            completeness.update(
                self._check_required_sections(content, required_sections)
            )

        elif filename.startswith("docs/"):
            required_sections = ["Overview|Introduction"]
            completeness.update(
                self._check_required_sections(content, required_sections)
            )

        # Check for common documentation elements
        checks = [
            ("code_examples", bool(r"```" in content), "Code examples"),
            (
                "has_lists",
                bool(re.search(r"^[\s]*[-\*\+]", content, re.MULTILINE)),
                "Lists or bullet points",
            ),
            (
                "has_headings",
                bool(re.search(r"^#{1,6}\s", content, re.MULTILINE)),
                "Section headings",
            ),
            (
                "has_links",
                bool(re.search(r"\[.*\]\(.*\)", content)),
                "Internal or external links",
            ),
        ]

        for _check_name, present, description in checks:
            if not present:
                completeness["missing_elements"].append(description)
                completeness["score"] -= 5

        # Ensure score doesn't go below 0
        completeness["score"] = max(0, completeness["score"])

        return completeness

    def _check_required_sections(
        self, content: str, required_sections: FlextCore.Types.StringList
    ) -> dict[str, Any]:
        """Check for required sections in content."""
        result = {"required_sections_present": [], "missing_required_sections": []}

        for section_pattern in required_sections:
            patterns = section_pattern.split("|")
            found = False

            for pattern in patterns:
                if re.search(
                    rf"^#{1, 6}.*\b{re.escape(pattern)}\b",
                    content,
                    re.MULTILINE | re.IGNORECASE,
                ):
                    found = True
                    result["required_sections_present"].append(pattern)
                    break

            if not found:
                result["missing_required_sections"].append(section_pattern)
                self.results["recommendations"].append(
                    f"Add '{section_pattern}' section"
                )

        return result

    def _calculate_quality_score(self, analysis: dict[str, Any]) -> float:
        """Calculate overall quality score for the content."""
        score = 100.0

        metrics = analysis["metrics"]
        readability = analysis["readability"]
        completeness = analysis["completeness"]

        # Completeness score (major factor)
        score -= (100 - completeness["score"]) * 0.5

        # Readability score
        if readability["readability_score"] < 60:
            penalty = (60 - readability["readability_score"]) * 0.3
            score -= min(penalty, 20)

        # Content metrics
        if metrics["word_count"] < 100:
            score -= 10

        if metrics["heading_count"] == 0:
            score -= 15

        if metrics["link_count"] == 0:
            score -= 5

        # Structure bonus
        if analysis["structure"]["has_table_of_contents"]:
            score += 5

        if analysis["structure"]["heading_hierarchy_valid"]:
            score += 5

        return max(0, min(100, score))

    def _identify_issues(self, analysis: dict[str, Any]) -> list[dict[str, Any]]:
        """Identify content issues that need attention."""
        issues = []

        # Completeness issues
        if not analysis["completeness"]["word_count_sufficient"]:
            issues.append({
                "type": "insufficient_content",
                "severity": "medium",
                "message": f"Content too short ({analysis['metrics']['word_count']} words)",
            })

        if analysis["completeness"]["missing_elements"]:
            issues.append({
                "type": "missing_elements",
                "severity": "high",
                "message": f"Missing: {', '.join(analysis['completeness']['missing_elements'])}",
            })

        # Readability issues
        if analysis["readability"]["readability_score"] < 50:
            issues.append({
                "type": "poor_readability",
                "severity": "medium",
                "message": f"Content difficult to read (score: {analysis['readability']['readability_score']})",
            })

        # Structure issues
        if not analysis["structure"]["heading_hierarchy_valid"]:
            issues.append({
                "type": "heading_hierarchy",
                "severity": "low",
                "message": "Heading hierarchy is not logical",
            })

        if analysis["metrics"]["heading_count"] == 0:
            issues.append({
                "type": "no_headings",
                "severity": "high",
                "message": "Document has no section headings",
            })

        return issues

    def _generate_suggestions(
        self, analysis: dict[str, Any]
    ) -> FlextCore.Types.StringList:
        """Generate improvement suggestions based on analysis."""
        suggestions = []

        metrics = analysis["metrics"]
        readability = analysis["readability"]
        structure = analysis["structure"]

        if metrics["word_count"] < 200:
            suggestions.append(
                "Expand content with more detailed explanations and examples"
            )

        if readability["readability_score"] < 60:
            suggestions.append(
                "Simplify language and sentence structure for better readability"
            )

        if not structure["has_table_of_contents"] and metrics["heading_count"] > 3:
            suggestions.append("Add a table of contents for better navigation")

        if metrics["code_block_count"] == 0 and "tutorial" in analysis["file"].lower():
            suggestions.append("Add code examples to illustrate concepts")

        if metrics["link_count"] == 0:
            suggestions.append(
                "Add relevant links to related documentation or external resources"
            )

        return suggestions

    def analyze_files_batch(self, file_paths: list[Path]) -> dict[str, Any]:
        """Analyze multiple files and aggregate results."""
        for file_path in file_paths:
            self.analyze_file(file_path)

        # Generate overall recommendations
        self._generate_overall_recommendations()

        return self.results

    def _generate_overall_recommendations(self) -> None:
        """Generate overall recommendations based on batch analysis."""
        if not self.results["content_scores"]:
            return

        avg_score = sum(self.results["content_scores"].values()) / len(
            self.results["content_scores"]
        )

        if avg_score < 70:
            self.results["recommendations"].append({
                "priority": "high",
                "type": "overall_quality",
                "message": f"Overall documentation quality needs improvement (avg score: {avg_score:.1f})",
                "actions": [
                    "Focus on adding missing content and sections",
                    "Improve readability and structure",
                    "Add more examples and practical guidance",
                ],
            })

        # Check for common issues across files
        all_issues = []
        for file_issues in [
            analysis.get("issues", [])
            for analysis in self.results.values()
            if isinstance(analysis, dict)
        ]:
            all_issues.extend(file_issues)

        if all_issues:
            issue_types = Counter(issue["type"] for issue in all_issues)
            most_common = issue_types.most_common(1)
            if most_common:
                common_issue = most_common[0][0]
                self.results["recommendations"].append({
                    "priority": "medium",
                    "type": "common_issue",
                    "message": f"Address common issue across files: {common_issue.replace('_', ' ')}",
                    "actions": [
                        "Implement consistent fixes",
                        "Update style guidelines",
                    ],
                })

    def generate_report(self, format: str = "json") -> str:
        """Generate content analysis report."""
        import json

        if format == "json":
            return json.dumps(self.results, indent=2, default=str)
        if format == "summary":
            return self._generate_summary_report()
        return json.dumps(self.results, default=str)

    def _generate_summary_report(self) -> str:
        """Generate human-readable summary report."""
        if not self.results["content_scores"]:
            return "No content analysis results available."

        scores = list(self.results["content_scores"].values())
        avg_score = sum(scores) / len(scores)

        report = f"""
Content Quality Analysis Summary
=================================

Files Analyzed: {self.results["files_analyzed"]}
Average Quality Score: {avg_score:.1f}/100

Score Distribution:
- Excellent (90-100): {len([s for s in scores if s >= 90])}
- Good (70-89): {len([s for s in scores if 70 <= s < 90])}
- Needs Improvement (50-69): {len([s for s in scores if 50 <= s < 70])}
- Poor (<50): {len([s for s in scores if s < 50])}

Top Recommendations:
"""

        # Show top recommendations
        for rec in self.results["recommendations"][:3]:
            if isinstance(rec, dict):
                report += f"- {rec['message']}\n"
            else:
                report += f"- {rec}\n"

        return report

    def save_report(self, output_path: str = "docs/maintenance/reports/"):
        """Save content analysis report."""
        import os
        from datetime import UTC, datetime

        Path(output_path).mkdir(exist_ok=True, parents=True)

        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        filename = f"content_analysis_{timestamp}.json"
        filepath = os.path.join(output_path, filename)

        with Path(filepath).open("w", encoding="utf-8") as f:
            import json

            json.dump(self.results, f, indent=2, default=str)

        return filepath


def analyze_file_content(
    file_path: str, config_path: str | None = None
) -> dict[str, Any]:
    """Convenience function to analyze a single file."""
    analyzer = ContentAnalyzer(config_path)
    return analyzer.analyze_file(Path(file_path))


def analyze_files_content(
    file_paths: FlextCore.Types.StringList, config_path: str | None = None
) -> dict[str, Any]:
    """Convenience function to analyze multiple files."""
    analyzer = ContentAnalyzer(config_path)
    paths = [Path(fp) for fp in file_paths]
    return analyzer.analyze_files_batch(paths)


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) < 2:
        sys.exit(1)

    file_path = sys.argv[1]
    config_path = sys.argv[2] if len(sys.argv) > 2 else None

    results = analyze_file_content(file_path, config_path)

    if results["issues"]:
        for _issue in results["issues"][:2]:
            pass

    if results["suggestions"]:
        for _suggestion in results["suggestions"][:2]:
            pass
