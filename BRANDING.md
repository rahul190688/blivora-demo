# Apex Analytix - Branding Guidelines for POC

## Color Palette

### Primary Colors
- **Black**: `#000000` - Primary text, logo
- **Vivid Cyan Blue**: `#0693e3` - Accent color, links, buttons
- **White**: `#ffffff` - Backgrounds, contrast

### Secondary/Accent Colors (from WordPress theme)
- **Vivid Purple**: `#9b51e0`
- **Vivid Green Cyan**: `#00d084`
- **Vivid Red**: `#cf2e2e` (for alerts/urgent)
- **Luminous Vivid Orange**: `#ff6900` (for warnings)

## Typography
- **Primary Font**: Professional sans-serif (System font stack)
- **Font Sizes**:
  - Huge: 42px
  - Large: 36px
  - Medium: 20px
  - Normal: 16px
  - Small: 13px

## Visual Style
- **Clean & Minimal**: Modern, uncluttered interfaces
- **Data-Driven**: Charts, metrics, analytics
- **High Contrast**: Easy readability
- **Professional**: Enterprise-grade appearance
- **Trustworthy**: Authoritative, reliable look

## Logo
- Location: `/wp-content/themes/apexanalytix/assets/images/header/logo.svg`
- Colors: Black text with blue accent
- Format: SVG (scalable)
- Style: Modern, clean wordmark

## UI Components

### Buttons
- **Primary**: Vivid Cyan Blue (#0693e3) background, white text
- **Secondary**: White background, black text, blue border
- **Danger**: Vivid Red (#cf2e2e)

### Alerts
- **Info**: Vivid Cyan Blue (#0693e3)
- **Success**: Vivid Green Cyan (#00d084)
- **Warning**: Luminous Vivid Orange (#ff6900)
- **Error**: Vivid Red (#cf2e2e)

### Cards & Panels
- White background
- Subtle shadow for depth
- Border: Light gray or none
- Border radius: Minimal (2-4px)

## Dashboard Style
- Clean white backgrounds
- Blue accent for active/selected states
- Black text for high contrast
- Data visualization in blue color scheme
- Minimal borders and dividers

## Terminology

### Company-Specific Terms
- "Support Request" (not just "ticket")
- "Risk Level" (instead of just priority)
- "Business Impact"
- "Compliance Flag"
- "Supplier-Related"
- "System Affected"
- "Resolution SLA"

### Department Categories
- Finance & Accounting
- Supplier Risk Management
- Compliance & Audit
- IT & Systems
- Operations
- Recovery Services
- Third-Party Management

## POC Branding Checklist

- [ ] Apply color scheme (Black, Blue, White)
- [ ] Add Apex logo to header
- [ ] Use company terminology
- [ ] Professional, minimal UI
- [ ] Data-driven dashboard
- [ ] High-contrast design
- [ ] Enterprise-grade look
- [ ] Custom field labels matching Apex business

## Implementation Notes

### Frappe Customization
1. **Custom Theme**: Create `apex_theme.json` with color variables
2. **Logo Upload**: Add to `public/images/apex-logo.svg`
3. **CSS Overrides**: Custom stylesheet for Apex branding
4. **DocType Labels**: Rename fields to match Apex terminology
5. **Dashboard**: Custom dashboard with Apex metrics

### Color Variables for Code
```python
# Apex Analytix Theme Colors
APEX_BLACK = "#000000"
APEX_BLUE = "#0693e3"
APEX_WHITE = "#ffffff"
APEX_PURPLE = "#9b51e0"
APEX_GREEN = "#00d084"
APEX_RED = "#cf2e2e"
APEX_ORANGE = "#ff6900"
```

### CSS Variables
```css
:root {
  --apex-black: #000000;
  --apex-blue: #0693e3;
  --apex-white: #ffffff;
  --apex-purple: #9b51e0;
  --apex-green: #00d084;
  --apex-red: #cf2e2e;
  --apex-orange: #ff6900;
}
```
