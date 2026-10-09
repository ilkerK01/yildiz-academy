---
lang: en
slug: cyber-kill-chain
order_index: 11
title: Cyber Kill Chain and the Stages of an Attack
summary: An introduction to the seven stages of the Cyber Kill Chain, practical attack scenarios, and how defenders can detect and disrupt attacks at each stage.
tags: [cti, attack-lifecycle, cyber-kill-chain]
---

# Cyber Kill Chain and the Stages of an Attack

## Lesson Goal

This lesson examines cyberattacks not simply as malicious actions visible at the final stage, but as a series of related activities. Using the **Cyber Kill Chain** model, we will explore the steps an adversary may take from researching a target to achieving an objective. We will also discuss how CTI analysts use the model to interpret incidents, formulate intelligence questions, and prioritize defensive action.

By the end of this lesson, you should be able to identify the seven stages, map observations from an incident scenario to those stages, and explain the model's limitations.

## Key Concepts

- Cyber Kill Chain
- Reconnaissance
- Weaponization
- Delivery
- Exploitation
- Installation
- Command and Control (C2)
- Actions on Objectives
- Indicator of Compromise (IOC)
- Tactics, Techniques, and Procedures (TTPs)
- Detection and Disruption

## What Is the Cyber Kill Chain?

The Cyber Kill Chain is a model developed by Lockheed Martin for examining targeted cyberattacks through seven successive stages. It helps defenders consider not only **what an adversary does**, but also **where an attack can be detected or disrupted**.

The classic sequence is:

`Reconnaissance → Weaponization → Delivery → Exploitation → Installation → Command and Control → Actions on Objectives`

This sequence is an educational framework rather than an inflexible formula. In real incidents, evidence for every stage may not be available, and attackers can skip, repeat, or perform steps in parallel. Analysts should not assume that every attack follows the sequence exactly.

## 1. Reconnaissance

At this stage, an adversary gathers information about a prospective target. Areas of interest may include internet-facing services, publicly available employee profiles, technologies used by the organization, and its domain infrastructure.

Example observations:

- Research into publicly available employee information
- Collection of information about internet-exposed systems
- Attempts to understand the target organization's technology environment

**CTI perspective:** The sectors targeted, methods of research, and recurring patterns of target selection across campaigns can be useful. The mere availability of public information does not prove that an attack has taken place.

**Defensive approach:** Reduce unnecessary information exposure, maintain an inventory of externally accessible assets, and investigate unusual scanning activity in context.

## 2. Weaponization

During weaponization, the adversary may prepare a malicious payload or attack content tailored to the target. For example, a document intended to exploit a software vulnerability could be combined with a malicious component.

Because weaponization often happens within the adversary's own environment, the target organization may find it difficult to observe directly. Analysts frequently infer this stage from recovered samples, campaign reports, or malware behavior.

**CTI perspective:** Similarities in tools, document formats, and malware families may help cluster related campaigns. A single similarity, however, does not establish definitive attribution.

## 3. Delivery

Delivery is the stage in which attack content reaches the target. A phishing email, malicious link, harmful attachment, or compromised website may serve as the delivery mechanism.

Example observations:

- An email with a suspicious attachment
- A link directing a user to a fake login page
- A URL associated with a previously reported attack campaign

**CTI perspective:** Analysts may examine email headers, URLs, domain information, file hashes, and delivery timestamps. The reliability, freshness, and context of each IOC should be evaluated.

**Defensive approach:** Email security controls, link and attachment analysis, user awareness, and network filtering.

## 4. Exploitation

In this stage, an adversary attempts to obtain the intended execution or access by exploiting a vulnerability or taking advantage of a user action.

For example, a suspicious process starting after a user opens a malicious document, or the exploitation of an application vulnerability, may be relevant to this stage. However, not every phishing incident involves a software vulnerability. Incidents involving stolen credentials also highlight the limitations of the classic model.

**CTI perspective:** Investigate which vulnerability, technique, or condition was actually exploited. The presence of a CVE reference does not, by itself, demonstrate that the vulnerability was exploited in the incident.

**Defensive approach:** Patch management, attack-surface reduction, application hardening, and monitoring for suspicious process behavior.

## 5. Installation

Installation refers to an adversary placing malware or a component that can help maintain access within the target environment. For example, the attacker might establish a malicious service or persistence mechanism.

