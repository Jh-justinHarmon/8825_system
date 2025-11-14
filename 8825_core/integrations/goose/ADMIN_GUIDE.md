# Goose MCP Bridge - Admin Guide

**For:** System Administrators  
**Version:** 2.0.0  
**Last Updated:** November 10, 2025

---

## 👨‍💼 Admin Responsibilities

As an admin, you're responsible for:
- Initial setup and configuration
- User onboarding
- Notion integration
- Monitoring and maintenance
- Troubleshooting issues

---

## 🔧 Initial Setup

### 1. Install Dependencies

```bash
# Python dependencies
pip install notion-client python-dotenv

# Goose
pip install goose-ai

# Or install all 8825 dependencies
pip install -r requirements.txt
```

**Note:** MCP servers auto-start on login via LaunchAgent.  
**See:** [STARTUP_AUTOMATION.md](../../../STARTUP_AUTOMATION.md) for automation details.

### 2. Run Setup Script

```bash
cd 8825_core/integrations/goose
./SETUP_GOOSE.sh
```

This creates:
- `~/.config/goose/config.yaml`
- Makes server executable
- Tests basic functionality

### 3. Configure Notion

```bash
cd focuses/joju/tasks
cp config.example.json config.json
```

Edit `config.json`:
```json
{
  "notion": {
    "api_key": "secret_YOUR_NOTION_API_KEY",
    "database_id": "YOUR_DATABASE_ID",
    "workspace": "Joju"
  }
}
```

**Get Notion credentials:**
1. Go to https://www.notion.so/my-integrations
2. Create integration: "8825 Joju Tasks"
3. Copy API key
4. Share database with integration
5. Copy database ID from URL

### 4. Test Integration

```bash
cd focuses/joju/tasks
python3 notion_sync.py test
```

Should output: `✅ Connected to Notion successfully`

### 5. Initial Sync

```bash
python3 notion_sync.py pull
```

Downloads all tasks to local cache.

---

## 👥 User Onboarding

### For Each New Team Member:

**1. Verify Access**
- Add to `CONFIG['allowed_users']` in `server.py` if needed
- Default: justin_harmon, matthew_galley, cam_watkins

**2. Install Goose**
```bash
pip install goose-ai
```

**3. Configure Goose**
User should have `~/.config/goose/config.yaml` pointing to MCP bridge.

**4. Test Access**
```bash
cd "/path/to/8825"
goose session start
> "List available tools"
```

Should show 12 tools.

**5. Provide User Guide**
Share [USER_GUIDE.md](USER_GUIDE.md) with new user.

---

## 🔐 Security & Authentication

### Current Setup

**Authentication Framework:**
- User list configured in `server.py`
- Currently permissive (for testing)
- Ready to enforce

**To Enable Strict Auth:**

Edit `server.py`:
```python
def authenticate_user(self, user_id: str) -> bool:
    """Authenticate user"""
    return user_id in CONFIG['allowed_users']

# Then in handle_request:
if not self.authenticate_user(request.get('user')):
    return {'error': 'Unauthorized'}
```

### Credentials Management

**Notion API Key:**
- Stored in: `focuses/joju/tasks/config.json`
- Protected by: `.gitignore`
- Access: Only via task layer

**Best Practices:**
- Rotate API keys quarterly
- Use separate keys for dev/prod
- Monitor API usage
- Audit access logs

---

## 📊 Monitoring

### Log Files

**Location:** `8825_core/integrations/goose/mcp-bridge/logs/`

**Format:** `mcp_bridge_YYYYMMDD.log`

**What's Logged:**
- All tool calls
- Errors and retries
- Performance metrics
- User actions

**View Real-Time:**
```bash
tail -f mcp-bridge/logs/mcp_bridge_*.log
```

**Search Logs:**
```bash
grep "ERROR" mcp-bridge/logs/*.log
grep "task_id" mcp-bridge/logs/*.log
grep "justin_harmon" mcp-bridge/logs/*.log
```

### Performance Metrics

**Check Response Times:**
```bash
grep "Calling tool" mcp-bridge/logs/*.log | wc -l  # Total calls
grep "Failed" mcp-bridge/logs/*.log | wc -l        # Failures
```

**Monitor Notion API:**
- Check rate limits
- Monitor sync times
- Track error rates

### Health Checks

**Daily:**
```bash
# Test MCP server
echo '{"method":"tools/list"}' | python3 mcp-bridge/server.py

# Test Notion connection
cd focuses/joju/tasks
python3 notion_sync.py test

# Check logs for errors
grep "ERROR" mcp-bridge/logs/mcp_bridge_$(date +%Y%m%d).log
```

**Weekly:**
```bash
# Sync tasks
cd focuses/joju/tasks
python3 notion_sync.py pull

# Archive old logs
mv mcp-bridge/logs/mcp_bridge_$(date -d '30 days ago' +%Y%m%d).log mcp-bridge/logs/archive/
```

---

## 🔄 Maintenance

### Daily Tasks
- [ ] Check logs for errors
- [ ] Monitor system status
- [ ] Respond to user issues

### Weekly Tasks
- [ ] Sync tasks with Notion
- [ ] Review performance metrics
- [ ] Archive old logs
- [ ] Update documentation if needed

### Monthly Tasks
- [ ] Review user access list
- [ ] Check API usage/limits
- [ ] Update dependencies
- [ ] Backup configurations

### Quarterly Tasks
- [ ] Rotate API keys
- [ ] Security audit
- [ ] Performance review
- [ ] Team training refresh

---

## 🆘 Troubleshooting

### Common Issues

#### "Task management not available"

**### 3. Configure Notion (For Task Management)**

**Location:** `focuses/joju/tasks/`

