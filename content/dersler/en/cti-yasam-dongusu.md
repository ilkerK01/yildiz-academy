---
lang: en
slug: cti-yasam-dongusu
title: The CTI Lifecycle
summary: The core process threat intelligence goes through, from defining requirements to feedback.
---

# The CTI Lifecycle

## Lesson Goal

This lesson explains that cyber threat intelligence is not just about
collecting data or building IOC lists. It covers how CTI work is a systematic
process that starts with a specific need and continues through collecting,
processing and analyzing information, delivering it to the right people and
receiving feedback.

## Key Concepts

- Planning and Direction
- Collection
- Processing
- Analysis
- Dissemination
- Feedback
- Intelligence Requirement
- PIR (Priority Intelligence Requirement)
- Intelligence consumer

## What Is the CTI Lifecycle?

The CTI lifecycle is the series of stages followed to turn raw data into threat
intelligence that can be used for decision-making.

Although the process looks linear, in practice it repeats continuously. New
questions that come out of one analysis can lead to new collection needs.

In general, the process can be shown like this:

`Planning → Collection → Processing → Analysis → Dissemination → Feedback`

The goal is not to collect as much data as possible, but to produce
intelligence that answers the right question.

## 1. Planning and Direction

The first stage determines which questions need to be answered.

Example questions for an organization might be:

- Which threat actors target our sector?
- Which ransomware groups are active in our region?
- Which threats are associated with the technologies our organization uses?
- What risk does a specific campaign pose to our organization?

This stage should also determine who will use the intelligence.

The SOC team may care about technical IOCs, while executives may want to know
the business impact and risk level of an attack.

## Intelligence Requirement

An intelligence requirement defines which question the analyst needs to
answer.

Priority, critical questions are usually expressed as **Priority Intelligence
Requirements (PIRs)**.

For example:

> Which active threat groups target the financial sector and use phishing?

This question sets the direction of the collection and analysis process.

A large amount of data collected without a specific requirement does not
automatically amount to intelligence.

## 2. Collection

At this stage, the data needed to answer the defined questions is collected.

Sources can include:

- Open sources
- Security vendor reports
- IOC sharing platforms
- Malware analysis services
- Internal logs
- SIEM records
- EDR data
- CERT and government publications
- Dark web or threat actor sources

Sources should be chosen according to the research question.

Researching the history of an IP address and researching the target sectors of
a specific threat actor may not require the same data sources.

## 3. Processing

Collected data is often not ready for direct analysis.

In the processing stage, raw data is organized and made suitable for analysis.

These tasks can include:

- Removing duplicate records
- Normalizing IOCs
- Standardizing date and time information
- Converting file formats
- Classifying data
- Filtering out irrelevant records
- Bringing data from different sources into a common structure

For example, IP addresses and domain records obtained from different sources
can be merged into a single working table.

## 4. Analysis

The analysis stage is one of the most important parts of the CTI process.

Here, processed data is evaluated to produce meaningful conclusions.

The analyst might look for answers to questions such as:

- Do different IOCs belong to the same infrastructure?
- Are there shared TTPs between two campaigns?
- Is a specific threat actor actually relevant to the organization?
- Could the observed activity be linked to a previously known campaign?
- How reliable are the sources?

Analysis is not just putting data side by side. The relationships between the
data and their context have to be evaluated.

## The Difference Between Data and Intelligence

Finding an IP address on its own is data.

Determining that this IP was recently associated with the C2 infrastructure of
a specific malware family is information.

Assessing that the same infrastructure is being used in an active campaign
targeting the organization's sector can turn into intelligence that supports a
decision.

That is why context is critical in the analysis stage.

## 5. Dissemination

The intelligence produced must reach the right person, in the right format, at
the right time.

The same analysis can be presented differently to different consumers.

For the SOC team, for example:

- IP addresses
- Domains
- Hash values
- YARA or Sigma rules
- MITRE ATT&CK techniques

may be important.

For management, on the other hand:

- Why the threat matters to the organization
- The targeted sector
- Possible business impact
- Risk level
- Recommended actions

are more meaningful.

A good intelligence report should be shaped around the needs of its audience.

## 6. Feedback

The last stage of the lifecycle is feedback.

Consumers of the intelligence can be asked questions such as:

- Did the information meet the need?
- Is more technical detail needed?
- Did the analysis arrive in time?
- Did a new research question come up?
- Which topics need to be tracked regularly?

This feedback shapes the planning stage of the next CTI cycle.

That is why the CTI lifecycle is not a process that ends, but one that keeps
improving.

## An Example CTI Cycle

Imagine a financial institution that wants to produce threat intelligence
about phishing campaigns.

**Planning:** Active phishing groups targeting the financial sector will be
researched.

**Collection:** Security reports, phishing IOCs, email samples and threat
actor records will be collected.

**Processing:** Domain, IP, URL and date information will be organized and
duplicate records removed.

**Analysis:** Shared infrastructure, TTPs used and threat actor relationships
will be examined.

**Dissemination:** Technical IOCs will go to the SOC team; risk and target
profile will go to management.

**Feedback:** The research will be redirected based on the SOC team's new
findings and needs.

## Conclusion

The CTI lifecycle turns threat data systematically into intelligence that
supports decisions.

The starting point of successful CTI work is not a tool or a data source, but
the right question to answer.

In general, the process follows this relationship:

`Requirement → Data → Analysis → Intelligence → Decision → Feedback`

This approach moves CTI work beyond simply collecting IOCs and makes it serve
the organization's real security needs.
