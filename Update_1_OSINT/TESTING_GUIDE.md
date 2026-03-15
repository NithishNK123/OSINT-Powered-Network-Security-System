# Quick Start Testing Guide

## 1. Start the Application

```bash
cd "c:\Users\User\OneDrive\Desktop\Final OSINT\Update_1_OSINT"
python dashboard/app.py
```

The server should start at: `http://localhost:5000`

## 2. Login Test Cases

### Test Case 1: Viewer Access
1. Go to http://localhost:5000/login
2. Select **Viewer** role
3. Enter any username/password (demo mode)
4. Click "Login"

**Expected Results**:
- Dashboard loads with KPI cards
- Sidebar shows only: **Dashboard** navigation item
- Clicking /analyze, /settings, /history redirects to /dashboard
- Settings link not visible in sidebar

### Test Case 2: Analyst Access
1. Go to http://localhost:5000/login
2. Select **Analyst** role
3. Enter any username/password
4. Click "Login"

**Expected Results**:
- All pages accessible: Dashboard, Analyze, Alerts, History, Reports
- Settings link NOT visible (Admin only)
- Can perform threat analysis
- Can search history and export reports
- Report selection buttons work

### Test Case 3: Admin Access
1. Go to http://localhost:5000/login
2. Select **Admin** role
3. Enter any username/password
4. Click "Login"

**Expected Results**:
- ALL pages accessible including Settings
- Settings link visible in sidebar
- Can adjust theme, risk thresholds, API toggles
- Theme toggle animation works (diagonal wave, 1.6s)

## 3. Feature Testing

### Analyze Page
- **Access**: Analyst, Admin
- **Test**:
  1. Enter IP address: `185.10.10.10`
  2. Click "Analyze"
  3. Should show: High risk, 78 score, 3 open ports
  4. Result contains: threat type, open ports table, AI explanation
  5. Should have Export PDF and Export Excel buttons

### History Page
- **Access**: Analyst, Admin
- **Test**:
  1. Enter search query in search box
  2. Select "High Risk" from dropdown
  3. Click "Filter"
  4. Results should update
  5. Click page numbers for pagination
  6. Verify risk badges are color-coded

### Reports Page
- **Access**: Analyst, Admin
- **Test**:
  1. Click on a report card
  2. Verify selection shows blue border
  3. Info card should appear with report name
  4. Buttons should enable (change opacity)
  5. Click Download/View buttons (functions ready for implementation)

### Alerts Page
- **Access**: Analyst, Admin
- **Test**:
  1. Page displays alert cards (if any alerts exist)
  2. Each alert shows: target, risk level, threat type, timestamp
  3. Action buttons present: Investigate, Block IP, Dismiss
  4. If no alerts: Empty state with success icon displays

### Settings Page
- **Access**: Admin only
- **Test - Theme Toggle**:
  1. Click sun/moon icon to toggle theme
  2. Should see diagonal wave animation (1.6s)
  3. All colors should transition smoothly
  4. Verify header, sidebar, cards all update
  5. Refresh page - theme persists
  6. Test dark → light → dark transitions

- **Test - Risk Thresholds**:
  1. Adjust sliders for Low/Medium/High risk
  2. Verify visual reference bars update
  3. Click Save Thresholds
  4. Verify message confirms save

- **Test - API Toggles**:
  1. Toggle VirusTotal, AbuseIPDB, Shodan switches
  2. Click Save Integration
  3. Verify settings persist after reload

- **Test - Automation**:
  1. Enable auto-monitor checkbox
  2. Enter targets (comma-separated IPs)
  3. Set scan interval
  4. Click Save Settings
  5. Verify automation persists

## 4. RBAC Bypass Testing

### Test Unauthorized Route Access
```bash
# As Viewer, try accessing analyst feature directly:
curl http://localhost:5000/analyze -H "Cookie: session=..."
# Expected: Redirect to /login or 403 Forbidden

# As Analyst, try accessing admin feature directly:
curl http://localhost:5000/settings -H "Cookie: session=..."
# Expected: Redirect to /dashboard or 403 Forbidden
```

