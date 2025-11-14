# Survey Data

This folder contains structured survey responses from various sources.

## 📊 Survey Types

### **Notion Screener**
- Pre-beta screening survey
- User qualification data
- Interest level indicators
- Use case information

### **Product Feedback**
- Feature satisfaction ratings
- Pain point identification
- Feature requests
- UX feedback

### **NPS/CSAT**
- Net Promoter Score
- Customer Satisfaction Score
- Likelihood to recommend
- Overall satisfaction

## 📁 File Format

### Naming Convention:
```
YYYYMMDD_SurveyType_Source.{json|csv}
```

Examples:
- `20251110_NotionScreener_Responses.json`
- `20251110_ProductFeedback_Beta.csv`
- `20251110_NPS_Q4.json`

### JSON Structure:
```json
{
  "survey_id": "notion_screener_001",
  "survey_type": "screener",
  "date": "2025-11-10",
  "source": "notion",
  "responses": [
    {
      "respondent_id": "R001",
      "timestamp": "2025-11-10T10:30:00Z",
      "answers": {
        "question_1": "answer",
        "question_2": "answer"
      }
    }
  ],
  "metadata": {
    "total_responses": 100,
    "completion_rate": 0.85
  }
}
```

## 🔄 Processing

Survey data is automatically processed by:
```bash
python3 focuses/joju/user_engagement/process_surveys.py
```

This extracts:
- Key insights
- Common themes
- Quantitative metrics
- Qualitative feedback

## 📈 Analytics

View survey analytics:
```bash
python3 focuses/joju/user_engagement/survey_analytics.py
```

Generates:
- Response rate trends
- Sentiment analysis
- Feature priority rankings
- User segment analysis
