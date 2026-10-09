---
lang: en
slug: diamond-model
order_index: 12
title: Diamond Model of Intrusion Analysis
summary: Learn to analyze relationships among adversaries, capabilities, infrastructure, and victims, and to connect CTI events using evidence rather than assumptions.
tags: [cti, diamond-model, intrusion-analysis, threat-analysis]
---

# Diamond Model of Intrusion Analysis

## Lesson Goal

This lesson introduces a way to view cyber incidents not merely as lists of IP addresses, file hashes, or techniques, but as **relationships among an adversary, a capability, infrastructure, and a victim**. The Diamond Model helps analysts structure their evidence, identify missing information, and connect incidents without making unsupported claims.

By the end of this lesson, you should be able to identify its four core vertices, describe an intrusion as a *diamond event*, connect related events, and distinguish observation from analytical inference.

## Key Concepts

- Diamond Model of Intrusion Analysis
- Adversary
- Capability
- Infrastructure
- Victim
- Event
- Pivoting
- Activity Thread
- Attribution
- Confidence Level

## What Is the Diamond Model?

The Diamond Model is a framework for organizing and analyzing cyber intrusion activity. Its central idea is straightforward: **an adversary** uses **a capability**, through **infrastructure**, against **a victim**.

The four vertices can be pictured as a diamond:

```text
                Adversary
               /         \
     Infrastructure     Capability
               \         /
                  Victim
```

This diagram is conceptual. Analysts do not need to know every vertex to describe an event. In many investigations the victim and the malicious capability are known, while the adversary remains unidentified.

The model is especially useful when studying connections across multiple incidents rather than treating every alert as an isolated event.

## 1. Adversary

The adversary is the person, group, or organization responsible for directing or carrying out an activity.

Useful questions include:

- Who might be behind the observed activity?
- What evidence supports a link to a tracked threat cluster?
- What is the actor's possible objective?
- Which alternative explanations need to be considered before attribution?

**Important:** Two incidents involving the same malware or infrastructure are not automatically the work of the same adversary. Tools and services may be shared, rented, reused, or imitated.

## 2. Capability

Capability refers to the technical mechanisms and methods used to affect a target.

Examples include:

- A malicious document containing a macro
- A credential-harvesting login page
- A particular malware family
- A PowerShell-based execution technique
- Exploitation of a software vulnerability

Do not confuse capability with infrastructure. **A fake login page and its credential-harvesting behavior** describe a capability, while **the domain and server hosting that page** are infrastructure.

## 3. Infrastructure

Infrastructure includes the technical resources used to deliver, support, or control an operation.

Examples include:

- Phishing domains and web servers
- Command-and-control (C2) servers
- Email delivery systems
- Proxies and redirectors
- Hosting accounts and network resources

Time matters when interpreting infrastructure. An IP address can have different owners or purposes at different times. Seeing the same IP in two reports is therefore not necessarily strong evidence of a shared operation.

## 4. Victim

The victim is the person, account, device, organization, or other asset targeted by the activity.

Relevant attributes can include:

- Industry and business context
- The user's job role
- Affected account or device
- Location and technologies in use
- The target's likely value to the attacker

Shared victim characteristics may suggest a targeting pattern, but they cannot independently prove common adversary ownership.

## 5. Building a Diamond Event

The basic unit of analysis is an **event** associated with an observed activity. Besides the four vertices, a useful event record includes timing, evidence sources, and uncertainty.

Example:

| Field | Sample observation |
| --- | --- |
| Event ID | EVT-001 |
| Time | September 12, 09:15 UTC |
| Adversary | Unknown |
| Capability | Credential-harvesting login page |
| Infrastructure | `login-update.example` (fictional) |
| Victim | Employee of a financial organization |
| Evidence | Email header and verified URL record |
| Confidence | High for observed infrastructure/method; insufficient for attribution |

The event does not identify the adversary, but it makes known facts and outstanding questions explicit.

## 6. Pivoting and Activity Threads

