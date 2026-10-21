-- ============================================================
-- LifeLine Blood Donor Finder — Database Schema
-- SPPU SE AI&DS Community Engagement Project
-- MySQL 8.0+
-- ============================================================

CREATE DATABASE IF NOT EXISTS blood_donor_finder
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE blood_donor_finder;

-- ------------------------------------------------------------
-- admins
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS admins (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    username     VARCHAR(50)  NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name    VARCHAR(100) NOT NULL,
    created_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- donors
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS donors (
    id                 INT AUTO_INCREMENT PRIMARY KEY,
    full_name          VARCHAR(100) NOT NULL,
    age                TINYINT UNSIGNED NOT NULL,
    gender             ENUM('Male','Female','Other') NOT NULL,
    blood_group        ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
    phone              CHAR(10) NOT NULL,
    email              VARCHAR(150) NULL,
    area               VARCHAR(100) NOT NULL,
    city               VARCHAR(100) NOT NULL,
    last_donation_date DATE NULL,
    is_available       TINYINT(1) NOT NULL DEFAULT 1,
    consent_given      TINYINT(1) NOT NULL,
    is_verified        TINYINT(1) NOT NULL DEFAULT 0,
    notes              TEXT NULL,
    registered_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_donor_age  CHECK (age BETWEEN 18 AND 65),
    CONSTRAINT chk_consent     CHECK (consent_given = 1)
) ENGINE=InnoDB;

CREATE INDEX IF NOT EXISTS idx_donor_search
    ON donors (blood_group, city, area, is_available);

-- ------------------------------------------------------------
-- blood_requests
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS blood_requests (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    patient_name     VARCHAR(100) NOT NULL,
    blood_group      ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
    units_required   TINYINT UNSIGNED NOT NULL DEFAULT 1,
    hospital_name    VARCHAR(150) NOT NULL,
    area             VARCHAR(100) NOT NULL,
    city             VARCHAR(100) NOT NULL,
    contact_name     VARCHAR(100) NOT NULL,
    contact_phone    CHAR(10) NOT NULL,
    urgency          ENUM('Normal','Urgent','Critical') NOT NULL DEFAULT 'Normal',
    additional_notes TEXT NULL,
    status           ENUM('Pending','In Progress','Fulfilled','Cancelled')
                     NOT NULL DEFAULT 'Pending',
    created_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- survey_responses
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS survey_responses (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    respondent_name   VARCHAR(100) NULL,
    age_group         ENUM('Under 18','18-25','26-35','36-45','46-60','60+') NOT NULL,
    area              VARCHAR(100) NOT NULL,
    donated_before    ENUM('Yes','No') NOT NULL,
    willing_to_donate ENUM('Yes','No','Maybe') NOT NULL,
    awareness_source  ENUM('Social Media','Friends/Family','Hospital','NGO','College','Other') NOT NULL,
    knows_blood_group ENUM('Yes','No') NOT NULL,
    biggest_barrier   ENUM('Fear of Needles','Lack of Time','Lack of Awareness',
                          'Health Concerns','No Nearby Camp','Other') NOT NULL,
    suggestions       TEXT NULL,
    submitted_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- campaigns
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS campaigns (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    title            VARCHAR(150) NOT NULL,
    description      TEXT NULL,
    campaign_date    DATE NOT NULL,
    location         VARCHAR(200) NOT NULL,
    organizer        VARCHAR(150) NOT NULL,
    expected_donors  SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    actual_donors    SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    created_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- stakeholders
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS stakeholders (
    id                 INT AUTO_INCREMENT PRIMARY KEY,
    name               VARCHAR(100) NOT NULL,
    organization       VARCHAR(150) NOT NULL,
    role               VARCHAR(100) NOT NULL,
    contact            VARCHAR(150) NULL,
    interaction_notes  TEXT NULL,
    interaction_date   DATE NOT NULL,
    created_at         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- feedback
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS feedback (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NULL,
    email       VARCHAR(150) NULL,
    role        ENUM('Donor','Requester','Volunteer','Public') NOT NULL,
    rating      TINYINT UNSIGNED NOT NULL,
    message     TEXT NOT NULL,
    submitted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_rating CHECK (rating BETWEEN 1 AND 5)
) ENGINE=InnoDB;

-- ============================================================
-- SEED DATA
-- ============================================================

-- Demo donors
INSERT INTO donors (full_name, age, gender, blood_group, phone, email, area, city, last_donation_date, is_available, consent_given, is_verified, notes) VALUES
('Arjun Kulkarni',  24, 'Male',   'O+',  '9876543210', 'arjun.k@example.com',   'Kothrud',    'Pune', '2024-08-15', 1, 1, 1, NULL),
('Priya Sharma',    29, 'Female', 'A+',  '9123456789', NULL,                    'Deccan',     'Pune', '2024-06-01', 1, 1, 1, NULL),
('Rohan Deshmukh',  33, 'Male',   'B+',  '9988776655', 'rohan.d@example.com',   'Shivajinagar','Pune','2024-03-20', 0, 1, 0, 'Travelling until Dec'),
('Sneha Patil',     22, 'Female', 'AB+', '9011223344', NULL,                    'Hadapsar',   'Pune', NULL,          1, 1, 0, NULL),
('Vikram Yadav',    45, 'Male',   'O-',  '8800991122', 'vikram.y@example.com',  'Nigdi',      'Pune', '2023-12-10', 1, 1, 1, 'Available weekends');

-- Demo blood requests
INSERT INTO blood_requests (patient_name, blood_group, units_required, hospital_name, area, city, contact_name, contact_phone, urgency, status) VALUES
('Meena Joshi',   'O+', 2, 'Sahyadri Hospital',       'Karve Road',   'Pune', 'Ravi Joshi',   '9876501234', 'Urgent',   'Pending'),
('Suresh Kumar',  'B+', 1, 'Ruby Hall Clinic',         'Sangamwadi',   'Pune', 'Anita Kumar',  '9765432109', 'Critical', 'In Progress');

-- Demo campaigns
INSERT INTO campaigns (title, description, campaign_date, location, organizer, expected_donors, actual_donors) VALUES
('LifeLine Camp – Kothrud Edition',
 'Community blood donation camp organised in partnership with Janwadi Blood Bank. Free health checkup for donors.',
 '2025-02-14', 'Kothrud Community Hall, Pune', 'SPPU AI&DS Students', 80, 67),
('Save a Life – College Drive',
 'Intra-college donation drive targeting first-time donors. Awareness stalls and refreshments provided.',
 '2025-11-20', 'MIT College Auditorium, Pune', 'LifeLine Volunteers', 100, 0);

-- Demo stakeholders
INSERT INTO stakeholders (name, organization, role, contact, interaction_notes, interaction_date) VALUES
('Dr Anjali Rane',   'Janwadi Blood Bank, Pune',  'Medical Officer & Blood Bank In-Charge',
 'rane.anjali@janwadibb.org',
 'Initial meeting to validate eligibility criteria and discuss data sharing MoU. Confirmed: age 18–65, no questionnaire on platform, full compatibility check by professional only. Agreed to provide monthly camp schedule.',
 '2024-09-05'),
('Mr Prakash Nair',  'Indian Red Cross Society – Pune Chapter', 'District Coordinator',
 'prakash.nair@redcross.in',
 'Discussed awareness campaign co-branding and volunteer training. Red Cross to share 2 outreach volunteers for College Drive. LifeLine logo to carry Red Cross acknowledgement.',
 '2024-10-12');

-- Demo survey responses
INSERT INTO survey_responses (respondent_name, age_group, area, donated_before, willing_to_donate, awareness_source, knows_blood_group, biggest_barrier, suggestions) VALUES
('Amit Tiwari',  '18-25',  'Kothrud',     'No',  'Yes',   'College',      'Yes', 'Fear of Needles',    'Organise camps near college.'),
('Kavya Menon',  '26-35',  'Deccan',      'Yes', 'Yes',   'Social Media', 'Yes', 'Lack of Time',       'Provide flexible camp timings.'),
(NULL,           '36-45',  'Hadapsar',    'No',  'Maybe', 'Hospital',     'No',  'Lack of Awareness',  NULL),
('Renu Bhatt',   '18-25',  'Shivajinagar','No',  'Yes',   'Friends/Family','Yes','No Nearby Camp',     'More camps in residential areas.'),
(NULL,           '26-35',  'Nigdi',       'Yes', 'Yes',   'NGO',          'Yes', 'Health Concerns',    'Publish clear eligibility guidelines.');

-- Demo feedback
INSERT INTO feedback (name, email, role, rating, message) VALUES
('Arjun Kulkarni', 'arjun.k@example.com', 'Donor',     5, 'Super easy to register! Happy to help save lives.'),
('Anonymous',       NULL,                  'Requester', 4, 'Found a matching donor within hours. Great initiative.');
