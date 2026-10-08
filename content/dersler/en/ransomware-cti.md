---
lang: en
slug: ransomware-cti
title: CTI in Ransomware Incidents
summary: Correlating the threat actor, infrastructure, campaign and victim profile in ransomware cases.
---

# CTI in Ransomware Incidents

## Lesson Goal

This lesson explains how ransomware incidents are analyzed within CTI. It
focuses on evaluating the ransomware family, threat actor, infrastructure used,
victim profile, TTPs and campaign relationships together.

## Key Concepts

- Ransomware
- Ransomware-as-a-Service (RaaS)
- Affiliate
- Leak site
- Double extortion
- Threat actor
- TTP
- Campaign correlation

## The Ransomware Ecosystem

CTI analysis of ransomware incidents is not limited to naming the malware that
was used. The group behind the attack, the infrastructure used, the targeted
sectors, operational methods and campaign links must all be evaluated together.

Modern ransomware operations can involve different roles, such as malware
developers, infrastructure providers, initial access brokers, affiliates and
the people running the negotiation infrastructure.

Because of this structure, directly matching a ransomware family to a single
attacker group is not always correct.

## Ransomware-as-a-Service

In the **Ransomware-as-a-Service (RaaS)** model, developers or operators
provide the ransomware infrastructure. Associated actors called affiliates gain
access to the target systems and carry out the attack.

This model can lead to the same ransomware family being used by different
actors, which makes threat actor attribution more complex.

## Leak Sites

Some ransomware groups practice double extortion by threatening to publish
stolen data. These sites can contain information about the victim
organization, publication date, sector, country and the group claiming the
attack.

Attackers' own publications should not be accepted as fact without independent
verification.

## Key Information to Research

The following elements can be examined in a ransomware case:

- Ransomware family
- Group or operator name
- First seen date
- Targeted sectors and countries
- TTPs used
- Related IPs and domains
- Ransom notes
- Leak site entries
- Known campaigns
- Official government statements

## Source Verification

CISA and FBI advisories, MITRE ATT&CK, security vendor research reports and
ransomware tracking services should be evaluated together.

It is especially important not to rely on a single source for threat actor
attribution.

## Assessing Attribution

In CTI reports, threat actor attribution should always come with a confidence
level. Phrases such as "associated with", "assessed with high confidence" or
"similar TTPs were observed" reflect the strength of the available evidence
more accurately.

## Conclusion

Ransomware CTI analysis generally aims to reveal this chain of relationships:

`Incident → Malware → Group → Infrastructure → TTP → Campaign → Victim profile`

This approach places a single incident within a broader threat context.

## Related Lab

**Attack on the Pipeline**  
A case-based CTI lab that uses the Colonial Pipeline incident to research the
ransomware family, the RaaS model, threat actor attribution and the impact on
critical infrastructure.
