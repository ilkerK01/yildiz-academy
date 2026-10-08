---
lang: en
slug: osint-arastirma-kaynak-dogrulama
title: OSINT Research and Source Verification
summary: How to assess source reliability, information accuracy and the traceability of your research when collecting from open sources.
---

# OSINT Research and Source Verification

## Lesson Goal

This lesson explains that in OSINT work, finding information is not enough.
What really matters for a CTI analyst is evaluating where the information came
from, confirming it with other sources and recording how the research was
done.

In OSINT research, wrong, outdated or out-of-context information can directly
affect the outcome of an analysis.

## Key Concepts

- OSINT
- Source reliability
- Information verification
- Cross-check
- Primary source
- Secondary source
- Pivoting
- Metadata
- Research trail
- Confidence Level

## What Is OSINT?

OSINT stands for **Open Source Intelligence**.

It is the process of collecting information from publicly or legally
accessible sources, evaluating it and producing meaningful conclusions.

OSINT sources are not just search engines.

In research you may come across sources such as:

- News sites
- Official government publications
- Security vendor reports
- Social media
- Domain registration records
- Certificate records
- Open code platforms such as GitHub
- Malware analysis services
- Internet archives
- Forums
- Public posts by threat actors

The main problem is not getting to information, but understanding how reliable
the information you found is.

## Start Research with a Question

Good OSINT research should not begin by reaching for tools.

First, decide which question needs to be answered.

For example, imagine we have a suspicious domain:

`secure-example-login.com`

Instead of immediately searching dozens of different services, you can first
write down research questions.

When was the domain created?

Which IP addresses is it associated with?

Has it been seen in malicious activity before?

Which other domains share infrastructure with it?

Is it linked to a known attack campaign?

Once the questions are set, it becomes much easier to see which sources to
use.

## Primary and Secondary Sources

When evaluating sources, it is important to understand where the information
originates.

A **primary source** is directly connected to the event or the data.

For example:

A security advisory published by an organization itself, or a technical
analysis of a malware sample that was examined directly, is closer to a primary
source.

A **secondary source** interprets or republishes information taken from other
sources.

For example, a security news site summarizing another company's research can
be a secondary source.

Secondary sources are not worthless, but whenever possible a critical finding
should be traced back to the original source.

## Evaluating Source Reliability

When using a source, it is not enough that it looks professional.

You can ask questions like these:

Who published the source?

Has the source provided reliable information before?

When was the information published?

Is there technical evidence behind the claim?

Do other independent sources support the same information?

Is the source sharing its own observation, or repeating another source?

For example, a forum user's message saying:

> This IP belongs to an APT group.

is not enough on its own to make an attribution.

But if the same IP is linked to the same campaign in different technical
reports, malware analyses and network records, the confidence level of the
finding can increase.

## What Is a Cross-check?

A cross-check is the process of trying to verify a piece of information by
comparing it against different sources.

For example, if a domain is claimed to be associated with a specific threat
actor, you can look for support in:

Passive DNS records,

Threat intelligence platforms,

Malware sandbox reports,

Security vendor research,

Certificate records.

There is an important detail here, though.

Five different websites showing the same information does not necessarily mean
five independent sources.

All of those sites may be pulling data from the same threat feed.

So you need to evaluate not only the number of sources, but also **whether the
sources are independent of each other**.

## Why Dates Matter

A large share of CTI data can lose value over time.

An IP address may have been used as a malicious C2 server last year, but today
the same IP may be assigned to a different system.

Similarly, a domain may have been used for phishing in the past but changed
hands later.

That is why, in research, you should distinguish between:

First seen date,

Last seen date,

Report date,

Registration date,

Observation date.

Assuming that an old IOC is still active today can lead to wrong conclusions.

## Pivoting

In OSINT and CTI research, moving from one finding to another is called
**pivoting**.

For example, research might proceed like this:

`Domain → IP → Other domains on the same IP → Certificate → Other infrastructure`

or:

`Malware hash → C2 domain → IP → Related campaign`

Pivoting expands the scope of research.

But remember that not every relationship you find is a threat relationship.

For example, two domains on the same IP does not necessarily mean both belong
to the same threat actor. Shared hosting may be in use.

Relationships found through pivoting should therefore be verified separately.

## Using Metadata

Metadata provides additional information about a piece of data.

For example, a file's metadata fields can contain:

- Creation time
- File type
- Software used
- Author information
- Language
- Geographic information

But metadata can be changed easily.

So metadata should not be treated as strong attribution evidence on its own.

Metadata can be a **starting point for research**, but it should be supported
by other sources.

## Keeping a Research Trail

It is important that a CTI analyst's research can be repeated later.

During research, it helps to record:

- The source used
- Date accessed
- The value searched
- The result obtained
- An assessment of the result's reliability
- Pivots made
- The conclusion the analyst drew

For example, you might keep an entry like:

`09.09.2026 — example.com — Passive DNS lookup — association found with IP 203.0.113.10.`

This makes it possible to understand later how the analysis was produced.

## Separating Fact from Assessment

In CTI reporting, the observed fact and the analyst's assessment must be kept
apart.

For example:

**Fact:**

The domain resolved to IP address `203.0.113.10` on September 8.

**Assessment:**

Given that this IP was previously used in the same phishing campaign, the
domain is likely associated with the campaign.

The second statement is the result of analysis.

This distinction is especially important in attribution work.

## Confidence Level

Not every CTI conclusion has the same level of certainty.

Analysts can therefore express their assessments with specific confidence
levels.

For example:

**Low confidence:** Limited or unverified evidence is available.

**Moderate confidence:** Several data points support the assessment, but
significant uncertainties remain.

**High confidence:** Multiple reliable and independent sources strongly
support the assessment.

Using confidence levels lets the analyst express the difference between "we
know this for certain" and "the available data points to this".

## Common OSINT Mistakes

One of the most common mistakes in OSINT research is accepting the first
result you find as correct.

Likewise, treating old IOCs as current, using a social media post without
independent verification, or counting different services that pull from the
same source as independent evidence can all lower the quality of an analysis.

Another mistake is treating correlation as attribution.

A technical relationship between two systems does not automatically prove that
they are run by the same threat actor.

## Example Research

Imagine an analyst has a suspicious domain:

`invoice-example.com`

Initial research shows the domain was registered recently.

A passive DNS lookup returns a specific IP address.

Other domains with similar names are found on the same IP.

A malware analysis service shows that one of these domains was used as C2 by a
malicious file.

A security vendor report also states that the same infrastructure was used in
a recent phishing campaign.

At this point the analyst can make an assessment based not on a single source
but on several findings.

Even so, rather than saying:

> This domain definitely belongs to group X.

the assessment should match the level of evidence available.

## Conclusion

The goal of OSINT research is not just to find information on the internet.

A good CTI analyst constantly asks three questions:

**Where did I get this information?**

**How reliable is it?**

**Can I verify it with another source?**

OSINT data only becomes threat intelligence once verification, context and
analysis are added.
