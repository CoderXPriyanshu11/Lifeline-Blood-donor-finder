# Feedback Analysis
## LifeLine Blood Donor Finder — SPPU SE AI&DS CEP

---

## 1. Collection Method

Feedback is collected via the LifeLine `/feedback` route. Users provide:
- Their role (Donor / Requester / Volunteer / Public)
- A 1–5 star rating
- An open-text message
- Optionally: name and email

All submissions are stored in the `feedback` table and are accessible to admins via `/admin/feedback`. The admin dashboard displays the average rating as a KPI card.

---

## 2. Useful SQL Queries for Analysis

```sql
-- Average rating overall
SELECT ROUND(AVG(rating), 2) AS avg_rating
FROM feedback;

-- Rating distribution
SELECT rating, COUNT(*) AS count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM feedback), 1) AS pct
FROM feedback
GROUP BY rating
ORDER BY rating DESC;

-- Average rating by role
SELECT role,
       COUNT(*) AS responses,
       ROUND(AVG(rating), 2) AS avg_rating
FROM feedback
GROUP BY role
ORDER BY avg_rating DESC;

-- Recent feedback (last 30 days)
SELECT name, role, rating, message, submitted_at
FROM feedback
WHERE submitted_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
ORDER BY submitted_at DESC;

-- Feedback with 3 stars or below (issues to address)
SELECT id, name, role, rating, message, submitted_at
FROM feedback
WHERE rating <= 3
ORDER BY rating ASC, submitted_at DESC;
```

---

## 3. Theme Tagging Framework

Open-text feedback messages are manually or programmatically tagged with one or more themes:

| Theme Tag | Keywords to Look For | Example Message |
|-----------|---------------------|-----------------|
| `ux_positive` | easy, simple, smooth, fast, great, love | "Super easy to register!" |
| `ux_negative` | confusing, slow, hard, difficult, error | "The form gave an error twice." |
| `privacy` | safe, private, masked, concern, worried | "Glad my number was masked." |
| `feature_request` | wish, add, why no, please include | "Wish there was a notification." |
| `impact` | saved, found donor, helped | "Found a donor within hours." |
| `disclaimer_effective` | understood, clear, medical | "The disclaimer made me feel informed." |
| `campaign_feedback` | camp, drive, event, location | "Camp was well-organised." |

---

## 4. Pilot Feedback Themes
*(Illustrative — from 12 pilot responses, Oct 2024)*

| Theme | # Responses | % |
|-------|-------------|---|
| UX Positive | 7 | 58 % |
| Impact (request fulfilled / donor found) | 3 | 25 % |
| Feature Request (notifications) | 2 | 17 % |
| UX Negative | 1 | 8 % |
| Privacy Positive | 4 | 33 % |

> **Note:** These are sample/illustrative figures. Actual feedback is stored in the database.

---

## 5. Sample Pilot Responses
*(Illustrative)*

| Role | Rating | Message | Theme Tag |
|------|--------|---------|-----------|
| Donor | ★★★★★ | "Super easy to register! Happy to help save lives." | ux_positive, impact |
| Requester | ★★★★☆ | "Found a matching donor within hours. Great initiative." | impact |
| Volunteer | ★★★★☆ | "The campaign page needs more details about timing." | feature_request |
| Public | ★★★☆☆ | "Would be useful to have WhatsApp contact option." | feature_request |

---

## 6. How Feedback Shaped the Platform

| Feedback Theme | Action Taken |
|----------------|-------------|
| Feature Request: notifications | Noted in future scope; deferred Phase 1 |
| UX Negative: form error confusion | Improved error box styling with specific messages |
| Privacy Positive | Reinforced masking approach; added explicit privacy note on search page |
| Campaign page lacks timing info | Camp descriptions now prompted to include timing |
| Impact stories | Used anonymised stories in Phase 3 social media posts |

---

## 7. Reporting Cadence

| Period | Action |
|--------|--------|
| Weekly (Phase 1) | Check admin feedback table for UX issues; fix immediately |
| Monthly | Run theme-tagging on new responses; update analysis doc |
| End of each campaign | Collect targeted feedback from camp attendees |
| Semester end | Compile full analysis for CEP report |
