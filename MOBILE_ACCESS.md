# 📱 Mobile Access Guide - ANYWHERE ACCESS

## 🎯 The Problem Solved

You want to access your ReviewFlow dashboard from:
- ✅ Same WiFi as your laptop
- ✅ Different WiFi networks
- ✅ Mobile data (4G/5G)
- ✅ From anywhere in the world

## 🚀 The Solution

### Method 1: Dynamic URL Page (RECOMMENDED)

**On your laptop, when connected to same WiFi as mobile:**

1. **Get your laptop's local IP:**
   ```bash
   # On Mac/Linux
   ipconfig getifaddr en0
   
   # Result example: 192.168.1.100
   ```

2. **On your mobile browser, visit:**
   ```
   http://YOUR_LAPTOP_IP:8000/dashboard/
   ```
   
   Example: `http://192.168.1.100:8000/dashboard/`

3. **Bookmark this page on mobile!** 📌
   - It shows the current active public tunnel URL
   - Auto-refreshes every 10 seconds
   - Always shows the latest URL even after tunnel restarts
   - Click "Open Dashboard" to access from anywhere

### Method 2: Direct Public URL (When on different WiFi)

**Current public URL:**
```
https://5b70656ec5cabd.lhr.life/dashboard/login
```

⚠️ **Important:** This URL changes when the tunnel restarts!

**To get the latest URL:**

1. **From terminal on laptop:**
   ```bash
   ./show_current_url.sh
   ```

2. **Check API from mobile (if on same WiFi):**
   ```
   http://YOUR_LAPTOP_IP:8000/dashboard/api/current-url
   ```

3. **Check text file:**
   ```bash
   cat CURRENT_URL.txt
   ```

## 🔑 Login Credentials

```
Username: shubham-dev
Password: yourlaptop
```

## 🛡️ Tunnel Protection Active

Your setup includes:
- ✅ Persistent tunnel with auto-restart
- ✅ Keep-alive monitor (checks every 60s)
- ✅ Maximum downtime: 60 seconds
- ✅ Automatic URL logging

## 📊 Monitoring

**Check tunnel status:**
```bash
# Get current URL
./show_current_url.sh

# Check tunnel logs
tail -f localhostrun.log

# Check keep-alive monitor
tail -f tunnel_keepalive.log

# Test tunnel health
curl https://5b70656ec5cabd.lhr.life/health
```

## 🎯 Best Practice Workflow

**For mobile access:**

1. **First time setup (on same WiFi):**
   - Get laptop IP: `ipconfig getifaddr en0`
   - Visit `http://LAPTOP_IP:8000/dashboard/` on mobile
   - Bookmark this page
   - Click "Open Dashboard"

2. **Daily use (from anywhere):**
   - Open bookmarked page
   - See current public URL
   - Click "Open Dashboard"
   - Login and use

3. **If tunnel URL changed:**
   - The bookmarked page automatically shows new URL
   - No manual steps needed!

## ⚙️ Services Running

Make sure these are active:
```bash
# Check services
ps aux | grep -E "(uvicorn|ssh.*localhost.run|tunnel_keepalive)"

# Restart if needed
./start.sh
```

## 🔧 Troubleshooting

**"No tunnel here" on mobile:**
1. Check if laptop is online and services running
2. Visit bookmarked page to get latest URL
3. Tunnel may have restarted - wait 60 seconds
4. Check tunnel status: `./show_current_url.sh`

**Can't access from same WiFi:**
1. Verify laptop IP: `ipconfig getifaddr en0`
2. Ensure mobile and laptop on SAME WiFi
3. Try: `http://LAPTOP_IP:8000/dashboard/`

**Can't access from different WiFi:**
1. Get latest public URL from bookmarked page
2. Or run `./show_current_url.sh` on laptop
3. Public URL changes when tunnel restarts

## 📱 QR Code Access

**Generate QR code for current URL:**
```bash
./show_current_url.sh
```

Scan the QR code with your mobile camera to quickly access the dashboard!

---

**Last Updated:** $(date)
**Current Tunnel:** https://5b70656ec5cabd.lhr.life