Not every attack requires software to be installed persistently. Fileless activity and temporary access techniques may not fit neatly into this stage.

**CTI perspective:** New services, startup entries, unexpected files, and incident-related file hashes may provide useful evidence.

**Defensive approach:** Endpoint Detection and Response (EDR), application controls, monitoring of system changes, and least-privilege access.

## 6. Command and Control (C2)

An adversary may establish a communication channel with a compromised system to issue commands or direct further actions remotely. C2 traffic can sometimes resemble legitimate web traffic.

A CTI analyst might ask:

- Which domain or IP address receives the suspicious connections?
- How frequently do the connections occur?
- Has the infrastructure been associated with a previously reported campaign?
- How strong is the evidence supporting that relationship?

**Defensive approach:** Review DNS and network logs, investigate unusual outbound connections, and restrict access to confirmed malicious destinations.

An IP match alone is not definitive proof of C2 activity. Shared services and changing infrastructure may produce false positives.

## 7. Actions on Objectives

This stage covers the activities through which an adversary attempts to achieve the primary objective. The objective might involve exfiltrating data, encrypting systems, disrupting operations, collecting information, or causing another form of impact.

**CTI perspective:** Assess organizational impact, the types of data targeted, and possible adversary motivations. Do not state a specific motive or attacker identity as fact when the available evidence does not support it.

**Defensive approach:** Monitor data access and transfers, apply network segmentation, maintain backups, and activate incident-response and business-continuity procedures when needed.

## Case Study: A Fictional Phishing and Ransomware Campaign

Imagine an employee receives a suspicious invoice-themed email. A malicious process is later observed on their endpoint, and encryption activity is detected on a server.

| Cyber Kill Chain stage | Fictional observation | Analyst's question |
| --- | --- | --- |
| Reconnaissance | The email contains details relevant to the employee's role | Could this information have been gathered from public sources? |
| Weaponization | The attachment reportedly resembles a known malware family | What technical evidence supports this similarity? |
| Delivery | The employee receives a phishing email with an attachment | Was the same content delivered to other employees? |
| Exploitation | A suspicious process starts after the attachment is opened | What event triggered the process? |
| Installation | An unexpected persistence entry is identified | Is this entry connected to the attack? |
| Command and Control | Repeated outbound connections are observed from the endpoint | Are these confirmed C2 communications? |
| Actions on Objectives | Some files are observed being encrypted | What is the scope and business impact? |

**Important:** This is an illustrative analysis, not a description of a verified incident. A lack of evidence for a particular stage does not prove that the stage never occurred.

## Cyber Kill Chain vs. MITRE ATT&CK

The Cyber Kill Chain provides a high-level view of the progression of a targeted attack through seven stages. **MITRE ATT&CK** is a more detailed knowledge base that organizes real-world adversary behavior into tactics and techniques.

For example, an event described as **Delivery** in the Cyber Kill Chain might be associated with a specific Initial Access technique in ATT&CK. However, the two frameworks are not equivalent or directly interchangeable at every level.

In CTI work, the Kill Chain can help explain the overall attack progression, while ATT&CK can describe specific behaviors in greater technical detail.

## Limitations of the Model

- The seven stages may not occur in the same order in every attack.
- Cloud-based attacks, credential misuse, and living-off-the-land activity may not fit neatly into the classic stages.
- Adversaries can repeat stages or pursue multiple targets simultaneously.
- Associating an IOC with a stage does not prove that the complete attack chain occurred.
- The model does not independently identify an adversary or establish intent.

For these reasons, analysts should use the model alongside logs, incident timelines, technical observations, and other intelligence sources.

## Quick Exercise

Match the following observations to the most appropriate Cyber Kill Chain stages:

1. An email containing a suspicious link is sent to an employee.
2. A compromised endpoint establishes outbound connections at regular intervals.
3. An attacker attempts to transfer sensitive files outside the organization.
4. A suspicious persistence mechanism appears on an endpoint.

**Answers:** 1. Delivery; 2. Command and Control; 3. Actions on Objectives; 4. Installation.

## Conclusion

The Cyber Kill Chain helps CTI analysts ask three important questions systematically:

- At which stage is the adversary operating, and what evidence supports that assessment?
- Which activities might have been detected earlier?
- Which defensive controls could have interrupted the attack?

The goal is not just to memorize the stages. It is to organize incident findings within a meaningful framework and support evidence-based defensive decisions.
