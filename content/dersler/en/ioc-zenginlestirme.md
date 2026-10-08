---
lang: en
slug: ioc-zenginlestirme
title: IOC Enrichment and Pivoting
summary: Enriching IOCs with contextual information and moving to related indicators.
---

# IOC Enrichment and Pivoting

## Lesson Goal

This lesson explains how the IOCs used in threat intelligence work should be
evaluated not as isolated indicators but within a broader threat context. Using
IOC enrichment and pivoting, it covers how to move from a single indicator to
related infrastructure, malware, campaign and threat actor information.

## Key Concepts

- IOC (Indicator of Compromise)
- IOC enrichment
- Pivoting
- ASN
- Domain and IP relationships
- File hash values
- C2 infrastructure
- Passive CTI and OSINT sources

## What Is an IOC?

An **IOC (Indicator of Compromise)** is a technical indicator of malicious or
suspicious activity. IP addresses, domain names, URLs, file hashes and email
addresses are among the most common IOC types.

In CTI work, simply detecting an IOC is not enough. You need to determine which
threat, infrastructure, malware, campaign or threat actor the indicator is
related to.

## IOC Enrichment

IOC enrichment is the process of supporting an existing indicator with
additional information gathered from different open sources.

For example, for an IP address you might research:

- The ASN it belongs to
- Geographic location
- Hosting provider
- First and last seen dates
- Records of malicious activity
- Related domain names
- Associated malware families
- Its relationship to C2 infrastructure

This information lets an IOC that means little on its own be evaluated within a
broader threat context.

## Pivoting

**Pivoting** means moving from one indicator to other, related indicators.

An example research chain:

`IP → ASN → Domain → URL → Hash → Malware`

Starting from a single indicator, this approach can uncover attacker
infrastructure, malware families and campaign relationships.

## Useful Sources

During IOC analysis you can use VirusTotal, ThreatFox, MalwareBazaar, URLhaus,
AbuseIPDB, WHOIS/RDAP services, ASN lookup services, MITRE ATT&CK and threat
research reports from security vendors.

Whenever possible, information should be confirmed by more than one independent
source.

## Passive Research Approach

Connecting directly to a suspicious IP address or domain can create unnecessary
security risk. For that reason, research should be carried out through passive
CTI and OSINT sources as much as possible.

## Evaluating IOCs in Context

An IOC appearing in a threat database is not, on its own, definitive proof of
malicious intent. Shared hosting infrastructure, old records and false
positives must be taken into account.

IOCs should therefore be evaluated together with timing, source reliability,
related indicators and threat context.

## Conclusion

IOC enrichment and pivoting are core processes of CTI analysis. The goal is not
only to decide whether an indicator is malicious, but to uncover the larger
threat structure it belongs to.

## Related Labs

**Tracing a hash**  
A hands-on lab on researching the malware family and related threat
information starting from a file hash.

**On the Trail of a Suspicious IP**  
A hands-on CTI scenario that has you pivot from an IP address to its ASN,
threat type, malware and related samples.
