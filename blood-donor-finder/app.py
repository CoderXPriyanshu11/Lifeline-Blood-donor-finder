"""
app.py – LifeLine Blood Donor Finder
SPPU SE AI&DS Community Engagement Project
Main Flask application: routes, validation, admin panel.
"""
from __future__ import annotations

import re
import json
import logging
from datetime import date, datetime
from functools import wraps
from collections import defaultdict

from flask import (
    Flask, render_template, request, redirect, url_for,
    session, flash, jsonify, g,
)
from werkzeug.security import check_password_hash

from config import Config
from db import init_pool, close_db, query, execute

# ── App setup ─────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.config.from_object(Config)

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s [%(name)s] %(message)s")

init_pool(app)
app.teardown_appcontext(close_db)

# ── Constants ─────────────────────────────────────────────────────────────────
BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

COMPATIBILITY: dict[str, list[str]] = {
    "A+":  ["A+", "A-", "O+", "O-"],
    "A-":  ["A-", "O-"],
    "B+":  ["B+", "B-", "O+", "O-"],
    "B-":  ["B-", "O-"],
    "AB+": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
    "AB-": ["A-", "B-", "AB-", "O-"],
    "O+":  ["O+", "O-"],
    "O-":  ["O-"],
}

# ── Helpers ───────────────────────────────────────────────────────────────────
PHONE_RE = re.compile(r"^\d{10}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def mask_phone(phone: str) -> str:
    """Show first 2 + last 2 digits, mask the rest."""
    if not phone or len(phone) < 4:
        return "XXXXXXXXXX"
    return phone[:2] + "X" * (len(phone) - 4) + phone[-2:]


def mask_email(email: str) -> str:
    """Show first char + last char before @."""
    if not email or "@" not in email:
        return ""
    local, domain = email.split("@", 1)
    if len(local) <= 2:
        return f"{'X' * len(local)}@{domain}"
    return f"{local[0]}{'X' * (len(local) - 2)}{local[-1]}@{domain}"


app.jinja_env.filters["mask_phone"] = mask_phone
app.jinja_env.filters["mask_email"] = mask_email


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "admin_id" not in session:
            flash("Please log in to access the admin panel.", "warning")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


# ── Public routes ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    stats = query(
        """SELECT
            (SELECT COUNT(*) FROM donors)                           AS total_donors,
            (SELECT COUNT(*) FROM donors WHERE is_available = 1)    AS available_donors,
            (SELECT COUNT(*) FROM blood_requests)                   AS total_requests,
            (SELECT COUNT(*) FROM blood_requests WHERE status='Fulfilled') AS fulfilled_requests
        """,
        fetchone=True,
    )
    upcoming = query(
        "SELECT * FROM campaigns WHERE campaign_date >= CURDATE() ORDER BY campaign_date LIMIT 3"
    )
    return render_template("index.html", stats=stats, upcoming=upcoming)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = {}
    errors = []

    if request.method == "POST":
        form = request.form.to_dict()
        full_name  = form.get("full_name", "").strip()
        age_raw    = form.get("age", "").strip()
        gender     = form.get("gender", "").strip()
        blood_group = form.get("blood_group", "").strip()
        phone      = form.get("phone", "").strip()
        email      = form.get("email", "").strip() or None
        area       = form.get("area", "").strip()
        city       = form.get("city", "").strip()
        last_don   = form.get("last_donation_date", "").strip() or None
        is_avail   = 1 if form.get("is_available") else 0
        consent    = form.get("consent_given")

        # Validation
        if not full_name:
            errors.append("Full name is required.")
        if not age_raw.isdigit() or not (18 <= int(age_raw) <= 65):
            errors.append("Age must be between 18 and 65.")
        if gender not in ("Male", "Female", "Other"):
            errors.append("Please select a valid gender.")
        if blood_group not in BLOOD_GROUPS:
            errors.append("Please select a valid blood group.")
        if not PHONE_RE.match(phone):
            errors.append("Phone must be exactly 10 digits.")
        if email and not EMAIL_RE.match(email):
            errors.append("Enter a valid email address.")
        if not area:
            errors.append("Area is required.")
        if not city:
            errors.append("City is required.")
        if last_don:
            try:
                datetime.strptime(last_don, "%Y-%m-%d")
            except ValueError:
                errors.append("Invalid last donation date format.")
        if not consent:
            errors.append("You must provide explicit consent to register as a donor.")

        if not errors:
            try:
                execute(
                    """INSERT INTO donors
                       (full_name, age, gender, blood_group, phone, email,
                        area, city, last_donation_date, is_available, consent_given)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (full_name, int(age_raw), gender, blood_group, phone, email,
                     area, city, last_don, is_avail, 1),
                )
                return redirect(url_for("thank_you", kind="register"))
            except Exception as exc:
                app.logger.error("Donor insert error: %s", exc)
                errors.append("Database error. Please try again.")

    return render_template("register.html", form=form, errors=errors,
                           blood_groups=BLOOD_GROUPS)


@app.route("/request-blood", methods=["GET", "POST"])
def request_blood():
    form = {}
    errors = []

    if request.method == "POST":
        form = request.form.to_dict()
        patient_name = form.get("patient_name", "").strip()
        blood_group  = form.get("blood_group", "").strip()
        units_raw    = form.get("units_required", "1").strip()
        hospital     = form.get("hospital_name", "").strip()
        area         = form.get("area", "").strip()
        city         = form.get("city", "").strip()
        contact_name = form.get("contact_name", "").strip()
        contact_phone = form.get("contact_phone", "").strip()
        urgency      = form.get("urgency", "Normal").strip()
        notes        = form.get("additional_notes", "").strip() or None

        if not patient_name:
            errors.append("Patient name is required.")
        if blood_group not in BLOOD_GROUPS:
            errors.append("Please select a valid blood group.")
        if not units_raw.isdigit() or int(units_raw) < 1:
            errors.append("Units required must be a positive number.")
        if not hospital:
            errors.append("Hospital name is required.")
        if not area:
            errors.append("Area is required.")
        if not city:
            errors.append("City is required.")
        if not contact_name:
            errors.append("Contact name is required.")
        if not PHONE_RE.match(contact_phone):
            errors.append("Contact phone must be exactly 10 digits.")
        if urgency not in ("Normal", "Urgent", "Critical"):
            errors.append("Invalid urgency level.")

        if not errors:
            try:
                execute(
                    """INSERT INTO blood_requests
                       (patient_name, blood_group, units_required, hospital_name,
                        area, city, contact_name, contact_phone, urgency, additional_notes)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (patient_name, blood_group, int(units_raw), hospital,
                     area, city, contact_name, contact_phone, urgency, notes),
                )
                return redirect(url_for("search",
                                        blood_group=blood_group,
                                        city=city))
            except Exception as exc:
                app.logger.error("Request insert error: %s", exc)
                errors.append("Database error. Please try again.")

    return render_template("request_blood.html", form=form, errors=errors,
                           blood_groups=BLOOD_GROUPS)


