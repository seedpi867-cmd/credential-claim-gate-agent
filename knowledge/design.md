# Design: Credential Claim Gate

The first slice is deliberately deterministic.

The gate does not try to decide whether medical, legal, therapy, accounting, tax, or investment statements are correct. Correctness is a later and harder problem. This agent only asks whether generated text has crossed a custody boundary by claiming regulated authority.

The important split:

- discussion of a regulated domain is allowed;
- referral to a professional is a warning;
- limitation language is a warning;
- claiming licensed identity, professional relationship, diagnosis, prescription, legal representation, tax/accounting certification, or personalized investment authority is blocked.

This is the same pattern as stale CI expiry and loop-shrink promotion gates: the problem is not just content. It is authority custody. A sentence can be syntactically normal and still be an invalid actor claim.

Next work:

- quote-aware scanning so quoted examples do not automatically block;
- jurisdiction-specific title fixtures;
- stronger separation between personal finance education and investment directives;
- integration point for scanning blog drafts before deploy.
