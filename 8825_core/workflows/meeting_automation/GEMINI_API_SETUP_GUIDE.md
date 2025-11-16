# Gemini API Setup Guide

**Visual walkthrough for setting up Google Gemini API for 8825**

---

## Step-by-Step Instructions

### 1. Open Google AI Studio

Go to: https://aistudio.google.com/app/apikey

### 2. Click "Create API Key"

You'll see a dialog like this:

![Google AI Studio - Create API Key Dialog](google_ai_studio_project_selection.png)

### 3. Fill in the Dialog

**Name your key:**
- Enter: `8825`
- (Or any name you prefer - this is just for your reference)

**Choose an imported project:**
- Select: **"Default Gemini Project"**
- This is the recommended option for most users

**Options you'll see:**
- ❌ **Import project** - Only if you have existing Google Cloud projects
- ❌ **Create project** - Creates a new Google Cloud project (advanced)
- ✅ **Default Gemini Project** - **SELECT THIS ONE** (easiest option)

### 4. Create the Key

Click the button: **"Create API key in new project"**

### 5. Copy Your Key

- Google will generate a key that starts with `AIzaSy...`
- Copy this key immediately
- Store it securely (you won't be able to see it again)

---

## What to Do Next

### Option A: Use the HTML Setup Tool

1. Open `gemini_integration_setup.html` in your browser
2. Paste your API key in the input field
3. Click "Test Connection" to verify it works
4. Click "Save & Activate" to download the `.env` file
5. Place the `.env` file in `8825_core/` directory

### Option B: Manual Setup

Create a file called `.env` in `8825_core/` with this content:

```bash
# Google Gemini API Configuration
GOOGLE_GEMINI_API_KEY=AIzaSy...your-key-here...
```

---

## Troubleshooting

### "I don't see Default Gemini Project"

**Solution:** Click "Create project" instead. This will create a new Google Cloud project for you.

### "My key doesn't work"

**Check:**
1. Key starts with `AIzaSy`
2. No extra spaces before/after the key
3. You copied the entire key
4. Your Google account has API access enabled

### "Rate limit exceeded"

**Free tier limits:**
- 15 requests per minute
- 1,500 requests per day

**Solution:** Wait a minute and try again, or upgrade to paid tier.

---

## Security Best Practices

✅ **DO:**
- Store your key in `.env` file
- Add `.env` to `.gitignore`
- Keep your key private
- Use environment variables

❌ **DON'T:**
- Commit keys to Git
- Share keys publicly
- Hardcode keys in source files
- Use the same key across multiple projects

---

## Free Tier Details

**What you get for free:**
- 15 requests per minute
- 1,500 requests per day
- Access to Gemini 1.5 Flash
- No credit card required

**Perfect for:**
- Testing and development
- Small-scale automation
- Personal projects
- Learning and experimentation

---

## Next Steps

After setting up your API key:

1. ✅ Test the connection using the HTML tool
2. ✅ Save the `.env` file to `8825_core/`
3. ✅ Restart any running 8825 services
4. ✅ Try parsing a resume or meeting transcript

---

## Support

**Google AI Studio Documentation:**
https://ai.google.dev/gemini-api/docs

**8825 Documentation:**
See `IMPROVEMENTS_IMPLEMENTATION.md` for integration details

**Questions?**
Check the troubleshooting section above or consult Google's API docs.

---

**Last Updated:** 2025-11-14  
**Version:** 1.0
