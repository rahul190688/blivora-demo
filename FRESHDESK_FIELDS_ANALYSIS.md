# Freshdesk Field Analysis - Apex Analytix

## Current Freshdesk Setup

### Navigation (Left Panel)
1. Dashboard
2. Tickets ← **PRIMARY**
3. Contacts
4. Solutions (Knowledge Base)
5. Forums
6. Analytics
7. Admin
8. Chat
9. Collapse

### Ticket Fields (Right Panel) - 23 Custom Fields

#### **P0 - CRITICAL for POC** (Must Have)
1. ✅ **Status** - (Frappe Helpdesk has this)
2. ✅ **Priority** - (Frappe Helpdesk has this)
3. ✅ **Agent** - (Frappe Helpdesk has this via assignment)
4. ✅ **Contact name** - (Frappe Helpdesk has this)
5. ✅ **Phone number** - (Frappe Helpdesk has this)
6. 🔴 **Client** - WHO is the ticket for (Customer/Department)
7. 🔴 **Product** - What product/service
8. 🔴 **Type** - Issue or Inquiry
9. 🔴 **Internal group** - Which team handles it
10. 🔴 **Division** - Business division

#### **P1 - HIGH Priority** (Important for POC)
11. 🟡 **Project code** - Project tracking
12. 🟡 **Apex Application or Service** - Which system
13. 🟡 **Issue or Inquiry** - Classification
14. 🟡 **Module** - System module affected
15. 🟡 **Client perceived priority level** - How urgent customer thinks it is
16. 🟡 **Internal team status** - Internal workflow status
17. 🟡 **Tag** - Categorization

#### **P2 - MEDIUM Priority** (Nice to have for POC)
18. 🟢 **3rd level** - Escalation level
19. 🟢 **Root cause owner** - Who owns the root cause
20. 🟢 **Implementation firm** - Partner/vendor
21. 🟢 **Internal Training Inquiry** - Training related?

#### **P3 - LOW Priority** (Post-POC)
22. 🔵 **Fixed in Release** - Version tracking
23. 🔵 **ADO Number** - Azure DevOps tracking

---

## POC Field Strategy

### Phase 1: Core Fields (Week 1)
**Add to HD Ticket via Custom Fields:**

1. **Client** (Link to Customer)
   - Type: Link
   - Options: HD Customer
   - Required: Yes

2. **Product/Service** (Select)
   - Options:
     - Risk Management Platform
     - Payment Processing
     - Supplier Onboarding
     - Audit & Recovery
     - Compliance Platform
     - Other

3. **Division** (Select)
   - Options:
     - Finance & Accounting
     - Supplier Risk
     - Compliance & Audit
     - IT & Systems
     - Operations
     - Recovery Services

4. **Internal Group** (Select)
   - Options:
     - Help Desk L1
     - Technical Support L2
     - Development Team
     - Infrastructure
     - Business Analysts
     - Management

5. **Apex Application or Service** (Select)
   - Options:
     - Risk Portal
     - Supplier Management
     - Payment Platform
     - Audit System
     - Compliance Dashboard
     - Other

6. **Issue Type** (Select)
   - Options:
     - Issue (Something broken)
     - Inquiry (Question/Request)
     - Feature Request
     - Access Request
     - Training Request

7. **Module** (Data field)
   - Type: Data
   - Description: Specific module/component affected

8. **Client Perceived Priority** (Select)
   - Options:
     - Critical - Business stopped
     - High - Major impact
     - Medium - Moderate impact
     - Low - Minor inconvenience

9. **Internal Team Status** (Select)
   - Options:
     - New
     - Acknowledged
     - In Progress
     - Waiting on Customer
     - Waiting on 3rd Party
     - Resolved - Pending Closure
     - Closed

10. **Project Code** (Data field)
    - Type: Data
    - Description: Project reference number

### Phase 2: Advanced Fields (Post-POC)
- Tag (Multiple select)
- 3rd Level (Select)
- Root Cause Owner
- Implementation Firm
- Fixed in Release
- ADO Number
- Internal Training Inquiry

---

## Field Mapping: Freshdesk → Frappe Helpdesk

| Freshdesk Field | Frappe Helpdesk | Action Required |
|----------------|----------------|----------------|
| Status | ✅ HD Ticket.status | Already exists |
| Priority | ✅ HD Ticket Priority | Already exists |
| Agent | ✅ Assignment | Already exists |
| Contact name | ✅ HD Customer | Already exists |
| Phone number | ✅ HD Customer.phone | Already exists |
| Client | 🔴 Custom Field | CREATE |
| Product | 🔴 Custom Field | CREATE |
| Type | 🔴 Custom Field | CREATE |
| Internal group | 🔴 Custom Field | CREATE |
| Division | 🔴 Custom Field | CREATE |
| Project code | 🟡 Custom Field | CREATE (P1) |
| Apex App/Service | 🟡 Custom Field | CREATE (P1) |
| Module | 🟡 Custom Field | CREATE (P1) |
| Client Priority | 🟡 Custom Field | CREATE (P1) |
| Internal Status | 🟡 Custom Field | CREATE (P1) |
| Tag | 🟡 Tag system | Use existing |

---

## POC Success Criteria

### Must Demonstrate:
1. ✅ All critical fields visible and working
2. ✅ Ticket creation with Apex-specific fields
3. ✅ Filtering by Department, Product, Type
4. ✅ Auto-assignment by Internal Group
5. ✅ Professional Apex branding
6. ✅ Simple analytics dashboard

### Demo Script Fields:
**Create a sample ticket showing:**
- Client: "Finance Department - Vendor Inquiry"
- Product: "Risk Management Platform"
- Division: "Supplier Risk"
- Internal Group: "Technical Support L2"
- Apex Application: "Risk Portal"
- Issue Type: "Issue"
- Module: "Supplier Onboarding"
- Client Perceived Priority: "High"
- Internal Team Status: "In Progress"
- Project Code: "RISK-2026-Q2"

This demonstrates ALL the complexity of current Freshdesk setup!

---

## Implementation Order

### Day 1: Core Custom Fields (5 fields)
1. Client
2. Product/Service
3. Division
4. Internal Group
5. Issue Type

### Day 2: Extended Fields (5 fields)
6. Apex Application or Service
7. Module
8. Client Perceived Priority
9. Internal Team Status
10. Project Code

### Day 3: Dashboard & Filtering
- Create ticket list views
- Add filters for all new fields
- Build simple analytics

### Day 4: Automation
- Auto-assign by Internal Group
- Auto-escalate by Client Perceived Priority
- Email templates

### Day 5: Testing & Demo
- Create 10 test tickets
- Test all workflows
- Prepare demo

---

## Questions for Rahul:

1. **Top 5 Most Used Fields?** (To prioritize for POC)
2. **Auto-assignment logic?** (How do you route tickets currently?)
3. **Critical workflows?** (What MUST work for demo?)
4. **Sample ticket data?** (Can you share 2-3 real ticket examples?)

---

## Cost Comparison

### Current Freshdesk
- **Customization**: Heavy (20+ custom fields)
- **Cost**: $49-79/agent/month (Pro/Enterprise required for this many custom fields)
- **20 agents**: $980-1,580/month = **$11,760-18,960/year**

### Blivora Demo (Custom Solution)
- **Customization**: Unlimited
- **Cost**: **$0** (self-hosted)
- **Savings**: **$12,000-19,000/year**
- **Plus**: Full control, unlimited fields, custom integrations

---

**This level of customization PROVES you need a custom solution!** ✅
