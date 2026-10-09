---
lang: en
slug: threat-hunting
order_index: 18
title: Threat Hunting Fundamentals
summary: Learn hypothesis-driven threat hunting using Windows event logs, Sysmon, SIEM data, Sigma detection logic, and MITRE ATT&CK.
tags: [cti, threat-hunting, detection-engineering, mitre-attack, sigma]
---

# Threat Hunting Fundamentals

## Lesson Objectives

This lesson introduces **Threat Hunting**, explains how it differs from reactive alert investigation, and demonstrates how Cyber Threat Intelligence (CTI) can support testable hunting hypotheses. The exercises rely on **fictional, harmless event records** rather than live malware or production systems.

## Key Concepts

- Threat Hunting
- Hypothesis-Driven Hunting
- IOC (Indicator of Compromise)
- TTP (Tactics, Techniques and Procedures)
- SIEM (Security Information and Event Management)
- EDR (Endpoint Detection and Response)
- Windows Event Logs and Sysmon
- Sigma Rule
- False Positive / False Negative
- Baseline and Evidence

## What Is Threat Hunting?

Threat Hunting is a **proactive, hypothesis-driven** search for signs of adversary behavior in available security telemetry. Instead of waiting for automated alerts, a hunter looks for activity that may be consistent with a known or suspected technique.

For example, responding to an EDR alert about a blocked malicious file is reactive investigation. Searching across endpoints for unusual process relationships that have not triggered alerts is a hunting activity.

Importantly, unusual behavior is not automatically malicious. Findings need context and corroboration.

## How CTI Supports Threat Hunting

CTI reports describe adversary objectives, capabilities, and **TTPs**. A hunter translates these observations into questions that available data can answer.

Example:

- **Intelligence observation:** Some intrusions involve unusual command interpreters after initial access.
- **Hypothesis:** Office applications may have launched suspicious command interpreters in our environment.
- **Required data:** Parent/child process relationships, command line, user, and timestamp.
- **Validation:** Investigate cases not explained by approved automation, administrative tools, or testing.

Individual IOCs can become outdated quickly. Behavioral hunting based on TTPs may remain useful across changes in attacker infrastructure.

## 1. The Hunting Workflow

1. **Define scope:** Select target systems and a time range.
2. **Form a hypothesis:** Describe observable behavior that can be tested or disproven.
3. **Prepare telemetry:** Verify log availability, timestamps, and collection coverage.
4. **Search:** Identify candidate events in SIEM, EDR, or log platforms.
5. **Validate:** Compare candidates with known business activity, historical baselines, and independent data.
6. **Document and improve:** Record outcomes, escalate confirmed concerns, and improve detections or visibility.

A hunt with no findings does **not** prove that an adversary is absent. Missing telemetry, limited scope, or an unsuitable hypothesis can affect the result.

## 2. Common Data Sources

| Source | Example evidence |
|---|---|
| Windows Security Log | Logons and process creation (when configured) |
| Sysmon | Process creation, network connections, and selected events |
| EDR | Process trees, behavior detections, endpoint context |
| DNS logs | Domain queries and timing relationships |
| Proxy / Firewall | Connection and web access observations |
| SIEM | Search and correlation across data sources |

Useful examples include Windows Security **Event ID 4688** for process creation when the required auditing is enabled; Sysmon **Event ID 1** for process creation; and Sysmon **Event ID 3** for network connections when enabled. An event ID alone does not establish malicious activity.

## 3. Example Hunting Scenario

An organization is investigating command interpreters launched by Office applications. The following records are **entirely fictional**:

| Time | Host | Parent Image | Image | User |
|---|---|---|---|---|
| 09:10 | PC-01 | explorer.exe | WINWORD.EXE | ayse |
| 09:11 | PC-01 | WINWORD.EXE | powershell.exe | ayse |
| 09:14 | PC-02 | explorer.exe | powershell.exe | admin |
| 09:17 | PC-03 | scheduler.exe | powershell.exe | svc-backup |

The `WINWORD.EXE → powershell.exe` relationship deserves closer review. It is **not sufficient evidence of compromise** by itself. Questions to ask include:

- Did the document originate from a trusted internal workflow?
- What do the command line, signature, and executable path indicate?
- Are there related network connections, file creations, or persistence events?
- Could an authorized plugin or business automation explain the behavior?

The other PowerShell records might correspond to administrative and backup workflows. They still require validation, but may receive different priorities.

## 4. Detection Logic with Sigma

**Sigma** is an open, portable rule format for describing log-based detections. The simplified example below looks for PowerShell launched by common Office applications within appropriately mapped **process creation** events:

```yaml
# Simplified educational example; validate before production use.
title: Office Application Spawning PowerShell
id: 7925fb1f-a449-44f0-ae56-6a6b99b5089f
status: experimental
description: Finds PowerShell launched by a common Office application.
logsource:
  product: windows
  category: process_creation
detection:
  selection_parent:
    ParentImage|endswith:
      - '\\WINWORD.EXE'
      - '\\EXCEL.EXE'
  selection_child:
    Image|endswith:
      - '\\powershell.exe'
      - '\\pwsh.exe'
  condition: selection_parent and selection_child
falsepositives:
  - Legitimate macros or enterprise automation
level: medium
```

This rule produces an **investigation signal**, not an automatic verdict of malicious activity. Field mappings, expected exceptions, and tests must be adjusted for the environment.

## 5. Mapping to MITRE ATT&CK

Potentially suspicious PowerShell activity can be investigated in relation to **T1059.001 – PowerShell**. However, the process name alone may not provide enough evidence to assign the technique confidently. Command-line context, execution purpose, and supporting telemetry matter.

ATT&CK categorizes behaviors; it does not independently prove that an attack happened or identify an actor.

## 6. Writing a Hunt Report

A concise hunt report might include:

- **Hypothesis:** Unusual PowerShell executions originating from Office applications.
- **Scope:** Windows user endpoints over the last seven days.
- **Sources:** Sysmon process creation records and EDR process trees.
- **Findings:** One candidate process chain requiring investigation.
- **Limitations:** Some endpoints may lack complete Sysmon coverage.
- **Next steps:** Validate the business context and network activity; escalate when warranted.

Clear outcomes such as **confirmed malicious**, **benign**, or **inconclusive** prevent analysts from disguising uncertainty.

## Mini Exercise

Answer these questions:

1. How does threat hunting differ from investigating alerts?
2. Why does `WINWORD.EXE → powershell.exe` not prove an attack on its own?
3. Which two additional data sources could corroborate the event?
4. Why should missing telemetry be documented in the report?

**Evaluation:** A strong answer distinguishes hypotheses from evidence and suggests additional validation without ignoring benign explanations.

## Conclusion

Threat Hunting transforms CTI into testable investigation hypotheses. Effective hunting depends not just on finding unusual events, but on **validating evidence, documenting uncertainty, and improving defensive visibility**.
