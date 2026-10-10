"""
ScamShield AI - Vercel Serverless Function Handler
Provides HTTP API endpoints for scam analysis and metadata on Vercel.
"""

import os
import sys
import json
from http.server import BaseHTTPRequestHandler

# Ensure root src is importable
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.signal_extractor import SignalExtractor
from src.risk_scoring import calculate_risk_score
from src.explanations import generate_explanation

_extractor = SignalExtractor()


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "status": "online",
            "service": "ScamShield AI - Detection API",
            "version": "1.0.0",
            "hackathon": "RAKSHAM AI Cybersecurity Hackathon | IIT Delhi",
            "endpoints": {
                "GET /": "Health & Service metadata",
                "POST /api/analyze": "Submit message payload for AI/heuristic scam analysis"
            }
        }
        self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            body = json.loads(post_data.decode('utf-8'))
            message = body.get('message', '')
            sender = body.get('sender', '')
            url = body.get('url', '')
            
            if not message or not message.strip():
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                err = {"error": "Missing or empty 'message' field in JSON request body."}
                self.wfile.write(json.dumps(err).encode('utf-8'))
                return
            
            # Run ScamShield analysis pipeline
            extracted = _extractor.extract_signals(text=message, sender=sender, url=url)
            signals = extracted.get("signals", [])
            scoring = calculate_risk_score(signals)
            xai = generate_explanation(
                signals=signals,
                risk_score=scoring["final_score"],
                risk_level=scoring["risk_level"],
                url_details=extracted.get("url_details", [])
            )
            
            result = {
                "success": True,
                "input_length": len(message),
                "risk_score": scoring["final_score"],
                "risk_level": scoring["risk_level"],
                "confidence": scoring["confidence"],
                "signals_detected": [
                    {
                        "signal_id": s.get("id"),
                        "name": s.get("name"),
                        "category": s.get("category"),
                        "evidence": s.get("evidence"),
                        "weight": s.get("weight")
                    }
                    for s in signals
                ],
                "explanation": xai
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result, indent=2).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            err = {"error": f"Internal analysis exception: {str(e)}"}
            self.wfile.write(json.dumps(err).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
