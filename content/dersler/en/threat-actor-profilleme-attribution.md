---
lang: en
slug: threat-actor-profilleme-attribution
title: Threat Actor Profiling and Attribution
summary: Profiling threat actors by behavior, infrastructure, targets and campaigns, and weighing the uncertainty in attribution work.
---

# Threat Actor Profiling and Attribution

## Lesson Goal

This lesson explains how threat actors are profiled in CTI work and why it is
hard to tie an attack to a specific group or actor.

Defining a threat actor only by the malware or IP addresses it uses is usually
not enough.

Analysts evaluate many different data points together, such as:

- TTPs
- Targeted sectors
- Infrastructure used
- Malware families
- Campaigns
- Timing
- Language and operational habits

This process is generally called **threat actor profiling**.

## Key Concepts

- Threat Actor
- Threat Group
- APT
- Campaign
- Attribution
- Alias
- TTP
- Infrastructure
- Malware
- Victimology
- Confidence Level
- False Flag

## What Is a Threat Actor?

Threat actor is a general term for a person, group or organization that
carries out cyber attacks or malicious activity.

Threat actors can have different motivations.

For example:

- Financial gain
- Espionage
- Political goals
- Hacktivism
- Sabotage
- Data theft
- Competitive advantage

So it is not correct to put all attackers in the same category.

A ransomware group and an espionage group assessed to be state-sponsored can
have very different goals and ways of working.

## The Difference Between a Threat Group and a Campaign

In CTI work, it is important not to confuse a **threat group** with a
**campaign**.

A threat group is a cluster of attackers associated with specific behavioral
characteristics and operations.

A campaign is attack activity carried out over a period of time against a
specific target or for a specific goal.

For example, the same threat group might run, at different times:

- A phishing campaign targeting financial institutions,
- Another espionage campaign targeting government agencies.

In that case the group may be the same, but the campaigns are different.

## What Is an APT?

APT stands for **Advanced Persistent Threat**.

It is generally used to describe threat actors or groups that have significant
resources, run long-term operations and focus on specific targets.

But the term APT does not always mean technically sophisticated attacks.

A group can also run effective, long-lasting operations using:

- Simple phishing techniques,
- Known vulnerabilities,
- Off-the-shelf malware tools.

What matters is the purpose, persistence and operational structure of the
attack.

## How Is a Threat Actor Profile Built?

A threat actor profile never relies on a single data point.

The analyst brings together information from different categories.

### Targets

Which sectors does the actor target?

For example:

- Finance
- Defense
- Energy
- Healthcare
- Telecommunications
- Government agencies

The geographic distribution of targets can also matter.

A group that consistently targets particular countries or regions can offer
clues about the purpose of its operations.

## Victimology

Studying the people, organizations, sectors or countries an attacker targets
is called **victimology**.

For example, if a group's past operations consistently targeted:

- Defense companies,
- Diplomatic institutions,
- Research centers,

this can provide important information about the group's motivation.

But the target profile alone is not enough for attribution.

More than one threat actor can target the same sector.

## TTP Analysis

TTP stands for **Tactics, Techniques and Procedures**.

It is used to understand how an attacker behaves during an operation.

For example, if an actor consistently:

- Uses spear phishing,
- Sends particular file types,
- Runs payloads with PowerShell,
- Performs credential dumping,
- Uses similar persistence methods,

these behaviors can be part of the actor's operational profile.

TTPs usually live longer than IOCs such as IPs or domains.

But attackers can change their techniques over time.

So a TTP match does not provide definitive attribution on its own either.

## Malware Use

A threat actor can be associated with specific malware families.

For example, the analyst might observe this relationship:

`Threat Actor → Malware → C2 Infrastructure`

But the use of a piece of malware in a specific attack does not automatically
tie the attack to the group previously associated with that malware.

Some malware families:

- Can be used by more than one group,
- Can be sold on the dark web,
- Can be open source,
- Can be copied by other groups.

So a malware link should be supported by other evidence.

## Infrastructure Analysis

The infrastructure attackers use is also an important data source for
profiling.

For example, you can examine:

- Domain registrations
- IP addresses
- Hosting providers
- DNS records
- TLS certificates
- C2 servers
- Redirect infrastructure

Infrastructure characteristics that repeat across several campaigns can help
establish relationships between threat actors.

But care is needed here too.

Using the same hosting service does not prove two attacks were carried out by
the same group.

## Timing Analysis

