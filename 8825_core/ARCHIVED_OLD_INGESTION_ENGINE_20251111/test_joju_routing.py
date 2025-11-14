#!/usr/bin/env python3
"""
Test that Joju content routes correctly
"""

from classifier import InboxClassifier

def test_joju_routing():
    """Test that Joju-related content routes to joju focus"""
    classifier = InboxClassifier()
    
    test_cases = [
        {
            "name": "Joju User Testing",
            "filename": "Joju_User_Testing_Summary_20251110.docx",
            "data": {
                "content_type": "note",
                "content": {
                    "title": "Joju Intake Design Sprint User Testing"
                },
                "metadata": {}
            },
            "expected_focus": "joju"
        },
        {
            "name": "HCSS Meeting",
            "filename": "TGIF_Weekly_Meeting.json",
            "data": {
                "content_type": "note",
                "content": {
                    "title": "TGIF Store Rollout Discussion"
                },
                "metadata": {}
            },
            "expected_focus": "hcss"
        },
        {
            "name": "Generic Note",
            "filename": "random_note.json",
            "data": {
                "content_type": "note",
                "content": {
                    "title": "Some random thoughts"
                },
                "metadata": {}
            },
            "expected_focus": "jh"
        }
    ]
    
    print(f"\n{'='*80}")
    print("Testing Joju Routing")
    print(f"{'='*80}\n")
    
    passed = 0
    failed = 0
    
    for test in test_cases:
        item = classifier.classify(test["data"], test["filename"])
        
        if item.target_focus == test["expected_focus"]:
            print(f"✅ {test['name']}: Routed to '{item.target_focus}' (correct)")
            passed += 1
        else:
            print(f"❌ {test['name']}: Routed to '{item.target_focus}' (expected '{test['expected_focus']}')")
            failed += 1
    
    print(f"\n{'='*80}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*80}\n")
    
    return failed == 0

if __name__ == "__main__":
    success = test_joju_routing()
    exit(0 if success else 1)
