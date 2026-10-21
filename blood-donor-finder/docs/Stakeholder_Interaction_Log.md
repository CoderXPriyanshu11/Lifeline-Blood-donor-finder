# Stakeholder Interaction Log
## LifeLine Blood Donor Finder — SPPU SE AI&DS CEP

---

## Stakeholder Map

| # | Stakeholder | Organization | Role | Contact Mode |
|---|-------------|--------------|------|--------------|
| 1 | Dr Anjali Rane | Janwadi Blood Bank, Pune | Medical Officer & Blood Bank In-Charge | In-person + Email |
| 2 | Mr Prakash Nair | Indian Red Cross Society – Pune Chapter | District Coordinator | In-person + Phone |
| 3 | Prof. Sunita Jadhav | SPPU AI&DS Dept | Faculty Mentor (CEP Guide) | In-person + Portal |
| 4 | Student Volunteer Team | SPPU SE AI&DS | 6-member volunteer group | WhatsApp Group |

---

## Interaction 1 — Dr Anjali Rane, Janwadi Blood Bank

**Date:** 5 September 2024  
**Mode:** In-person meeting at Janwadi Blood Bank, Pune  
**Attendees:** 2 project team members + Dr Rane

### Agenda
- Understand clinical requirements and constraints for a digital donor registry.
- Clarify what the platform may and may not claim regarding eligibility and compatibility.
- Discuss potential data-sharing or co-branding arrangement.

### Discussion Summary

Dr Rane confirmed that standard blood donor eligibility criteria include:
- Age: 18–65 years
- Weight: ≥ 45 kg
- Haemoglobin: ≥ 12.5 g/dL (checked on-site only)
- No donation within the last 3 months
- Free from certain medical conditions (checked via on-site questionnaire)

She emphasised that **no digital platform may certify eligibility** — this must be assessed by trained staff at the point of donation. She also cautioned against displaying full compatibility charts without a clear disclaimer that actual compatibility requires cross-matching.

### Decisions Influenced

| Decision | Outcome |
|----------|---------|
| Remove health questionnaire from registration | Accepted: only last donation date is captured as a soft reminder |
| Add explicit disclaimer on every relevant page | Implemented in base template footer and on registration/request/about pages |
| Compatibility filter labelled "general reference only" | Implemented in search page with clear notice |
| Age check 18–65 enforced | DB constraint + server-side validation added |
| Consent checkbox required | DB constraint + UI requirement |

### Follow-Up Actions
- [ ] Share final platform URL for review before launch.
- [ ] Request monthly camp schedule to populate Campaigns page.
- [x] Draft MoU clause: LifeLine is not affiliated with or endorsed by any blood bank; it is an independent community platform.

---

## Interaction 2 — Mr Prakash Nair, Indian Red Cross Society

**Date:** 12 October 2024  
**Mode:** In-person meeting at Red Cross Chapter Office, Pune  
**Attendees:** 2 project team members + Mr Nair

### Agenda
- Co-branding for awareness campaign materials.
- Volunteer support for the donation camp (Phase 2).
- Legal and ethical guidelines for volunteer-run blood drives.

### Discussion Summary

Mr Nair confirmed that Red Cross is open to co-branding awareness materials (posters, leaflets) as long as:
- The materials include a statement that "Blood transfusion and compatibility are decided by licensed medical staff."
- Red Cross is credited as a "supporting partner" rather than an organiser.
- No monetary exchange is implied or made.

He also offered 2 trained volunteers for camp registration duty and emphasised the importance of the buddy system for first-time donors.

### Decisions Influenced

| Decision | Outcome |
|----------|---------|
| Add Red Cross acknowledgment to poster templates | Accepted |
| Use buddy system at camp | Added to campaign plan (Phase 2) |
| 2 Red Cross volunteers for camp registration | Confirmed |
| Disclaimer wording reviewed | Revised with Mr Nair's suggested language |

---

## Interaction 3 — Prof. Sunita Jadhav, SPPU Faculty Mentor

**Date:** Weekly meetings throughout Sept–Nov 2024  
**Mode:** In-person (department) + SPPU Portal

### Key Guidance Received

- Ensured all five CEP documentation files are complete and evidence-based.
- Advised replacing any fabricated impact figures with clearly labelled "illustrative" data.
- Confirmed that parameterised SQL queries and password hashing are required for security marks.
- Suggested adding a "project limitations" section to the Impact Analysis document.
- Reviewed admin panel design; recommended adding a feedback analytics view.

---

## Interaction 4 — Student Volunteer Team

**Date:** Ongoing (Sept–Nov 2024)  
**Mode:** WhatsApp group + bi-weekly stand-up meetings

### Roles and Contributions

| Volunteer | Role | Contribution |
|-----------|------|-------------|
| Aditya Kulkarni | Backend Lead | Flask routes, DB schema |
| Pooja Deshmukh | Frontend | HTML/CSS, donor card design |
| Rahul More | Survey Design | Questionnaire instrument |
| Neha Patil | Campaign Ops | Posters, WhatsApp outreach |
| Siddharth Joshi | Admin Panel | Dashboard charts |
| Tanvi Shah | Documentation | CEP docs, README |

### Decisions Made in Team

- Agreed on privacy-first approach (masking contacts publicly).
- Chose Flask over Django for simplicity given team's Python familiarity.
- Decided not to implement SMS/email notification in Phase 1 (complexity, cost) — deferred to future scope.
