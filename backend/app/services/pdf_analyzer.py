import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import pandas as pd
from pathlib import Path

from .doc_parser import parse_document


@dataclass
class TableData:
    """Represents extracted table data"""
    title: str
    data: pd.DataFrame
    page: int
    row_count: int
    col_count: int


@dataclass
class DocumentStructure:
    """Represents the analyzed structure of a document"""
    doc_type: str  # "TEXT-HEAVY", "TABLE-HEAVY", "MIXED"
    text_ratio: float
    table_ratio: float
    total_pages: int
    tables: List[TableData]
    sections: List[str]
    word_count: int
    table_count: int


class PDFAnalyzer:
    def __init__(self):
        self.table_patterns = [
            r'\b\d+\s*\|\s*\d+\s*\|\s*\d+',  # Number | Number | Number
            r'\b[A-Z][a-z]+\s*\|\s*\d+',     # Word | Number
            r'\b\d+\s*%\s*\|\s*\d+',         # Number% | Number
            r'\b[A-Z]{2,}\s*\|\s*[A-Z]{2,}', # UPPERCASE | UPPERCASE
        ]
        
    def analyze_document(self, filename: str, content: bytes) -> DocumentStructure:
        """Main analysis function"""
        # Parse document
        raw_text = parse_document(filename, content)
        
        # Extract structure information
        text_blocks = self._extract_text_blocks(raw_text)
        tables = self._extract_tables(raw_text)
        sections = self._identify_sections(raw_text)
        
        # Calculate ratios
        text_word_count = sum(len(block.split()) for block in text_blocks)
        table_word_count = sum(len(str(table.data).split()) for table in tables)
        total_words = text_word_count + table_word_count
        
        text_ratio = text_word_count / total_words if total_words > 0 else 0
        table_ratio = table_word_count / total_words if total_words > 0 else 0
        
        # Determine document type
        doc_type = self._classify_document_type(text_ratio, table_ratio, len(tables))
        
        return DocumentStructure(
            doc_type=doc_type,
            text_ratio=text_ratio,
            table_ratio=table_ratio,
            total_pages=self._estimate_pages(raw_text),
            tables=tables,
            sections=sections,
            word_count=total_words,
            table_count=len(tables)
        )
    
    def _extract_text_blocks(self, text: str) -> List[str]:
        """Extract meaningful text blocks, excluding table-like content"""
        # Split by double newlines to get paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        # Filter out table-like content
        text_blocks = []
        for para in paragraphs:
            if not self._looks_like_table(para):
                text_blocks.append(para)
        
        return text_blocks
    
    def _looks_like_table(self, text: str) -> bool:
        """Check if text block looks like a table"""
        lines = text.split('\n')
        if len(lines) < 2:
            return False
        
        # Check for table patterns
        for pattern in self.table_patterns:
            if re.search(pattern, text):
                return True
        
        # Check for consistent separators
        separator_counts = []
        for line in lines[:5]:  # Check first 5 lines
            separators = len(re.findall(r'[|,;\t]', line))
            separator_counts.append(separators)
        
        # If most lines have similar separator counts, likely a table
        if len(set(separator_counts)) <= 2 and max(separator_counts) > 0:
            return True
        
        return False
    
    def _extract_tables(self, text: str) -> List[TableData]:
        """Extract tables from text"""
        tables = []
        lines = text.split('\n')
        
        current_table = []
        table_start = 0
        
        for i, line in enumerate(lines):
            if self._looks_like_table(line):
                if not current_table:
                    table_start = i
                current_table.append(line)
            else:
                if current_table:
                    # Process the table
                    table_data = self._process_table_lines(current_table, table_start)
                    if table_data:
                        tables.append(table_data)
                    current_table = []
        
        # Handle table at end of document
        if current_table:
            table_data = self._process_table_lines(current_table, table_start)
            if table_data:
                tables.append(table_data)
        
        return tables
    
    def _process_table_lines(self, lines: List[str], page: int) -> Optional[TableData]:
        """Convert table lines to structured data"""
        if len(lines) < 2:
            return None
        
        # Try to parse as CSV-like structure
        try:
            # Clean lines and split by common separators
            cleaned_lines = []
            for line in lines:
                # Replace multiple spaces with single space
                line = re.sub(r'\s+', ' ', line.strip())
                # Split by common table separators
                if '|' in line:
                    parts = [p.strip() for p in line.split('|')]
                elif '\t' in line:
                    parts = [p.strip() for p in line.split('\t')]
                else:
                    parts = [p.strip() for p in line.split(',')]
                cleaned_lines.append(parts)
            
            # Create DataFrame
            df = pd.DataFrame(cleaned_lines[1:], columns=cleaned_lines[0])
            
            return TableData(
                title=f"Table on page {page}",
                data=df,
                page=page,
                row_count=len(df),
                col_count=len(df.columns)
            )
        except Exception:
            return None
    
    def _identify_sections(self, text: str) -> List[str]:
        """Identify document sections"""
        sections = []
        
        # Common section patterns
        section_patterns = [
            r'^\d+\.\s*([A-Z][^.\n]+)',  # 1. Section Name
            r'^([A-Z][A-Z\s]+):',        # SECTION NAME:
            r'^([A-Z][a-z\s]+)\n[-=]+',  # Section Name\n----
        ]
        
        lines = text.split('\n')
        for line in lines:
            for pattern in section_patterns:
                match = re.match(pattern, line.strip())
                if match:
                    section_name = match.group(1).strip()
                    if len(section_name) > 3:  # Avoid short matches
                        sections.append(section_name)
                    break
        
        return sections
    
    def _estimate_pages(self, text: str) -> int:
        """Estimate number of pages based on content length"""
        # Rough estimate: 500 words per page
        word_count = len(text.split())
        return max(1, word_count // 500)
    
    def _classify_document_type(self, text_ratio: float, table_ratio: float, table_count: int) -> str:
        """Classify document as TEXT-HEAVY, TABLE-HEAVY, or MIXED"""
        if table_count == 0:
            return "TEXT-HEAVY"
        elif table_count >= 5 and table_ratio > 0.4:
            return "TABLE-HEAVY"
        elif table_ratio > 0.6:
            return "TABLE-HEAVY"
        elif text_ratio > 0.7:
            return "TEXT-HEAVY"
        else:
            return "MIXED"
    
    def generate_analysis_report(self, structure: DocumentStructure, raw_text: str) -> Dict:
        """Generate comprehensive analysis report"""
        report = {
            "document_type": structure.doc_type,
            "statistics": {
                "total_words": structure.word_count,
                "total_pages": structure.total_pages,
                "table_count": structure.table_count,
                "text_ratio": f"{structure.text_ratio:.1%}",
                "table_ratio": f"{structure.table_ratio:.1%}"
            },
            "sections": structure.sections,
            "tables": []
        }
        
        # Process tables
        for i, table in enumerate(structure.tables):
            table_report = {
                "title": table.title,
                "dimensions": f"{table.row_count} rows × {table.col_count} columns",
                "data": table.data.to_dict('records')[:10],  # First 10 rows
                "insights": self._analyze_table_content(table.data)
            }
            report["tables"].append(table_report)
        
        return report
    
    def _analyze_table_content(self, df: pd.DataFrame) -> List[str]:
        """Analyze table content for insights"""
        insights = []
        
        try:
            # Check for numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                for col in numeric_cols:
                    if df[col].notna().sum() > 0:
                        min_val = df[col].min()
                        max_val = df[col].max()
                        avg_val = df[col].mean()
                        insights.append(f"Column '{col}': Range {min_val:.2f} - {max_val:.2f}, Average {avg_val:.2f}")
            
            # Check for categorical columns
            categorical_cols = df.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                unique_count = df[col].nunique()
                if unique_count < 20:  # Not too many unique values
                    top_values = df[col].value_counts().head(3)
                    insights.append(f"Column '{col}': {unique_count} unique values, top: {dict(top_values)}")
        
        except Exception:
            insights.append("Table structure analysis completed")
        
        return insights
