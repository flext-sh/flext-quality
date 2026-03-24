#!/usr/bin/env python3
"""FLEXT Quality Content Analysis Tool.

Advanced content quality analysis including readability assessment,
completeness checking, and structural validation for documentation.
"""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import TypedDict

import yaml
from pydantic import TypeAdapter

from flext_quality import t


class ConfigDict(TypedDict, total=False):
    """Configuration dictionary structure."""

    content_checks: Mapping[str, bool]
    quality_thresholds: Mapping[str, int]


class MetricsDict(TypedDict, total=False):
    """Metrics dictionary structure."""

    word_count: int
    sentence_count: int
    character_count: int
    character_count_no_spaces: int
    line_count: int
    code_lines: int
    empty_lines: int
    heading_count: int
    list_count: int
    link_count: int
    image_count: int
    code_block_count: int
    avg_words_per_sentence: float
    avg_sentence_length: float
    code_to_content_ratio: float


class ReadabilityDict(TypedDict, total=False):
    """Readability analysis dictionary structure."""

    readability_score: float
    grade_level: float | str
    reading_level: str
    reading_ease: float
    avg_words_per_sentence: float
    avg_syllables_per_word: float


class StructureDict(TypedDict, total=False):
    """Structure analysis dictionary structure."""

    has_table_of_contents: bool
    toc_position: int
    heading_hierarchy_valid: bool
    sections: MutableSequence[Mapping[str, int | str]]
    depth_analysis: MutableMapping[str, int | float]


class CompletenessDict(TypedDict, total=False):
    """Completeness check dictionary structure."""

    score: int
    missing_elements: MutableSequence[str]
    required_sections_present: MutableSequence[str]
    optional_sections_present: MutableSequence[str]
    word_count_sufficient: bool
    missing_required_sections: MutableSequence[str]


class IssueDict(TypedDict, total=False):
    """Issue dictionary structure."""

    type: str
    severity: str
    message: str


class AnalysisDict(TypedDict, total=False):
    """Analysis result dictionary structure."""

    file: str
    metrics: MetricsDict
    readability: ReadabilityDict
    structure: StructureDict
    completeness: CompletenessDict
    quality_score: float
    issues: MutableSequence[IssueDict]
    suggestions: MutableSequence[str]
    error: str


class RecommendationDict(TypedDict, total=False):
    """Recommendation dictionary structure."""

    priority: str
    type: str
    message: str
    actions: MutableSequence[str]


class ResultsDict(TypedDict):
    """Results dictionary structure."""

    files_analyzed: int
    quality_metrics: MutableMapping[str, MetricsDict]
    content_scores: MutableMapping[str, float]
    readability_stats: MutableMapping[str, ReadabilityDict]
    completeness_checks: MutableMapping[str, CompletenessDict]
    recommendations: MutableSequence[RecommendationDict | str]


_RESULTS_ADAPTER: TypeAdapter[ResultsDict] = TypeAdapter(ResultsDict)


