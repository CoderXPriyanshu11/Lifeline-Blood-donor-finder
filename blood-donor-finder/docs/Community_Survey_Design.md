# Community Survey Design
## LifeLine Blood Donor Finder — SPPU SE AI&DS CEP

---

## 1. Purpose

The community survey was designed to:

1. Quantify existing blood donation awareness in the target population (Pune urban / peri-urban).
2. Identify the primary barriers that prevent willing residents from donating blood.
3. Gather demographic data to segment campaigns by age group and locality.
4. Measure the effectiveness of the LifeLine platform after launch (by comparing pre- and post-launch willingness scores).
5. Collect qualitative suggestions that directly inform feature prioritisation.

---

## 2. Target Respondents

| Segment | Rationale |
|---------|-----------|
| College students (18–25) | First-time donor pool; high social-media reach |
| Working adults (26–45) | Highest voluntary donation capacity nationally |
| Senior residents (46–65) | Often under-informed; eligibility concerns |
| Hospital visitors / attendants | Direct experience with blood shortage impact |
| NGO / volunteer members | Multiplier effect for outreach |

**Target sample size:** 150 respondents (pilot), 500+ (full rollout)  
**Sampling method:** Purposive convenience sampling at college campuses, housing societies, and hospital waiting areas in Kothrud, Deccan, Shivajinagar, Hadapsar, and Nigdi.

---

## 3. Survey Instrument

The survey is delivered both as a Google Form (offline capture) and via the LifeLine `/survey` route (online). The table below maps each question to its purpose.

| # | Question | Field Name | Type | Options | Purpose |
|---|----------|------------|------|---------|---------|
| 1 | Your Name | `respondent_name` | Text (optional) | Free text | Longitudinal follow-up |
| 2 | Age Group | `age_group` | Single-select | Under 18 / 18-25 / 26-35 / 36-45 / 46-60 / 60+ | Demographic segmentation |
| 3 | Your Area / Locality | `area` | Text (required) | Free text | Geographic gap analysis |
| 4 | Have you ever donated blood? | `donated_before` | Binary | Yes / No | Baseline donation rate |
| 5 | Are you willing to donate blood? | `willing_to_donate` | Tri-scale | Yes / No / Maybe | Intent-to-donate index |
| 6 | How did you learn about blood donation? | `awareness_source` | Single-select | Social Media / Friends–Family / Hospital / NGO / College / Other | Channel effectiveness |
| 7 | Do you know your own blood group? | `knows_blood_group` | Binary | Yes / No | Awareness gap KPI |
| 8 | Biggest barrier to donating blood? | `biggest_barrier` | Single-select | Fear of Needles / Lack of Time / Lack of Awareness / Health Concerns / No Nearby Camp / Other | Campaign focus driver |
| 9 | Any suggestions? | `suggestions` | Text (optional) | Free text | Qualitative insights |

---

## 4. Sample Pilot Findings
*(Illustrative figures from a pilot of 47 respondents, Oct 2024)*

| Metric | Value |
|--------|-------|
| Respondents who have donated before | 21 % |
| Willing to donate (Yes + Maybe) | 74 % |
| Know their own blood group | 68 % |
| Biggest single barrier | Fear of Needles (32 %) |
| Second barrier | No Nearby Camp (24 %) |
| Most cited awareness source | Social Media (38 %) |
| Suggestions mentioning "camp near college" | 41 % |

> **Note:** These are sample/illustrative figures for design reference. Actual survey data is stored in the `survey_responses` table and visible in the admin dashboard.

---

## 5. How Findings Shaped the Project

| Finding | Design Decision |
|---------|-----------------|
| 74% willing but not registered | Made donor registration the primary CTA on the homepage |
| Fear of Needles is top barrier | Awareness campaign messaging emphasises painless experience; links to medical FAQ |
| Social Media is top channel | Instagram/WhatsApp templates created for each campaign phase |
| No Nearby Camp (24%) | Admin campaign module added; upcoming camps shown on homepage and campaigns page |
| 32% don't know blood group | Survey question added; awareness posters encourage free blood-group testing camps |
| Qualitative: "flexible timings" | Campaigns now list morning and evening slots where possible |

---

## 6. Ethical Considerations

- Survey is fully voluntary; name is optional.
- No personally identifiable medical questions (the platform never collects health history).
- Data is stored on the project server and not shared with third parties.
- Results used only for academic CEP purposes and public awareness planning.