## 5. Theme Persistence Testing

1. **Set Theme**: Admin → Settings → Toggle theme to Light
2. **Refresh**: Press F5 or reload page
3. **Expected**: Light theme persists
4. **Toggle Back**: Switch to Dark mode
5. **Expected**: Dark theme persists
6. **Different Role**: Logout → Login as Analyst
7. **Expected**: Theme persists across roles

## 6. Visual Quality Checklist

### Dashboard
- [ ] KPI cards display correctly
- [ ] Chart visualizations render (Chart.js)
- [ ] Responsive layout (resize browser, check mobile view)
- [ ] Colors match design spec (navy #0a0e27 for dark mode)
- [ ] Icons from FontAwesome display properly

### Sidebar Navigation
- [ ] User avatar with role badge visible
- [ ] Access level card shows current permissions
- [ ] Navigation items responsive (collapse on mobile)
- [ ] Active page highlighted
- [ ] Hover effects on menu items

### Cards & Buttons
- [ ] Glassmorphism effect visible (slight transparency with blur)
- [ ] Neon accents glow slightly (on hover)
- [ ] Buttons change on hover (color shift)
- [ ] Disabled buttons appear grayed out (opacity, cursor change)

### Forms
- [ ] Input fields focus state visible
- [ ] Error messages display properly
- [ ] Submit buttons responsive
- [ ] Validation works

## 7. Browser DevTools Debugging

### Check Theme in Console
```javascript
// Check current theme
localStorage.getItem('socTheme')

// Manually switch theme
localStorage.setItem('socTheme', 'light')
location.reload()

// Check CSS variables
getComputedStyle(document.documentElement).getPropertyValue('--bg-primary')
```

### Check Session Data
1. Open DevTools → Application → Cookies
2. Look for `session` cookie
3. Flask session is server-side (backend validates)
4. User role stored in: Flask `session['user']['role']`

## 8. Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| 404 on new templates | Template file missing | Check `templates/` folder has `-new.html` files |
| 403 Unauthorized | Wrong role accessing route | Ensure `@require_role` decorator on route |
| Styling not loading | CSS file missing | Verify `modern-soc.css` exists in `static/css/` |
| Wave animation doesn't play | Browser doesn't support CSS | Check browser version (needs CSS animations) |
| Theme doesn't persist | localStorage disabled | Check browser settings, enable storage |
| Login fails | Session not initialized | Verify `SECRET_KEY` set, check `@before_request` hook |
| Images/Icons missing | Wrong path in templates | Verify FontAwesome CDN link in `base-new.html` |

## 9. Performance Monitoring

### Check Page Load Time
```bash
# In browser console
performance.measure('pageLoad')
performance.getEntriesByType('measure')
```

### Monitor CSS Rendering
1. DevTools → Performance tab
2. Record page transition with theme toggle
3. Look for "Rendering" section
4. Wave animation should take ~1.6s

### Check Network Usage
1. DevTools → Network tab
2. Monitor CSS file size (modern-soc.css should be ~30-50KB)
3. Ensure no 404 errors for assets

## 10. Production Checklist Before Deployment

- [ ] Change `app.config['SECRET_KEY']` to secure random string
- [ ] Set `DEMO_MODE = False` when APIs configured
- [ ] Enable HTTPS (SSL/TLS certificate)
- [ ] Set up proper database (production connstr)
- [ ] Configure session timeout (security)
- [ ] Setup logging and monitoring
- [ ] Test with real VirusTotal, AbuseIPDB, Shodan APIs
- [ ] Load test for concurrent users
- [ ] Security audit on RBAC implementation
- [ ] Backup and disaster recovery testing

---

**Status**: Ready for Testing ✅
**Last Updated**: Current Session
**Framework**: Flask 3.0.3 + Modern UI System