class FlextQualityContentAnalyzer:
    """Advanced content quality analysis system."""

    EXCELLENT_READABILITY_MIN = 90
    GOOD_READABILITY_MIN = 80
    FAIRLY_EASY_READABILITY_MIN = 70
    STANDARD_READABILITY_MIN = 60
    FAIRLY_DIFFICULT_READABILITY_MIN = 50
    DIFFICULT_READABILITY_MIN = 30

    MIN_WORD_COUNT = 100
    MIN_READABILITY_SCORE = 60
    MAX_AGE_DAYS = 90
    MIN_HEADINGS_FOR_TOC = 3
    MIN_ARGS_REQUIRED = 2

    def __init__(
        self,
        config_path: str | None = "docs/maintenance/config/audit_rules.yaml",
    ) -> None:
        """Initialize content analyzer with configuration.

        Args:
            config_path: Path to configuration file for content analysis rules.

        """
        self.config: Mapping[str, Mapping[str, bool] | Mapping[str, int] | str] = {}
        self.load_config(config_path)
        quality_metrics: MutableMapping[str, MetricsDict] = {}
        content_scores: MutableMapping[str, float] = {}
        readability_stats: MutableMapping[str, ReadabilityDict] = {}
        completeness_checks: MutableMapping[str, CompletenessDict] = {}
        recommendations: MutableSequence[RecommendationDict | str] = []
        self.results: ResultsDict = {
            "files_analyzed": 0,
            "quality_metrics": quality_metrics,
            "content_scores": content_scores,
            "readability_stats": readability_stats,
            "completeness_checks": completeness_checks,
            "recommendations": recommendations,
        }

    def load_config(self, config_path: str | None) -> None:
        """Load content analysis configuration."""
        default_config: Mapping[str, Mapping[str, bool] | Mapping[str, int] | str] = {
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
        if config_path is None:
            self.config = default_config
            return
        try:
            with Path(config_path).open(encoding="utf-8") as f:
                loaded: t.ContainerMapping | t.ContainerList | str | None = (
                    yaml.safe_load(f)
                )
                if isinstance(loaded, dict):
                    config_loaded: Mapping[
                        str,
                        Mapping[str, bool] | Mapping[str, int] | str,
                    ] = {k: v for k, v in loaded.items() if isinstance(v, (dict, str))}
                    self.config = config_loaded
                else:
                    self.config = default_config
        except (FileNotFoundError, KeyError):
            self.config = default_config

    def analyze_file(self, file_path: Path) -> AnalysisDict:
        """Perform comprehensive content analysis on a single file."""
        try:
            content = file_path.read_text(encoding="utf-8")
            filename = str(file_path.relative_to(file_path.parents[2]))
            issues_list: MutableSequence[IssueDict] = []
            suggestions_list: MutableSequence[str] = []
            analysis: AnalysisDict = {
                "file": filename,
                "metrics": self._calculate_content_metrics(content),
                "readability": self._analyze_readability(content),
                "structure": self._analyze_structure(content),
                "completeness": self._check_completeness(content, filename),
                "quality_score": 0.0,
                "issues": issues_list,
                "suggestions": suggestions_list,
            }

            analysis["quality_score"] = self._calculate_quality_score(analysis)

            analysis["issues"] = self._identify_issues(analysis)
            analysis["suggestions"] = self._generate_suggestions(analysis)

            files_count = self.results["files_analyzed"]
            self.results["files_analyzed"] = files_count + 1
            metrics = analysis.get("metrics")
            if metrics:
                self.results["quality_metrics"][filename] = metrics
            readability = analysis.get("readability")
            if readability:
                self.results["readability_stats"][filename] = readability
            completeness = analysis.get("completeness")
            if completeness:
                self.results["completeness_checks"][filename] = completeness
            quality_score = analysis.get("quality_score", 0)
            if isinstance(quality_score, (int, float)):
                self.results["content_scores"][filename] = quality_score

            return analysis

        except (
            FileNotFoundError,
            PermissionError,
            UnicodeDecodeError,
            OSError,
            ValueError,
        ) as e:
            error_result: AnalysisDict = {
                "file": str(file_path),
                "error": str(e),
                "quality_score": 0,
                "issues": [{"type": "analysis_error", "message": str(e)}],
                "suggestions": [],
            }
            return error_result

    def _calculate_content_metrics(
        self,
        content: str,
    ) -> MetricsDict:
        """Calculate basic content metrics."""
        words = re.findall(r"\b\w+\b", content)
        word_count = len(words)

        sentences = re.split(r"[.!?]+", content)
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_count = len(sentences)

        char_count = len(content)
        char_count_no_spaces = len(re.sub(r"\s", "", content))

        lines = content.split("\n")
        total_lines = len(lines)
        code_lines = len([
            line for line in lines if line.strip().startswith(("```", "    ", "\t"))
        ])
        empty_lines = len([line for line in lines if not line.strip()])

        headings = re.findall(r"^#{1,6}\s+.+", content, re.MULTILINE)
        heading_count = len(headings)

        list_items = re.findall(r"^[\s]*[-\*\+]\s+", content, re.MULTILINE)
        list_count = len(list_items)

        links = re.findall(r"\[([^\]]+)\]\([^\)]+\)", content)
        link_count = len(links)

        images = re.findall(r"!\[([^\]]*)\]\([^\)]+\)", content)
        image_count = len(images)

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

    def _analyze_readability(self, content: str) -> ReadabilityDict:
        """Analyze content readability using various metrics."""
        words = re.findall(r"\b\w+\b", content)
        sentences = re.split(r"[.!?]+", content)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not words or not sentences:
            return {"readability_score": 0, "grade_level": "N/A", "reading_ease": 0}

        avg_words_per_sentence = len(words) / len(sentences)

        syllable_count = sum(self._count_syllables(word) for word in words)
        avg_syllables_per_word = syllable_count / len(words)

        reading_ease = (
            206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)
        )
        reading_ease = max(0.0, min(100.0, reading_ease))

        grade_level = (
            (0.5 * avg_words_per_sentence) + (8.5 * avg_syllables_per_word) - 15.59
        )

        if reading_ease >= self.EXCELLENT_READABILITY_MIN:
            level = "Very Easy"
        elif reading_ease >= self.GOOD_READABILITY_MIN:
            level = "Easy"
        elif reading_ease >= self.FAIRLY_EASY_READABILITY_MIN:
            level = "Fairly Easy"
        elif reading_ease >= self.STANDARD_READABILITY_MIN:
            level = "Standard"
        elif reading_ease >= self.FAIRLY_DIFFICULT_READABILITY_MIN:
            level = "Fairly Difficult"
        elif reading_ease >= self.DIFFICULT_READABILITY_MIN:
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

    def _analyze_structure(self, content: str) -> StructureDict:
        """Analyze document structure and organization."""
        sections_list: MutableSequence[Mapping[str, int | str]] = []
        depth_analysis_dict: MutableMapping[str, int | float] = {}
        structure: StructureDict = {
            "has_table_of_contents": False,
            "toc_position": 0,
            "heading_hierarchy_valid": True,
            "sections": sections_list,
            "depth_analysis": depth_analysis_dict,
        }

        toc_patterns = [
            r"^#{1,6}.*\b[tT]able of [cC]ontents\b",
            r"^#{1,6}.*\b[cC]ontents?\b",
            r"^#{1,6}.*\b[tT]OC\b",
        ]

        for pattern in toc_patterns:
            toc_match = re.search(pattern, content, re.MULTILINE)
            if toc_match:
                structure["has_table_of_contents"] = True
                structure["toc_position"] = (
                    content[: toc_match.start()].count("\n")
                ) + 1
                break

        headings: MutableSequence[Mapping[str, int | str]] = []
        for match in re.finditer(r"^(#{1,6})\s+(.+)$", content, re.MULTILINE):
            level = len(match.group(1))
            title = match.group(2).strip()
            line_num = content[: match.start()].count("\n") + 1
            headings.append({"level": level, "title": title, "line": line_num})

        structure["sections"] = headings

        if len(headings) > 1:
            for i in range(1, len(headings)):
                cur_level = int(headings[i]["level"])
                prev_level = int(headings[i - 1]["level"])
                if cur_level > prev_level + 1:
                    structure["heading_hierarchy_valid"] = False
                    break

        depths: Sequence[int] = [int(h["level"]) for h in headings]
        max_depth = max(depths) if depths else 0
        avg_depth = sum(int(x) for x in depths) / len(depths) if depths else 0.0
        depth_dist: Mapping[int, int] = dict(Counter(depths))
        structure["depth_analysis"] = {
            "max_depth": max_depth,
            "avg_depth": avg_depth,
        }
        for key, val in depth_dist.items():
            structure["depth_analysis"][str(key)] = val

        return structure

    def _check_completeness(
        self,
        content: str,
        filename: str,
    ) -> CompletenessDict:
        """Check documentation completeness based on file type and content."""
        missing_elems: MutableSequence[str] = []
        required_present: MutableSequence[str] = []
        optional_present: MutableSequence[str] = []
        completeness: CompletenessDict = {
            "score": 100,
            "missing_elements": missing_elems,
            "required_sections_present": required_present,
            "optional_sections_present": optional_present,
            "word_count_sufficient": True,
            "missing_required_sections": list[str](),
        }

        word_count = len(re.findall(r"\b\w+\b", content))
        thresholds_val = self.config.get("quality_thresholds")
        thresholds: Mapping[str, bool | int | str] = (
            dict(thresholds_val) if isinstance(thresholds_val, dict) else {}
        )
        min_words_val = thresholds.get("min_word_count", 100)
        min_words = 100
        if isinstance(min_words_val, int):
            min_words = min_words_val

        if word_count < min_words:
            completeness["word_count_sufficient"] = False
            if "missing_elements" in completeness:
                completeness["missing_elements"].append(
                    f"Minimum word count ({min_words})",
                )
            if "score" in completeness:
                completeness["score"] -= 20

        if filename.endswith("README.md"):
            required_sections = [
                "Purpose|Overview|Introduction",
                "Installation|Setup",
                "Usage",
            ]
            result = self._check_required_sections(content, required_sections)
            if "required_sections_present" in completeness:
                completeness["required_sections_present"].extend(
                    result.get("required_sections_present", []),
                )
            if "missing_elements" in completeness:
                completeness["missing_elements"].extend(
                    result.get("missing_required_sections", []),
                )

        elif filename.startswith("docs/"):
            required_sections = ["Overview|Introduction"]
            result = self._check_required_sections(content, required_sections)
            if "required_sections_present" in completeness:
                completeness["required_sections_present"].extend(
                    result.get("required_sections_present", []),
                )
            if "missing_elements" in completeness:
                completeness["missing_elements"].extend(
                    result.get("missing_required_sections", []),
                )

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
                if "missing_elements" in completeness:
                    completeness["missing_elements"].append(description)
                if "score" in completeness:
                    completeness["score"] -= 5

        if "score" in completeness:
            completeness["score"] = max(0, completeness["score"])

        return completeness

    def _check_required_sections(
        self,
        content: str,
        required_sections: t.StrSequence,
    ) -> MutableMapping[str, MutableSequence[str]]:
        """Check for required sections in content."""
        required_present: MutableSequence[str] = []
        missing_required: MutableSequence[str] = []
        result: MutableMapping[str, MutableSequence[str]] = {
            "required_sections_present": required_present,
            "missing_required_sections": missing_required,
        }

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
                recommendations = self.results["recommendations"]
                recommendations.append(f"Add '{section_pattern}' section")

        return result

    def _calculate_quality_score(
        self,
        analysis: AnalysisDict,
    ) -> float:
        """Calculate overall quality score for the content."""
        score = 100.0

        metrics = analysis.get("metrics", {})
        readability = analysis.get("readability", {})
        completeness = analysis.get("completeness", {})
        structure = analysis.get("structure", {})

        completeness_score = completeness.get("score", 100)
        if isinstance(completeness_score, int):
            score -= (100 - completeness_score) * 0.5

        readability_score = readability.get("readability_score", 0)
        if (
            isinstance(readability_score, (int, float))
            and readability_score < self.MIN_READABILITY_SCORE
        ):
            penalty = (self.MIN_READABILITY_SCORE - readability_score) * 0.3
            score -= min(penalty, 20)

        word_count = metrics.get("word_count", 0)
        if isinstance(word_count, int) and word_count < self.MIN_WORD_COUNT:
            score -= 10

        heading_count = metrics.get("heading_count", 0)
        if isinstance(heading_count, int) and heading_count == 0:
            score -= 15

        link_count = metrics.get("link_count", 0)
        if isinstance(link_count, int) and link_count == 0:
            score -= 5

        if structure.get("has_table_of_contents"):
            score += 5

        if structure.get("heading_hierarchy_valid"):
            score += 5

        return max(0.0, min(100.0, score))

    def _identify_issues(self, analysis: AnalysisDict) -> MutableSequence[IssueDict]:
        """Identify content issues that need attention."""
        issues: MutableSequence[IssueDict] = []

        metrics = analysis.get("metrics", {})
        readability = analysis.get("readability", {})
        completeness = analysis.get("completeness", {})
        structure = analysis.get("structure", {})

        if not completeness.get("word_count_sufficient"):
            word_count = metrics.get("word_count", 0)
            issues.append({
                "type": "insufficient_content",
                "severity": "medium",
                "message": f"Content too short ({word_count} words)",
            })

        missing = completeness.get("missing_elements", [])
        if missing:
            issues.append({
                "type": "missing_elements",
                "severity": "high",
                "message": f"Missing: {', '.join(missing)}",
            })

        readability_score = readability.get("readability_score", 0)
        if (
            isinstance(readability_score, (int, float))
            and readability_score < self.FAIRLY_DIFFICULT_READABILITY_MIN
        ):
            issues.append({
                "type": "poor_readability",
                "severity": "medium",
                "message": f"Content difficult to read (score: {readability_score})",
            })

        if not structure.get("heading_hierarchy_valid"):
            issues.append({
                "type": "heading_hierarchy",
                "severity": "low",
                "message": "Heading hierarchy is not logical",
            })

        heading_count = metrics.get("heading_count", 0)
        if isinstance(heading_count, int) and heading_count == 0:
            issues.append({
                "type": "no_headings",
                "severity": "high",
                "message": "Document has no section headings",
            })

        return issues

    def _generate_suggestions(self, analysis: AnalysisDict) -> MutableSequence[str]:
        """Generate improvement suggestions based on analysis."""
        suggestions: MutableSequence[str] = []

        metrics = analysis.get("metrics", {})
        readability = analysis.get("readability", {})
        structure = analysis.get("structure", {})

        word_count = metrics.get("word_count", 0)
        if isinstance(word_count, int) and word_count < 2 * self.MIN_WORD_COUNT:
            suggestions.append(
                "Expand content with more detailed explanations and examples",
            )

        readability_score = readability.get("readability_score", 0)
        if (
            isinstance(readability_score, (int, float))
            and readability_score < self.MIN_READABILITY_SCORE
        ):
            suggestions.append(
                "Simplify language and sentence structure for better readability",
            )

        heading_count = metrics.get("heading_count", 0)
        if isinstance(heading_count, int) and (
            not structure.get("has_table_of_contents")
            and heading_count > self.MIN_HEADINGS_FOR_TOC
        ):
            suggestions.append("Add a table of contents for better navigation")

        code_block_count = metrics.get("code_block_count", 0)
        file_name = analysis.get("file", "")
        if (
            isinstance(code_block_count, int)
            and isinstance(file_name, str)
            and code_block_count == 0
            and "tutorial" in file_name.lower()
        ):
            suggestions.append("Add code examples to illustrate concepts")

        link_count = metrics.get("link_count", 0)
        if isinstance(link_count, int) and link_count == 0:
            suggestions.append(
                "Add relevant links to related documentation or external resources",
            )

        return suggestions

    def analyze_files_batch(self, file_paths: Sequence[Path]) -> ResultsDict:
        """Analyze multiple files and aggregate results."""
        for file_path in file_paths:
            self.analyze_file(file_path)

        self._generate_overall_recommendations()

        return self.results

    def _generate_overall_recommendations(self) -> None:
        """Generate overall recommendations based on batch analysis."""
        content_scores = self.results["content_scores"]
        if not content_scores:
            return

        score_values = [float(v) for v in content_scores.values()]
        avg_score = sum(score_values) / len(score_values)

        recommendations = self.results["recommendations"]

        if avg_score < self.GOOD_READABILITY_MIN:
            recommendations.append({
                "priority": "high",
                "type": "overall_quality",
                "message": f"Overall documentation quality needs improvement (avg score: {avg_score:.1f})",
                "actions": [
                    "Focus on adding missing content and sections",
                    "Improve readability and structure",
                    "Add more examples and practical guidance",
                ],
            })

        all_issues: MutableSequence[t.StrMapping] = []
        for result_value in self.results.values():
            if isinstance(result_value, dict):
                issues_val: Sequence[t.StrMapping] | None = result_value.get("issues")
                if isinstance(issues_val, list):
                    all_issues.extend(issues_val)

        if all_issues:
            issue_types = Counter(str(issue.get("type", "")) for issue in all_issues)
            most_common = issue_types.most_common(1)
            if most_common:
                common_issue = most_common[0][0]
                recommendations.append({
                    "priority": "medium",
                    "type": "common_issue",
                    "message": f"Address common issue across files: {common_issue.replace('_', ' ')}",
                    "actions": [
                        "Implement consistent fixes",
                        "Update style guidelines",
                    ],
                })

    def generate_report(self, output_format: str = "json") -> str:
        """Generate content analysis report."""
        if output_format == "json":
            return _RESULTS_ADAPTER.dump_json(self.results, indent=2).decode()
        if output_format == "summary":
            return self._generate_summary_report()
        return _RESULTS_ADAPTER.dump_json(self.results).decode()

    def _generate_summary_report(self) -> str:
        """Generate human-readable summary report."""
        content_scores = self.results["content_scores"]
        if not content_scores:
            return "No content analysis results available."

        scores = [float(v) for v in content_scores.values()]
        avg_score = sum(scores) / len(scores)

        report = f"""
Content Quality Analysis Summary
=================================

Files Analyzed: {self.results["files_analyzed"]}
Average Quality Score: {avg_score:.1f}/100

Score Distribution:
- Excellent ({self.EXCELLENT_READABILITY_MIN}-100): {len([s for s in scores if s >= self.EXCELLENT_READABILITY_MIN])}
- Good ({self.GOOD_READABILITY_MIN}-{self.EXCELLENT_READABILITY_MIN - 1}): {len([s for s in scores if self.GOOD_READABILITY_MIN <= s < self.EXCELLENT_READABILITY_MIN])}
- Needs Improvement ({self.FAIRLY_DIFFICULT_READABILITY_MIN}-{self.GOOD_READABILITY_MIN - 1}): {len([s for s in scores if self.FAIRLY_DIFFICULT_READABILITY_MIN <= s < self.GOOD_READABILITY_MIN])}
- Poor (<{self.FAIRLY_DIFFICULT_READABILITY_MIN}): {len([s for s in scores if s < self.FAIRLY_DIFFICULT_READABILITY_MIN])}

Top Recommendations:
"""

        recommendations = self.results["recommendations"]
        for rec in recommendations[:3]:
            if isinstance(rec, dict):
                report += f"- {rec.get('message', '')}\n"
            else:
                report += f"- {rec}\n"

        return report

    def save_report(self, output_path: str = "docs/maintenance/reports/") -> str:
        """Save content analysis report.

        Args:
            output_path: Directory path where to save the report.

        Returns:
            File path of the saved report.

        """
        Path(output_path).mkdir(exist_ok=True, parents=True)

        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        filename = f"content_analysis_{timestamp}.json"
        filepath = Path(output_path) / filename

        Path(filepath).write_bytes(_RESULTS_ADAPTER.dump_json(self.results, indent=2))

        return str(filepath)


def analyze_file_content(
    file_path: str,
    config_path: str | None = None,
) -> AnalysisDict:
    """Convenience function to analyze a single file."""
    analyzer = FlextQualityContentAnalyzer(config_path)
    return analyzer.analyze_file(Path(file_path))


def analyze_files_content(
    file_paths: t.StrSequence,
    config_path: str | None = None,
) -> ResultsDict:
    """Convenience function to analyze multiple files."""
    analyzer = FlextQualityContentAnalyzer(config_path)
    paths = [Path(fp) for fp in file_paths]
    return analyzer.analyze_files_batch(paths)


if __name__ == "__main__":
    import sys

    MIN_ARGS = 2
    if len(sys.argv) < MIN_ARGS:
        sys.exit(1)

    file_path = sys.argv[1]
    config_path = sys.argv[2] if len(sys.argv) > MIN_ARGS else None

    results = analyze_file_content(file_path, config_path)

    issues = results.get("issues")
    if issues:
        for _issue in issues[:2]:
            pass

    suggestions = results.get("suggestions")
    if suggestions:
        for _suggestion in suggestions[:2]:
            pass
