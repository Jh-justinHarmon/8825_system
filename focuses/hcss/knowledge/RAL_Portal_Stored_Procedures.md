# RAL Portal - Stored Procedures Documentation
**Source:** RAL - Stored Procedure Documentation.pdf (22 pages)  
**Last Updated:** 2025-11-11  
**Total Procedures:** 47

---

## Table of Contents

1. [Client Management](#client-management)
2. [Bank & Cession Operations](#bank--cession-operations)
3. [Project Management](#project-management)
4. [Reporting](#reporting)
5. [Tax Operations](#tax-operations)
6. [System Utilities](#system-utilities)

---

## Client Management

### 1. ActiveClientLocations
**Purpose:** Searches for currently active client locations

**Tables Consumed:**
- Clients
- ClientLocations
- Locations

---

### 2. ActiveClientsWithNoLocation
**Purpose:** Searches for active clients with no location data

**Tables Consumed:**
- Clients
- ClientLocations
- Locations

---

### 3. Agency Client Licensing Auth List
**Purpose:** Lists agencies authorized to work with specific clients

**Logic:** Searches for clients with user_id of MAX and role name 'Accountant', joins with Users table

**Tables Consumed:**
- Clients
- Agencies
- LicensingAuths
- PublicAccountants
- ClientRoles
- UserRoles
- Users

---

### 4. AgencyContactsPerClient
**Purpose:** Lists agency and contact information for selected client as JSON

**Tables Consumed:**
- Agencies
- AgencyLocations
- ContactLocations
- Contacts

---

### 15. ClientRolesAll
**Purpose:** Lists different specialists assisting each client

**Tables Consumed:**
- Clients
- ClientRoles
- UserRoles
- Users

---

### 16. ClientStatusForAgency
**Purpose:** Finds clients without active projects

**Tables Consumed:**
- ClientContacts
- Projects
- Clients

---

### 17. ClientsWithMissingBankAccountsCessions
**Purpose:** Lists clients with missing bank account sessions

**Tables Consumed:**
- ClientsByAccountant
- ClientBankAccounts
- ClientCessions
- Agencies

---

### 18. ClientTaxStatus
**Purpose:** Lists tax status of client

**Parameters:**
- `TaxYear` (int) - e.g., 2016
- `Agency_ID` (int)

**Tables Consumed:**
- Calendars
- ClientBankAccountsCompleted
- ClientCessionsCompleted
- Clients
- ClientBankAccounts
- EntityEvents
- AppEvents
- Agencies
- ClientRoles
- Users

---

### 14. ClientAttributeReport
**Purpose:** Lists multiple client attributes with related information

**Tables Consumed:**
- Clients
- Agencies
- LicensingAuths
- PublicAccountants
- ClientRoles
- UserRoles
- Users

---

## Bank & Cession Operations

### 7. BankAccountStatus
**Purpose:** Displays bank account status for client

**Parameters:**
- `User_ID` (int)
- `FilterWorkedType` (int)
- `Calendar_ID` (int) - Format: YYYYMMDD
- `ReportInclude` (varchar(50)) - Values: 'rxNotBx', 'received', or 'booked'

**Tables Consumed:**
- ClientBankAccounts
- Calendars
- Clients
- ClientBankAccountDatas
- Banks
- BankAccounts
- Users
- Agencies
- ClientRoles
- BankCessionDeliveries

---

### 8. BankAndCessionStatus
**Purpose:** Lists bank and cession status attributes for client

**Tables Consumed:**
- ClientBankAccounts
- Calendars
- Clients
- ClientBankAccountDatas
- BankAccounts
- ClientRoles
- ClientCessions
- BankCessionFrequencies
- BankCessionDeliveries
- Users
- ClientCession_ID
- Carriers
- Administrator_ID
- InsuranceTypes
- Agencies
- ClientCessionDatas
- CessionInsuranceTypes

---

### 9. BanksCessionCompleteForTaxYear
**Purpose:** Lists completed bank sessions for each tax year

**Tables Consumed:**
- Calendars
- Clients
- ClientBankAccounts
- ClientCessions
- AppEvents
- EntityEvents
- UserRoles
- ClientRoles

---

### 12. CessionStatus
**Purpose:** Displays cession status for client

**Parameters:**
- `User_ID` (int)
- `FilterWorkedType` (int)
- `Calendar_ID` (int) - Format: YYYYMMDD
- `ReportInclude` (varchar(50)) - Values: 'rxNotBx', 'received', or 'booked'

**Tables Consumed:**
- ClientCessions
- Calendars
- BankCessionFrequencies
- ClientCessionDatas
- InsuranceTypes
- Agencies
- Clients
- ClientRoles
- Users
- CessionInsuranceTypes
- Carriers

---

### 11. CessionsProducts_Gap_Warranty
**Purpose:** Lists clients with limited lifetime GAP warranty

**Tables Consumed:**
- ClientCessions
- Clients
- Agencies
- CessionInsuranceTypes
- InsuranceTypes
- ClientCessionDatas

---

### 13. CessionsWithoutProducts
**Purpose:** Lists client sessions without products added

**Tables Consumed:**
- ClientCessions
- Clients
- Agencies
- Administrators
- CessionInsuranceTypes
- InsuranceTypes

---

## Project Management

### 26. GetProjectsStatus
**Purpose:** Retrieves current project status attributes

**Tables Consumed:**
- Projects
- ProjectTasks
- EntityProjects

---

### 34. ProjectList
**Purpose:** Lists current projects with relevant attributes

**Tables Consumed:**
- Users
- DueDays
- Projects
- EntityProjects
- ProjectTasks
- Clients
- Agencies

---

### 35. ProjectMatrixReport
**Purpose:** Generates project report in matrix format

**Tables Consumed:**
- ProjectList
- ProjectTasks
- Projects
- ProjectTaskActivities

---

### 36. ProjectMatrixTaskNames
**Purpose:** Generates matrix of task names for project

**Tables Consumed:**
- ProjectTasks
- Projects
- ProjectTaskActivities

---

### 37. ProjectsListByClientorAgent
**Purpose:** Lists projects for client or agent

**Parameters:**
- `EntityTypeID` (int)

**Tables Consumed:**
- Projects
- EntityProjects
- Users
- StatusTables

---

### 38. ProjectTimeLineData
**Purpose:** Generates project timeline with task info and update dates

**Parameters:**
- `Project_ID` (int)

**Tables Consumed:**
- ProjectTaskActivities
- ProjectTasks
- Users

---

### 39. ProjectViewData
**Purpose:** Lists project attributes from multiple tables

**Parameters:**
- `Project_ID` (int)

**Tables Consumed:**
- Projects
- ProjectTasks
- Users
- UserRoles
- StatusTables

---

### 40. ProjectViewDataByAlertSegment
**Purpose:** Returns empty set from Users table (Deprecated)

**Tables Consumed:**
- Users

---

### 41. ProjectViewDataByClient
**Purpose:** View client project data

**Parameters:**
- `Entity_ID` (int)

**Tables Consumed:**
- Projects
- EntityProjects
- ProjectTasks
- Users
- UserRoles
- StatusTables

---

### 42. ProjectViewDataByUser
**Purpose:** View user project data

**Parameters:**
- `User_ID` (int)

**Tables Consumed:**
- Projects
- EntityProjects
- ProjectTasks
- Users
- UserRoles
- StatusTables

---

### 43. ProjectViewDataByUserByDate
**Purpose:** Lists active projects by DueBy attribute

**Parameters:**
- `User_ID` (int)

**Tables Consumed:**
- Projects
- EntityProjects
- ProjectTasks
- Users
- UserRoles
- StatusTables

---

### 33. ProjectCheckSumsByEntityEvents
**Purpose:** Generates project report with check sums for entity events

**Tables Consumed:**
- EntityEvents
- AppEvents
- Projects

---

## Reporting

### 5. AnnualComplianceStatus
**Purpose:** Queries annual tax compliance status for clients

**Tables Consumed:**
- ProjectTasks
- ContactLocations
- Projects
- Clients
- Agencies

---

### 31. ProductDescReport
**Purpose:** Lists account managers (Accountant, Manager, Owner) with related info

**Tables Consumed:**
- CessionInsuranceTypePeriods
- ClientCessions
- Users
- Carriers
- Administrators
- CessionInsuranceTypes
- InsuranceTypes
- Clients
- ClientRoles

---

### 32. ProductSummaryByCarrierAdminClient
**Purpose:** Generates product summary with carrier, administrator, and client

**Tables Consumed:**
- ClientCessions
- Clients
- Agencies
- Carriers
- Administrators
- CessionInsuranceTypes
- InsuranceTypes
- ClientBankAccounts
- BankAccounts
- Banks
- CessionInsuranceTypePeriods

---

## Tax Operations

### 45. TaxesMailedAndReceived
**Purpose:** Lists client taxes mailed and received dates

**Tables Consumed:**
- ProjectTasks
- Projects
- Clients
- Agencies

---

## Contact Management

### 19. ContactsAfterCleanup
**Purpose:** Cleans up stored client contact data

**Tables Consumed:**
- Clients
- ClientContacts
- Classifications
- Agencies

---

### 20. ContactsByClient
**Purpose:** Lists contacts for each client

**Tables Consumed:**
- Clients
- ClientRALContacts
- Classifications
- Agencies
- RALContacts

---

### 21. CorporateMailMerge
**Purpose:** Returns table with President, VP, Secretary, Treasurer, Shareholders, Directors

**Tables Consumed:**
- Clients
- Locations
- ClientLocations
- RALContacts
- ClientRALContacts

---

### 22. DealershipProducerFlagContacts
**Purpose:** Selects dealerships where producer flag = 1

**Tables Consumed:**
- ClientRALContacts
- RALContacts
- Clients

---

### 25. DirectorOfficerByClient
**Purpose:** Returns officers/directors for client

**Tables Consumed:**
- Clients
- ClientLocations
- Locations
- ClientRALContacts
- RALContacts

---

### 44. ShareholderByClient
**Purpose:** Lists client shareholders (RICShareholderFlag = 1)

**Tables Consumed:**
- Clients
- ClientRALContacts
- RALContacts
- Classifications
- Agencies

---

## System Utilities

### 6. AppEventsLoop
**Purpose:** Lists clients with EntityEventPeriod attribute

**Tables Consumed:**
- F8886_2017
- AppEvents
- EntityEvents
- UserRoles
- ClientRoles

---

### 10. CalendarInsert
**Purpose:** Inserts new entry into Calendars_TD table

**Tables Consumed:**
- Calendars_TD

---

### 23. DestroyTestAgencyUsers
**Purpose:** Deletes test data from database

**Tables Consumed:**
- ProjectTasks
- Users
- AspNetUsers
- AspNetUserRoles
- ClientRoles
- EntityUsers
- Contacts

---

### 24. DetectDuplicates
**Purpose:** Detects duplicate records in Calendars table

**Tables Consumed:**
- Calendars

---

### 27. GetUserClientsWithAccessCheck
**Purpose:** Search agency contacts for selective client access

**Tables Consumed:**
- Contacts
- Users
- RALContacts

---

### 46. TemplateContinuityCheck
**Purpose:** Checks template continuity, returns TaskSequence

**Parameters:**
- `Template_ID` (int)

**Tables Consumed:**
- (Not specified)

---

### 47. UserClientAccessCheck
**Purpose:** Determines if agent has access to client

**Parameters:**
- `username` (VARCHAR(50))
- `clientid` (int)

**Returns:** `HasAccess` attribute (boolean)

**Tables Consumed:**
- Users
- RALContacts
- ClientRALContacts
- Clients

---

## Simple Lookup Procedures

### 28. p_getbyid_client
**Purpose:** Retrieve client name

**Parameters:**
- `Client_ID` (int)

**Tables Consumed:**
- Clients

---

### 29. p_getbyid_clientinsurancetype
**Purpose:** Retrieves client insurance info

**Parameters:**
- `ClientInsuranceType_ID` (int)

**Tables Consumed:**
- ClientInsuranceTypes

---

### 30. p_getbyid_insurancetype
**Purpose:** Retrieves insurance type

**Parameters:**
- `InsuranceType_ID` (int)

**Tables Consumed:**
- InsuranceTypes

---

## Summary Statistics

- **Total Procedures:** 47
- **Client Management:** 10 procedures
- **Bank & Cession:** 7 procedures
- **Project Management:** 11 procedures
- **Reporting:** 3 procedures
- **Contact Management:** 6 procedures
- **Tax Operations:** 1 procedure
- **System Utilities:** 6 procedures
- **Simple Lookups:** 3 procedures

---

## Common Patterns

### Parameter Types
- `int` - Most IDs and numeric values
- `varchar(50)` - Text fields
- `YYYYMMDD` - Date format for Calendar_ID

### Common Tables
- **Clients** - Used in 30+ procedures
- **Users** - Used in 20+ procedures
- **Projects/ProjectTasks** - Used in 15+ procedures
- **Agencies** - Used in 15+ procedures
- **ClientRoles** - Used in 10+ procedures

### Authorization Patterns
- Most procedures respect user roles via ClientRoles/UserRoles joins
- Access control enforced at database level
- Many procedures filter by User_ID parameter

---

**Document Source:** RAL - Stored Procedure Documentation.pdf (22 pages)  
**Extracted:** 2025-11-11  
**Location:** `focuses/hcss/knowledge/RAL_Portal_Stored_Procedures.md`