@app.route("/search")
def search():
    blood_group   = request.args.get("blood_group", "").strip()
    city          = request.args.get("city", "").strip()
    area          = request.args.get("area", "").strip()
    avail_only    = request.args.get("avail_only", "1")
    compatible    = request.args.get("compatible", "0")

    donors_result = []

    if blood_group or city:
        groups = [blood_group] if blood_group else BLOOD_GROUPS
        if blood_group and compatible == "1":
            groups = COMPATIBILITY.get(blood_group, [blood_group])

        placeholders = ",".join(["%s"] * len(groups))
        params: list = list(groups)

        sql = f"""SELECT id, full_name, blood_group, area, city,
                         last_donation_date, is_available, is_verified,
                         phone, email
                  FROM donors
                  WHERE blood_group IN ({placeholders})
                    AND consent_given = 1"""

        if city:
            sql += " AND city LIKE %s"
            params.append(f"%{city}%")
        if area:
            sql += " AND area LIKE %s"
            params.append(f"%{area}%")
        if avail_only == "1":
            sql += " AND is_available = 1"

        sql += " ORDER BY is_verified DESC, registered_at DESC LIMIT 100"
        donors_result = query(sql, tuple(params))

    return render_template(
        "search.html",
        donors=donors_result,
        blood_groups=BLOOD_GROUPS,
        q_bg=blood_group,
        q_city=city,
        q_area=area,
        q_avail=avail_only,
        q_compat=compatible,
    )


