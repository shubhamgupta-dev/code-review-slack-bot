# 📱 Mobile Access Troubleshooting Guide

## Current Status
✅ **Server is running** on port 8000
✅ **Local IP detected**: 192.168.29.169
✅ **Server accessible** from computer

---

## 🔍 Common Issues & Solutions

### Issue 1: Mobile on Different WiFi Network ⚠️

**Problem:** Mobile device is on cellular data or different WiFi

**Solution:**
1. **On your mobile:**
   - Go to Settings → WiFi
   - Connect to the **same WiFi** as your computer
   - Turn OFF cellular data temporarily

2. **Verify WiFi:**
   - Computer WiFi name: Check your Mac's WiFi menu
   - Mobile WiFi name: Must match exactly

---

### Issue 2: macOS Firewall Blocking Connections 🔥

**Problem:** macOS Firewall blocks incoming connections

**Solution - Option A (Temporary - Recommended for testing):**
```bash
# Check firewall status
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

# If enabled, temporarily disable (requires admin password):
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off
```

**Solution - Option B (Permanent - Add Exception):**
1. Open **System Preferences** (System Settings on macOS 13+)
2. Go to **Security & Privacy** → **Firewall**
3. Click lock icon and enter password
4. Click **Firewall Options**
5. Click **+** button
6. Add **Python** (find it in `/usr/local/bin/python3` or `/opt/homebrew/bin/python3`)
7. Set to **Allow incoming connections**
8. Click **OK**

---

### Issue 3: VPN or Proxy Enabled 🔒

**Problem:** VPN or proxy routing traffic differently

**Solution:**
1. **Disable VPN** temporarily on both devices
2. **Disable proxy** settings
3. Try accessing again

---

### Issue 4: Router AP Isolation Enabled 🚫

**Problem:** Router has "AP Isolation" or "Client Isolation" enabled

**Solution:**
1. Open router admin page (usually 192.168.1.1 or 192.168.0.1)
2. Look for **Wireless Settings** → **AP Isolation** or **Client Isolation**
3. **Disable** this feature
4. Save and restart router

---

### Issue 5: Wrong IP Address 📍

**Problem:** Using incorrect IP address

**Current IPs to try:**

1. **Primary IP**: `http://192.168.29.169:8000/dashboard/?token=demo-token-123`

2. **Get latest IP:**
```bash
# On your Mac terminal:
ipconfig getifaddr en0
```

3. **Build URL:**
```
http://[YOUR_IP]:8000/dashboard/?token=demo-token-123
```

---

## ✅ Step-by-Step Verification

Run these commands to verify setup:

```bash
# 1. Check server is running
lsof -i :8000

# 2. Get your IP address
ipconfig getifaddr en0

# 3. Test local access
curl -I http://192.168.29.169:8000/dashboard/?token=demo-token-123

# 4. Check firewall status
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
```

---

## 🎯 Quick Fix Commands

### Enable Access (Run in Terminal):

```bash
# Stop firewall temporarily (requires password)
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off

# Show QR code with latest IP
python3 show_qr_code.py

# Re-enable firewall later
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
```

---

## 📱 Mobile Testing Checklist

On your mobile device:

- [ ] Connected to WiFi (not cellular data)
- [ ] WiFi name matches computer's WiFi
- [ ] VPN is disabled
- [ ] Browser allows HTTP (not just HTTPS)
- [ ] Tried clearing browser cache
- [ ] Tried different browser (Chrome, Safari)

---

## 🔧 Alternative Solutions

### Option 1: Use ngrok (Works from anywhere)

```bash
# Install ngrok from https://ngrok.com
# Get auth token and configure

# Start ngrok tunnel
ngrok http 8000

# Use the https:// URL provided
# Example: https://abc123.ngrok.io/dashboard/?token=demo-token-123
```

### Option 2: Use Tailscale (Secure VPN)

```bash
# Install Tailscale from https://tailscale.com
# On both devices

# Access using Tailscale IP
# Find IP: tailscale ip
```

### Option 3: Use localhost.run (Quick & Easy)

```bash
# No installation needed
ssh -R 80:localhost:8000 localhost.run

# Use the URL provided
```

---

## 🌐 Test URLs

Try these URLs **IN ORDER** on your mobile:

1. **Primary:** `http://192.168.29.169:8000/dashboard/?token=demo-token-123`

2. **Alternative ports (if port 8000 is blocked):**
   - Change port in code and try `http://192.168.29.169:8080/dashboard/?token=demo-token-123`

3. **Using hostname (if supported):**
   ```bash
   # Get hostname
   hostname
   # Use: http://YOUR_HOSTNAME.local:8000/dashboard/?token=demo-token-123
   ```

---

## 🔍 Diagnostic Commands

Run these to diagnose issues:

```bash
# 1. Check all network interfaces
ifconfig | grep "inet "

# 2. Check WiFi network name
networksetup -getairportnetwork en0

# 3. Test port is open
nc -zv 192.168.29.169 8000

# 4. Check server logs
# (Check the terminal where server is running)

# 5. Ping your computer from mobile terminal app
# ping 192.168.29.169
```

---

## 💡 Most Common Fix

**90% of the time, it's one of these:**

1. **Different WiFi networks** → Connect to same WiFi
2. **Firewall blocking** → Temporarily disable firewall
3. **VPN enabled** → Disable VPN
4. **Cellular data active** → Turn off mobile data

---

## 🆘 Need More Help?

If still not working, provide:
1. Mobile device type (iPhone/Android)
2. Error message (if any)
3. Results of: `ipconfig getifaddr en0`
4. Screenshot of error on mobile

---

## ✅ Success Indicators

When it works, you should see:
- Dashboard loads on mobile browser
- Purple Slack-style sidebar
- PR cards displayed
- No connection errors
- Smooth, responsive layout

---

**Last Updated:** 2025-12-12
**Your IP:** 192.168.29.169
**Port:** 8000
**Access URL:** http://192.168.29.169:8000/dashboard/?token=demo-token-123
