# Project Impact Analysis
## LifeLine Blood Donor Finder — SPPU SE AI&DS CEP

---

## 1. Project Goal Recap

LifeLine aims to:
- Reduce the time it takes for a family member to find a compatible blood donor in their city.
- Increase voluntary blood donor registrations in the Pune urban area.
- Raise awareness of blood donation and reduce the key barriers identified in the community survey.

---

## 2. Impact Metrics Table

| Metric | Measurement Method | Baseline (Pre-Launch) | Target (6 months) | Actual* |
|--------|-------------------|----------------------|--------------------|---------|
| Registered donors | DB count: `SELECT COUNT(*) FROM donors` | 0 | 200 | — |
| Available donors | `WHERE is_available=1` | 0 | 150 | — |
| Blood requests submitted | `SELECT COUNT(*) FROM blood_requests` | 0 | 50 | — |
| Requests fulfilled | `WHERE status='Fulfilled'` | 0 | 30 | — |
| Fulfilment rate | Fulfilled / Total requests × 100 | — | ≥ 60% | — |
| Survey responses | `SELECT COUNT(*) FROM survey_responses` | 0 | 300 | — |
| Average feedback rating | `AVG(rating)` | — | ≥ 4.0 / 5 | — |
| Blood groups represented | `COUNT(DISTINCT blood_group)` in donors | 0 | 8 (all groups) | — |
| Cities covered | `COUNT(DISTINCT city)` | 0 | ≥ 5 | — |
| Campaigns organised | `SELECT COUNT(*) FROM campaigns` | 0 | 4 | — |
| Camp attendees | `SUM(actual_donors)` across campaigns | 0 | 150 | — |
| Donors who know blood group (survey) | % of `knows_blood_group='Yes'` responses | 68% (pilot) | 80% | — |

> *Actual figures to be populated after 6-month evaluation period.

---

## 3. Before-and-After Comparison Plan

### Before (Baseline State)
- No centralised donor directory for the target community.
- Families rely on word-of-mouth, hospital notice boards, or Facebook groups.
- Average reported "search time" to find a donor: anecdotally 2–6 hours (per pilot interviews).
- 26% of survey respondents were unaware of any local blood bank.

### After (Expected State at 6 Months)
- 200+ searchable, consented donors across 5+ cities.
- Families can find matching donors within minutes via the LifeLine search.
- Reported awareness of local donation resources increases (measured via follow-up survey).
- At least 3 awareness campaigns have taken place, with ≥ 150 total attendees.

### Measurement Method for Before-After
1. **Pre-launch survey** (already collected, baseline).
2. **Post-launch survey** (same instrument, 6 months later) — compare willingness and awareness scores.
3. **Admin dashboard KPIs** — tracked automatically via the DB.
4. **Exit interviews** with 10 requesters whose requests were fulfilled.

---

## 4. Social Impact Indicators

| Indicator | How Measured |
|-----------|-------------|
| Lives potentially saved | 1 donation ≈ 3 lives (WHO estimate); `actual_donors × 3` (illustrative) |
| Donors aware of eligibility criteria | % who selected "Lack of Awareness" as barrier decreased in follow-up survey |
| Gender-inclusive participation | M/F/Other breakdown in `donors.gender` |
| First-time donors | Donors with `last_donation_date IS NULL` |

---

## 5. Limitations

1. **No direct clinical outcome data** — LifeLine records connections, not whether a donation actually occurred. Fulfilled requests depend on admin manually updating the status.
2. **Self-selection bias** — Donors who register on a digital platform may already be more motivated than the general population; survey respondents who come to the platform are similarly self-selected.
3. **Offline gap** — Residents without smartphones or internet access cannot use the platform. Offline outreach (camps, posters) is needed to reach this segment.
4. **Admin dependency** — The platform's data quality depends on admins verifying donors and updating request statuses. Volunteer burnout is a risk.
5. **Medical outcomes unverifiable** — LifeLine cannot confirm whether blood compatibility was acceptable or whether the patient recovered. The platform intentionally avoids this responsibility.
6. **Geographic scope** — Phase 1 is limited to Pune. Results may not generalise to rural or Tier-2 city contexts.

---

## 6. Next Steps / Future Scope

| Priority | Feature / Action |
|----------|-----------------|
| High | Email/SMS notification to donors when a matching request is submitted |
| High | Donor login so donors can update their own availability |
| Medium | QR code for each donor to share in camp/WhatsApp campaigns |
| Medium | Multi-language support (Marathi) |
| Medium | API integration with partner blood bank inventory systems |
| Low | Mobile app (React Native) for faster donor search |
| Low | Gamification: donor badges and milestones |

---

## 7. Ethical Reflection

LifeLine was designed with a deliberate ethics-first approach:

- **Privacy by default:** Phone and email are masked publicly; full details are admin-only.
- **No medical overreach:** The platform explicitly defers all clinical decisions to qualified professionals.
- **Informed consent:** A separate, mandatory consent checkbox with plain-language explanation is required for every donor registration.
- **Transparency:** The About page clearly states what the platform does and does not do.
- **Data minimisation:** No health history, weight, or haemoglobin data is collected or stored.
- **Right to erasure:** Donors are informed they may request deletion at any time.

These choices reflect the project's commitment to community service without compromising user safety or autonomy.