@app.route("/campaigns")
def campaigns():
    camps = query("SELECT * FROM campaigns ORDER BY campaign_date DESC")
    today = date.today()
    return render_template("campaign.html", campaigns=camps, today=today)


@app.route("/survey", methods=["GET", "POST"])
def survey():
    form = {}
    errors = []

    if request.method == "POST":
        form = request.form.to_dict()
        age_group        = form.get("age_group", "").strip()
        area             = form.get("area", "").strip()
        donated_before   = form.get("donated_before", "").strip()
        willing          = form.get("willing_to_donate", "").strip()
        awareness_source = form.get("awareness_source", "").strip()
        knows_bg         = form.get("knows_blood_group", "").strip()
        barrier          = form.get("biggest_barrier", "").strip()
        suggestions      = form.get("suggestions", "").strip() or None
        resp_name        = form.get("respondent_name", "").strip() or None

        VALID_AGES    = {"Under 18","18-25","26-35","36-45","46-60","60+"}
        VALID_DONAT   = {"Yes","No"}
        VALID_WILLING = {"Yes","No","Maybe"}
        VALID_AWARE   = {"Social Media","Friends/Family","Hospital","NGO","College","Other"}
        VALID_KNOWS   = {"Yes","No"}
        VALID_BARRIER = {"Fear of Needles","Lack of Time","Lack of Awareness",
                          "Health Concerns","No Nearby Camp","Other"}

        if age_group not in VALID_AGES:       errors.append("Select a valid age group.")
        if not area:                           errors.append("Area is required.")
        if donated_before not in VALID_DONAT: errors.append("Indicate if you have donated before.")
        if willing not in VALID_WILLING:       errors.append("Indicate willingness to donate.")
        if awareness_source not in VALID_AWARE: errors.append("Select a valid awareness source.")
        if knows_bg not in VALID_KNOWS:        errors.append("Indicate if you know your blood group.")
        if barrier not in VALID_BARRIER:       errors.append("Select a valid barrier.")

        if not errors:
            try:
                execute(
                    """INSERT INTO survey_responses
                       (respondent_name, age_group, area, donated_before,
                        willing_to_donate, awareness_source, knows_blood_group,
                        biggest_barrier, suggestions)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (resp_name, age_group, area, donated_before, willing,
                     awareness_source, knows_bg, barrier, suggestions),
                )
                return redirect(url_for("thank_you", kind="survey"))
            except Exception as exc:
                app.logger.error("Survey insert error: %s", exc)
                errors.append("Database error. Please try again.")

    return render_template("survey.html", form=form, errors=errors)


@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    form = {}
    errors = []

    if request.method == "POST":
        form = request.form.to_dict()
        name    = form.get("name", "").strip() or None
        email   = form.get("email", "").strip() or None
        role    = form.get("role", "").strip()
        rating_raw = form.get("rating", "").strip()
        message = form.get("message", "").strip()

        VALID_ROLES = {"Donor","Requester","Volunteer","Public"}

        if role not in VALID_ROLES:      errors.append("Select a valid role.")
        if not rating_raw.isdigit() or not (1 <= int(rating_raw) <= 5):
            errors.append("Rating must be between 1 and 5.")
        if not message:                  errors.append("Message is required.")
        if email and not EMAIL_RE.match(email):
            errors.append("Enter a valid email address.")

        if not errors:
            try:
                execute(
                    """INSERT INTO feedback (name, email, role, rating, message)
                       VALUES (%s,%s,%s,%s,%s)""",
                    (name, email, role, int(rating_raw), message),
                )
                return redirect(url_for("thank_you", kind="feedback"))
            except Exception as exc:
                app.logger.error("Feedback insert error: %s", exc)
                errors.append("Database error. Please try again.")

    return render_template("feedback.html", form=form, errors=errors)


@app.route("/thank-you/<kind>")
def thank_you(kind: str):
    allowed = {"register", "survey", "feedback", "request"}
    if kind not in allowed:
        return redirect(url_for("index"))
    return render_template("thank_you.html", kind=kind)


@app.route("/about")
def about():
    return render_template("about.html")


# ── Admin routes ──────────────────────────────────────────────────────────────

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if "admin_id" in session:
        return redirect(url_for("admin_dashboard"))

    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        admin = query("SELECT * FROM admins WHERE username=%s", (username,), fetchone=True)
        if admin and check_password_hash(admin["password_hash"], password):
            session.permanent = True
            session["admin_id"]   = admin["id"]
            session["admin_name"] = admin["full_name"]
            flash(f"Welcome back, {admin['full_name']}!", "success")
            return redirect(url_for("admin_dashboard"))
        error = "Invalid username or password."

    return render_template("admin_login.html", error=error)


@app.route("/admin/logout")
@login_required
def admin_logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("admin_login"))


@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    kpi = query(
        """SELECT
            (SELECT COUNT(*) FROM donors)                              AS total_donors,
            (SELECT COUNT(*) FROM donors WHERE is_available=1)         AS available_donors,
            (SELECT COUNT(*) FROM donors WHERE is_verified=1)          AS verified_donors,
            (SELECT COUNT(*) FROM blood_requests)                      AS total_requests,
            (SELECT COUNT(*) FROM blood_requests WHERE status='Pending') AS pending_requests,
            (SELECT COUNT(*) FROM blood_requests WHERE status='Fulfilled') AS fulfilled_requests,
            (SELECT COUNT(*) FROM survey_responses)                    AS survey_count,
            (SELECT ROUND(AVG(rating),1) FROM feedback)                AS avg_rating
        """,
        fetchone=True,
    )
    recent_requests = query(
        "SELECT * FROM blood_requests ORDER BY created_at DESC LIMIT 5"
    )
    recent_donors = query(
        "SELECT * FROM donors ORDER BY registered_at DESC LIMIT 5"
    )
    return render_template("admin_dashboard.html",
                           kpi=kpi,
                           recent_requests=recent_requests,
                           recent_donors=recent_donors)


@app.route("/admin/api/analytics")
@login_required
def admin_analytics():
    """JSON endpoint consumed by Chart.js on the dashboard."""

    # 1. Donors by blood group
    bg_rows = query(
        "SELECT blood_group, COUNT(*) AS cnt FROM donors GROUP BY blood_group ORDER BY blood_group"
    )
    donors_by_bg = {"labels": [r["blood_group"] for r in bg_rows],
                    "data": [r["cnt"] for r in bg_rows]}

    # 2. Requests by status
    status_rows = query(
        "SELECT status, COUNT(*) AS cnt FROM blood_requests GROUP BY status"
    )
    requests_by_status = {"labels": [r["status"] for r in status_rows],
                          "data": [r["cnt"] for r in status_rows]}

    # 3. Monthly donor registrations (last 12 months)
    monthly_rows = query(
        """SELECT DATE_FORMAT(registered_at,'%Y-%m') AS month, COUNT(*) AS cnt
           FROM donors
           WHERE registered_at >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
           GROUP BY month ORDER BY month"""
    )
    monthly_reg = {"labels": [r["month"] for r in monthly_rows],
                   "data": [r["cnt"] for r in monthly_rows]}

    # 4. Requests by blood group
    req_bg_rows = query(
        "SELECT blood_group, COUNT(*) AS cnt FROM blood_requests GROUP BY blood_group ORDER BY blood_group"
    )
    requests_by_bg = {"labels": [r["blood_group"] for r in req_bg_rows],
                      "data": [r["cnt"] for r in req_bg_rows]}

    # 5. Donors by city
    city_rows = query(
        "SELECT city, COUNT(*) AS cnt FROM donors GROUP BY city ORDER BY cnt DESC LIMIT 8"
    )
    donors_by_city = {"labels": [r["city"] for r in city_rows],
                      "data": [r["cnt"] for r in city_rows]}

    # 6. Survey barriers
    barrier_rows = query(
        "SELECT biggest_barrier, COUNT(*) AS cnt FROM survey_responses GROUP BY biggest_barrier"
    )
    survey_barriers = {"labels": [r["biggest_barrier"] for r in barrier_rows],
                       "data": [r["cnt"] for r in barrier_rows]}

    return jsonify(
        donors_by_bg=donors_by_bg,
        requests_by_status=requests_by_status,
        monthly_reg=monthly_reg,
        requests_by_bg=requests_by_bg,
        donors_by_city=donors_by_city,
        survey_barriers=survey_barriers,
    )


@app.route("/admin/donors")
@login_required
def admin_donors():
    search_q    = request.args.get("q", "").strip()
    filter_bg   = request.args.get("blood_group", "").strip()
    filter_avail = request.args.get("avail", "").strip()

    sql = "SELECT * FROM donors WHERE 1=1"
    params: list = []

    if search_q:
        sql += " AND (full_name LIKE %s OR phone LIKE %s OR city LIKE %s OR area LIKE %s)"
        like = f"%{search_q}%"
        params.extend([like, like, like, like])
    if filter_bg and filter_bg in BLOOD_GROUPS:
        sql += " AND blood_group = %s"
        params.append(filter_bg)
    if filter_avail == "1":
        sql += " AND is_available = 1"
    elif filter_avail == "0":
        sql += " AND is_available = 0"

    sql += " ORDER BY registered_at DESC"
    donors = query(sql, tuple(params))

    return render_template("admin_donors.html",
                           donors=donors,
                           blood_groups=BLOOD_GROUPS,
                           q=search_q,
                           filter_bg=filter_bg,
                           filter_avail=filter_avail)


@app.route("/admin/donors/<int:donor_id>/toggle-verified", methods=["POST"])
@login_required
def admin_toggle_verified(donor_id: int):
    execute(
        "UPDATE donors SET is_verified = NOT is_verified WHERE id=%s",
        (donor_id,)
    )
    flash("Verification status updated.", "success")
    return redirect(url_for("admin_donors",
                            q=request.form.get("q",""),
                            blood_group=request.form.get("blood_group",""),
                            avail=request.form.get("avail","")))


@app.route("/admin/donors/<int:donor_id>/toggle-available", methods=["POST"])
@login_required
def admin_toggle_available(donor_id: int):
    execute(
        "UPDATE donors SET is_available = NOT is_available WHERE id=%s",
        (donor_id,)
    )
    flash("Availability status updated.", "success")
    return redirect(url_for("admin_donors",
                            q=request.form.get("q",""),
                            blood_group=request.form.get("blood_group",""),
                            avail=request.form.get("avail","")))


@app.route("/admin/donors/<int:donor_id>/delete", methods=["POST"])
@login_required
def admin_delete_donor(donor_id: int):
    execute("DELETE FROM donors WHERE id=%s", (donor_id,))
    flash("Donor record deleted.", "danger")
    return redirect(url_for("admin_donors"))


@app.route("/admin/requests")
@login_required
def admin_requests():
    filter_status = request.args.get("status", "").strip()
    sql = "SELECT * FROM blood_requests WHERE 1=1"
    params: list = []
    if filter_status:
        sql += " AND status = %s"
        params.append(filter_status)
    sql += " ORDER BY created_at DESC"
    requests_list = query(sql, tuple(params))
    return render_template("admin_requests.html",
                           requests=requests_list,
                           filter_status=filter_status)


@app.route("/admin/requests/<int:req_id>/update-status", methods=["POST"])
@login_required
def admin_update_request_status(req_id: int):
    new_status = request.form.get("status", "Pending")
    valid = {"Pending", "In Progress", "Fulfilled", "Cancelled"}
    if new_status in valid:
        execute("UPDATE blood_requests SET status=%s WHERE id=%s", (new_status, req_id))
        flash("Request status updated.", "success")
    return redirect(url_for("admin_requests"))


@app.route("/admin/requests/<int:req_id>/delete", methods=["POST"])
@login_required
def admin_delete_request(req_id: int):
    execute("DELETE FROM blood_requests WHERE id=%s", (req_id,))
    flash("Blood request deleted.", "danger")
    return redirect(url_for("admin_requests"))


@app.route("/admin/campaigns", methods=["GET", "POST"])
@login_required
def admin_campaigns():
    errors = []
    if request.method == "POST":
        title    = request.form.get("title", "").strip()
        desc     = request.form.get("description", "").strip() or None
        camp_date = request.form.get("campaign_date", "").strip()
        location = request.form.get("location", "").strip()
        organizer = request.form.get("organizer", "").strip()
        expected = request.form.get("expected_donors", "0").strip()
        actual   = request.form.get("actual_donors", "0").strip()

        if not title:    errors.append("Title required.")
        if not camp_date: errors.append("Campaign date required.")
        if not location: errors.append("Location required.")
        if not organizer: errors.append("Organizer required.")

        if not errors:
            execute(
                """INSERT INTO campaigns
                   (title, description, campaign_date, location, organizer,
                    expected_donors, actual_donors)
                   VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                (title, desc, camp_date, location, organizer,
                 int(expected) if expected.isdigit() else 0,
                 int(actual) if actual.isdigit() else 0),
            )
            flash("Campaign added.", "success")
            return redirect(url_for("admin_campaigns"))

    camps = query("SELECT * FROM campaigns ORDER BY campaign_date DESC")
    today = date.today()
    return render_template("admin_campaigns.html",
                           campaigns=camps, today=today, errors=errors)


