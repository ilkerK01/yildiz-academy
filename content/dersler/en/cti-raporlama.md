---
lang: en
slug: cti-raporlama
order_index: 13
title: CTI Reporting and Intelligence Products
summary: Learn to turn threat intelligence findings into evidence-based, audience-specific reports that support actionable decisions.
tags: [cti, reporting, intelligence-products, tlp, analysis]
---

# CTI Reporting and Intelligence Products

## Lesson Goal

This lesson explains how CTI findings become useful intelligence products. A good report does not merely list indicators of compromise (IOCs) or an incident timeline. It explains **what matters, which evidence supports the assessment, what remains uncertain, and what the recipient should do next**.

## Key Concepts

- Intelligence Product
- Intelligence Requirement / PIR
- Tactical, Operational, Strategic Intelligence
- Executive Summary
- Key Judgment
- Confidence Level
- Source Reliability
- Indicator of Compromise (IOC)
- MITRE ATT&CK TTP
- Traffic Light Protocol (TLP)
- Dissemination and Feedback

## 1. What Is an Intelligence Product?

An **intelligence product** is an analyzed output intended to answer a specific intelligence requirement for a defined audience. Unlike raw data, it provides **interpretation, context, and decision support**.

A bare list containing `203.0.113.42` is of limited use. The finding becomes actionable when an analyst adds evidence of a campaign association, observation dates, confidence, and systems to investigate. This address is reserved for documentation and is not a real threat indicator.

The first question should always be: **Who will read this product, and what decision are they trying to make?**

## 2. Products for Different Audiences

| Product type | Audience | Contents and purpose |
| --- | --- | --- |
| Tactical Intelligence | SOC, Detection Engineering | IOCs, TTPs, detection guidance, queries, near-term actions |
| Operational Intelligence | Incident Response, security managers | Campaign developments, adversary activity, targeting and response |
| Strategic Intelligence | Executives, risk teams | Trends, business impact, threat priorities and investment decisions |

One incident may require several products. A SOC analyst needs a practical detection lead; an executive needs to understand potential disruption and choices.

## 3. Core Report Structure

An effective CTI report can include:

1. **Title, date and scope:** What period, sector or activity was analyzed?
2. **TLP and distribution:** Who is permitted to receive the information?
3. **Executive Summary:** The most important finding and why it matters in 3–5 sentences.
4. **Key Judgments:** Main assessments grounded in evidence.
5. **Evidence & Analysis:** Sources, timeline, IOC context and TTPs.
6. **Impact & Relevance:** Why the finding matters to the organization.
7. **Recommended Actions:** Concrete steps with ownership and priorities.
8. **Limitations & Confidence:** Unknowns, conflicting evidence and confidence levels.
9. **References / Appendix:** Sources, indicator tables and detailed technical material.

Adjust the structure to the audience, but make sure the intelligence question is answered.

## 4. Executive Summary and Key Judgments

The **Executive Summary** provides the conclusion for readers who may not review the technical detail. Avoid jargon where possible and emphasize organizational relevance.

A **Key Judgment** is an analytic assessment derived from observations. For example:

> Three phishing messages reviewed over the past two weeks used similar sending infrastructure and credential-harvesting page designs. This suggests they may belong to a related activity cluster, but the evidence is insufficient to attribute them to one threat actor.

Notice the separation between **observed evidence** and **analytic inference**. Avoid unsupported certainty such as “definitely the same group.”

## 5. Confidence and Source Evaluation

Confidence expresses the analyst's assessment of the quality and consistency of supporting evidence. It is **not the same as the probability that a threat will materialize**.

- **High confidence:** Strong, consistent evidence from reliable, independent sources.
- **Moderate confidence:** Reasonable supporting evidence, with meaningful gaps.
- **Low confidence:** Limited, indirect or unverified evidence.

These terms should follow an organizational analytic standard. **Source reliability** and **information credibility** are different: a generally reliable source can still report an inaccurate claim.

State which missing evidence might alter the conclusion.

## 6. Sharing Boundaries with TLP

The **Traffic Light Protocol (TLP) 2.0**, maintained by FIRST, indicates permitted information-sharing boundaries:

- **TLP:RED:** Only the specified recipients; no further sharing.
- **TLP:AMBER:** Limited sharing within the recipient's organization and with clients who need to know to protect themselves. **TLP:AMBER+STRICT** limits sharing to the recipient organization.
- **TLP:GREEN:** Sharing within the community, but not publicly.
- **TLP:CLEAR:** No sharing restrictions.

TLP is not an information classification system or encryption method. Consult FIRST's current TLP definition for the authoritative rules.

## 7. Presenting IOCs and TTPs

Indicators should appear in a structured table:

| Indicator | Type | First/last seen | Context | Suggested action |
| --- | --- | --- | --- | --- |
| `login-check.example` | Domain | Example event date | Fictional phishing page | Review proxy/DNS logs |
| `203.0.113.42` | IPv4 | Example event date | Fictional connection | Correlate with asset records |

**Note:** All indicators above are illustrative and must not be added to real blocking lists.

Include relevant **tactics, techniques and procedures (TTPs)** alongside indicators. For instance, relate phishing, a spoofed sign-in page and account misuse to MITRE ATT&CK where supported by evidence. TTP context can remain valuable even when individual indicators change.

## 8. Writing Actionable Recommendations

Weak: “Improve organizational security.”

Better: “The SOC team should review proxy and DNS records for the past 14 days for requests to the identified domain, then investigate related endpoints for unusual authentication activity.”

A useful recommendation names an **owner, priority, scope and verification method**. Remember that one IOC alone does not prove compromise; assess the possibility of false positives.

## 9. Sample CTI Report — Fictional Phishing Campaign

**Title:** Fictional Credential-Phishing Activity Targeting a Financial Organization

**Date:** 9 October 2026

**Marking:** TLP:CLEAR — fictional training material

### Executive Summary

Three similar phishing emails were reported at a fictional financial organization during a two-week period. The messages directed users to a spoofed sign-in page. There is not enough corroborating evidence to attribute the activity to a specific threat actor. The immediate priority is to identify affected users and investigate possible credential misuse.

### Key Judgments

- Similar themes and page designs support the possibility of coordinated activity (**moderate confidence**).
- Actual credential compromise has not been verified (**low confidence**).
- Available findings do not support attribution to a named threat actor.

### Evidence

- Three sample phishing messages and email headers.
- Fictional web pages sharing a visual template.
- Training-only domain: `login-check.example`.

### Recommended Actions

1. **SOC:** Investigate access to the relevant URL/domain.
2. **Identity team:** Check suspicious sessions and MFA events for exposed accounts.
3. **Awareness team:** Publish a short advisory on similar phishing themes.
4. **CTI:** Update the campaign assessment and confidence as new evidence emerges.

### Limitations

All event data is fictional. No conclusion can be drawn about actual compromise, actor identity, or total impact.

## 10. Mini Exercise

An analyst sends executives a 50-line list of hashes and IP addresses. The report does not discuss business impact or recommended actions.

**Questions:**

1. Why is this report unsuitable for an executive audience?
2. Which three items should the Executive Summary include?
3. How would you communicate a low-confidence finding?
4. Does TLP:GREEN allow publication on social media?

**Short answer:** Executives need threat context, business impact and decision options—not just indicators. Explain why confidence is low; TLP:GREEN does not permit public publication.

## Conclusion

CTI reporting is not a competition to publish the longest indicator list. The objective is to deliver **traceable intelligence, appropriate to the audience, on time, with clearly stated uncertainty and useful decisions**. Begin with the intelligence question, support judgments with evidence, and end with concrete actions.
