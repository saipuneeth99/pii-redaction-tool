# PII Redaction Evaluation Report

This document outlines the mathematical framework used to benchmark the performance of the Presidio Vault engine against a human-annotated ground-truth dataset.

## Mathematical Approach

The engine computes three primary Key Performance Indicators (KPIs) based on the overlap between the engine's detections and the ground truth annotations. 

We classify every character in the document as either belonging to a PII entity or not. 
* **True Positive (TP):** A character correctly flagged as PII by the engine.
* **False Positive (FP):** A character incorrectly flagged as PII by the engine (Over-redaction).
* **False Negative (FN):** A character that is actually PII but was missed by the engine (Data Leak).
* **True Negative (TN):** A normal text character correctly left alone by the engine.

### 1. Recall (Sensitivity)
**Formula:** `TP / (TP + FN)`
**Explanation:** Of all the actual sensitive data in the document, what percentage did the model successfully catch? In enterprise security, **Recall is the most critical metric** because a low recall indicates data leaks.

### 2. Precision
**Formula:** `TP / (TP + FP)`
**Explanation:** Of everything the model flagged as sensitive, what percentage was actually sensitive? Due to our strict "Zero-Leak" engineering policy, our engine casts a wide net, meaning False Positives are occasionally expected. Therefore, Precision may mathematically dip in favor of maintaining near-perfect Recall.

### 3. Accuracy
**Formula:** `(TP + TN) / (TP + TN + FP + FN)`
**Explanation:** The overall percentage of correct classification decisions made by the engine across the entire document. Because TN (normal text) vastly outnumbers PII in a typical document, this metric is highly robust but can mask isolated PII failures.

---

## Final Performance Metrics

*The following values represent the engine's benchmarked performance against the provided sample dataset.*

* **Recall:** [RECALL_VALUE]%
* **Precision:** [PRECISION_VALUE]%
* **Accuracy:** [ACCURACY_VALUE]%