@app.route("/admin/campaigns/<int:camp_id>/delete", methods=["POST"])
@login_required
def admin_delete_campaign(camp_id: int):
    execute("DELETE FROM campaigns WHERE id=%s", (camp_id,))
    flash("Campaign deleted.", "danger")
    return redirect(url_for("admin_campaigns"))


@app.route("/admin/stakeholders", methods=["GET", "POST"])
@login_required
def admin_stakeholders():
    errors = []
    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        org      = request.form.get("organization", "").strip()
        role     = request.form.get("role", "").strip()
        contact  = request.form.get("contact", "").strip() or None
        notes    = request.form.get("interaction_notes", "").strip() or None
        int_date = request.form.get("interaction_date", "").strip()

        if not name:     errors.append("Name required.")
        if not org:      errors.append("Organization required.")
        if not role:     errors.append("Role required.")
        if not int_date: errors.append("Interaction date required.")

        if not errors:
            execute(
                """INSERT INTO stakeholders
                   (name, organization, role, contact, interaction_notes, interaction_date)
                   VALUES (%s,%s,%s,%s,%s,%s)""",
                (name, org, role, contact, notes, int_date),
            )
            flash("Stakeholder added.", "success")
            return redirect(url_for("admin_stakeholders"))

    stks = query("SELECT * FROM stakeholders ORDER BY interaction_date DESC")
    return render_template("admin_stakeholders.html",
                           stakeholders=stks, errors=errors)


@app.route("/admin/stakeholders/<int:stk_id>/delete", methods=["POST"])
@login_required
def admin_delete_stakeholder(stk_id: int):
    execute("DELETE FROM stakeholders WHERE id=%s", (stk_id,))
    flash("Stakeholder deleted.", "danger")
    return redirect(url_for("admin_stakeholders"))


@app.route("/admin/survey")
@login_required
def admin_survey():
    responses = query("SELECT * FROM survey_responses ORDER BY submitted_at DESC")
    return render_template("admin_survey.html", responses=responses)


@app.route("/admin/feedback")
@login_required
def admin_feedback():
    feedbacks = query("SELECT * FROM feedback ORDER BY submitted_at DESC")
    return render_template("admin_feedback.html", feedbacks=feedbacks)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=Config.DEBUG, host="0.0.0.0", port=5000)
