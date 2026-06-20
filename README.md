# BracU Courses

A structured archive of academic materials from BRAC University, covering all courses completed across the undergraduate Computer Science and Engineering program. This repository is intended as a personal reference and study resource.

---

## Contents

| Course | Title | Level |
|--------|-------|-------|
| BIO101 | Biology | Gen Ed |
| CHE101 | Chemistry | Gen Ed |
| ECO101 | Economics | Gen Ed |
| ENV103 | Environmental Science | Gen Ed |
| HUM101 | Humanities | Gen Ed |
| PHY112 | Physics II | Gen Ed |
| STA301 | Statistics | Gen Ed |
| CSE110 | Programming Language I | Year 1 |
| CSE220 | Data Structures | Year 2 |
| CSE221 | Data Structures Lab | Year 2 |
| CSE230 | Discrete Mathematics | Year 2 |
| CSE250 | Electrical Circuits | Year 2 |
| CSE251 | Electronic Circuits | Year 2 |
| CSE260 | Digital Logic Design | Year 2 |
| CSE320 | Computer Networks | Year 3 |
| CSE321 | Operating Systems | Year 3 |
| CSE330 | Algorithms | Year 3 |
| CSE340 | Computer Architecture | Year 3 |
| CSE341 | Assembly Language | Year 3 |
| CSE350 | Software Engineering | Year 3 |
| CSE360 | Computer Graphics | Year 3 |
| CSE370 | Database Systems | Year 3 |
| CSE421 | Artificial Intelligence | Year 4 |
| CSE422 | Machine Learning | Year 4 |
| CSE423 | Computer Graphics (Advanced) | Year 4 |
| CSE443 | Data Science | Year 4 |
| CSE460 | VLSI Design | Year 4 |
| CSE470 | Web Technologies | Year 4 |
| CSE471 | Advanced Web Frameworks | Year 4 |

---

## Folder Structure

Each course folder typically contains a subset of the following:

```
COURSE_CODE/
├── Lecture Slides/
├── Lecture Notes/
├── Lab/
├── Assignment/
├── Practice Sheets/
├── Previous Questions/
├── Books/
└── Project/
```

---

## What Is and Is Not Tracked

This repository tracks academic content only: lecture slides, notes, assignments, lab sheets, practice problems, previous exam questions, textbooks, and source code written for coursework.

The following are excluded via `.gitignore`:

- `node_modules/` directories from web course projects (CSE470, CSE471). Run `npm install` inside any project folder to restore dependencies.
- Python compiled files (`__pycache__`, `.pyc`) from data science and AI courses.
- EDA tool cache files from circuit design course (CSE460), including `.cdb`, `.hdb`, and `.qmsg` files. Source schematics and symbols are kept.
- C/C++ object files from operating systems and assembly labs.
- Nested `.git` folders from lab projects that have their own repositories.
- OS-generated files (`.DS_Store`, `Thumbs.db`).

---

## Lab Projects with Separate Repositories

Some lab work exists as standalone Git repositories and is not tracked inline here. These include xv6-based OS labs (CSE321), web application projects (CSE470, CSE471), and the data science project (CSE443).

---

## Notes

- Materials are organized as collected during study; naming conventions vary across courses and semesters.
- Some older courses may have incomplete folder structures.
- All content is for personal academic reference.

---

## Author

Tahsin Raihan Robbani
BSc in Computer Science and Engineering
BRAC University