⚠️ **CRITICAL:** Notion requires specific SDK version!

```bash
# Install correct version FIRST
pip3 install notion-client==1.0.0

# Configure credentials
cd focuses/joju/tasks
cp config.example.json config.json
# Edit config.json with:
# - Notion API key (from v2.0: config/8825_config.json)
# - Database ID (must have UUID dashes)
```

**Test connection:**
```bash
python3 notion_sync.py test
```

**If errors:** See `focuses/joju/tasks/NOTION_SETUP_COMPLETE.md`

**Common Issues:**
- "DatabasesEndpoint has no attribute 'query'" → Wrong SDK version
- "Invalid request URL" → Database ID needs dashes
- Empty task data → Property name mismatch

#### "No cached tasks"

**Cause:** Haven't synced yet

**Fix:**
```bash
cd focuses/joju/tasks
python3 notion_sync.py pull
```

#### "Connection timeout"

**Cause:** Network or Notion API issues

**Fix:**
1. Check internet connection
2. Verify Notion status: https://status.notion.so
3. Check API rate limits
4. Retry with: `python3 notion_sync.py pull`

#### "Permission denied"

**Cause:** File permissions

**Fix:**
```bash
chmod +x mcp-bridge/server.py
chmod +x SETUP_GOOSE.sh
```

#### "User can't see tools"

**Cause:** Goose config issue

**Fix:**
```bash
# Check config
cat ~/.config/goose/config.yaml

# Recreate config
cd 8825_core/integrations/goose
./SETUP_GOOSE.sh

# Restart Goose
killall goose
goose session start
```

---

## 🔍 Debugging

### Enable Debug Logging

Edit `server.py`:
```python
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO
    ...
)
```

### Test Components Individually

**Test MCP Server:**
```bash
echo '{"method":"tools/list","params":{}}' | python3 mcp-bridge/server.py
```

**Test Task Manager:**
```bash
cd focuses/joju/tasks
python3 task_manager.py list
```

**Test Notion Sync:**
```bash
cd focuses/joju/tasks
python3 notion_sync.py pull
```

**Test User Engagement:**
```bash
cat focuses/joju/user_engagement/all_user_testing_data.json | python3 -m json.tool
```

### Check Dependencies

```bash
pip list | grep notion
pip list | grep goose
python3 --version  # Should be 3.7+
```

---

## 📈 Scaling

### Adding More Users

**Update allowed users:**
```python
# In server.py
CONFIG = {
    'allowed_users': [
        'justin_harmon',
        'matthew_galley',
        'cam_watkins',
        'new_user',  # Add here
    ],
}
```

### Adding More Tools

**Create new tool method:**
```python
def my_new_tool(self, param: str) -> Dict[str, Any]:
    """New tool description"""
    logger.info(f"Running new tool: {param}")
    
    try:
        # Tool logic here
        result = do_something(param)
        
        return {
            'status': 'success',
            'result': result
        }
    except Exception as e:
        logger.error(f"Tool failed: {e}")
        return {
            'status': 'error',
            'error': str(e)
        }
```

**Register in list_tools:**
```python
{
    'name': 'my_new_tool',
    'description': 'What this tool does',
    'inputSchema': {
        'type': 'object',
        'properties': {
            'param': {'type': 'string'}
        },
        'required': ['param']
    }
}
```

**Add to call_tool:**
```python
elif tool_name == 'my_new_tool':
    result = self.my_new_tool(args['param'])
```

### Performance Optimization

**Cache frequently accessed data:**
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_data(key: str):
    # Expensive operation
    return data
```

**Async operations (future):**
```python
import asyncio

async def async_tool():
    # Async logic
    pass
```

---

## 🔒 Security Best Practices

### Do:
- ✅ Rotate API keys regularly
- ✅ Monitor access logs
- ✅ Use separate dev/prod keys
- ✅ Restrict user access
- ✅ Keep dependencies updated

### Don't:
- ❌ Commit API keys to git
- ❌ Share credentials
- ❌ Disable authentication
- ❌ Ignore security warnings
- ❌ Use production keys in dev

---

## 📚 Admin Resources

### Documentation
- [PRODUCTION_READY.md](PRODUCTION_READY.md) - Technical details
- [USER_GUIDE.md](USER_GUIDE.md) - For end users
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [INDEX.md](INDEX.md) - All docs

### External Resources
- [Notion API Docs](https://developers.notion.com/)
- [Goose Documentation](https://github.com/square/goose)
- [MCP Protocol](https://modelcontextprotocol.io/)

### Support Channels
- Team Slack: #8825-support
- Logs: `mcp-bridge/logs/`
- Issues: Document in team wiki

---

## 📞 Escalation

### Level 1: User Issues
- Check user guide
- Verify configuration
- Test basic functionality

### Level 2: System Issues
- Check logs
- Test components
- Verify integrations

### Level 3: Critical Issues
- Review architecture
- Check external services
- Contact development team

---

## ✅ Admin Checklist

### New Installation
- [ ] Run SETUP_GOOSE.sh
- [ ] Configure Notion
- [ ] Test connection
- [ ] Initial sync
- [ ] Onboard first user
- [ ] Verify logging
- [ ] Document setup

### New User
- [ ] Add to allowed users
- [ ] Install Goose
- [ ] Configure Goose
- [ ] Test access
- [ ] Provide user guide
- [ ] Schedule training

### Monthly Review
- [ ] Check logs for patterns
- [ ] Review user access
- [ ] Update documentation
- [ ] Check API limits
- [ ] Backup configs
- [ ] Security audit

---

**Version:** 2.0.0  
**Last Updated:** November 10, 2025  
**For Questions:** Contact system admin team
