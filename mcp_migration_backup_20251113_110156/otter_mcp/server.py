"""
Otter MCP Server - Abstraction layer for Otter.ai API with Gmail fallback
"""

import os
import logging
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class OtterMCP:
    """MCP abstraction layer for Otter.ai with Gmail fallback"""
    
    def __init__(self):
        self.health_status = "initializing"
        self.failure_count = 0
        self.last_success = None
        self.current_source = None
        
        # Initialize APIs
        self._init_otter_api()
        self._init_gmail_api()
        
    def _init_otter_api(self):
        """Initialize Otter.ai unofficial API"""
        try:
            from otterai import OtterAI
            
            self.otter = OtterAI()
            self.otter.login(
                os.getenv('OTTER_EMAIL'),
                os.getenv('OTTER_PASSWORD')
            )
            
            # Test connection
            self.otter.get_user()
            
            self.health_status = "healthy"
            self.current_source = "otter_api"
            logger.info("Otter API initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Otter API: {e}")
            self.health_status = "degraded"
            self.current_source = "gmail_fallback"
    
    def _init_gmail_api(self):
        """Initialize Gmail API as fallback"""
        try:
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import Request
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build
            
            SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
                     'https://www.googleapis.com/auth/gmail.modify']
            
            creds = None
            token_path = os.getenv('GMAIL_TOKEN_PATH', 'token.json')
            creds_path = os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials.json')
            
            # Load existing token
            if os.path.exists(token_path):
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            
            # Refresh or get new token
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Save token
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
            
            self.gmail = build('gmail', 'v1', credentials=creds)
            logger.info("Gmail API initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Gmail API: {e}")
            raise
    
    def get_transcripts(self, filter_tgif=True, since=None):
        """Get transcripts with automatic fallback"""
        try:
            # Try Otter API first
            transcripts = self._get_from_otter(filter_tgif, since)
            
            self.failure_count = 0
            self.last_success = datetime.now()
            self.health_status = "healthy"
            self.current_source = "otter_api"
            
            return transcripts
            
        except Exception as e:
            logger.error(f"Otter API failed: {e}")
            self.failure_count += 1
            
            # Alert if multiple failures
            if self.failure_count >= 3:
                self._send_alert(f"Otter API failing: {self.failure_count} failures")
            
            # Fallback to Gmail
            logger.info("Switching to Gmail fallback")
            self.health_status = "degraded"
            self.current_source = "gmail_fallback"
            
            return self._get_from_gmail(filter_tgif, since)
    
    def _get_from_otter(self, filter_tgif, since):
        """Get transcripts from Otter API"""
        speeches = self.otter.get_speeches()
        
        # Filter by date if specified
        if since:
            speeches = [s for s in speeches if self._parse_date(s.created_at) >= since]
        
        # Filter for TGIF
        if filter_tgif:
            speeches = [s for s in speeches if 'TGIF' in s.title]
        
        return speeches
    
    def _get_from_gmail(self, filter_tgif, since):
        """Get transcripts from Gmail (fallback)"""
        query = 'from:no-reply@otter.ai'
        
        if filter_tgif:
            query += ' subject:TGIF'
        
        if since:
            after_date = since.strftime('%Y/%m/%d')
            query += f' after:{after_date}'
        
        # Search Gmail
        results = self.gmail.users().messages().list(
            userId='me',
            q=query,
            maxResults=50
        ).execute()
        
        messages = results.get('messages', [])
        
        # Get full message content
        transcripts = []
        for msg in messages:
            message = self.gmail.users().messages().get(
                userId='me',
                id=msg['id']
            ).execute()
            
            transcripts.append(self._parse_gmail_message(message))
        
        return transcripts
    
    def download_transcript(self, speech_id):
        """Download specific transcript"""
        try:
            # Try Otter API
            return self.otter.download_speech(speech_id, format='txt')
        except Exception as e:
            logger.error(f"Otter download failed: {e}")
            # Fallback: Get from Gmail
            return self._get_transcript_from_gmail(speech_id)
    
    def _parse_gmail_message(self, message):
        """Parse Gmail message to extract transcript"""
        # Extract headers
        headers = message['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
        
        # Extract body
        body = self._get_message_body(message['payload'])
        
        return {
            'id': message['id'],
            'title': subject,
            'created_at': date,
            'transcript': body,
            'source': 'gmail'
        }
    
    def _get_message_body(self, payload):
        """Extract message body from Gmail payload"""
        if 'body' in payload and 'data' in payload['body']:
            import base64
            return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        
        if 'parts' in payload:
            for part in payload['parts']:
                body = self._get_message_body(part)
                if body:
                    return body
        
        return ""
    
    def _send_alert(self, message):
        """Send alert notification"""
        logger.warning(f"ALERT: {message}")
        # TODO: Implement email/Slack notification
    
    def _parse_date(self, date_str):
        """Parse date string to datetime"""
        from dateutil import parser
        return parser.parse(date_str)
    
    def health_check(self):
        """Health check endpoint"""
        return {
            "status": self.health_status,
            "source": self.current_source,
            "failure_count": self.failure_count,
            "last_success": self.last_success.isoformat() if self.last_success else None
        }


# Initialize MCP server
mcp_server = OtterMCP()


# Flask endpoints
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify(mcp_server.health_check())


@app.route('/transcripts', methods=['GET'])
def get_transcripts():
    """Get transcripts endpoint"""
    filter_tgif = request.args.get('filter_tgif', 'true').lower() == 'true'
    since_str = request.args.get('since')
    
    since = None
    if since_str:
        from dateutil import parser
        since = parser.parse(since_str)
    
    try:
        transcripts = mcp_server.get_transcripts(filter_tgif, since)
        return jsonify({
            "status": "success",
            "count": len(transcripts),
            "source": mcp_server.current_source,
            "transcripts": transcripts
        })
    except Exception as e:
        logger.error(f"Error getting transcripts: {e}")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route('/transcript/<speech_id>', methods=['GET'])
def get_transcript(speech_id):
    """Get specific transcript"""
    try:
        transcript = mcp_server.download_transcript(speech_id)
        return jsonify({
            "status": "success",
            "speech_id": speech_id,
            "transcript": transcript
        })
    except Exception as e:
        logger.error(f"Error getting transcript {speech_id}: {e}")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.getenv('MCP_PORT', 8829))
    logger.info(f"Starting Otter MCP server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
