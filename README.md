<div align="center">

# 🛰️ Aetheris Orbital Dynamics — Enterprise IAM Labs

### *Advanced Identity Engineering, Zero-Trust Architecture, & Automated Lifecycle Governance*

[![Platform](https://img.shields.io/badge/Platform-Microsoft_Entra_ID-0078D4?style=flat-square&logo=microsoft&logoColor=white)](https://github.com/asiabennett-ux)
[![Automation](https://img.shields.io/badge/Automation-Python_3.11_%2F_Graph_API-3776AB?style=flat-square&logo=python&logoColor=white)](https://github.com/asiabennett-ux)
[![Security Standard](https://img.shields.io/badge/Standard-NIST_SP_800--63_%2F_Zero_Trust-orange?style=flat-square)](https://github.com/asiabennett-ux)

</div>

---

## ⚡ What this repository is

Most IAM lab write-ups stop at *"here is where you click in the portal."* These are built differently. 

Every lab models a high-stakes operational challenge at **Aetheris Orbital Dynamics**—a fast-growing orbital launch and satellite telemetry provider. Every scenario is built end-to-end, automated through Python and the Microsoft Graph SDK, and rigorously validated using real sign-in telemetry, audit records, and raw token outputs.

### 🧩 The 4-Question Engineering Framework
Every individual lab folder answers four essential questions:
1. 🎯 **What business problem does this solve?** (*The Requirement*)
2. ⚙️ **Can you configure it correctly?** (*The Implementation*)
3. 🔬 **Can you prove it works?** (*The Validation & Logs*)
4. ⚠️️ **Do you understand the failure modes?** (*Gotchas & Takeaways*)

---

## 🚀 Lab Index

### Phase 1: Identity Lifecycle & Provisioning
| Lab | Focus Area | Key Technical Outcome |
| :--- | :--- | :--- |
| **[lab-01-tenant-baseline](./lab-01-tenant-baseline/)** | Tenant setup, RBAC personas, business rules | Establishing granular admin scopes prevents privilege creep before automation begins. |
| **[lab-02-onboarding](./lab-02-onboarding/)** | Bulk user provisioning & temporary access packages | Handled malformed batch inputs gracefully without manual admin intervention. |
| **[lab-03-mover](./lab-03-mover/)** | Cross-division transfers & dynamic groups | Department transfers required explicit attribute restructuring to drop legacy clearance roles. |
| **[lab-04-offboarding](./lab-04-offboarding/)** | Python, PowerShell, Microsoft Graph SDK | Closed the active session exposure window down from over 2 minutes to **0.463 seconds**. |

### Phase 2: Access Control & Governance
| Lab | Focus Area | Key Technical Outcome |
| :--- | :--- | :--- |
| **[lab-05-conditional-access](./lab-05-conditional-access/)** | Zero-trust baselines, risk policies, CAE | Report-only mode flagged a critical telemetry service account that would have caused an outage on enforcement. |
| **[lab-06-pim](./lab-06-pim/)** | Privileged Access Management & JIT elevation | Eligible and active assignments cannot overlap, enforcing a strict dual-control elevation workflow. |

### Phase 3: Application Integration
| Lab | Focus Area | Key Technical Outcome |
| :--- | :--- | :--- |
| **[lab-07-federation](./lab-07-federation/)** | SAML SSO & Custom Claims transformations | A transformation failure on an empty attribute breaks the entire assertion rather than falling back gracefully. |

---

## 💡 The Core Architectural Philosophy

> *"Derived access is a fact. Approved access is a decision."*

* 🧬 **Attribute-Driven Scale:** Access tied to HR attributes scales dynamically with lifecycle state changes.
* 🛡️ **Controlled Exception Paths:** High-risk privileges require formal justification, strict expiration windows, and explicit sponsor approval, leaving an immutable audit trail.
* ⚡ **Proactive Revocation:** Offboarding automation immediately strips active refresh tokens rather than waiting for natural expiration cycles.

---

## 🛠️ Technical Stack & Tooling

* **Automation & Core APIs:** Python 3.11, Microsoft Graph SDK, PowerShell Core, REST Endpoints
* **Identity Platforms:** Microsoft Entra ID (P2), Active Directory DS, Hybrid Synchronization Architecture
* **Protocols & Standards:** SAML 2.0, OAuth 2.0 / OIDC, SCIM 2.0, NIST SP 800-63 Zero Trust Guidelines

---

## 📂 Repository Structure

```text
entra-id-labs/
├── aetheris-orbital-dynamics.md     # Org profile, personas, and business rules
├── lab-01-tenant-baseline/          # Tenant setup & foundational structure
├── lab-02-onboarding/               # Automated provisioning
├── lab-03-mover/                    # Dynamic department transitions
├── lab-04-offboarding/              # Python & Graph API revocation scripts
├── lab-05-conditional-access/       # Zero-trust access policies
├── lab-06-pim/                      # JIT administrative controls
└── lab-07-federation/               # SAML app integration & claims
