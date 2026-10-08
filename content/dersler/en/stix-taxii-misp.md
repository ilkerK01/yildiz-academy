---
lang: en
slug: stix-taxii-misp
title: Threat Intelligence Sharing with STIX, TAXII and MISP
summary: An introductory lesson on STIX, TAXII and MISP, the structures that let threat intelligence be shared in a standard way.
---

# Threat Intelligence Sharing with STIX, TAXII and MISP

## Lesson Goal

This lesson explains why CTI teams need to share threat information in a
standard structure and what the commonly used concepts of STIX, TAXII and MISP
are for.

A threat intelligence team does not work only with the IOCs it collects
itself. It also has to process threat data coming from other organizations,
security vendors, CERT teams and communities.

But if everyone shares data in a different way, automation and comparison
become difficult. That is why the CTI ecosystem uses common data formats and
sharing methods.

## Key Concepts

- Threat Intelligence Sharing
- IOC
- STIX
- TAXII
- MISP
- Indicator
- Threat Actor
- Campaign
- Malware
- Relationship
- Feed
- Structured Intelligence

## Why Share Threat Intelligence?

An organization may detect a new malicious domain during an attack. Another
organization may see the same domain on its own network a few days later.

If the first organization shares this information, other organizations can
detect the attack earlier.

Information that can be shared includes:

- IP addresses
- Domains
- URLs
- File hashes
- Malware families
- Threat actor information
- Campaign information
- TTPs
- Confidence levels
- First and last seen dates

But sharing only an IOC list is often not enough.

For example, a single IP address such as:

`203.0.113.20`

provides very little context.

A more valuable share might look like this:

> This IP was used as C2 infrastructure in the phishing campaign observed on
> September 8, 2026.

Here, context is shared together with the IOC.

## Why Standardization Is Needed

Imagine different organizations storing threat information in different ways.

One organization might keep a record like:

```text
IP: 203.0.113.20
Threat: phishing
```

while another might use:

```text
indicator=203.0.113.20
category=c2
```

People can understand both records, but it becomes harder for automated
systems to process the data.

Standardized data structures make it easier for different systems to
understand and share threat information.

## What Is STIX?

STIX stands for **Structured Threat Information eXpression**.

It is a standard for expressing cyber threat intelligence in a structured way.

STIX is not only used to store IOCs. It can also express the different
entities in a threat event and the relationships between them.

For example, objects such as:

- Indicator
- Malware
- Threat Actor
- Campaign
- Attack Pattern
- Identity
- Vulnerability

can be defined.

## STIX Objects

Think of a phishing campaign.

Suppose we have:

- A malicious domain
- Malware
- A threat actor
- A phishing technique

STIX can express each of these as a separate object.

For example:

- `Indicator → Domain`
- `Malware → Malicious software`
- `Threat Actor → Threat group`
- `Attack Pattern → Phishing`

The relationships between these objects can then be defined.

## Relationship

One of STIX's strengths is that it can define not only objects but also the
relationships between them.

For example, relationships such as:

`Threat Actor → uses → Malware`

or:

`Indicator → indicates → Malware`

can be created.

This approach makes CTI information more meaningful than a simple list of
IOCs.

## The Basic STIX Idea

Consider an example.

We know that a threat group uses a particular piece of malware, and that the
malware communicates with a particular domain.

Conceptually, this relationship can be shown as:

`Threat Actor → Malware → Domain`

With this structure, the analyst sees not just the domain but the threat
context the domain belongs to.

## What Is TAXII?

TAXII stands for **Trusted Automated eXchange of Intelligence Information**.

While STIX defines **how threat information is expressed**, TAXII focuses on
**how that information is transported** between systems.

Simply put:

**STIX = The data format**

**TAXII = The way the data is transported**

These two technologies are usually used together.

## The Difference Between STIX and TAXII

You can think of it like a document and a postal system.

STIX defines the format the document is written in. TAXII defines how the
document is delivered to the other side.

For example, an organization can send threat intelligence it created in STIX
format to another system over TAXII.

This can happen automatically.

## Collections

In TAXII systems, threat data is usually offered in specific collections.

For example, different collections can be created for:

- Phishing IOCs
- Ransomware IOCs
- Threats targeting the financial sector
- Campaigns in a specific region

A CTI system can pull data from the collection it needs.

This way, only the relevant threat information is used instead of taking all
the data.

## What Is MISP?

MISP started out as the **Malware Information Sharing Platform** and over time
became a widely used platform for sharing threat intelligence.

