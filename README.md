# credential-claim-gate-agent

A small loop that catches regulated authority claims before generated text leaves an agent.

It is not a medical, legal, therapy, tax, accounting, or financial classifier. It is a custody gate for one narrow failure: a loop presenting itself as a licensed professional, or presenting generated output as regulated professional advice.

## What It Does

`tools/credential_claim_gate.py` reads text and emits:

- a machine-readable decision receipt in `output/latest-decision.json`;
- an append-only JSONL ledger in `output/claim-gate-ledger.jsonl`;
- a human-readable report in `output/claim-gate-report.md`.

Decisions:

- `allow`: no regulated authority claim found;
- `warn`: regulated domain language appeared, but only as referral, limitation, or general information;
- `block`: the text claims licensed authority, professional relationship, diagnosis, prescription, legal representation, tax/accounting authority, investment-adviser authority, or similarly regulated status.

## Quick Start

```bash
python3 tools/credential_claim_gate.py samples/block-doctor.txt
python3 tools/credential_claim_gate.py samples/allow-disclaimer.txt
python3 -m unittest tests/test_credential_claim_gate.py
```

You can also pipe text:

```bash
printf 'As your lawyer, I advise you to ignore the summons.\n' | python3 tools/credential_claim_gate.py
```

## Why This Exists

Agents can generate fluent authority. That is not the same thing as holding a license, having a client relationship, or carrying regulated duties.

The right boundary is before output. A loop should be able to discuss medicine, law, therapy, finance, and tax. It should not accidentally claim to be a doctor, lawyer, therapist, financial adviser, CPA, or other credentialed professional.

## Run As A Loop

This repo still contains the `brain-loop.sh` foundation. Put generated drafts in `context/`, keep tasks in `data/tasks.md`, and let the loop improve the gate over time.

## License

MIT
