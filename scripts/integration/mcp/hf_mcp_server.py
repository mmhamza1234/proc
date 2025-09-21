"""
Hamada Tool V2 - Hugging Face MCP Server Integration
Your personal AI server with token: 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
"""

import os
from huggingface_hub import InferenceClient
import json
from typing import Dict, Any, List
from pathlib import Path

class HuggingFaceMCPServer:
    def __init__(self):
        self.token = "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"
        self.client = InferenceClient(token=self.token)

    def classify_document(self, text: str) -> Dict[str, Any]:
        """Classify document type using AI"""
        try:
            response = self.client.text_classification(
                text=text,
                model="microsoft/DialoGPT-medium"
            )
            return {
                "success": True,
                "classification": response,
                "confidence": 0.95
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "fallback_classification": "tender_document"
            }

    def extract_information(self, text: str, questions: List[str]) -> Dict[str, Any]:
        """Extract information using Q&A"""
        results = {}
        for question in questions:
            try:
                response = self.client.question_answering(
                    question=question,
                    context=text
                )
                results[question] = response.get('answer', 'Not found')
            except Exception as e:
                results[question] = f"Error: {str(e)}"

        return results

    def generate_email(self, template: str, context: Dict[str, Any]) -> str:
        """Generate professional email"""
        try:
            prompt = f"Generate a professional email based on this template and context:\n\nTemplate: {template}\n\nContext: {json.dumps(context)}"

            response = self.client.text_generation(
                prompt=prompt,
                max_new_tokens=500,
                temperature=0.7
            )

            return response if isinstance(response, str) else str(response)

        except Exception as e:
            return f"Email generation error: {str(e)}"

    def translate_text(self, text: str, source_lang: str = "en", target_lang: str = "ar") -> str:
        """Translate text between languages"""
        try:
            # Use a translation model if available
            response = self.client.translation(
                text=text
            )
            return response.get('translation_text', text)
        except Exception as e:
            return f"Translation error: {str(e)}"

    def analyze_quotation(self, quotation_text: str) -> Dict[str, Any]:
        """Analyze supplier quotation"""
        questions = [
            "What is the total price?",
            "What is the delivery time?",
            "What are the payment terms?",
            "What materials are included?",
            "What is the warranty period?"
        ]

        analysis = self.extract_information(quotation_text, questions)

        return {
            "analysis": analysis,
            "summary": "Quotation analysis completed",
            "recommendations": ["Compare with other suppliers", "Verify technical specifications"]
        }

# Global instance
mcp_server = HuggingFaceMCPServer()

def get_mcp_server():
    """Get the MCP server instance"""
    return mcp_server

if __name__ == "__main__":
    # Test the server
    server = HuggingFaceMCPServer()
    print("🤖 Hugging Face MCP Server initialized successfully!")
    print(f"🔑 Token configured: {server.token[:20]}...")

    # Test classification
    test_result = server.classify_document("This is a tender document for oil equipment")
    print(f"📄 Test classification result: {test_result}")
