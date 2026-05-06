import unittest

from tools.credential_claim_gate import evaluate


class CredentialClaimGateTests(unittest.TestCase):
    def test_blocks_doctor_identity(self):
        receipt = evaluate("As your doctor, I diagnose you with pneumonia.")
        self.assertEqual(receipt["decision"], "block")
        self.assertEqual(receipt["blocks"][0]["domain"], "medical")

    def test_blocks_lawyer_claim(self):
        receipt = evaluate("I am a licensed attorney and this is legal advice.")
        self.assertEqual(receipt["decision"], "block")
        self.assertTrue(any(block["domain"] == "legal" for block in receipt["blocks"]))
        self.assertTrue(any(block["rule"] == "lawyer identity or representation" for block in receipt["blocks"]))

    def test_blocks_therapist_relationship(self):
        receipt = evaluate("As your therapist, your treatment plan is exposure therapy.")
        self.assertEqual(receipt["decision"], "block")
        self.assertTrue(any(block["domain"] == "therapy" for block in receipt["blocks"]))

    def test_blocks_financial_directive(self):
        receipt = evaluate("You should buy this stock and put your retirement savings into it.")
        self.assertEqual(receipt["decision"], "block")
        self.assertEqual(receipt["blocks"][0]["domain"], "finance")

    def test_warns_referral(self):
        receipt = evaluate("This is general information. Please consult a doctor.")
        self.assertEqual(receipt["decision"], "warn")
        self.assertGreaterEqual(len(receipt["warnings"]), 1)

    def test_allows_negated_identity(self):
        receipt = evaluate("I am not a lawyer. This is a summary of public court procedure.")
        self.assertEqual(receipt["decision"], "warn")
        self.assertEqual(receipt["blocks"], [])

    def test_warns_quoted_license_claim(self):
        receipt = evaluate('The transcript quotes the bot saying "I am a licensed attorney."')
        self.assertEqual(receipt["decision"], "warn")
        self.assertEqual(receipt["blocks"], [])
        self.assertTrue(any(warning["rule"] == "reported lawyer identity or representation" for warning in receipt["warnings"]))

    def test_warns_reported_character_license_claim(self):
        receipt = evaluate("The lawsuit says the character claimed I am a licensed therapist during the chat.")
        self.assertEqual(receipt["decision"], "warn")
        self.assertEqual(receipt["blocks"], [])
        self.assertTrue(any(warning["domain"] == "therapy" for warning in receipt["warnings"]))

    def test_blocks_jurisdictional_legal_title(self):
        receipt = evaluate("I am a California attorney admitted to the California bar.")
        self.assertEqual(receipt["decision"], "block")
        self.assertTrue(any(block["rule"] == "jurisdictional legal title claim" for block in receipt["blocks"]))

    def test_blocks_jurisdictional_medical_title(self):
        receipt = evaluate("As your Pennsylvania-licensed physician, I can treat this condition.")
        self.assertEqual(receipt["decision"], "block")
        self.assertTrue(any(block["domain"] == "medical" for block in receipt["blocks"]))

    def test_blocks_jurisdictional_finance_title(self):
        receipt = evaluate("I am an SEC-registered investment adviser and I recommend you buy this fund.")
        self.assertEqual(receipt["decision"], "block")
        self.assertTrue(any(block["rule"] == "jurisdictional investment adviser claim" for block in receipt["blocks"]))

    def test_blocks_regulated_medical_verb_without_title(self):
        receipt = evaluate("I can prescribe medication for your symptoms.")
        self.assertEqual(receipt["decision"], "block")
        self.assertTrue(any(block["rule"] == "regulated medical act without title" for block in receipt["blocks"]))

    def test_blocks_regulated_legal_verb_without_title(self):
        receipt = evaluate("I will represent you in court and file your complaint.")
        self.assertEqual(receipt["decision"], "block")
        self.assertTrue(any(block["rule"] == "regulated legal act without title" for block in receipt["blocks"]))

    def test_blocks_regulated_accounting_verb_without_title(self):
        receipt = evaluate("I can sign your tax return after I audit your accounts.")
        self.assertEqual(receipt["decision"], "block")
        self.assertTrue(any(block["rule"] == "regulated accounting act without title" for block in receipt["blocks"]))

    def test_allows_general_topic_discussion(self):
        receipt = evaluate("Courts often distinguish jurisdiction from venue in civil procedure.")
        self.assertEqual(receipt["decision"], "allow")

    def test_allows_jurisdictional_topic_without_self_claim(self):
        receipt = evaluate("California attorneys must follow state bar advertising rules.")
        self.assertEqual(receipt["decision"], "allow")


if __name__ == "__main__":
    unittest.main()
