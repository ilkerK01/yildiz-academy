---
lang: en
slug: mitre-attack-cti
title: Using MITRE ATT&CK for CTI
summary: Mapping threat behavior to MITRE ATT&CK techniques and using it in CTI analysis.
---

# Using MITRE ATT&CK for CTI

## Lesson Goal

This lesson explains how the MITRE ATT&CK knowledge base is used in CTI
analysis. It covers classifying threat actor behavior through tactics,
techniques and procedures, and evaluating behavioral relationships between
different campaigns.

## Key Concepts

- MITRE ATT&CK
- Tactic
- Technique
- Sub-technique
- TTP
- Threat actor
- Campaign
- Behavioral correlation

## What Is MITRE ATT&CK?

MITRE ATT&CK is a knowledge base that classifies the tactics, techniques and
procedures threat actors use in real operations.

In CTI analysis, ATT&CK is used to evaluate the behavioral characteristics of
different attacks and threat actors through a shared vocabulary.

## Tactics and Techniques

A **tactic** is the attacker's overall goal; a **technique** is the method used
to reach that goal.

Initial Access, Execution, Persistence, Credential Access, Discovery, Command
and Control and Exfiltration are common examples of tactics.

## The TTP Concept

TTP stands for **Tactics, Techniques and Procedures**.

IOCs can be changed in a short time. Operational methods and behavior patterns,
on the other hand, tend to persist much longer. That is why TTPs are an
important source of data for threat actor and campaign analysis.

## The Difference Between IOCs and TTPs

An IP address or a hash value is a technical indicator tied to a specific
incident. A TTP describes the behavior the attacker used.

IOC and TTP data are not alternatives to each other; they complement each
other.

## ATT&CK Technique IDs

MITRE ATT&CK techniques are identified as `Txxxx`, and sub-techniques as
`Txxxx.xxx`.

These IDs make it possible to compare attack behavior described in different
sources against a shared reference system.

## Use in Threat Actor Analysis

Seeing similar TTPs across a threat actor's different operations can be
valuable for attribution. However, a single shared technique does not prove
that two incidents were carried out by the same actor.

ATT&CK mappings should therefore be evaluated together with IOCs,
infrastructure relationships, malware similarities and other CTI findings.

## Using ATT&CK in CTI Reports

During analysis, the general process is:

1. Identify the observed behavior.
2. Determine the relevant tactic.
3. Map the technique and, if applicable, the sub-technique.
4. Examine actors and campaigns that use the same techniques.
5. Evaluate the result together with other CTI findings.

## Conclusion

MITRE ATT&CK is not a tool that automatically identifies threat actors. Its
core value is helping classify attacker behavior systematically and supporting
behavioral correlation between different incidents.

## Related Lab

**Unravel the SolarWinds Chain**  
An advanced CTI lab that starts from a single IOC and traces the links between
SUNBURST, SolarWinds Orion, a MITRE ATT&CK technique, NOBELIUM, APT29 and the
related campaign.
