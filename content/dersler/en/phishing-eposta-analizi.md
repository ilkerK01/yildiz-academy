---
lang: en
slug: phishing-eposta-analizi
title: CTI Analysis of Phishing Emails
summary: Examining header fields in suspicious emails and extracting technical IOCs.
---

# CTI Analysis of Phishing Emails

## Lesson Goal

This lesson explains how to examine phishing emails from a CTI perspective and
how to extract technical indicators from email headers. It covers how an
incident can be placed in a broader threat context through the sending
infrastructure, email authentication mechanisms and the technical traces inside
the message.

## Key Concepts

- Phishing
- Email header analysis
- Received
- Return-Path
- Reply-To
- SPF
- DKIM
- DMARC
- Email-based IOCs

## Phishing and CTI

Besides being a social engineering tool, phishing emails can contain technical
indicators that matter for CTI analysis. Email headers, sending infrastructure,
authentication results and the links inside the message can reveal the source
and method of the attack.

## The Displayed Sender

The `From` field of an email contains the sender information shown to the
user. On its own, however, this field is not a reliable verification mechanism.

That is why the `Received`, `Return-Path`, `Reply-To`, `Message-ID` and
`Authentication-Results` fields should be examined together.

## The Received Field

`Received` lines show which servers relayed the email. The IP addresses found
here count as IOCs worth researching.

Because an email can contain several `Received` lines, the delivery chain must
be analyzed carefully.

## Return-Path and Reply-To

`Return-Path` shows where undeliverable messages are sent back to; `Reply-To`
shows where the message goes if the user replies.

These fields differing from the displayed sender address is an indicator that
deserves a closer look. On its own, however, it should not be treated as proof
of malicious intent.

## SPF, DKIM and DMARC

SPF checks whether the sending IP is authorized to send email on behalf of the
domain. DKIM provides cryptographic verification of message integrity and
authorized sending. DMARC evaluates the SPF and DKIM results together with the
displayed sender domain.

Results such as `spf=fail`, `dkim=none` or `dmarc=fail` can raise the level of
suspicion.

## IOCs You Can Extract

The following indicators can be obtained from a phishing email:

- Source IP address
- Sender domain
- Return-Path domain
- Reply-To address
- URLs inside the message
- Hash values of attachments
- Suspicious subdomains

## Safe Analysis Approach

Suspicious links should not be opened directly, unknown attachments should
never be run in uncontrolled environments, and research should be carried out
through passive sources as much as possible.

## Conclusion

Phishing email analysis lets you extract technical indicators about attacker
infrastructure from a single message. Correlating those indicators helps place
the incident within a broader threat campaign.

## Related Lab

**Who Sent the Invoice?**  
A hands-on lab on examining the header fields of a suspicious email, extracting
the source IP and domain indicators, and evaluating email authentication
results.
