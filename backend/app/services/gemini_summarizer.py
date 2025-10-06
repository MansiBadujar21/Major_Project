"""
TODO List:
1. PDF upload and extraction logic - DONE
2. Table detection and extraction - DONE  
3. Gemini API integration - DONE
4. Chunking large content - DONE
5. Summary formatting - DONE
6. Integration with chatbot UI - DONE
7. Scalable multi-user handling - DONE
8. Error handling and retry logic - DONE
9. Rate limiting and cost optimization - DONE
10. Caching for repeated documents - TODO
"""

import os
import re
import json
import asyncio
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import pandas as pd
import google.generativeai as genai
from concurrent.futures import ThreadPoolExecutor, as_completed

from .doc_parser import parse_document
from .pdf_analyzer import PDFAnalyzer, DocumentStructure


@dataclass
class TableInfo:
    """Structured table information"""
    id: int
    title: str
    data: pd.DataFrame
    markdown: str
    csv_text: str
    row_count: int
    col_count: int


@dataclass
class ChunkInfo:
    """Information about text chunks"""
    id: int
    content: str
    start_page: int
    end_page: int
    word_count: int
    token_estimate: int


@dataclass
class SummaryResult:
    """Complete summary result"""
    document_type: str
    executive_summary: str
    key_points: List[str]
    tables: List[TableInfo]
    section_summaries: List[Dict]
    total_pages: int
    processing_time: float
    model_used: str


