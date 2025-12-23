# Sidebar Troubleshooting Guide

## Issue: Cannot Access Sidebar

If you're unable to see or access the sidebar, try these solutions:

## Quick Fixes

### 1. Look for the Sidebar Toggle Button
- **Location**: Top-left corner of the Streamlit app
- **Icon**: Three horizontal lines (☰) or an arrow (→)
- **Action**: Click to expand/collapse the sidebar

### 2. Check Browser Window Size
- Sidebar may be hidden on very small screens
- Try resizing your browser window
- Minimum recommended width: 1024px

### 3. Clear Browser Cache
- Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
- Or clear browser cache and reload

## Configuration Applied

I've added configuration to ensure the sidebar is always visible:

1. **`.streamlit/config.toml`** - Streamlit configuration
   - `hideSidebar = false` - Ensures sidebar is not hidden
   
2. **`st.set_page_config()`** in each page
   - `initial_sidebar_state="expanded"` - Forces sidebar to be open

## Manual Sidebar Access

If the sidebar still doesn't appear:

### Option 1: Keyboard Shortcut
- Press `S` key to toggle sidebar (when app is focused)

### Option 2: URL Parameter
- Add `?sidebar_state=expanded` to the URL
- Example: `http://localhost:8501?sidebar_state=expanded`

### Option 3: Streamlit Settings
1. Click the three dots (⋮) in top-right corner
2. Select "Settings"
3. Check "Always show sidebar"

## Verify Pages Are Detected

The sidebar navigation menu is automatically generated from the `pages/` directory. Verify:

```bash
ls pages/
```

You should see:
- `1_📊_Dashboard.py`
- `2_⚙️_Assumptions.py`
- `3_📈_Analysis.py`
- `4_ℹ️_Help.py`

## Expected Sidebar Layout

When working correctly, the sidebar should show:

```
┌─────────────────────────┐
│ ☰ [Toggle Button]       │
├─────────────────────────┤
│                         │
│  📊 Dashboard           │  ← Page Navigation
│  ⚙️ Assumptions          │     (Auto-generated)
│  📈 Analysis             │
│  ℹ️ Help                 │
├─────────────────────────┤
│                         │
│  [Page Content]          │  ← Page-specific content
│  (e.g., input sliders)   │     (e.g., on Assumptions)
│                         │
└─────────────────────────┘
```

## If Still Not Working

1. **Restart Streamlit**:
   ```bash
   # Stop current instance (Ctrl+C)
   streamlit run app.py
   ```

2. **Check Streamlit Version**:
   ```bash
   streamlit --version
   # Should be >= 1.28.0
   ```

3. **Check Browser Console**:
   - Open browser developer tools (F12)
   - Look for JavaScript errors
   - Check Network tab for failed requests

4. **Try Different Browser**:
   - Chrome, Firefox, Safari, Edge
   - Some browsers may have compatibility issues

## Contact

If the sidebar still doesn't appear after trying these solutions, there may be a deeper configuration issue. Check:
- Streamlit installation
- Browser compatibility
- Network/firewall settings blocking Streamlit