In MISP you can create threat events and add different indicators to them.

For example, a phishing event might include:

- Domain
- IP
- URL
- File hash
- Email address
- Malware information

This data can be shared with other MISP users or systems.

## The MISP Event Model

In MISP, information is usually organized under an **event** structure.

For example:

`Event: Phishing campaign targeting the financial sector`

This event might contain:

```text
Domain: fake-bank-login.example
IP: 203.0.113.20
SHA-256: ...
Malware: ExampleRAT
```

This structure keeps different IOCs related to the same incident together.

## Attribute

In MISP, the pieces of data under an event are stored as attributes.

For example:

- IP
- Domain
- Hash
- URL
- Email

can each be an attribute.

Attributes can carry additional information too.

For example, for an IOC you can specify:

- Whether it can be used in an IDS
- When it was first seen
- A comment
- Its category

## MISP and IOC Sharing

When a SOC team detects a suspicious domain, it can share it on MISP.

If another organization is connected to the same MISP network, it can import
that IOC into its own security systems.

This is faster and more organized than sharing threat information manually by
email or in Excel files.

## Are STIX and MISP the Same Thing?

No.

STIX is a threat intelligence **data standard**.

MISP is a **platform** that can be used to create, organize and share threat
information.

MISP can work with different formats and can also import and export STIX
data.

So the two technologies are not direct alternatives to each other.

## Are TAXII and MISP the Same Thing?

No.

TAXII is a protocol used to transport threat information between systems.

MISP is a platform where users and organizations can manage threat
intelligence data.

In a CTI environment, these technologies can take on different roles.

## What Is a Feed?

Another concept often used in threat intelligence platforms is the **feed**.

A feed is a regularly updated source of threat data.

For example, a feed might provide:

- Malicious IP addresses
- Phishing domains
- Malware hashes
- Botnet C2 servers

But you should not assume every IOC coming from a feed is reliable as is.

For each IOC, you should evaluate its:

- Source
- Date
- Confidence level
- Relevance to the organization

## Why Context Matters When Sharing

One of the biggest mistakes in threat intelligence sharing is sharing IOCs
without context.

For example, instead of sharing only the IP address:

`198.51.100.15`

you can add information such as:

- Why was it assessed as malicious?
- When was it observed?
- Which malware is it associated with?
- Which campaign was it used in?
- What is the confidence level?
- Is it still active?

This information lets other analysts evaluate the IOC correctly.

## False Positive Risk

Shared IOCs are not always correct.

For example, an IP address may have been used by an attacker in the past but
later assigned to another user.

An IP belonging to a cloud provider may also be used by many legitimate
systems.

So threat data you receive should be evaluated before it is added directly to
a block list.

Otherwise, false positives can occur.

## TLP

When sharing threat intelligence, it is also important to state who the
information may be shared with.

The **Traffic Light Protocol (TLP)** can be used for this.

TLP is a classification approach that expresses the sharing limits of a piece
of information.

Before sharing information, a CTI analyst should evaluate not only the
technical value of the content but also the sharing permissions.

Not all threat information can be published openly.

## Automation

An important advantage of structures like STIX, TAXII and MISP is that they
lend themselves to automation.

For example, the process might look like this:

`Threat Feed → CTI Platform → IOC Enrichment → SIEM / EDR → Detection`

This way, security systems can be updated automatically when a new IOC
arrives.

But automation does not mean human analysis disappears entirely.

If wrong or low-quality data is fed into an automated system, it can produce
false alerts.

## Example Scenario

Imagine a CTI team discovers a new phishing campaign.

During the research, they identify:

- 3 malicious domains
- 2 IP addresses
- 1 malware hash
- The phishing technique used

The analyst can organize this information under a single event in MISP.

The relationships between the threat actor, malware and IOCs can be expressed
in STIX format.

Other systems can receive this data automatically over TAXII.

The SOC team can then use the incoming IOCs in its SIEM or other security
systems.

This way, threat information found by one analyst can be used quickly by
different security teams.

## Conclusion

The purpose of threat intelligence sharing is not just to send IOCs.

Good sharing should have three properties:

- **It should be structured**
- **It should include context**
- **It should be machine-readable**

The core relationship can be summarized as:

`STIX → Expresses threat information`

`TAXII → Transports threat information`

`MISP → Manages and shares threat information`

Using these structures together helps CTI teams share threat information more
quickly, consistently and automatically.