**Pivoting** means following a known indicator or relationship to investigate additional, potentially relevant evidence. For example, an analyst might start with a suspicious domain, examine historical DNS data, and identify related domains. Every proposed link should be assessed independently.

An **activity thread** connects events through their sequence and relationships:

`Phishing email → Fake login page visit → Account sign-in attempt`

Such a sequence can support a hypothesis that the events belong to the same operation. However, proximity in time or similarity in technique does not by itself establish that conclusion.

When linking events, ask:

1. Was the same infrastructure used, and did the usage periods overlap?
2. Are the capabilities or TTPs meaningfully similar?
3. Do the victims share a relevant targeting pattern?
4. Could shared hosting or other benign explanations account for the link?
5. Which concrete records support each proposed connection?

## 7. CTI Case Study: A Phishing Campaign

The following scenario is entirely fictional. Domain names are examples only.

A SOC receives reports of three suspicious emails. The first two lead to the same fake login page but target different employees. The third leads to a different domain with a similar page layout and request flow.

**Event A:**

- Adversary: Unknown
- Capability: Corporate credential-harvesting page
- Infrastructure: `secure-login.example`
- Victim: Finance team employee
- Evidence: Email link and a page capture taken in a controlled environment

**Event B:**

- Adversary: Unknown
- Capability: Same phishing page pattern
- Infrastructure: `secure-login.example`
- Victim: Human resources employee
- Evidence: Second email report and URL record

**Event C:**

- Adversary: Unknown
- Capability: Similar but not conclusively identical page
- Infrastructure: `employee-auth.example`
- Victim: Employee at a separate organization
- Evidence: Screenshot and limited URL data

**Assessment:** Events A and B are strongly related because they share observed infrastructure. Event C cannot be assigned to the same campaign solely because its page looks similar. Historical DNS, registration timing, or more distinctive technical evidence would be needed.

**CTI output:** Report confirmed domains, targeted employee groups, observed phishing techniques, evidence sources, and unverified relationships separately.

## 8. Diamond Model vs. MITRE ATT&CK

The frameworks complement each other:

| Diamond Model | MITRE ATT&CK |
| --- | --- |
| Focuses on relationships among adversary, capability, infrastructure, and victim. | Categorizes adversary behavior as tactics and techniques. |
| Helps investigate links among events and campaigns. | Provides a common vocabulary for observed techniques. |
| Asks who used what, through which resources, against whom. | Asks which behavior or technique was observed. |

For example, a phishing incident can be labeled with an appropriate ATT&CK technique, while a diamond event captures its domain, victim, capability, and any supported relationship to an adversary.

## 9. Common Analytical Mistakes

- Making confident attribution from a single matching IOC.
- Treating shared hosting or legitimate services as proof of malicious ownership.
- Ignoring the time period during which infrastructure was used.
- Filling unknown vertices with guesses presented as facts.
- Omitting source quality or confidence assessments.
- Assuming similar TTPs always indicate the same campaign.

Sound CTI analysis separates **verified observations**, **inferences**, and **unanswered questions**.

## Mini Exercise

Two employees of one organization received emails linking to `notice.example`. In the same week, an employee of another company received a link to `alert.example`. Both domains display similar login pages.

1. Identify the Diamond Model vertices for each incident.
2. Which details are direct observations, and which are hypotheses?
3. What additional evidence would help assess whether the domains are operated by the same adversary?
4. How would you write an assessment without asserting that the actor is definitely the same?

**Expected approach:** Treat the domains as infrastructure, credential harvesting as the capability, and the employees as victims. Keep the adversary unknown. Visual similarity is an investigative lead, not proof of attribution.

## Conclusion

The Diamond Model provides a structured way to examine **Adversary – Capability – Infrastructure – Victim** relationships. Its greatest benefit is not just discovering connections, but also recognizing where the evidence does not justify a claim.

`Observation → Diamond Event → Cross-event links → Test alternatives → Evidence-based assessment`
