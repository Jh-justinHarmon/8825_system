# RAL Portal - Complete Technical Reference
**Portal URL:** https://rallc-web.azurewebsites.net/  
**Stage URL:** https://rallcstage.azurewebsites.net/  
**Client:** Reinsurance Associates (RAL)  
**Managed By:** HCSS  
**Last Updated:** 2025-11-11  
**Source Files:** 4 technical documents consolidated

---

## Table of Contents
1. [System Overview](#system-overview)
2. [API Documentation](#api-documentation)
3. [Database Schema (ERD)](#database-schema-erd)
4. [Technology Stack](#technology-stack)
5. [Authentication & Authorization](#authentication--authorization)
6. [Deployment Process](#deployment-process)
7. [Support & Contacts](#support--contacts)

---

## System Overview

### Purpose
RAL Portal is a critical business operations system used for:
- Customer quarterly reporting management
- Task management and work assignment
- Client/agent read-only access
- Approximately 12 reports (powered by stored procedures)

### Development History
- Initially developed: 2014-2016
- Primary users: RAL employees
- Secondary users: Agents and clients (read-only)

### Service Description
The portal manages customer quarterly reporting and contains all task management functionality to help RAL assign and track work for customers.

---

## API Documentation

### Base URLs
- **Stage:** `https://rallcstage.azurewebsites.net/api/`
- **Production:** Available upon request

### Authentication Flow (OAuth 2.0)

#### Step 1: Get OAuth Token
**Endpoint:** `POST /oauth/token`  
**Content-Type:** `application/x-www-form-urlencoded`

**Parameters:**
```
grant_type: client_credentials
client_id: a934a88b4bed4a12g7d888f5c43dcb68
client_secret: a1zdabwfPpFcFdMft6asfzLkO1aa_K9vKe9SJezPwWs
```

**Response:** `200 OK`
```json
{
  "access_token": "...",
  ...
}
```

**Usage:** Include in all subsequent requests as:
```
Authorization: Bearer {access_token}
```

---

### File Upload Workflow

#### Step 2: Create intakeDocument Record
**Endpoint:** `POST /api/intakeDocument/`  
**Content-Type:** `application/json`

**Payload:**
```json
{
  "originalFileName": "statement.pdf",
  "OriginationSource": "email"
}
```

**Response:** `200 OK` - Returns `intakeDocument` object with generated GUID filename

---

#### Step 3: Create intakeDocumentLog Record
**Endpoint:** `POST /api/intakeDocumentLog/`  
**Content-Type:** `application/json`

**Payload:**
```json
{
  "status": "UPLOADING",
  "type": "INTAKE",
  "description": "Uploading file statement.pdf to intake",
  "filepath": "ralstage",
  "filename": "d377ce77-ee09-47a1-8110-a786a03da605.pdf"
}
```

**Status Options:**
- `UPLOADING` - File upload in progress
- `PARSING` - Document being parsed
- `FAULTED` - Error occurred
- `COMMIT_ERROR` - Database commit failed
- `DISCARDED` - File discarded
- `ABORTED` - Process aborted
- `FINISHED` - Processing complete
- `COMMITTED` - Successfully committed

**Environment Options:**
- `ralstage` - Stage environment
- `ralprod` - Production environment

**Response:** `201 Created` - Returns `intakeDocument` and log entry

---

#### Step 4: Upload Statement File
**Endpoint:** `POST /api/files/uploadStatement/?name={guid_filename}`  
**Content-Type:** `multipart/form-data`

**Parameters:**
- **Query String:** `?name=` - GUID filename from Step 2
- **Form Data:** Binary PDF file

**Example:**
```
POST /api/files/uploadStatement/?name=d377ce77-ee09-47a1-8110-a786a03da605.pdf
Content-Type: multipart/form-data

[Binary PDF data]
```

**Response:** `200 OK`

---

#### Step 5: Update intakeDocument Status
**Endpoint:** `PUT /api/intakeDocument/`  
**Content-Type:** `application/json`

**Payload:** Full `intakeDocument` object from Step 2 with `status` changed to `"Waiting"`

**intakeDocument Schema:**
```json
{
  "administrator": "",
  "administrator_ID": "",
  "adminstratorParsedValue": "",
  "attachment": "",
  "attachment_ID": "",
  "bank": "",
  "bankParsedValue": "",
  "bank_ID": "",
  "client": "",
  "clientBankAccount": "",
  "clientBankAccountParsedValue": "",
  "clientBankAccount_ID": "",
  "clientCession": "",
  "clientCessionParsedValue": "",
  "clientCession_ID": "",
  "clientParsedValue": "",
  "client_ID": "",
  "completedOn": "",
  "createdOn": "",
  "documentIntakeLogs": "",
  "fileName": "",
  "filePassword": "",
  "filePath": "",
  "filingDate": "",
  "frequency_ID": "",
  "intakeDocument_ID": "",
  "isManuallyMapped": "",
  "modifiedOn": "",
  "month": "",
  "originalFileName": "",
  "originationSource": "",
  "provider": "",
  "providerId": "",
  "source": "",
  "startedOn": "",
  "status": "Waiting",
  "year": ""
}
```

**Response:** `200 OK` - Returns updated `intakeDocument` record

---

## Database Schema (ERD)

### RAL Portal Data Map - ERD 1.0
**Date:** 11/08/2022  
**Total Tables:** 35

### Key Tables

#### Tax Data Tables
- `2016_TAX_DATA`
- `2017_TAX_DATA`
- `2018_TAX_DATA`
- `TAX_CALC_DATA`

#### Core Business Tables
- `ACCOUNTANTS`
- `BANKS`
- `CLIENTS` (3 pages: CLIENTS, CLIENTS_P2, CLIENTS_P3)
- `CESSIONS` (2 pages: CESSIONS, CESSIONS_P2)
- `CESSION_INSURANCE`
- `PRODUCERS`
- `REINSURANCE`

#### System Tables
- `ASP_NET` - ASP.NET Identity/Authentication
- `USERS` - User management
- `CALENDARS` - Scheduling
- `DUE_DAYS` - Due date tracking
- `ENTITY` - Entity management
- `LICENSING` - License tracking

#### Workflow Tables
- `TASKS` - Task management
- `PROJECT_TASKS` - Project-specific tasks
- `TEMPLATES` - Document templates

#### Reporting Tables
- `FINAL_RESULT` (3 pages: FINAL_RESULT, FINAL_RESULT_1, FINAL_RESULT_2)
- `GENERAL` (2 pages: GENERAL, GENERAL_P2)
- `MISC` (2 pages: MISC, MISC_P2)

#### Reference Tables
- `RAL_CONTACTS` - Contact information
- `TABLES` - System tables metadata

**Note:** Full ERD diagrams available in source document. Each table includes detailed field definitions, relationships, and constraints.

---

## Technology Stack

### Frontend
- **Framework:** AngularJS v1.3.13 (2014)
- **UI Library:** jQuery v2.1.3
- **CSS Framework:** Bootstrap v0.12.0 (2014)
- **Type:** Progressive Web Application (PWA)

### Backend
- **Framework:** ASP.NET Core v4.5
- **ORM:** Entity Framework v6.1.3
- **API:** ASP.NET Web API v5.2.3 (REST)
- **Database:** Microsoft Azure SQL Database

### Development Tools
- Visual Studio Pro 2022
- SQL Server Management Studio
- Gitea (Version Control)

### Infrastructure
- **Hosting:** Microsoft Azure
- **Protocol:** HTTPS (SSL encrypted)
- **Architecture:** Split execution (device-side + server-side)

---

## Authentication & Authorization

### Access
- **URL:** https://rallcweb.azurewebsites.net/#/login
- **Type:** Web-based application
- **Protocol:** SSL encrypted HTTP

### Authentication Flow

1. **User Credentials Entered**
   - Password hashed using SHA-256
   - Delivered to server via JSON REST API

2. **Server Validation**
   - Password compared against salted hash in SQL database
   - Incorrect: Returns "authentication failed"
   - Correct: Generates expiring JWT token

3. **Token Management**
   - JWT token cached in session store (device-side)
   - Token passed with all subsequent API requests
   - Server revalidates token on each request
   - Invalid token → Request rejected

### Authorization

**Server-Side (Capability-Based)**
- JWT token includes user role data
- Each endpoint defines required role
- Unauthorized requests rejected

**Device-Side (PWA)**
- Anticipates lack of permission
- Renders unauthorized message if user attempts workaround
- Server rejects unauthorized attempts

**Note:** See REST API Documentation for role authorizations per endpoint

---

## Deployment Process

### Git-Based Deployment
- All deployments managed through Git
- Quick rollback capability
- Branch switching for production updates

### Three-Phase Iterative Process

#### Phase 1: Primary Development
**Location:** Non-production development server  
**Branch:** `dev`

**Requirements for Phase 1 Completion:**
- ✅ Lead Engineer and Client approval of feature set
- ✅ Automated tests cover new use cases and bug fixes
- ✅ Code passes all tests in suite
- ✅ Change requests reviewed for alignment with client expectations

**Output:** Feature branch created

---

#### Phase 2: Testing and Stabilization
**Location:** Stage Server  
**Testing Types:**
- Automated test runs
- Manual testing (Client, Lead Engineer, QA team)
- Functional testing
- Scalability testing
- Production-specific concern checks

**Requirements for Phase 2 Completion:**
- ✅ All bugs and aesthetic issues resolved
- ✅ Missing functionality added or deferred
- ✅ Scalability testing meets performance benchmarks
- ✅ All test suite runs complete successfully
- ✅ Client approves software version for production

**Issue Tracking:** All problems logged in Issue Tracker

---

#### Phase 3: Production Deployment
**Scheduled By:** Client and Lead Engineer

**Deployment Steps:**
1. **Backup**
   - Database backed up
   - Resource files (not under version control) backed up

2. **Git Update**
   - Production version updated by switching to next stable branch

3. **Database Migration**
   - Migration scripts applied

4. **Testing**
   - Test suite runs against new production environment
   - If tests fail: Client and Lead decide on hotfixes vs. rollback

5. **Hotfix Process (if needed)**
   - Hotfixes committed to Production stable branch
   - Later merged with master branch

6. **Completion**
   - All tests pass OR rollback completed
   - Server brought back online

7. **Post-Deployment**
   - Lead Engineer reports issues from push
   - Suggests process improvements
   - Recommends additional tests to prevent future problems

---

## Interfaces and Services

### WebScrapers
**Location:** VM `rallc-thedevs`

**Integrated Services:**
- **PDS** - Active
- **Allstate** - Active
- **Old National** - Active
- **BOK** - Currently out of service

**Note:** See Appendix II for manual run instructions and automation schedule

### Parser
**Location:** VM `rallc-parser`

**Note:** See Appendix III for settings detail

---

## Reporting

### Current Reports
- **Total:** Approximately 12 reports
- **Technology:** Powered by stored procedures
- **Features:**
  - Filters available
  - User-initiated export
  - No end-user report builder

**Note:** Full stored procedure documentation available in separate document

---

## Support & Contacts

### Primary Support
**Reinsurance Associates**
- **Contact:** Josie Brewer
- **Phone:** 870.353.7205
- **Email:** josie@reinsuranceassociates.com

### Third-Party Support (HCSS)
**Hammer Consulting & Support Services**

**Becky Hammer**
- **Phone:** 817.925.5833
- **Email:** becky@hammercss.com

**Justin Harmon**
- **Phone:** 718.753.7330
- **Email:** justin.harmon@hammercss.com

---

## Troubleshooting Guide

### User-Reported Errors

**Step 1: Version Check**
- Check version number (lower right corner of portal page)
- Compare to latest version in Teams channel

**Step 2: Browser Cache Reset**
- Log out
- Clear browser cache
- Log back in

**Step 3: Document Error**
- Replicate the error
- Document each step leading to issue
- Take screenshots

**Step 4: Report**
- Email Josie Brewer
- Include brief error description
- Attach relevant screenshots

---

## Release Cycle Process

### Current Process
1. **Identify Changes**
   - RAL requests
   - HCSS recommended maintenance

2. **Define Requirements**

3. **Release Approval**

4. **Development**
   - Work done on Stage site

5. **Testing**
   - RAL testing on Stage site

6. **Production Push**
   - Release pushed to production

---

## Technical Documentation References

### Available Documents
1. **RAL - DB Stored Procedures** (PDF)
   - Complete stored procedure documentation
   - Parameters and return values
   - Usage examples

2. **RAL - REST API Documentation** (PDF)
   - Complete endpoint reference
   - Role-based authorization details
   - Request/response schemas

3. **ERD - RAL Portal 1.0** (DOCX)
   - Complete database schema
   - Table relationships
   - Field definitions

4. **System Documentation - RAL Portal 2.0** (DOCX)
   - This document
   - System overview
   - Support processes

---

## Notes for HCSS Team

### Key Points
- Portal is **critical** for RAL business operations
- System has been in production since 2014-2016
- Technology stack is dated (AngularJS 1.x, Bootstrap 0.12)
- Git-based deployment allows quick rollbacks
- Three-phase release process ensures stability
- All API calls require OAuth token
- File upload is 5-step process with GUID-based naming

### Common Questions to Anticipate
1. **API Integration:** Use OAuth flow documented above
2. **File Upload:** Follow 5-step process exactly
3. **Database Schema:** Reference ERD for table relationships
4. **Deployment:** Follow 3-phase process, never skip testing
5. **Authentication:** JWT tokens expire, handle refresh
6. **Authorization:** Check role requirements per endpoint

---

**Document Compiled:** 2025-11-11  
**Compiled By:** 8825 System  
**Source Files:** 4 technical documents  
**Location:** `focuses/hcss/knowledge/RAL_Portal_Technical_Reference.md`