The hours and days on which attacker activity happens can also be used as
supporting data.

For example, operations that strongly overlap with working hours in a
particular time zone can contribute to some assessments.

But this kind of information is not direct evidence.

Attackers can:

- Work at different hours,
- Use automation,
- Deliberately create misleading timing.

So timing analysis should only be used as supporting data.

## Why Does the Same Group Have Several Names?

In the CTI world, the same or similar threat clusters can be tracked under
different names by different security companies.

For example, one company may give its own name to the activity it observes,
while another company describes the same activity cluster with a different
name.

These names are called **aliases**.

A threat actor may appear in different sources under different names such as:

`Group A`

`APT-X`

`Fancy Animal`

But different names do not always mean the companies are talking about the
same group.

Sometimes the activity clusters two companies track only partially overlap.

So alias relationships should be evaluated carefully.

## What Is Attribution?

Attribution is the attempt to determine the person, group or organization
behind an attack or campaign.

It is one of the hardest areas of analysis in CTI.

Different data points can be brought together for attribution:

- TTP similarities
- Malware use
- Infrastructure relationships
- Target profile
- Campaign history
- Operational timing
- Language characteristics
- Technical mistakes
- Previous reliable reports

But none of these pieces of evidence may give a definitive result on its own.

## Technical Attribution and Political Attribution

Technical analysis may lead to an assessment like:

> This attack shows strong similarities to activity previously associated with
> group X.

That does not mean the real person or state behind the attack has been
definitively identified.

Especially with state-sponsored actors, attribution may require not only
technical data but also information a CTI analyst may not have access to,
such as:

- Human intelligence,
- Legal information,
- Diplomatic sources,
- Classified intelligence.

That is why the language of certainty must be used carefully in technical CTI
reports.

## False Flag

Attackers can leave misleading traces to make attribution harder.

This kind of behavior can be called a **false flag**.

For example, an attacker can:

- Use another group's malware,
- Leave file names in a different language,
- Use infrastructure located in another country,
- Imitate the techniques of a known group.

The goal may be to lead the analyst to the wrong conclusion.

That is why attribution should never be made from a single piece of evidence.

## Analytic Trap: Similarity Is Not Equality

The same technique being used in two attacks does not show that they were
carried out by the same group.

For example, phishing is used by a huge number of threat actors.

Similarly:

`Same technique ≠ Same group`

`Same malware ≠ Same group`

`Same hosting provider ≠ Same group`

`Same target country ≠ Same group`

What matters for attribution is evaluating different pieces of evidence
together.

## Using Confidence Levels

Attribution results are often not definitive.

So the confidence level of the conclusion should be stated.

For example:

**Low confidence**

Evidence is limited and alternative explanations are strong.

**Moderate confidence**

Several data points support the assessment, but significant uncertainties
remain.

**High confidence**

Many independent and reliable data points support the same assessment.

For example:

> Based on similarities in TTPs, infrastructure and target profile, we assess
> with moderate confidence that the campaign is associated with actor X.

This statement is a much more sound CTI approach than:

> X definitely carried out the attack.

## An Example Threat Actor Profile

Imagine an analyst examining several different attack campaigns.

The following shared characteristics are identified:

- Targeting of the financial sector
- Initial access through spear phishing
- Similar PowerShell commands
- The same malware family
- A similar domain naming pattern
- The same hosting providers
- Shared working hours

This data may suggest a relationship between the campaigns.

But the analyst should not jump directly to the conclusion:

> The same group carried out all of these.

Instead, alternative explanations should also be considered.

For example, the malware used may also be used by other groups, or the hosting
provider may be popular with many different customers.

## Why Does a Threat Actor Profile Matter?

Threat actor profiling is not done only to find the person behind an attack.

Understanding a group's past behavior makes it easier to prepare for its
future activity.

For example, if it is known that a threat actor consistently:

- Targets specific sectors,
- Uses phishing,
- Relies heavily on particular TTPs,

defensive teams can put priority controls in place against those behaviors.

So a threat actor profile also helps shape defensive strategy.

## Conclusion

Threat actor attribution is not a name-matching exercise.

The analyst evaluates different data points together, such as:

`Target + TTP + Malware + Infrastructure + Campaign history + Time`

And the most important rule is:

**Seeing a relationship does not mean making a definitive attribution.**

A good CTI analyst states not only which conclusion they reached, but also how
confident they are in it and which alternative explanations exist.
