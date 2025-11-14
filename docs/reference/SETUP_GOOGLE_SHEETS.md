# Google Sheets API Setup for Toast Schedule Manager

## Quick Setup (5 minutes)

### 1. Install Required Packages
```bash
pip install gspread oauth2client
```

### 2. Set Up Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable **Google Sheets API**:
   - Search for "Google Sheets API"
   - Click "Enable"

### 3. Create Service Account

1. Go to **IAM & Admin** → **Service Accounts**
2. Click **Create Service Account**
3. Name it: `toast-schedule-manager`
4. Click **Create and Continue**
5. Skip role assignment (click Continue)
6. Click **Done**

### 4. Create Credentials

1. Click on the service account you just created
2. Go to **Keys** tab
3. Click **Add Key** → **Create New Key**
4. Choose **JSON**
5. Download the JSON file

### 5. Save Credentials

```bash
mkdir -p ~/.config/gspread
mv ~/Downloads/your-project-*.json ~/.config/gspread/service_account.json
```

### 6. Share Sheet with Service Account

1. Open the downloaded JSON file
2. Copy the `client_email` (looks like: `toast-schedule-manager@project.iam.gserviceaccount.com`)
3. In Google Sheets, click **Share**
4. Paste the email
5. Give **Editor** access
6. Uncheck "Notify people"
7. Click **Share**

## Usage

### Initialize and Create Sheet
```python
from toast_sheet_manager import ToastScheduleManager

manager = ToastScheduleManager()
manager.connect("Toast Installation Schedule")
```

### Update Store Status
```python
# Update equipment status
manager.update_store_status(
    "1191",
    network_status="Shipped - Tracking #12345",
    notes="Equipment shipped via FedEx, arriving 11/17"
)

# Update installation progress
manager.update_store_status(
    "1887",
    toast_status="✓ Installed",
    onsite_status="✓ Complete"
)
```

### Add New Store
```python
manager.add_store(
    date="11/20/2025",
    day="Thursday",
    store_id="2001",
    location="Austin, TX",
    toast_status="Ordered",
    network_equipment="PRNSC24P + 3 APs",
    notes="Rush order"
)
```

### Check What Needs Attention
```python
needs_attention = manager.get_stores_needing_attention()
for store in needs_attention:
    print(f"{store['Store ID']} - {store['Location']}")
```

### Mark Installation Complete
```python
manager.mark_complete("1191")
```

## Quick Commands

### Run the example
```bash
python toast_sheet_manager.py
```

### Update from command line (create this helper)
```python
# quick_update.py
from toast_sheet_manager import ToastScheduleManager
import sys

manager = ToastScheduleManager()
manager.connect("Toast Installation Schedule")

store_id = sys.argv[1]
field = sys.argv[2]
value = sys.argv[3]

manager.update_store_status(store_id, **{field: value})
```

Then use:
```bash
python quick_update.py 1191 network_status "Shipped - Arriving 11/17"
```

## Troubleshooting

**Error: "Credentials not found"**
- Make sure JSON file is at `~/.config/gspread/service_account.json`

**Error: "Spreadsheet not found"**
- Make sure you shared the sheet with the service account email

**Error: "Permission denied"**
- Service account needs Editor access to the sheet

**Error: "API not enabled"**
- Enable Google Sheets API in Cloud Console
