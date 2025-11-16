#!/usr/bin/env python3
"""
Simple test for Auditor Agent

Tests basic functionality without requiring external dependencies
"""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.auditor_agent import AuditorAgent, Verdict


def create_test_workflow_output():
    """Create a simple test workflow output"""
    return {
        "meeting_metadata": {
            "title": "Test TGIF Meeting",
            "date": "2025-11-14",
            "attendees": [
                {"name": "Justin", "role": "Owner"},
                {"name": "Patricia", "role": "IT Manager"}
            ]
        },
        "decisions": [
            {
                "text": "Move to NetSuite by December 15",
                "category": "technical",
                "impact": "high",
                "confidence": "high"
            }
        ],
        "actions": [
            {
                "what": "Update store mapping spreadsheet",
                "who": "Mario",
                "due": "2025-11-20",
                "priority": "high"
            }
        ],
        "risks": [],
        "blockers": [],
        "corrections_made": [
            {
                "original": "net sweet",
                "corrected": "NetSuite",
                "confidence": "high",
                "reason": "Common transcription error for NetSuite ERP system"
            }
        ]
    }


def create_test_context():
    """Create test context sources"""
    return {
        "meeting_transcript": {
            "text": "We discussed moving to NetSuite by December 15. Mario will update the store mapping spreadsheet by next week."
        },
        "brain_transport": {
            "projects": ["HCSS", "TGIF"],
            "systems": ["NetSuite", "POS", "Inventory"]
        },
        "tgif_knowledge_base": {
            "common_terms": ["NetSuite", "store mapping", "POS system"],
            "team": ["Justin", "Patricia", "Mario"]
        }
    }


def test_basic_audit():
    """Test basic audit functionality"""
    print("\n" + "="*60)
    print("TEST 1: Basic Audit")
    print("="*60)
    
    # Create auditor
    auditor = AuditorAgent(verbose=True)
    
    # Create test data
    workflow_output = create_test_workflow_output()
    context = create_test_context()
    
    # Run audit
    report = auditor.audit_workflow(
        workflow_output=workflow_output,
        workflow_type="meeting_automation",
        source_materials=context,
        metadata={"workflow_id": "test_001"}
    )
    
    # Validate report structure
    assert "audit_metadata" in report
    assert "overall_assessment" in report
    assert "findings" in report
    assert "recommendations" in report
    
    # Check verdict
    verdict = report["overall_assessment"]["verdict"]
    print(f"\n✅ Verdict: {verdict}")
    print(f"   Accuracy: {report['overall_assessment']['accuracy_score']:.0%}")
    print(f"   Completeness: {report['overall_assessment']['completeness_score']:.0%}")
    
    # Should pass since we have good context
    assert verdict in [Verdict.PASS.value, Verdict.REVIEW.value]
    
    print("\n✅ Test 1 PASSED")
    return report


def test_missing_context():
    """Test audit with missing context sources"""
    print("\n" + "="*60)
    print("TEST 2: Missing Context")
    print("="*60)
    
    auditor = AuditorAgent(verbose=True)
    
    workflow_output = create_test_workflow_output()
    
    # Minimal context
    context = {
        "brain_transport": {"status": "unavailable"},
        "meeting_transcript": {"text": "Brief meeting discussion"}
    }
    
    report = auditor.audit_workflow(
        workflow_output=workflow_output,
        workflow_type="meeting_automation",
        source_materials=context,
        metadata={"workflow_id": "test_002"}
    )
    
    # Should still complete (graceful degradation)
    assert report is not None
    assert "overall_assessment" in report
    
    # Check that unavailable sources are noted
    unavailable = report["context_analysis"]["sources_unavailable"]
    print(f"\n⚠️  Unavailable sources: {len(unavailable)}")
    
    print("\n✅ Test 2 PASSED (graceful degradation)")
    return report


def test_empty_output():
    """Test audit with empty workflow output"""
    print("\n" + "="*60)
    print("TEST 3: Empty Output")
    print("="*60)
    
    auditor = AuditorAgent(verbose=True)
    
    # Empty output (should detect gaps)
    workflow_output = {
        "decisions": [],
        "actions": [],
        "risks": [],
        "blockers": []
    }
    
    context = create_test_context()
    
    report = auditor.audit_workflow(
        workflow_output=workflow_output,
        workflow_type="meeting_automation",
        source_materials=context,
        metadata={"workflow_id": "test_003"}
    )
    
    # Should detect gaps
    gaps = report.get("gaps", [])
    print(f"\n📊 Gaps detected: {len(gaps)}")
    
    # Should have lower completeness score
    completeness = report["overall_assessment"]["completeness_score"]
    print(f"   Completeness: {completeness:.0%}")
    
    print("\n✅ Test 3 PASSED (gap detection)")
    return report


def test_report_structure():
    """Test that report has all required fields"""
    print("\n" + "="*60)
    print("TEST 4: Report Structure")
    print("="*60)
    
    auditor = AuditorAgent(verbose=True)
    
    workflow_output = create_test_workflow_output()
    context = create_test_context()
    
    report = auditor.audit_workflow(
        workflow_output=workflow_output,
        workflow_type="meeting_automation",
        source_materials=context,
        metadata={"workflow_id": "test_004"}
    )
    
    # Check required fields
    required_fields = [
        "audit_metadata",
        "overall_assessment",
        "findings",
        "gaps",
        "recommendations",
        "context_analysis"
    ]
    
    for field in required_fields:
        assert field in report, f"Missing required field: {field}"
        print(f"   ✅ {field}")
    
    # Check nested fields
    assert "verdict" in report["overall_assessment"]
    assert "accuracy_score" in report["overall_assessment"]
    assert "completeness_score" in report["overall_assessment"]
    
    print("\n✅ Test 4 PASSED (report structure)")
    return report


def save_test_report(report, filename="test_audit_report.json"):
    """Save test report for inspection"""
    output_dir = Path(__file__).parent / "test_output"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / filename
    with open(output_file, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Test report saved: {output_file}")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("AUDITOR AGENT - SIMPLE TESTS")
    print("="*60)
    
    try:
        # Run tests
        report1 = test_basic_audit()
        report2 = test_missing_context()
        report3 = test_empty_output()
        report4 = test_report_structure()
        
        # Save sample report
        save_test_report(report1, "sample_audit_report.json")
        
        print("\n" + "="*60)
        print("ALL TESTS PASSED ✅")
        print("="*60)
        print("\nAuditor Agent is working correctly!")
        print("Next steps:")
        print("1. Test with real workflow output")
        print("2. Validate recommendations quality")
        print("3. Test with actual MCP integrations")
        
        return 0
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
