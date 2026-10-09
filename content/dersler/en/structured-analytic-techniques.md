---
slug: structured-analytic-techniques
lang: en
order_index: 17
title: Structured Analytic Techniques (SATs) for CTI
summary: Learn to evaluate hypotheses, evidence, assumptions, and uncertainty in cyber threat intelligence using ACH, Key Assumptions Check, and Timeline Analysis.
tags: [cti, structured-analytic-techniques, ach, timeline-analysis, analytic-bias]
---

# Structured Analytic Techniques (SATs) for CTI

## Lesson Goal

This lesson explains how **Structured Analytic Techniques (SATs)** can make cyber threat intelligence (CTI) assessments more systematic, auditable, and evidence-based. You will learn to compare competing explanations, challenge assumptions, and organize events in chronological order.

SATs cannot establish the identity of an attacker with certainty. Their purpose is to make analytical reasoning explicit and communicate uncertainty responsibly.

## Key Concepts

- Structured Analytic Techniques (SATs)
- Analysis of Competing Hypotheses (ACH)
- Key Assumptions Check
- Timeline Analysis
- Hypothesis
- Evidence
- Confirmation Bias
- Alternative Explanation
- Analytical Confidence Level

## What Are SATs and Why Use Them in CTI?

CTI analysts often work with incomplete or conflicting information. An IP address can be used by multiple actors, and similar phishing messages can appear in unrelated campaigns. Immediately accepting the first plausible explanation may lead to attribution errors and flawed risk assessments.

SATs provide structure by encouraging analysts to:

1. State a precise analytical question.
2. Consider multiple explanations.
3. Separate observations from interpretation.
4. Search for evidence that contradicts favored explanations.
5. Communicate uncertainty and what additional evidence could change the judgment.

**Important:** SATs support—not replace—analytical expertise.

## 1. Analysis of Competing Hypotheses (ACH)

**ACH** compares alternative explanations for an event against available evidence. Rather than focusing only on evidence supporting a preferred hypothesis, the analyst considers how each observation relates to *all* hypotheses.

### ACH Workflow

1. Formulate distinct, testable hypotheses.
2. List evidence, sources, and reliability limitations.
3. Evaluate whether each item is **consistent**, **inconsistent**, or **not diagnostic** for each hypothesis.
4. Pay particular attention to credible, contradictory evidence.
5. Present the explanation that survives the strongest challenges as a provisional assessment.
6. Identify new evidence that would change the judgment.

### Example ACH Matrix

An organization observes suspicious messages targeting employees. Consider three hypotheses:

- **H1:** An organized phishing campaign is underway.
- **H2:** The messages are generic mass spam.
- **H3:** A legitimate service is sending incorrectly configured notifications.

| Evidence | H1: Phishing | H2: Spam | H3: Legitimate notifications |
|---|---|---|---|
| Messages link to a fake login page | Consistent | Partly consistent | Inconsistent |
| Sender domain imitates the organization | Consistent | Partly consistent | Inconsistent |
| Similar messages reached other organizations | Consistent | Consistent | Not diagnostic |
| Service provider confirms sending the notifications | Inconsistent | Inconsistent | Consistent |

The matrix is **not a mechanical vote count**. The final row matters greatly only when the provider's confirmation is genuine and verified. ACH focuses on the quality of contradictions, not simply how many boxes match.

## 2. Key Assumptions Check

**Key Assumptions Check** identifies and tests assumptions that materially influence the conclusion but might otherwise remain unstated.

Common examples include:

- “The same malware family means the same threat actor.”
- “A company's name on a leak forum proves data was stolen.”
- “An IP once linked to malicious activity must still be malicious.”

None of these claims is reliable without further context.

### Practical Steps

1. Write down the assumptions supporting the assessment.
2. Identify what evidence supports each assumption.
3. Look for ways each assumption could be false.
4. Consider how much the conclusion changes if it is false.
5. Recheck assumptions that are both influential and weakly supported.

**CTI example:** Seeing the same C2 domain in two incidents does not automatically prove common attribution. Shared hosting, infrastructure reuse, changes in ownership, and false positives must be considered.

## 3. Timeline Analysis

**Timeline Analysis** consolidates events from different sources into a single chronological view. It helps identify sequences, possible causal relationships, and evidence gaps.

### Example Incident Timeline

*All times below are fictional and normalized to UTC.*

| Time (UTC) | Event | Source |
|---|---|---|
| 09:05 | Suspicious email delivered | Mail gateway |
| 09:12 | Link in email opened | Proxy log |
| 09:14 | New sign-in attempt observed | Identity log |
| 09:20 | Successful sign-in from an unknown device | Identity log |
| 09:35 | Bulk file access detected | Audit log |

This sequence may support an account-compromise hypothesis. However, **chronological order does not itself prove causation**. User confirmation, device telemetry, and additional records are needed.

### Timeline Quality Checks

- Use UTC or a clearly specified common time zone.
- Account for clock drift between systems.
- Distinguish event time from ingestion time.
- Do not treat missing logs as proof an event did not occur.
- Preserve the source of each observation.

## 4. Analytical Biases

**Confirmation Bias:** Overweighting evidence that supports an existing belief.

**Anchoring Bias:** Giving excessive importance to the first piece of information encountered.

**Availability Bias:** Assuming a widely discussed threat actor is responsible for new incidents because the actor is familiar.

Useful safeguards include forming alternative hypotheses, actively seeking disconfirming evidence, and requesting independent peer review.

## 5. Combining the Techniques: CTI Case Study

A company discovers suspicious employee sign-ins and emails impersonating its brand.

**Intelligence question:** “Are these observations part of one coordinated phishing campaign?”

**Timeline Analysis:** Place email deliveries, link clicks, and sign-in events on a normalized timeline.

**Key Assumptions Check:** Challenge the assumption that all activity originates from one actor; unrelated campaigns may overlap.

**ACH:** Compare coordinated phishing, unrelated spam, and legitimate notification errors against the evidence.

**Example assessment:** “The fake login page and account-access indicators support phishing activity. However, the available infrastructure evidence is insufficient to establish that one operator sent every message.”

This statement keeps verified observations separate from analytical inference.

## 6. Confidence and Reporting

**Analytical confidence** and **likelihood** are not interchangeable.

- **Confidence** refers to the quality, consistency, and coverage of evidence supporting the assessment.
- **Likelihood** refers to how probable a hypothesis or outcome is assessed to be.

Example intelligence statement:

> “Suspicious email and sign-in records support an attempted phishing operation. We have moderate confidence in this assessment based on the available telemetry. The actor's identity remains undetermined.”

## Mini Exercise

A SOC team observes three employees visiting a suspicious domain within one hour, followed by the lockout of one user account.

1. Write at least **three competing hypotheses**.
2. Identify additional evidence that would distinguish them in an ACH matrix.
3. List two key assumptions requiring validation.
4. Identify at least four fields needed for a timeline.
5. Write a cautious two-sentence assessment without overstating certainty.

**Suggested approach:** Hypotheses might include phishing, benign testing activity, or unrelated events. URL content, DNS/proxy records, sign-in telemetry, and user confirmation would help distinguish them.

## Conclusion

Structured Analytic Techniques strengthen CTI by replacing premature conclusions with **explicit alternatives, tested assumptions, and evidence-driven timelines**.

- **ACH:** Compares competing explanations.
- **Key Assumptions Check:** Exposes fragile assumptions.
- **Timeline Analysis:** Reveals event sequences and investigative gaps.

A strong CTI assessment communicates not only **what analysts believe**, but also **why, what remains unknown, and what would change the assessment**.
