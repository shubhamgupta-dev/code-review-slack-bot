# 🌐 Public Access Setup Guide

Access your ReviewFlow dashboard from ANYWHERE on the internet using a public URL!

---

## Option 1: ngrok (Recommended - Easy & Secure)

### Step 1: Get ngrok Auth Token

1. Go to: https://dashboard.ngrok.com/get-started/setup
2. Sign up (free account) or log in
3. Copy your authtoken (looks like: `2abC1dEf2GhI3jKl4MnO5pQr6StU7vWx8YzA9bCd0EfG1`)

### Step 2: Configure & Start

**Quick Setup:**
```bash
./SETUP_PUBLIC_ACCESS.sh
```
(Script will ask for your authtoken)

**Or Manual Setup:**
```bash
# Configure ngrok with your token
ngrok config add-authtoken YOUR_TOKEN_HERE

# Start ngrok tunnel
ngrok http 8000
```

### Step 3: Get Your Public URL

When ngrok starts, you'll see something like:
```
Forwarding    https://abc123xyz.ngrok.io -> http://localhost:8000
```

**Your Public Dashboard URL:**
```
https://abc123xyz.ngrok.io/dashboard/?token=demo-token-123
```

✅ **Works from ANYWHERE** - Share with anyone!
✅ **Secure HTTPS** - Encrypted connection
✅ **Free tier** - No payment needed for basic use

---

## Option 2: localhost.run (No Signup Required!)

### Instant Public URL

```bash
ssh -R 80:localhost:8000 localhost.run
```

You'll get a URL like: `https://xyz123.lhr.life`

**Your Dashboard URL:**
```
https://xyz123.lhr.life/dashboard/?token=demo-token-123
```

✅ **No signup** required
✅ **Instant** setup
⚠️ URL changes each time

---

## Option 3: Tailscale (Private Network)

Access from anywhere on YOUR devices only (most secure!)

### Setup:

1. **Already running on Mac** (IP: 100.96.3.158)
2. **Install Tailscale on mobile:**
   - iOS: https://apps.apple.com/app/tailscale/id1470499037
   - Android: https://play.google.com/store/apps/details?id=com.tailscale.ipn
3. **Log in with same account**

**Your Tailscale URL:**
```
http://100.96.3.158:8000/dashboard/?token=demo-token-123
```

✅ **Most secure** - Only your devices
✅ **Works everywhere** - No firewall issues
✅ **Always same IP** - Doesn't change

---

## Comparison

| Method | Signup? | Free? | Security | Ease |
|--------|---------|-------|----------|------|
| **ngrok** | Yes | Yes (with limits) | 🔒🔒🔒 HTTPS | ⭐⭐⭐⭐⭐ |
| **localhost.run** | No | Yes | 🔒🔒🔒 HTTPS | ⭐⭐⭐⭐⭐ |
| **Tailscale** | Yes | Yes | 🔒🔒🔒🔒🔒 Private | ⭐⭐⭐⭐ |

---

## 🎯 Recommended Solution

**For quick testing:** Use **localhost.run** (no signup!)
```bash
ssh -R 80:localhost:8000 localhost.run
```

**For sharing with team:** Use **ngrok** (professional, reliable)
```bash
./SETUP_PUBLIC_ACCESS.sh
```

**For personal use:** Use **Tailscale** (most secure)
```
http://100.96.3.158:8000/dashboard/?token=demo-token-123
```

---

## 📱 Mobile Access with Public URL

Once you have a public URL:

1. **No WiFi requirements** - Works on cellular data
2. **No firewall issues** - Bypasses all network restrictions
3. **Share with team** - Anyone can access (if you share the token)
4. **Generate QR code** - Click "📱 QR Code" button in dashboard

---

## 🔧 Troubleshooting

### ngrok: "authtoken not found"
```bash
# Configure with your token from ngrok.com
ngrok config add-authtoken YOUR_TOKEN
```

### localhost.run: "Connection refused"
- Make sure server is running: `lsof -i :8000`
- Try again: `ssh -R 80:localhost:8000 localhost.run`

### Tailscale: "Can't connect"
- Install Tailscale app on mobile
- Log in with SAME account as Mac
- Check Tailscale is running on both devices

---

## ⚠️ Security Notes

### ngrok & localhost.run:
- URL is **publicly accessible** by anyone who has it
- Keep your `?token=demo-token-123` secret
- For production, use proper authentication

### Tailscale:
- Only devices on YOUR Tailscale network can access
- Most secure option for personal/team use
- No risk of public exposure

---

## 🚀 Quick Start Commands

### Test localhost.run (No Signup):
```bash
ssh -R 80:localhost:8000 localhost.run
```

### Setup ngrok (One-time):
```bash
./SETUP_PUBLIC_ACCESS.sh
```

### Start ngrok:
```bash
ngrok http 8000
```

### Use Tailscale:
```bash
# Already working! Just use:
http://100.96.3.158:8000/dashboard/?token=demo-token-123
```

---

## 📊 Server Status

Check if server is running:
```bash
./CHECK_STATUS.sh
```

Or:
```bash
lsof -i :8000
```

---

## 🎉 Success Indicators

When public access works:
- ✅ ngrok/localhost.run shows "online" status
- ✅ Dashboard loads on mobile from anywhere
- ✅ No WiFi/firewall requirements
- ✅ Works on cellular data
- ✅ Can share URL with team

---

**Last Updated:** 2025-12-12
**Server Port:** 8000
**Local IP:** 192.168.29.169
**Tailscale IP:** 100.96.3.158
