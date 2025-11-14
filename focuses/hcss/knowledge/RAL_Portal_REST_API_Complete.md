# RAL Portal - Complete REST API Reference
**Source:** RAL - REST API Documentation.pdf (263 pages)  
**Last Updated:** 2025-11-11  
**Base URL (Stage):** https://rallcstage.azurewebsites.net/api/

---

## Controllers Overview

1. [AccountsController](#accountscontroller) - User account management
2. [AdministratorsController](#administratorscontroller) - Administrator management
3. [AgenciesController](#agenciescontroller) - Agency management
4. [BankAccountsController](#bankaccountscontroller) - Bank account operations
5. [BanksController](#bankscontroller) - Bank management
6. [CalendarsController](#calendarscontroller) - Calendar operations
7. [CarriersController](#carrierscontroller) - Insurance carrier management
8. [CessionInsuranceTypesController](#cessioninsurancetypescontroller) - Cession insurance types
9. [ClientBankAccountsController](#clientbankaccountscontroller) - Client bank accounts
10. [ClientCessionsController](#clientcessionscontroller) - Client cessions
11. [ClientsController](#clientscontroller) - Client management
12. [FilesController](#filescontroller) - File operations
13. [IntakeDocumentController](#intakedocumentcontroller) - Document intake
14. [ProjectsController](#projectscontroller) - Project management
15. [ReportsController](#reportscontroller) - Reporting endpoints

---

## AccountsController
**Route Prefix:** `/api/accounts`

### Purpose
Regulates and manages user account functions within the system.

### Endpoints

#### 1. GetUsers
- **Route:** `/api/accounts/users`
- **Method:** GET
- **Purpose:** Generates a list of active users
- **Authorization:** Admin
- **Returns:** IHttpActionResult

#### 2. GetUser
- **Route:** `/api/accounts/user/{id:guid}`
- **Method:** GET
- **Purpose:** Returns user details by GUID
- **Authorization:** Admin
- **Parameters:** `id` (GUID)
- **Returns:** IHttpActionResult

#### 3. GetUserByName
- **Route:** `/api/accounts/user/{username}`
- **Method:** GET
- **Purpose:** Retrieves user details by username
- **Parameters:** `username` (string)
- **Returns:** Task

#### 4. ResetUser
- **Route:** `/api/accounts/reset`
- **Method:** POST
- **Purpose:** Sends password reset email to user
- **Authorization:** Admin
- **Process:** Calls DoResetUser method, sends email with reset link
- **Returns:** Task

#### 5. DoResetUser
- **Route:** `/api/accounts/reset`
- **Method:** POST (Internal)
- **Purpose:** Internal method that sends reset email
- **Parameters:** User model, UserManager model
- **Returns:** Task

#### 6. ForgotPassword
- **Route:** `/api/accounts/forgot`
- **Method:** POST
- **Purpose:** Initiates forgotten password flow
- **Authorization:** AllowAnonymous
- **Process:** Generates email confirmation token, sends reset instructions
- **Returns:** Task

#### 7. CreateUser
- **Route:** `/api/accounts/create`
- **Method:** POST
- **Purpose:** Creates new user account
- **Authorization:** AllowAnonymous
- **Process:** Validates request, calls DoCreateUser
- **Returns:** Task

#### 8. UpdateUser
- **Route:** `/api/accounts/update`
- **Method:** PUT
- **Purpose:** Updates user profile
- **Authorization:** Admin
- **Returns:** Task

#### 9. ConfirmEmail
- **Route:** `/api/accounts/ConfirmEmail`
- **Method:** POST
- **Purpose:** Confirms user email address
- **Authorization:** AllowAnonymous
- **Process:** Validates email, saves new user if needed
- **Returns:** Task (HTTP 200 OK on success)

#### 10. ChangePassword
- **Route:** `/api/accounts/ResetPassword`
- **Method:** POST
- **Purpose:** Resets user password
- **Returns:** Task

#### 11. DeleteUser
- **Route:** `/api/accounts/user/{id:guid}`
- **Method:** DELETE
- **Purpose:** Allows admin to delete user
- **Authorization:** Admin
- **Parameters:** `id` (GUID string)
- **Returns:** Task

#### 12. AssignRolesToUser
- **Route:** `/api/accounts/user/{id:guid}/roles`
- **Method:** HttpPut
- **Purpose:** Assigns roles to user
- **Authorization:** Admin
- **Parameters:**
  - `id` (string) - User GUID
  - `rolesToAssign` (string array) - Roles to assign
- **Returns:** Task

#### 13. AssignClaimsToUser
- **Route:** `/api/accounts/user/{id:guid}/assignclaims`
- **Method:** POST
- **Purpose:** Assigns claims to user
- **Authorization:** Admin
- **Parameters:**
  - `id` (string) - User GUID
  - Claims list (ClaimBindingModel[])
- **Returns:** Task

#### 14. RemoveClaimsFromUser
- **Route:** `/api/accounts/user/{id:guid}/removeclaims`
- **Method:** POST
- **Purpose:** Removes claims from user
- **Authorization:** Admin
- **Parameters:**
  - `id` (string) - User GUID
  - Claims list (ClaimBindingModel[])
- **Returns:** Task

---

## FilesController
**Route Prefix:** `/api/files`

### Purpose
Handles file upload and download operations, particularly for statement processing.

### Key Endpoints

#### UploadStatement
- **Route:** `/api/files/uploadStatement/?name={guid_filename}`
- **Method:** POST
- **Purpose:** Uploads statement file to Azure storage for automation engine processing
- **Parameters:**
  - Query String: `name` - GUID filename from intakeDocument creation
  - Form Data: Binary PDF file
- **Content-Type:** multipart/form-data
- **Authorization:** Bearer token required
- **Returns:** HTTP 200 OK on success
- **Process:** Sends file to Azure intakeDocumentStorage container

---

## IntakeDocumentController
**Route Prefix:** `/api/intakeDocument`

### Purpose
Manages document intake workflow for statement processing automation.

### Endpoints

#### 1. Create IntakeDocument
- **Route:** `/api/intakeDocument/`
- **Method:** POST
- **Purpose:** Creates intake document record for uploaded statement
- **Content-Type:** application/json
- **Payload:**
```json
{
  "originalFileName": "statement.pdf",
  "OriginationSource": "email"
}
```
- **Returns:** HTTP 200 OK with intakeDocument object (includes generated GUID filename)
- **Authorization:** Bearer token required

#### 2. Update IntakeDocument
- **Route:** `/api/intakeDocument/`
- **Method:** PUT
- **Purpose:** Updates intake document status (typically to "Waiting" for automation engine)
- **Content-Type:** application/json
- **Payload:** Full intakeDocument object with modified status
- **Returns:** HTTP 200 OK with updated intakeDocument record
- **Authorization:** Bearer token required

### IntakeDocument Schema
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
  "status": "",
  "year": ""
}
```

---

## IntakeDocumentLogController
**Route Prefix:** `/api/intakeDocumentLog` or `/api/DocumentIntakeLogs`

### Purpose
Tracks document intake progress for debugging and monitoring automation engine.

### Endpoints

#### Create IntakeDocumentLog
- **Route:** `/api/intakeDocumentLog/` or `/api/DocumentIntakeLogs`
- **Method:** POST
- **Purpose:** Creates log entry for intake document processing
- **Content-Type:** application/json
- **Payload:**
```json
{
  "status": "UPLOADING",
  "type": "INTAKE",
  "description": "Uploading file statement.pdf to intake",
  "filepath": "ralstage",
  "filename": "d377ce77-ee09-47a1-8110-a786a03da605.pdf"
}
```
- **Returns:** HTTP 201 Created with intakeDocument and log entry
- **Authorization:** Bearer token required

### Status Values
- `UPLOADING` - File upload in progress
- `PARSING` - Document being parsed by automation engine
- `FAULTED` - Error occurred during processing
- `COMMIT_ERROR` - Database commit failed
- `DISCARDED` - File discarded (invalid/duplicate)
- `ABORTED` - Process manually aborted
- `FINISHED` - Processing completed successfully
- `COMMITTED` - Successfully committed to database

### Environment Values
- `ralstage` - Stage environment
- `ralprod` - Production environment

---

## ClientsController
**Route Prefix:** `/api/clients`

### Purpose
Manages client records and related operations.

### Common Endpoints
- GET `/api/clients` - List all clients
- GET `/api/clients/{id}` - Get client by ID
- POST `/api/clients` - Create new client
- PUT `/api/clients/{id}` - Update client
- DELETE `/api/clients/{id}` - Delete client

**Note:** Full endpoint details available in source documentation (263 pages total)

---

## ProjectsController
**Route Prefix:** `/api/projects`

### Purpose
Manages project workflow, tasks, and status tracking.

### Common Operations
- Project creation and updates
- Task assignment and tracking
- Status management
- Timeline data
- Project-client associations

---

## ReportsController
**Route Prefix:** `/api/reports`

### Purpose
Generates various reports powered by stored procedures.

### Report Types
- Bank account status reports
- Cession status reports
- Tax compliance reports
- Project status reports
- Client attribute reports

**Note:** Approximately 12 reports available, all powered by stored procedures with filter capabilities

---

## Stored Procedures

### Overview
Stored procedures are utilized to perform complex data operations and reporting tasks within the RAL Portal. Below is a list of key stored procedures and their purposes.

#### Procedure Name #1: ActiveClientLocations
- **Description:** Searches for currently active client locations.
- **Tables Consumed:** Clients, ClientLocations, Locations

#### Procedure Name #2: ActiveClientsWithNoLocation
- **Description:** Searches for active clients with no location data.
- **Tables Consumed:** Clients, ClientLocations, Locations

#### Procedure Name #3: Agency Client Licensing Auth List
- **Description:** Searches for clients with a user_id of MAX, and with a role name of ‘Accountant’ from the client roles table, and joins it with data from the Users table to create a table representing which agencies are authorized to work with which clients.
- **Tables Consumed:** Clients, Agencies, LicensingAuths, PublicAccountants, ClientRoles, UserRoles, Users

#### Procedure Name #4: AgencyContactsPerClient
- **Description:** Lists the agency, and contact information of a selected client as JSON values.
- **Tables Consumed:** Agencies, AgencyLocations, ContactLocations, Contacts

#### Procedure Name #5: AnnualComplianceStatus
- **Description:** Queries information representing the annual tax compliance status of the clients stored in the “Clients” table.
- **Tables Consumed:** ProjectTasks, ContactLocations, Projects, Clients, Agencies

#### Procedure Name #6: AppEventsLoop
- **Description:** Lists clients that have an associated “EntityEventPeriod” attribute stored.
- **Tables Consumed:** F8886_2017, AppEvents, EntityEvents, UserRoles, ClientRoles

#### Procedure Name #7: BankAccountStatus
- **Description:** Displays attributes representing the bank account status of a given client, requires input in the form of “User_ID” as an int, “Filter-WorkedType” as an int, “Calendar_ID” as an int in the following format: ‘YYYYMMDD’, and “ReportInclude” as a varchar(50) the “ReportInclude” attribute specified as ‘rxNotBx’, ‘received’, or ‘booked’.
- **Tables Consumed:** ClientBankAccounts, Calendars, Clients, ClientBankAccountDatas, Banks, BankAccounts, Users, Agencies, ClientRoles, BankCessionDeliveries

#### Procedure Name #8: BankAndCessionStatus
- **Description:** Lists multiple attributes relevant to the bank and cession status of a client.
- **Tables Consumed:** ClientBankAccounts, Calendars, Clients, ClientBankAccountDatas, BankAccounts, ClientRoles, ClientCessions, BankCessionFrequencies, BankCessionDeliveries, Users, ClientCession_ID, Carriers, Administrator_ID, InsuranceTypes, Agencies, ClientRoles, ClientCessionDatas, CessionInsuranceTypes

#### Procedure Name #9: BanksCessionCompleteForTaxYear
- **Description:** Lists the completed bank sessions for each tax year.
- **Tables Consumed:** Calendars, Clients, ClientBankAccounts, ClientCessions, AppEvents, EntityEvents, UserRoles, ClientRoles

#### Procedure Name #10: CalendarInsert
- **Description:** Inserts a new entry into the “Calendars_TD” table.
- **Tables Consumed:** Calendars_TD

#### Procedure Name #11: CessionsProducts_Gap_Warranty
- **Description:** Lists clients who currently have a limited lifetime GAP warranty.
- **Tables Consumed:** ClientCessions, Clients, Agencies, CessionInsuranceTypes, InsuranceTypes, ClientCessionDatas

#### Procedure Name #12: CessionStatus
- **Description:** Displays attributes representing the session status of a given client, requires input in the form of “User_ID” as an int, “FilterWorked-Type” as an int, “Calendar_ID” as an int in the following format: ‘YYYYMMDD’, and “ReportInclude” as a varchar(50) the “Report-Include” attribute specified as, ‘rxNotBx’, ‘received’, or ‘booked’.
- **Tables Consumed:** ClientCessions, Calendars, BankCessionFrequencies, ClientCessionDatas, InsuranceTypes, Agencies, Clients, ClientRoles, Users, CessionInsuranceTypes, Carriers

#### Procedure Name #13: CessionsWithoutProducts
- **Description:** Lists client sessions without products currently added.
- **Tables Consumed:** ClientCessions, Clients, Agencies, Administrators, CessionInsuranceTypes, InsuranceTypes

#### Procedure Name #14: ClientAttributeReport
- **Description:** Lists multiple client attributes along with other relevant information.
- **Tables Consumed:** Clients, Agencies, LicensingAuths, PublicAccountants, ClientRoles, UserRoles, Users

#### Procedure Name #15: ClientRolesAll
- **Description:** Lists the different specialists assisting each client.
- **Tables Consumed:** Clients, ClientRoles, UserRoles, Users

#### Procedure Name #16: ClientStatusForAgency
- **Description:** Searches for clients that currently do not have an active project associated with their account.
- **Tables Consumed:** ClientContacts, Projects, Clients

#### Procedure Name #17: ClientsWithMissingBankAccountsCessions
- **Description:** Lists clients with missing bank account sessions.
- **Tables Consumed:** ClientsByAccountant, ClientBankAccounts, ClientCessions, Agencies

#### Procedure Name #18: ClientTaxStatus
- **Description:** Lists the tax status of a given client, requires input in the form of the “TaxYear” as an int (ex: 2016), and the Agency_ID as an int.
- **Tables Consumed:** Calendars, ClientBankAccountsCompleted, ClientCessionsCompleted, Clients, ClientBankAccounts, EntityEvents, AppEvents, Agencies, ClientRoles, Users

#### Procedure Name #19: ContactsAfterCleanup
- **Description:** Cleans up the stored data for client contacts.
- **Tables Consumed:** Clients, ClientContacts, Classifications, Agencies

#### Procedure Name #20: ContactsByClient
- **Description:** Lists the contacts associated with each client.
- **Tables Consumed:** Clients, ClientRALContacts, Classifications, Agencies, RALContacts

#### Procedure Name #21: CorporateMailMerge
- **Description:** Returns a table listing attributes such as President, Vice President, Secretary, Treasurer, Shareholders, and Directors, associated with a Client_ID & name.
- **Tables Consumed:** Clients, Locations, ClientLocations, RALContacts, ClientRALContacts

#### Procedure Name #22: DealershipProducerFlagContacts
- **Description:** Selects dealerships where the dealership producer flag attribute is equal to “1” along with relevant info.
- **Tables Consumed:** ClientRALContacts, RALContacts, Clients

#### Procedure Name #23: DestroyTestAgencyUsers
- **Description:** Deletes test data from database.
- **Tables Consumed:** ProjectTasks, Users, AspNetUsers, AspNetUserRoles, ClientRoles, EntityUsers, Contacts

#### Procedure Name #24: DetectDuplicates
- **Description:** Detects duplicate records in the Calendars table.
- **Tables Consumed:** Calendars

#### Procedure Name #25: DirectorOfficerByClient
- **Description:** Returns a table listing attributes such as President, Vice President, Secretary, Treasurer, Shareholders, and Directors, associated with a Client_ID & name.
- **Tables Consumed:** Clients, ClientLocations, Locations, ClientRALContacts, RALContacts

#### Procedure Name #26: GetProjectsStatus
- **Description:** Retrieves attributes from various tables, together representing the current status of a project.
- **Tables Consumed:** Projects, ProjectTasks, EntityProjects

#### Procedure Name #27: GetUserClientsWithAccessCheck
- **Description:** Search agency contacts to see if there’s selective client access.
- **Tables Consumed:** Contacts, Users, RALContacts

#### Procedure Name #28: p_getbyid_client
- **Description:** Retrieve client name, requires input in the form of the “Client_ID” as an int.
- **Tables Consumed:** Clients

#### Procedure Name #29: p_getbyid_clientinsurancetype
- **Description:** Retrieves client insurance info, requires input in the form of “ClientInsuranceType_ID” as an int.
- **Tables Consumed:** ClientInsuranceTypes

#### Procedure Name #30: p_getbyid_insurancetype
- **Description:** Retrieves type of insurance, requires input in the form of “InsuranceType_ID” as an int.
- **Tables Consumed:** InsuranceTypes

#### Procedure Name #31: ProductDescReport
- **Description:** Lists the different account managers associated with a client, such as the Accountant, Manager, and Owner, along with other related information.
- **Tables Consumed:** CessionInsuranceTypePeriods, ClientCessions, Users, Carriers, Administrators, CessionInsuranceTypes, InsuranceTypes, Clients, ClientRoles

#### Procedure Name #32: ProductSummaryByCarrierAdminClient
- **Description:** Generates a product summary involving the carrier, administrator and client involved with a product along with multiple relevant attributes.
- **Tables Consumed:** ClientCessions, Clients, Agencies, Carriers, Administrators, CessionInsuranceTypes, InsuranceTypes, ClientBankAccounts, BankAccounts, Banks, CessionInsuranceTypePeriods

#### Procedure Name #33: ProjectCheckSumsByEntityEvents
- **Description:** Generates a project report representing check sums associated with entity events.
- **Tables Consumed:** EntityEvents, AppEvents, Projects

#### Procedure Name #34: ProjectList
- **Description:** Lists current projects along with relevant attributes from the Projects table, along with attributes from other tables related to the current project.
- **Tables Consumed:** Users, DueDays, Projects, EntityProjects, ProjectTasks, Clients, Agencies

#### Procedure Name #35: ProjectMatrixReport
- **Description:** Generates a project report in the form of a matrix.
- **Tables Consumed:** ProjectList, ProjectTasks, Projects, ProjectTaskActivities

#### Procedure Name #36: ProjectMatrixTaskNames
- **Description:** Generates a matrix representing task names associated with a project.
- **Tables Consumed:** ProjectTasks, Projects, ProjectTaskActivities

#### Procedure Name #37: ProjectsListByClientorAgent
- **Description:** Lists projects involved with either a client or agent, requires input in the form of the “EntityTypeID” as an int.
- **Tables Consumed:** Projects, EntityProjects, Users, StatusTables

#### Procedure Name #38: ProjectTimeLineData
- **Description:** Generates a project time line listing the task info, update dates, and user associated with a project. Requires input in the form of a “Project_ID” as an int.
- **Tables Consumed:** ProjectTaskActivities, ProjectTasks, Users

#### Procedure Name #39: ProjectViewData
- **Description:** Lists the multiple attributes from multiple tables associated with a project, requires input in the form of the “Project_ID” as in int.
- **Tables Consumed:** Projects, ProjectTasks, Users, UserRoles, StatusTables

#### Procedure Name #40: ProjectViewDataByAlertSegment
- **Description:** Returns an empty set of data from the Users table. (Deprecated)
- **Tables Consumed:** Users

#### Procedure Name #41: ProjectViewDataByClient
- **Description:** View client project data, requires input in the form of the “Entity_ID” as an int.
- **Tables Consumed:** Projects, EntityProjects, ProjectTasks, Users, UserRoles, StatusTables

#### Procedure Name #42: ProjectViewDataByUser
- **Description:** View user project data, requires input in the form of the “User_ID” as an int.
- **Tables Consumed:** Projects, EntityProjects, ProjectTasks, Users, UserRoles, StatusTables

#### Procedure Name #43: ProjectViewDataByUserByDate
- **Description:** Lists currently active projects by “DueBy” attribute, requires input in the form of the “User_ID” as an int.
- **Tables Consumed:** Projects, EntityProjects, ProjectTasks, Users, UserRoles, StatusTables

#### Procedure Name #44: ShareholderByClient
- **Description:** Lists clients who are shareholders along with relevant info, where the “RICShareholderFlag” attribute is set to “1”, indicating that the client is a shareholder.
- **Tables Consumed:** Clients, ClientRALContacts, RALContacts, Classifications, Agencies

#### Procedure Name #45: TaxesMailedAndReceived
- **Description:** Lists client taxes that have been mailed, and the day that they were received, along with relevant attributes pertaining to this query.
- **Tables Consumed:** ProjectTasks, Projects, Clients, Agencies

#### Procedure Name #46: TemplateContinuityCheck
- **Description:** Checks the continuity of a given template. Requires as input a “Template_ID” as an int. Returns the current “TaskSequence”.
- **Tables Consumed:** 

#### Procedure Name #47: UserClientAccessCheck
- **Description:** Determines whether an agent has access to a client, returns a “HasAccess” attribute representing whether the access exists between the client and agent. Requires input in the form of a “username” as a VARCHAR(50), and a clientid as an int.
- **Tables Consumed:** Users, RALContacts, ClientRALContacts, Clients

---

## Authentication Flow

### OAuth 2.0 Token Endpoint
- **Route:** `/oauth/token`
- **Method:** POST
- **Content-Type:** application/x-www-form-urlencoded

**Parameters:**
```
grant_type=client_credentials
client_id=a934a88b4bed4a12g7d888f5c43dcb68
client_secret=a1zdabwfPpFcFdMft6asfzLkO1aa_K9vKe9SJezPwWs
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

**Usage:**
All API requests must include:
```
Authorization: Bearer {access_token}
```

### Token Management
- Tokens are JWT (JSON Web Tokens)
- Tokens expire after specified duration
- Token includes user role information
- Each request revalidates token server-side
- Invalid token → Request rejected with 401 Unauthorized

---

## Authorization Roles

### Admin
- Full system access
- User management
- Role assignment
- System configuration

### Accountant
- Client data access
- Financial reporting
- Tax compliance tracking

### Manager
- Project management
- Task assignment
- Team oversight

### Client (Read-Only)
- View own data
- Limited reporting access

### Agent (Read-Only)
- View assigned client data
- Limited access based on client assignments

**Note:** Each endpoint defines required role. Unauthorized requests return 403 Forbidden.

---

## Common Response Codes

- **200 OK** - Request successful
- **201 Created** - Resource created successfully
- **400 Bad Request** - Invalid request data
- **401 Unauthorized** - Missing or invalid token
- **403 Forbidden** - Insufficient permissions
- **404 Not Found** - Resource not found
- **500 Internal Server Error** - Server error

---

## File Upload Workflow (Complete)

### Step 1: Get OAuth Token
```
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&client_id=...&client_secret=...
```

### Step 2: Create IntakeDocument
```
POST /api/intakeDocument/
Authorization: Bearer {token}
Content-Type: application/json

{
  "originalFileName": "statement.pdf",
  "OriginationSource": "email"
}
```
**Response:** intakeDocument object with GUID filename

### Step 3: Create IntakeDocumentLog
```
POST /api/intakeDocumentLog/
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "UPLOADING",
  "type": "INTAKE",
  "description": "Uploading file statement.pdf to intake",
  "filepath": "ralstage",
  "filename": "{guid_from_step_2}.pdf"
}
```

### Step 4: Upload File
```
POST /api/files/uploadStatement/?name={guid_from_step_2}.pdf
Authorization: Bearer {token}
Content-Type: multipart/form-data

[Binary PDF data]
```

### Step 5: Update Status to Waiting
```
PUT /api/intakeDocument/
Authorization: Bearer {token}
Content-Type: application/json

{
  ...intakeDocument_from_step_2,
  "status": "Waiting"
}
```

**Result:** Automation engine processes file from Azure storage

---

## Error Handling

### Common Error Responses

**Authentication Failed:**
```json
{
  "error": "invalid_grant",
  "error_description": "The user name or password is incorrect."
}
```

**Unauthorized Access:**
```json
{
  "message": "Authorization has been denied for this request."
}
```

**Validation Error:**
```json
{
  "message": "The request is invalid.",
  "modelState": {
    "field": ["Error message"]
  }
}
```

---

## Rate Limiting & Best Practices

1. **Token Reuse:** Cache and reuse tokens until expiration
2. **Error Handling:** Implement retry logic with exponential backoff
3. **File Size:** Limit file uploads to reasonable sizes
4. **Batch Operations:** Use batch endpoints when available
5. **Pagination:** Use pagination for large result sets

---

## Additional Controllers

**Note:** The complete API includes 15+ controllers with 100+ endpoints total. Key controllers documented above. Full details available in 263-page source document.

### Other Controllers Include:
- AdministratorsController
- AgenciesController
- BankAccountsController
- BanksController
- CalendarsController
- CarriersController
- CessionInsuranceTypesController
- ClientBankAccountsController
- ClientCessionsController
- And more...

---

**Document Source:** RAL - REST API Documentation.pdf (263 pages)  
**Extracted:** 2025-11-11  
**Location:** `focuses/hcss/knowledge/RAL_Portal_REST_API_Complete.md`