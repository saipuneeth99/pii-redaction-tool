# Presidio Vault: Enterprise PII Redaction Engine

## Overview
Presidio Vault is a robust, production-ready enterprise application designed to securely identify and redact Personally Identifiable Information (PII) from `.docx` files. It leverages a hybrid approach using **Microsoft Presidio** (for regex/pattern matching) and **spaCy** (for advanced Named Entity Recognition), ensuring high-fidelity redaction while strictly preserving the original document formatting.

## Architecture: Hybrid Regex & NER Approach
To maximize detection coverage across varying document structures, the engine employs a dual-layered analysis strategy:

1. **Structured Data via Regex (Presidio):** 
   Highly formatted data types such as US Social Security Numbers (SSNs), Credit Cards, IPv4/IPv6 Addresses, Emails, and Phone Numbers are caught using Microsoft Presidio's optimized regular expression patterns.
2. **Unstructured Data via NLP (spaCy `en_core_web_sm` / `en_core_web_lg`):** 
   Context-dependent entities such as Full Names (`PERSON`), Company Names (`ORGANIZATION`), and Physical Addresses (`ADDRESS`) are dynamically detected using spaCy's linguistic and contextual models.

When an entity is detected, the `ConsistentMapper` uses the `Faker` library to generate a realistic replacement (e.g., replacing "John Doe" with "Michael Smith"). This mapping is strictly 1:1 throughout the document, ensuring contextual integrity (if "John Doe" appears 5 times, it is replaced by "Michael Smith" all 5 times).

## Engineering Trade-offs
In enterprise data security, a missed PII detection (Data Leak) is vastly more damaging than accidentally redacting a generic noun. Therefore, the engine is explicitly tuned to **favor Recall over Precision**.

* **The Recall Bias:** We have lowered the confidence thresholds for ambiguous entities (like isolated phone numbers in table cells) to ensure nothing slips through.
* **The Cost:** By intentionally casting a wider net, the system will occasionally flag non-PII terms, resulting in lower mathematical Precision. We consider this an acceptable and necessary trade-off for zero-leak compliance.

### Potential False Positives (Over-redaction)
Due to our high-recall tuning, spaCy may occasionally misclassify generic business terms as Named Entities:
* **ORGANIZATION False Positives:** Terms like "Board of Directors", "Engineering Team", "QA", or legal clauses like "Section IV" may be incorrectly flagged as companies.
* **PERSON False Positives:** Nouns that resemble names or job titles in dense legal text.
* *Mitigation:* A manual `DENY_LIST` is implemented in the core engine to explicitly ignore known financial/legal false positives (e.g., "Red Herring", "Fiscal Quarter", "IT").

### Potential False Negatives (Missed Redaction)
* **Highly Obfuscated Data:** Phone numbers written entirely in words ("Five Five Five One Two Three Four").
* **Non-Standard Names:** Ultra-rare proper nouns lacking surrounding sentence context (e.g., a standalone list of names in a table with no headers).

## Getting Started
Please refer to the setup instructions provided by the terminal commands to initialize the Flask environment and boot the Vanilla JS dashboard.
