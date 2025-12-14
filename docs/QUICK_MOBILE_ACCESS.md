# 📱 Quick Mobile Access Guide

## 🚀 3 Ways to Access from Mobile

### **Method 1: Local WiFi** (5 minutes setup)

**Your URL:**
```
http://192.168.29.169:8000/dashboard/?token=demo-token-123
```

**Steps:**
1. Disable firewall on computer:
   ```bash
   sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off
   ```
2. Connect mobile to SAME WiFi as computer
3. Turn off cellular data on mobile
4. Open URL in mobile browser

**Re-enable firewall after:**
```bash
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
```

---

### **Method 2: Tailscale** (Best - works anywhere!)

**Your Tailscale URL:**
```
http://100.96.3.158:8000/dashboard/?token=demo-token-123
```

**Steps:**
1. Install Tailscale app on mobile
2. Log in with same account as computer
3. Open URL in mobile browser
4. Works from ANYWHERE - no WiFi needed!

---

### **Method 3: QR Code** (Easiest!)

**Generate QR Code:**
```bash
./SHOW_QR.sh
```

Or click **📱 QR Code** button in dashboard!

---

## 🔧 Troubleshooting

**Not working?** Run diagnostic:
```bash
./diagnose_mobile_access.sh
```

**Need help?** Read:
- `MOBILE_ACCESS_SOLUTION.md` - Complete solutions
- `MOBILE_TROUBLESHOOTING.md` - Detailed troubleshooting

---

## ✅ Quick Checklist

- [ ] Server running? (`lsof -i :8000`)
- [ ] Firewall off? (`sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate`)
- [ ] Mobile on WiFi? (Not cellular data)
- [ ] Same WiFi network on both devices?
- [ ] VPN disabled on both devices?
- [ ] Using `http://` not `https://`?

---

**Your IPs:**
- Local: `192.168.29.169`
- Tailscale: `100.96.3.158`

**Server Port:** `8000`
**Token:** `demo-token-123`