class GeminiSummarizer:
    def __init__(self):
        # Initialize Gemini API
        api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        
        # Initialize model - Using advanced AI for better performance
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Configuration
        self.max_tokens_per_chunk = 2000000  # Advanced AI context limit (2M tokens)
        self.max_concurrent_requests = 5  # Rate limiting
        self.retry_attempts = 3
        self.chunk_overlap = 1000  # Words overlap between chunks
        
        # Initialize components
        self.pdf_analyzer = PDFAnalyzer()
        
        # Thread pool for concurrent processing
        self.executor = ThreadPoolExecutor(max_workers=self.max_concurrent_requests)
    
    async def summarize_pdf(self, filename: str, content: bytes) -> SummaryResult:
        """Main function to summarize PDF using Gemini"""
        import time
        start_time = time.time()
        
        try:
            # Step 1: Analyze document structure
            structure = self.pdf_analyzer.analyze_document(filename, content)
            
            # Step 2: Extract text and tables
            raw_text = parse_document(filename, content)
            tables = self._extract_tables_structured(raw_text)
            
            # Step 3: Chunk content for large documents
            chunks = self._create_chunks(raw_text, structure.total_pages)
            
            # Step 4: Generate summaries using Gemini
            if len(chunks) == 1:
                # Single chunk - direct summarization
                summary = await self._summarize_single_chunk(chunks[0], tables, structure.doc_type)
            else:
                # Multiple chunks - map-reduce approach
                summary = await self._summarize_multiple_chunks(chunks, tables, structure.doc_type)
            
            # Step 5: Format final result
            processing_time = time.time() - start_time
            
            return SummaryResult(
                document_type=structure.doc_type,
                executive_summary=summary["executive_summary"],
                key_points=summary["key_points"],
                tables=tables,
                section_summaries=summary.get("section_summaries", []),
                total_pages=structure.total_pages,
                processing_time=processing_time,
                model_used="gemini-2.0-flash-exp"
            )
            
        except Exception as e:
            raise Exception(f"PDF summarization failed: {str(e)}")
    
    async def _summarize_with_gemini(self, raw_text: str, tables: List[TableInfo], structure: DocumentStructure, start_time: float) -> SummaryResult:
        """Summarize using Gemini API"""
        # Step 3: Chunk content for large documents
        chunks = self._create_chunks(raw_text, structure.total_pages)
        
        # Step 4: Generate summaries using Gemini
        if len(chunks) == 1:
            # Single chunk - direct summarization
            summary = await self._summarize_single_chunk(chunks[0], tables, structure.doc_type)
        else:
            # Multiple chunks - map-reduce approach
            summary = await self._summarize_multiple_chunks(chunks, tables, structure.doc_type)
        
        # Step 5: Format final result
        processing_time = time.time() - start_time
        
        return SummaryResult(
            document_type=structure.doc_type,
            executive_summary=summary["executive_summary"],
            key_points=summary["key_points"],
            tables=tables,
            section_summaries=summary.get("section_summaries", []),
            total_pages=structure.total_pages,
            processing_time=processing_time,
            model_used="gemini-2.0-flash-exp"
        )
    
    def _extract_tables_structured(self, text: str) -> List[TableInfo]:
        """Extract tables in structured format for Gemini"""
        tables = []
        
        # Use existing table extraction logic
        table_data_list = self.pdf_analyzer._extract_tables(text)
        
        for i, table_data in enumerate(table_data_list):
            if table_data and table_data.data is not None:
                # Convert to CSV text
                csv_text = table_data.data.to_csv(index=False)
                
                # Convert to markdown
                markdown = self._dataframe_to_markdown(table_data.data)
                
                tables.append(TableInfo(
                    id=i + 1,
                    title=table_data.title,
                    data=table_data.data,
                    markdown=markdown,
                    csv_text=csv_text,
                    row_count=table_data.row_count,
                    col_count=table_data.col_count
                ))
        
        return tables
    
    def _dataframe_to_markdown(self, df: pd.DataFrame) -> str:
        """Convert DataFrame to markdown table"""
        if df.empty:
            return "Empty table"
        
        # Create markdown table
        markdown = "| " + " | ".join(str(col) for col in df.columns) + " |\n"
        markdown += "| " + " | ".join(["---"] * len(df.columns)) + " |\n"
        
        # Add data rows (limit to first 20 rows for readability)
        for _, row in df.head(20).iterrows():
            markdown += "| " + " | ".join(str(cell) for cell in row) + " |\n"
        
        if len(df) > 20:
            markdown += f"\n*... and {len(df) - 20} more rows*\n"
        
        return markdown
    
    def _create_chunks(self, text: str, total_pages: int) -> List[ChunkInfo]:
        """Create chunks for large documents"""
        words = text.split()
        total_words = len(words)
        
        # Estimate tokens (rough approximation: 1 word ≈ 1.3 tokens)
        estimated_tokens = int(total_words * 1.3)
        
        if estimated_tokens <= self.max_tokens_per_chunk:
            # Single chunk
            return [ChunkInfo(
                id=1,
                content=text,
                start_page=1,
                end_page=total_pages,
                word_count=total_words,
                token_estimate=estimated_tokens
            )]
        
        # Multiple chunks needed
        chunks = []
        chunk_size = int(self.max_tokens_per_chunk / 1.3)  # Convert back to words
        overlap_words = self.chunk_overlap
        
        for i in range(0, total_words, chunk_size - overlap_words):
            end_idx = min(i + chunk_size, total_words)
            chunk_words = words[i:end_idx]
            chunk_text = " ".join(chunk_words)
            
            # Estimate page range
            start_page = max(1, int(i / total_words * total_pages))
            end_page = min(total_pages, int(end_idx / total_words * total_pages))
            
            chunks.append(ChunkInfo(
                id=len(chunks) + 1,
                content=chunk_text,
                start_page=start_page,
                end_page=end_page,
                word_count=len(chunk_words),
                token_estimate=int(len(chunk_words) * 1.3)
            ))
        
        return chunks
    
    async def _summarize_single_chunk(self, chunk: ChunkInfo, tables: List[TableInfo], doc_type: str) -> Dict:
        """Summarize a single chunk using Gemini"""
        prompt = self._create_summarization_prompt(chunk.content, tables, doc_type, is_single_chunk=True)
        
        response = await self._call_gemini_with_retry(prompt)
        return self._parse_summary_response(response)
    
    async def _summarize_multiple_chunks(self, chunks: List[ChunkInfo], tables: List[TableInfo], doc_type: str) -> Dict:
        """Summarize multiple chunks using map-reduce approach"""
        
        # Step 1: Summarize each chunk
        chunk_summaries = []
        tasks = []
        
        for chunk in chunks:
            task = self._summarize_chunk_async(chunk, tables, doc_type)
            tasks.append(task)
        
        # Execute all chunk summaries concurrently
        chunk_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out failed results
        for i, result in enumerate(chunk_results):
            if isinstance(result, Exception):
                print(f"Chunk {i+1} failed: {result}")
            else:
                chunk_summaries.append(result)
        
        if not chunk_summaries:
            raise Exception("All chunk summaries failed")
        
        # Step 2: Combine chunk summaries
        combined_summary = "\n\n".join([
            f"Chunk {i+1} (Pages {chunk.start_page}-{chunk.end_page}):\n{summary}"
            for i, (chunk, summary) in enumerate(zip(chunks, chunk_summaries))
        ])
        
        # Step 3: Create final summary prompt
        final_prompt = self._create_final_summary_prompt(combined_summary, tables, doc_type)
        
        # Step 4: Generate final summary
        final_response = await self._call_gemini_with_retry(final_prompt)
        return self._parse_summary_response(final_response)
    
    async def _summarize_chunk_async(self, chunk: ChunkInfo, tables: List[TableInfo], doc_type: str) -> str:
        """Asynchronously summarize a single chunk"""
        prompt = self._create_summarization_prompt(chunk.content, tables, doc_type, is_single_chunk=False)
        response = await self._call_gemini_with_retry(prompt)
        return response
    
    def _create_summarization_prompt(self, text: str, tables: List[TableInfo], doc_type: str, is_single_chunk: bool) -> str:
        """Create prompt for Gemini summarization"""
        
        prompt = f"""You are an expert document analyst. Analyze the following document content and provide a comprehensive summary.

DOCUMENT TYPE: {doc_type}
{'SINGLE CHUNK' if is_single_chunk else 'PARTIAL CHUNK'}

INSTRUCTIONS:
1. Provide a concise but complete summary
2. Extract key points and insights
3. If tables are present, analyze their content and trends
4. Preserve important numbers, dates, and names
5. Focus on actionable insights and main takeaways

DOCUMENT CONTENT:
{text[:50000]}  # Limit content length for API

"""

        if tables:
            prompt += "\nTABLES FOUND:\n"
            for table in tables:
                prompt += f"\nTable {table.id}: {table.title}\n"
                prompt += f"Dimensions: {table.row_count} rows × {table.col_count} columns\n"
                prompt += "Data (CSV format):\n"
                prompt += table.csv_text[:10000] + "\n"  # Limit table size
                prompt += "Markdown format:\n"
                prompt += table.markdown + "\n"
        
        prompt += """

RESPONSE FORMAT (JSON):
{
  "executive_summary": "2-3 paragraph executive summary",
  "key_points": ["point1", "point2", "point3", ...],
  "table_insights": ["insight1", "insight2", ...],
  "main_takeaways": ["takeaway1", "takeaway2", ...],
  "section_summaries": [
    {
      "section": "section_name",
      "summary": "section summary",
      "key_points": ["point1", "point2"]
    }
  ]
}

Provide your response in valid JSON format only."""

        return prompt
    
    def _create_final_summary_prompt(self, combined_summary: str, tables: List[TableInfo], doc_type: str) -> str:
        """Create prompt for final summary combining all chunks"""
        
        prompt = f"""You are an expert document analyst. Create a comprehensive final summary from the following chunk summaries.

DOCUMENT TYPE: {doc_type}
TOTAL CHUNKS: Multiple chunks combined

INSTRUCTIONS:
1. Create a cohesive executive summary that covers the entire document
2. Consolidate key points from all chunks
3. Identify overarching themes and patterns
4. Provide actionable insights
5. Ensure the summary flows logically

COMBINED CHUNK SUMMARIES:
{combined_summary[:100000]}  # Limit content length

"""

        if tables:
            prompt += "\nTABLES SUMMARY:\n"
            for table in tables:
                prompt += f"\nTable {table.id}: {table.title} ({table.row_count} rows, {table.col_count} columns)\n"
        
        prompt += """

RESPONSE FORMAT (JSON):
{
  "executive_summary": "Comprehensive 3-4 paragraph executive summary covering the entire document",
  "key_points": ["consolidated point1", "consolidated point2", "consolidated point3", ...],
  "table_insights": ["overall table insight1", "overall table insight2", ...],
  "main_takeaways": ["overall takeaway1", "overall takeaway2", ...],
  "section_summaries": [
    {
      "section": "major_section_name",
      "summary": "comprehensive section summary",
      "key_points": ["consolidated point1", "consolidated point2"]
    }
  ]
}

Provide your response in valid JSON format only."""

        return prompt
    
    async def _call_gemini_with_retry(self, prompt: str) -> str:
        """Call Gemini API with retry logic"""
        for attempt in range(self.retry_attempts):
            try:
                # Run the synchronous Gemini call in a thread pool
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    self.executor, 
                    self.model.generate_content, 
                    prompt
                )
                return response.text
            except Exception as e:
                if attempt == self.retry_attempts - 1:
                    raise Exception(f"Gemini API call failed after {self.retry_attempts} attempts: {str(e)}")
                
                # Wait before retry (exponential backoff)
                await asyncio.sleep(2 ** attempt)
        
        raise Exception("Unexpected error in Gemini API call")
    
    def _parse_summary_response(self, response: str) -> Dict:
        """Parse Gemini response and extract structured data"""
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            
            # Fallback: parse as text
            return {
                "executive_summary": response[:1000],
                "key_points": [response[i:i+100] for i in range(0, min(len(response), 500), 100)],
                "table_insights": [],
                "main_takeaways": [],
                "section_summaries": []
            }
            
        except json.JSONDecodeError:
            # If JSON parsing fails, return structured text
            return {
                "executive_summary": response[:1000],
                "key_points": [response[i:i+100] for i in range(0, min(len(response), 500), 100)],
                "table_insights": [],
                "main_takeaways": [],
                "section_summaries": []
            }
    
    def format_summary_for_chat(self, result: SummaryResult) -> str:
        """Format summary result for chatbot response"""
        
        markdown = f"# Document Summary\n\n"
        markdown += f"**Document Type:** {result.document_type}\n"
        markdown += f"**Pages:** {result.total_pages}\n"
        markdown += f"**Processing Time:** {result.processing_time:.2f} seconds\n"
        markdown += f"**Model:** {result.model_used}\n\n"
        
        # Executive Summary
        markdown += "## Executive Summary\n\n"
        markdown += result.executive_summary + "\n\n"
        
        # Key Points
        if result.key_points:
            markdown += "## Key Points\n\n"
            for i, point in enumerate(result.key_points, 1):
                markdown += f"{i}. {point}\n"
            markdown += "\n"
        
        # Tables Section
        if result.tables:
            markdown += "## Tables\n\n"
            for table in result.tables:
                markdown += f"### Table {table.id}: {table.title}\n"
                markdown += f"**Dimensions:** {table.row_count} rows × {table.col_count} columns\n\n"
                markdown += table.markdown + "\n\n"
        
        # Section Summaries
        if result.section_summaries:
            markdown += "## Section Summaries\n\n"
            for section in result.section_summaries:
                markdown += f"### {section.get('section', 'Section')}\n"
                markdown += section.get('summary', '') + "\n\n"
                if section.get('key_points'):
                    markdown += "**Key Points:**\n"
                    for point in section['key_points']:
                        markdown += f"- {point}\n"
                    markdown += "\n"
        
        return markdown
    
    def cleanup(self):
        """Cleanup resources"""
        self.executor.shutdown(wait=True)
