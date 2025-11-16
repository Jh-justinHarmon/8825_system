# 8825 System Port Registry

**Purpose:** Track all ports used by 8825 services to avoid conflicts

---

## Active Ports

| Port | Service | Status | File |
|------|---------|--------|------|
| 5000 | ❌ AirTunes (macOS) | System Reserved | N/A |
| 5001 | Integration Server | 🟢 Available | integration_server.py |
| 5002 | Reserved | 🟢 Available | - |
| 5003 | Reserved | 🟢 Available | - |

---

## Port Allocation Rules

- **5000-5099:** Web servers and APIs
- **5100-5199:** Database services
- **5200-5299:** Background workers
- **5300-5399:** Testing/development

---

## Next Available Port

**5001** - Use for Integration Server

---

## Notes

- Port 5000 is reserved by macOS AirTunes
- Always check `lsof -i :PORT` before using
- Update this file when allocating new ports

**Last Updated:** 2025-11-14
