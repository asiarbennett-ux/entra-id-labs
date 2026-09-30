# 🛰️ Aetheris Orbital Dynamics — Enterprise Organization Profile

> *The fictional operational blueprint and architectural foundation for every lab in this repository. Consistent context turns a random set of portal clicks into a cohesive, production-grade identity architecture.*

---

## 🏢 Company Snapshot

| Category | Operational Specs |
| :--- | :--- |
| **Industry** | Commercial Aerospace & Real-Time Satellite Telemetry |
| **Headquarters** | Carrollton, Texas (Mission Control Alpha) |
| **Workforce Scale** | ~150 specialized aerospace engineers, ground-station operators, and security personnel |
| **Key Customers** | Commercial space agencies, national orbital networks, and defense prime contractors |
| **Data Classifications** | High-altitude telemetry feeds, live tracking data, proprietary satellite bus configurations, and restricted launch telemetry |
| **Operating Model** | Hybrid — hardened on-site ground control stations, secure remote engineering pods, and vetted third-party subcontractors |

---

## ⚡ Why This Environment is Hard
We don't build generic labs. Every security control, conditional access rule, and lifecycle policy in this repository is forged under brutal operational constraints:

1. **Clearance Level is an Identity Attribute:** Not everyone with an enterprise badge gets eyes on live satellite positioning feeds. Security clearance is a mandatory gating factor for high-value access.
2. **Third-Party Contractors:** External engineering vendors share our digital airspace, requiring aggressively scoped, time-bound, and expiring access—zero permanent standing trust.
3. **Telemetry Protection & Auditing:** Ground-station feeds demand flawless, immutable audit trails and immediate anomaly visibility to satisfy strict regulatory frameworks.
4. **Program Compartmentalization:** Strict isolation ensures engineers working on Constellation Alpha have zero visibility into Constellation Beta's command channels.
5. **Legacy Ground Hardware:** Older telemetry tracking gear often predates modern authentication standards and requires specialized app proxies and legacy protocol lockdowns.
6. **Zero-Tolerance Offboarding:** Turnover is real and fast. A stale account on an active satellite control plane is an unacceptable operational vulnerability.

---

## 🛡️ Privileged Access Tiers

| Tier | Target Scope | Enforcement & Control Model |
| :--- | :--- | :--- |
| **Tier 0** | Global Administrators, Privileged Role Administrators | **PIM-Enforced Only:** Requires multi-factor approval, active business justification, and hardware-backed MFA. Zero standing access. |
| **Tier 1** | Workload Admins (Application, User, and Security Administrators) | **Just-in-Time:** PIM-eligible activation backed by strict MFA and explicit session time limits. |
| **Tier 2** | Helpdesk & Telemetry Support Crews | **Scoped & Reviewed:** Permanent administrative unit scoping with mandatory quarterly access reviews. |
| **Break-Glass** | Emergency Global Recovery Accounts (`admin-breakglass`) | **FIDO2-Locked & Alerted:** Explicitly excluded from standard Conditional Access, protected by physical hardware keys, and wired for instant high-priority SOC paging on every single login. |

---

## 📋 Standing Business Rules

### 🔐 Authentication & Identity
* **Phishing Resistance Mandate:** All interactive personnel must satisfy hardware-backed, phishing-resistant MFA.
* **Death to Legacy Auth:** Legacy authentication protocols (IMAP, POP, older basic auth paths) are permanently blocked tenant-wide.
* **Privileged Hardware Requirement:** Any administrative activation requires certified hardware tokens.

### 👥 Authorization & Group Management
* **Role-Based Grouping:** Access is granted strictly via automated security group memberships—never through direct user-to-resource assignments.
* **Lifecycle Automation:** Group memberships dynamically mirror HR attributes and active clearance levels.
* **Privilege Ceiling:** No standing administrative permissions are permitted above Tier 2.

### ⏱️ Lifecycle & Governance
* **The Joiner:** Provisioned automatically based on department structure and employment classification.
* **The Mover:** Department changes automatically trigger immediate access recalculations within the next sync cycle.
* **The Leaver:** Same-day account disablement, immediate active session revocation, and automated license harvesting.
