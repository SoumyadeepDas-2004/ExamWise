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
<img width="375" height="458" alt="image" src="https://github.com/user-attachments/assets/d88ba496-a998-49bd-a613-71319b438e56" />

---

## 🛠️ Tech Stack

### Core
- Python
- JSON-based data pipelines

### Data & Analytics
- DuckDB
- Strong schema validation

### AI / NLP
- Retrieval-Augmented Generation (RAG)
- Embedding-based semantic search
- Context-bounded LLM responses

### Vector Store
- ChromaDB

---

## 📂 Project Structure 

<img width="772" height="344" alt="image" src="https://github.com/user-attachments/assets/d2b7f224-c768-4da0-9f91-0c4c9b81e4b9" />

---

## Pipeline Architecture

```bash
User Query
   ↓
Query Classifier
(intent: analytics / conceptual / factual)
   ↓
Query Cleaning & Normalization
   ↓
Embedding Generation (MiniLM-B6)
   ↓
Semantic Similarity Search
(ChromaDB – existing vectors)
   ↓
Top-K Context Retrieval
(PYQs + syllabus + notes)
   ↓
Context Validation
(unit / subject / semester alignment)
   ↓
Prompt Builder
(context-only constraint)
   ↓
LLM Answer Generation
(RAG, no hallucination)
   ↓
Final Answer to User
```

---

## 📊 Example Outputs

- Topic-wise frequency analysis
- Unit-wise yield classification
- Cleaned and structured PYQ datasets
- Context-grounded AI-generated answers

---

## ▶️ How to Run (Developers)

### ✅ Recommended (One-Command Pipeline)

This project is designed to run as a **single end-to-end pipeline**.

```bash
python pipelines/pipeline.py
```

---

## 🧰 Tools & Technologies Used

- **Programming Language:** Python 3.11

- **Data Formats:** JSON  
  Raw PYQs, normalized datasets, syllabus index, analytics outputs

- **Embedding Model:** MiniLM-B6  
  Used exclusively for vector embedding generation (not text generation)

- **Semantic Analysis:**  
  Rule-based + embedding-assisted semantic matching using syllabus topic index and alias maps

- **Parsing & Normalization:**  
  Custom Python parsers with schema-driven normalization and regex-based word-boundary matching

- **Vector Store:** ChromaDB  
  Stores embeddings of syllabus, PYQs, and notes for semantic retrieval

- **Retrieval Method:** Retrieval-Augmented Generation (RAG)  
  LLM responses are generated strictly from retrieved context (hallucination-safe)

- **Analytics Engine:**  
  Custom Python analytics pipeline with weighted exam group scoring (A / B / C)

- **Analytical Database:** DuckDB  
  Used for fast, local analytical queries on derived exam statistics

- **Version Control:** Git & GitHub

---

## ⚠️ Current Scope & Limitations (TL;DR)

- **Currently implemented for:**  
  **MAKAUT B.Tech (CSE) – 6th Semester – Computer Networks**

- **Why limited to one subject?**  
  Cleaning, normalizing, and semantically aligning academic data (PYQs + syllabus) requires **significant manual verification and engineering effort** to ensure correctness and avoid noisy or misleading analytics.

- **Intentional design choice:**  
  The scope is intentionally constrained to **validate data quality, pipeline correctness, and analytical accuracy** before scaling.

- **Scalability roadmap:**  
  The system architecture is **subject-agnostic and modular** and is designed to scale horizontally across:
  - multiple subjects  
  - different semesters  
  - additional departments and universities  

> **TL;DR:** One subject today for correctness and depth.  
> Many subjects tomorrow without redesign.

---
