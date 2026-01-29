# 📘 ExamWise  
### LLM-Powered Exam Analytics & Intelligent Question Analysis System  
*Focused on MAKAUT University Exams*

---

## 🚀 What is ExamWise?

**ExamWise** is an **end-to-end exam analytics and intelligent question analysis system** that transforms **previous year question papers (PYQs)** and **official syllabus data** into **actionable exam intelligence** using **data engineering, NLP, and LLM-based reasoning**.

It helps answer questions like:
- Which topics are most frequently asked?
- Which units are high-yield vs low-yield?
- How exam patterns change across years?
- Can an AI answer questions strictly from syllabus + PYQs without hallucinating?

---

## 🎯 Problem Statement (Non-Technical View)

Traditional exam preparation:
- Is intuition-based
- Lacks data-backed prioritization
- Treats all topics equally

**ExamWise converts raw exam papers into structured, measurable insights**, enabling smarter preparation and analysis.

---

## 🧠 What the System Does

### 1️⃣ Data Ingestion & Normalization
- Ingests raw PYQs (multi-year)
- Cleans formatting noise and inconsistencies
- Normalizes questions into a unified schema
- Merges year-wise data into a single dataset

---

### 2️⃣ Syllabus Intelligence
- Parses official syllabus documents
- Builds a **topic → unit index**
- Uses a rich **alias map**  
  (e.g., `CRC` ↔ `Cyclic Redundancy Check`)

---

### 3️⃣ Automated Unit & Topic Mapping
- Backfills missing unit information using:
  - syllabus topic index
  - alias-based semantic matching
  - strict word-boundary detection
- Avoids false positives and over-tagging

---

### 4️⃣ Exam Analytics Engine
- Computes:
  - topic-wise question frequency
  - unit-wise question distribution
  - weighted importance based on exam groups (A/B/C)
- Classifies topics as **High / Medium / Low Yield**
- Stores analytics in **DuckDB** for fast querying

---

### 5️⃣ Intelligent Question Answering (RAG)
- Builds a **vector store** over:
  - syllabus
  - notes
  - PYQs
- Uses **Retrieval-Augmented Generation (RAG)**
- Answers questions **only when grounded in retrieved context**
- Designed to **prevent hallucinations**

---

## 🏗️ High-Level Architecture
<img width="357" height="429" alt="image" src="https://github.com/user-attachments/assets/f79931a7-10b3-40a5-9d7d-c6217f6faa57" />





