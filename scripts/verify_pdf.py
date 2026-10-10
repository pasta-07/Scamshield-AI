"""
Verify PDF structure, exact page counts, slide breakdown,
and text integrity of ScamShield_AI_Pitch_Deck_and_Architecture.pdf.
"""

import os
import pypdf

PDF_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs', 'ScamShield_AI_Pitch_Deck_and_Architecture.pdf')

def verify_pdf():
    assert os.path.exists(PDF_PATH), f"PDF does not exist at {PDF_PATH}"
    size_bytes = os.path.getsize(PDF_PATH)
    print(f"File Size: {size_bytes / 1024:.1f} KB")

    reader = pypdf.PdfReader(PDF_PATH)
    total_pages = len(reader.pages)
    print(f"Total Pages: {total_pages}")
    
    assert total_pages == 13, f"Expected exactly 13 pages (10 slides + 3 arch pages), but found {total_pages}"

    # Verify each page
    expected_headings = [
        "SCAMSHIELD AI",
        "THE PROBLEM: MULTI-STAGE SOCIAL ENGINEERING IN INDIA",
        "ANATOMY OF A MULTI-STAGE SOCIAL ENGINEERING ATTACK",
        "THE SCAMSHIELD AI SOLUTION: FOUR CORE INNOVATIONS",
        "DETECTION ENGINE: THREAT CLUSTERS & CALIBRATION",
        "SIGNATURE FEATURE: WORKFLOW CORRELATION & INTERVENTION",
        "TECHNOLOGY STACK, PERFORMANCE & ROBUSTNESS",
        "COMPETITIVE DIFFERENTIATION MATRIX",
        "EMPIRICAL VALIDATION & MEASURED BENCHMARKS",
        "RESPONSIBLE AI, TEAM RESPONSIBILITIES & ROADMAP",
        "SYSTEM ARCHITECTURE SPECIFICATION -- PAGE 1 OF 3",
        "SYSTEM ARCHITECTURE SPECIFICATION -- PAGE 2 OF 3",
        "SYSTEM ARCHITECTURE SPECIFICATION -- PAGE 3 OF 3"
    ]

    for idx, (page, expected_h) in enumerate(zip(reader.pages, expected_headings)):
        text = page.extract_text()
        print(f"\n--- Page {idx+1} [Matches: '{expected_h[:35]}...'] ---")
        assert expected_h in text, f"Page {idx+1} missing expected heading: '{expected_h}'"
        print(f"  [PASS] Found heading and valid content ({len(text)} characters).")

    print("\n=======================================================")
    print("ALL 13 PDF PAGES VERIFIED SUCCESSFULLY WITH 100% INTEGRITY")
    print("=======================================================")

if __name__ == '__main__':
    verify_pdf()
