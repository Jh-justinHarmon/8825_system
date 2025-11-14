# RAL Portal - Complete Database Schema (ERD)
**Source:** ERD - RAL Portal 1.0.docx (OCR Extracted)
**Extracted:** 2025-11-11
**Total Diagrams:** 35

---

## Table of Contents

1. [Administrators](#image-019---administrators)
2. [Agencies](#image-019---agencies)
3. [AgencyLocations](#image-019---agencylocations)
4. [AppEvents](#image-005---appevents)
5. [AspNetUserClaims](#image-007---aspnetuserclaims)
6. [AspNetUserLogins](#image-007---aspnetuserlogins)
7. [AspNetUsers](#image-007---aspnetusers)
8. [BSMatrices](#image-005---bsmatrices)
9. [BankAccounts](#image-029---bankaccounts)
10. [BankCessionDeliveries](#image-033---bankcessiondeliveries)
11. [BankCessionFrequencies](#image-033---bankcessionfrequencies)
12. [BankLocations](#image-029---banklocations)
13. [Banks](#image-029---banks)
14. [BaseTables](#image-003---basetables)
15. [Calendars](#image-001---calendars)
16. [Carriers](#image-024---carriers)
17. [ClientBankAccounts](#image-015---clientbankaccounts)
18. [ClientCessionDatas](#image-033---clientcessiondatas)
19. [ClientCessions](#image-033---clientcessions)
20. [ClientLocations](#image-015---clientlocations)
21. [ClientRoles](#image-022---clientroles)
22. [ContactLocations](#image-024---contactlocations)
23. [DismissedAlerts](#image-005---dismissedalerts)
24. [DueDayChanges](#image-030---duedaychanges)
25. [DueDays](#image-030---duedays)
26. [EntityTypes](#image-002---entitytypes)
27. [FinalResult](#image-023---finalresult)
28. [LicensingAuthLocations](#image-011---licensingauthlocations)
29. [LicensingAuths](#image-011---licensingauths)
30. [ProjectTasks](#image-017---projecttasks)
31. [ProjectTemplateTasks](#image-017---projecttemplatetasks)
32. [RALContacts](#image-012---ralcontacts)
33. [ReinsuranceManagerLocations](#image-032---reinsurancemanagerlocations)
34. [ReinsuranceManagers](#image-032---reinsurancemanagers)
35. [RelatedTables](#image-003---relatedtables)
36. [States](#image-024---states)
37. [TaxCalcData](#image-034---taxcalcdata)
38. [TaxCalcData2018](#image-021---taxcalcdata2018)
39. [TaxClientFormLog](#image-034---taxclientformlog)
40. [TemplateTaskActions](#image-006---templatetaskactions)
41. [Templates](#image-006---templates)
42. [UserActivityTokens](#image-026---useractivitytokens)
43. [UserRoleAssignments](#image-026---userroleassignments)
44. [Users](#image-026---users)
45. [__MigrationHistory](#image-005---__migrationhistory)

---

## Image 000 - Diagram 0

**Source Image:** `erd_page_000.png`

### OCR Extracted Text
```
2017 TAX DATA

[dbo]. [TaxCalcData2017_old]

Client] [varchar](255) NULL

[dbo].[TaxCalcData201 7]

Client] [varchar](255) NULL

EIN] [varchar(255) NULL EIN] [varchar(255) NULL

OVERPAYMENT TO C/Y] [money] NULL OVERPAYMENT] [money] NULL
1st Quarter] [money] NULL Q1] [money] NUL
2nd Quarter] [money] NULL Q2] [money] NUL

3rd Quarter] [money] NULL Q3] [money] NULL

4th Quarter] [money] NULL @4] [money] NULL

Amount Deposited with Extension] [money] NULL

Extension] [money] NULL

FQ] [varchar((255) NUL InsuranceLicenceDate] [datetime] NULL

varchar](255) NU Client_id] [int] NULL
varchar](255) NU

varchar](255) NU

[dbo]. [TaxClientFormLog_2017]
Px | CONSTRAINT [PK_TaxClientFormLog] C

TaxClientFormLog_ID] [int] IDENTITY(1,1)

varchar](255) NU
varchar](255) NU

varchar(255) NU Client_ID] [int] NOT NULL

varchar|(255) NU Year] [int] NOT NULL

varchar(255) NU FormCreated] [int] NOT NULL

warehar255)NU ProjectCreated] [int] NOT NULL

varchar](255) NU

TaxClientFormLog_ID] ASC
varchar](255) NU

varchar](255) NU
varchar](255) NU
varchar](255) NU

varchar](255) NU

varchar](255) NU

Clients

[dbo]. [TaxClientsNew2017]

[ClientName] [varchar](255) NULL Client_ID

[Client_ID] [float] NULL
```

---

## Image 001 - Calendars

**Source Image:** `erd_page_001.png`

**Tables in this diagram:** Calendars

### OCR Extracted Text
```
CALENDARS

[dbo].[Calendars] [dbo]. [Calendars_TD]

Px | CONSTRAINT [PK_dbo.Calendars] CLUSTERED Px | CONSTRAINT [PK_dbo.Calendarsff] CLUSTERED}

Calendar_ID] [int] IDENTITY(1,1) NOT NULL PK | [Calendar_ID] [int] IDENTITY(1,1) NOT NULL
CalendarDate] [datetime] NOT NULL CalendarDate] [datetime] NOT NULL

Year] [int] NOT NULL Year] [int] NOT NULL

YearMonth] [int] NOT NULL YearWeek] [int] NULL

Quarter] [int] NOT NULL YearMonth] [int] NOT NULL

QuarterDescription] [varchar](2) NULL YearQuarter] [int] NULL

MonthName] [varchar](10) NULL Quarter] [int] NOT NULL

Month] [int] NOT NULL QuarterDescription] [varchar](2) NULL
LastMonthofQuarter] [int] NOT NULL MonthName] [varchar](10) NULL
Week] [int] NOT NULL Month] [int] NOT NULL

DayOfYear] [int] NOT NULL LastMonthofQuarter] [int] NOT NULL
DayOfQuarter] [int] NOT NULL Week] [int] NOT NULL

DayOfMonth] [int] NOT NULL DayOfYear] [int] NOT NULL

DayOfWeek] [int] NOT NULL DayOfQuarter] [int] NOT NULL

DayNameOfWeek] [varchar(10) NULL DayOfMonth] [int] NOT NULL

YearQuarter] [int] NOT NULL DayOfWeek] [int] NOT NULL

YearWeek] [int] NOT NULL DayNameOfWeek] [varchar(10) NULL

Calendar_ID] ASC Calendar_ID] ASC
```

---

## Image 002 - EntityTypes

**Source Image:** `erd_page_002.png`

**Tables in this diagram:** EntityTypes

### OCR Extracted Text
```
ENTITY

[dbo]. [EntityEvents] [dbo]. [EntityUsers]
Px | CONSTRAINT [PK_dbo.EntityEvents] CLUSTERE! Px | CONSTRAINT [PK_dbo.EntityUsers] CLUSTERED

EntityEvent_ID] [int] IDENTITY(1,1) NOT NULL EntityUser_ID] [int] IDENTITY(1,1) NOT NULL

EntityType_ID] [int] NOT NULL

User_ID] [int] NOT NULL

Entity_ID] [int] NOT NULL EntityType_ID] [int] NOT NULL

AppEvent_ID] [int] NOT NULL

Entity_ID] [int] NOT NULL

EntityEventPeriod] [int] NOT NULL UserOrganizationld] [varchar](255) NULL

EntityEventCreatedDate] [datetine] NOT NULL Contact_ID] [int] NULL

Project_ID] [int] NOT NULL EntityUser_ID] ASC

ProjectlaskChecksum] [int] NULL

EntityEvent_ID] ASC
[dbo]. [EntityLockouts]
Px | CONSTRAINT [PK_dbo.EntityLockouts] CLUSTER

EntityLockout_ID] [int] IDENTITY(1,1) NOT NULL

[dbo]. [EntityRelations]

EntityType_ID] [int] NOT NULL
CONSTRAINT [PK_dbo.EntityRelations] CLUSTER

; ; ; Entity_ID] [int] NOT NULL
EntityRelation_ID] [int] IDENTITY(1,1) NOT NULL

; ; | ControllerName] [varchar(255) NOT NULL
EntityRelationType_ID] [int] NOT NULL

— ‘ User_ID] [int] NOT NULL
HomeEntityType_ID] [int] NOT NULL

; . IsActive] [bit] NOT NULL
HomeEntity_ID] [int] NOT NULL

; | ActiveStartDateTime] [datetime] NOT NULL
RelatedEntityType_ID] [int] NOT NULL

; | LastActivityDateTime] [datetine] NOT NULL
RelatedEntity_ID] [int] NOT NULL

; | EntityLockout_ID] ASC
ActiveFromDate] [datetime] NOT NULL

ActiveToDate] [datetime] NULL

EntityRelationDescription] [varchar(255) NOT NULL]

[dbo].[EntityTypes]
Px | CONSTRAINT [PK_dbo.EntityTypes] CLUSTERED

[EntityType_1D] [int] IDENTITY(1,1) NOT NULL

[EntityTypeName] [varchar(25) NOT NULL
[dbo]. [EntityRelationTypes]
[EntityType_ID] ASC
CONSTRAINT [PK_dbo.EntityRelationTypes] CLUS

[EntityRelationType_ID] [int] IDENTITY(1,1) NOT NUL

[EntityRelationTypeName] [varchar(25) NOT NULL .
Projects AppEvents
[EntityRelationType_ID] ASC Project_ID AppEvent_ID

EntityRelation_ID] ASC
```

---

## Image 003 - BaseTables

**Source Image:** `erd_page_003.png`

**Tables in this diagram:** RelatedTables, BaseTables

### OCR Extracted Text
```
TABLES

[dbo].[BaseTables]

Px | CONSTRAINT [PK_dbo.BaseTables] CLUSTERED

[dbo].[RelatedTables]

Px | CONSTRAINT [PK_dbo.RelatedTables] CLUSTER!

[RelatedTableld] [int] IDENTITY(1,1) NOT NULL BaseTableld] [int] IDENTITY(1,1) NOT NULL

[RelatedTableld] ASC RelatedTableld] [int] NOT NULL

otherld] [int] NOT NULL

RelatedTable_RelatedTableld] [int] NULL

[dbo]. [StatusTables]

Px | CONSTRAINT [PK_dbo.StatusTables] CLUSTERE

RelatedTable 1_RelatedTableld] [int] NULL

BaseTableld] ASC

[Status_|D] [int] IDENTITY(1,1) NOT NULL

[StatusName] [varchar(50) NOT NULL
[StatusDesc] [varchar](100) NULL

[Status_ID] ASC
```

---

## Image 004 - Diagram 4

**Source Image:** `erd_page_004.png`

### OCR Extracted Text
```
CONSTRAINT [PK_ dbo. Bankscession2016] CL

[BankCession2016_1D) [int] IDENTITY (1,1) NOT N

[BankDataw] [varchar](255) NULL

[Accountant] [varchar] (255) NULL
[Agency] [varchar](255) NULL

[Client] [varchar)(255) NULL

[Bankinsurer] [varchar](255) NULL

[AccountNumberProduct] [varchar](255) NULL

[Contact] [varchar](255) NULL

[Contactemail] [varchar](255) NULL

[DOCUMENTSRCVD] [varchar](255) NULL

[Login] [varchar](255) NULL.
(JAN_R] [varchar](255) NULL
(JAN_B] [varchar](255) NULL
[FEB_R] [varchar](255) NULL.
[FEB_B] [varchar](255) NULL
[MAR_R] [varchar](255) NULL.
[MAR_B] [varchar](255) NULL.
[APR_R] [varchar](255) NULL.
[APR_B] [varchar](255) NULL
[MAY _R] [varchar](255) NULL.
[MAY _B] [varchar](255) NULL
(JUN_R] [varchar](255) NULL.
(JUN_B] [varchar](255) NULL
(JUL_R] [varchar](255) NULL
(JUL_B) [varchar](255) NULL
[AUG_R] [varchar](255) NULL.
[AUG_B] [varchar](255) NULL
[SEP_R] [varchar](255) NULL
[SEP_B] [varchar](255) NULL.
[OCT_R] [varchar](255) NULL
[OCT_B] [varchar](255) NULL.
[NOV_R] [varchar](255) NULL.
[NOV_B] [varchar](255) NULL
[DEC_R] [varchar](255) NULL
[DEC_B] [varchar](255) NULL
[Quarterly] [bit] NULL.
[JAN_R_Date] [date] NULL.
(JAN_B Date] [date] NULL
[FEB_R_Date] [date] NULL
[FEB_B_Date] [date] NULL
[MAR_R_Date] [date] NULL
[MAR_B_Date] [date] NULL
[APR_R_Date] [date] NULL
[APR_B_Date] [date] NULL
[MAY _R_Date] [date] NULL

[MAY _B Date] [date] NULL

CESSIONS P2

NOTE: The table on
the right, is simply the

second half of the table on the
left, since the attributes were
too long to fit on one page.

[JUN_R_Date] [date] NULL
[JUN_B_Date] [date] NULL.
[JUL_R_Date] [date] NULL

[JUL_B_Date] [date] NULL

[AUG_R_Date] [date] NULL
[AUG_B_Date] [date] NULL
[SEP_R_Date] [date] NULL
[SEP_B_Date] [date] NULL
[OCT_R_Date] [date] NULL
[OCT_B_Date] [date] NULL
[NOV_R_Date] [date] NULL
[NOV_B_Date] [date] NULL
[DEC_R_Date] [date] NULL
[DEC_B_Date] [date] NULL

[BS_D] fint] NOT NULL

[Client_1D} fint] NULL

[BankData] [bit] NULL

[BankCession2016_ID] ASC
```

---

## Image 005 - __MigrationHistory

**Source Image:** `erd_page_005.png`

**Tables in this diagram:** DismissedAlerts, BSMatrices, __MigrationHistory, AppEvents

### OCR Extracted Text
```
MISC P2

[dbo].[__MigrationHistory] [dbo].[DismissedAlerts]
CONSTRAINT [PK dbo. MiarationHistory2] CLUSTERED CONSTRAINT [PK dbo. DismissedAlerts] CLUSTERED

(Migration! d] [nvarchar](150) NOT NULL [DismissedAlerts_ID] [int] IDENTITY (1,1) NOT NULL
[ContextKey] [nvarchar](300) NOT NULL {User_ID) fint] NOT NULL

[Model] [varbinary](max) NOT NULL [DismissedDate] [datetime] NOT NULL
[ProductVersion] [nvarchar](32) NOT NULL [DismissedType] fint] NOT NULL

[Migration!d] ASC [DismissedAlerts_ID] ASC

[Contextkey] ASC

[dbo].[BSMatrices]
CONSTRAINT [PK_dbo.BSMatrices] CLUSTERED

[BSMatrix_|D] [int] IDENTITY(1,1) NOT NULL

[dbo].[AppEvents]

CONSTRAINT [PK_dbo.AppEvents] CLUSTERED
[AppEvent_[D] fint] IDENTITY (4,1) NOT NULL [Client_1D) fint] NOT NULL
[EventName] [varchar](100) NOT NULL {Carrier_1D) fint] NOT NULL
[EventFrequency] [varchar](100) NOT NULL [InsuranceType_|D] [int] NOT NULL
[ProjectTemplate_ID] [int] NOT NULL [Administrator_ID] [int] NOT NULL
[EventFrequencyDateNum] [int] NULL [InsuranceTypedesc] [varchar](8000) NULL
{EntityType_ID] [int] NOT NULL [InsuranceTypeContact] [varchar] (8000) NULL
{Entity_|D) [int] NOT NULL [MGAName] [varchar](8000) NULL
[ActiveFromDate] [datetime] NULL [TrustBankNamé] [varchar] (8000) NULL
[ActiveToDate] [datetime] NULL [TrustBankAcct] [varchar](000) NULL
[AppEvent_ID] ASC [TrustBankContact] [varchar](000) NULL
[InvestmentBankName] [varchar](000) NULL

[InvestmentBankAcct] [varchar](000) NULL

EntityTypes

EntityType_ID

Client_ID

Administrators

Administrator_ID

[investmentBankContact] [varchar](000) NULL

[Bs_ID_Product] [int] NOT NULL.

[Bs_ID_Trust] [int] NOT NULL

Carriers
[Bs_ID_Investment] [int] NOT NULL

Carier_ID

[BSMatrix_ID] ASC

InsuranceTypes

Client_ID
```

---

## Image 006 - Templates

**Source Image:** `erd_page_006.png`

**Tables in this diagram:** TemplateTaskActions, Templates

### OCR Extracted Text
```
TEMPLATES

[dbo].[Templates]
fr | cossmaurindonmmncue |
PK

[Template_|D] [int] IDENTITY(1,1) NOT NULL

[dbo].[TemplateTaskActions]
(PK | [lemplateTaskAction_ID) [int] IDENTITY (1,1) NOT NULL.

[TemplateName] [varchar](255) NOT NULL

[TemplateTask_1D) [int] NOT NULL

[TemplateDesc] [varchar](255) NULL [TaskResultFlag] [bit] NOT NULL

{CreateDate] [datetime] NOT NULL [NextAction_ID] fint] NOT NULL

{IsDefautt] [bit] NOT NULL [TemplateTaskAction_ID] ASC

{Template_ID] ASC

[dbo] [TemplateTasks]
| | CONSTRAINT [PK_dbo. TemplateTasks] CLUSTERED

‘PK | [TemplateTask_ID] [int] IDENTITY(1,1) NOT NULL

[Template_ID} {int} NOT NULL

[Taskitem_1D} [int] NOT NULL

[TaskSequence] [int] NOT NULL.

[CreateDate] [datetime] NOT NULL

[TemplateTask_1D] ASC

Taskitems

Taskitem_ID
```

---

## Image 007 - AspNetUsers

**Source Image:** `erd_page_007.png`

**Tables in this diagram:** AspNetUserClaims, AspNetUserLogins, AspNetUsers

### OCR Extracted Text
```
ASP_NET

[dbo].[AspNetUsers] [dbo].[AspNetUserLogins]

Px | CONSTRAINT [PK_dbo.AspNetUsers] CLUSTEREI Px | CONSTRAINT [PK_dbo.AspNetUserLogins] CLUS

Id] [nvarchar|(128) NOT NULL

LoginProvider] [nvarchar](128) NOT NULL
FirstName] [nvarchar}(100) NOT NULL ProviderKey] [nvarchar](128) NOT NULL

LastName] [nvarchar](100) NOT NULL

Userld] [nvarchar(128) NOT NULL

UserOrganizationld] [nvarchar\128) NULL LoginProvider] ASC

Email] [nvarchar](256) NULL ProviderkKey] ASC

EmailConfirmed] [bit] NOT NULL Userld] ASC

PasswordHash] [nvarchar](max) NULL

SecurityStamp] [nvarchar](max) NULL [dbo].[AspNetUserClaims]
PhoneNumber] [nvarchar](max) NULL Px | CONSTRAINT [PK_dbo.AspNetUserClaims] CLUS

PhoneNumberConfirmed] [bit] NOT NULL [Id] [int] IDENTITY(4,1) NOT NULL
TwoFactorEnabled] [bit] NOT NULL [Userld] [nvarchar](128) NOT NULL

LockoutEndDateUtc] [datetime] NULL [ClaimType] [nvarchar](max) NULL

LockoutEnabled] [bit] NOT NULL [ClaimValue] [nvarchar](max) NULL

AccessFailedCount] [int] NOT NULL [Id] ASC

UserName] [nvarchar(256) NOT NULL

IsActive] [bit] NOT NULL
[dbo]. [AspNetRoles]

Id] ASC
CONSTRAINT [PK_dbo.AspNetRoles] CLUSTERE

[Id] [nvarchar](128) NOT NULL

[Name] [nvarchar](256) NOT NULL
[dbo]. [AspNetUserRoles]
| [RoleType_ID] [bigint] NULL
CONSTRAINT [PK_dbo.AspNetUserRoles] CLUS’

[Userld] [nvarchar|(128) NOT NULL [Discriminator] [nvarchar](128) NOT NULL

[ld] ASC

[Roleld] [nvarchar](128) NOT NULL

[Userld] ASC

[Roleld] ASC UserOrganizations RoleTypes
UserOrganizationld RoleType_ID
```

---

## Image 008 - Diagram 8

**Source Image:** `erd_page_008.png`

### OCR Extracted Text
```
FINAL RESULT 2

This is a Temporary

StatementType] [varchar](7) NOT NULL T;
able

ClientName] [varchar](255) NOT NULL

BankName] Warenar( i) NOT NEN: It is generated as the result
BankAccountNumber] [varchar](1) NOT NULL of a stored procedure at run-
CarrierName] [varchar](255) NULL time and is not used for

AdministratorN: har](255) NULL a zi
nner eae) storing data otherwise.

InsuranceTypeName] [varchar](255) NULL
ReceivedYearMonth] [varchar](61) NULL
BookedYearMonth] [varchar](61) NULL
Client_ID] [int] NOT NULL
AccountOrCession_|D] [int] NOT NULL
AcctName] [varchar](255) NULL
Comments] [varchar](max) NULL

calrx] [int] NULL

calbx] [int] NULL

AgencyName] [varchar(255) NULL
sQuarterly] [bit] NOT NULL

Frequency] [varchar](255) NOT NULL
Delivery] [varchar](255) NULL
ContactEmail] [varchar](255) NULL
PercentRecieved] [int] NULL
PercentBooked] [int] NULL
PercentCompleted] [int] NULL

PercentRecievedCurrentYear] [int] NULL

PercentBookedCurrentYear] [int] NULL

PercentCompletedC urrentYear] [int] NULL
```

---

## Image 009 - Diagram 9

**Source Image:** `erd_page_009.png`

### OCR Extracted Text
```
KEY

Rectangles with
Circular Edges

These indicate a table that is listed on
another page, one that provides a

key reference to a table on the
page where it is placed upon. Clicking
on them will lead to the sheet on
which they are defined.

‘These reference an
‘existing primary key.

[dbo]. [TaxClientFormLog_2017]
FK CONSTRAINT [PK_TaxClientFormLoa] C
i TaxClientFormLog_ID] [int] IDENTITY(1,1)

These reference a Client_ID] [int] NOT NULL
missing foreign key Year] [int] NOT NULL
dependency, that need
‘be added, and
‘inherited from the ProjectCreated] [int] NOT NULL
itable the arrow TaxClientFormLog_ID] ASC

‘originates from.

CONSTRAINT [PK dbo.ClientBankAccounts] CLUSTERED

FormCreated] [int] NOT NULL

[ClientBankAccount_ID] [int] IDENTITY (1,1) NOT NULL

{Client_1D] fint] NOT NULL

These reference a
i possible foreign key [IsQuarterly) [bit] NOT NULL
i ‘relationship, origin [ContactName] [verchar](256) NULL
' unknown. [ContactEmail] [varchar](255) NULL

[BS_[D] [int] NOT NULL

[BankAccount_{D] fint] NOT NULL

[ActiveFromDate] [datetime] NULL.
[ActiveToDate] [datetime] NULL
[User_ID] [int] NOT NULL
[Contact_ID] [int] NULL

These reference an [RecordCreatecDate} [datetime] NULL

existing foreign key. (BankCessionDelvery_[D) Int NULL

[SurplusAccount] [bit] NULL

[ClientBankAccount_ID] ASC

These reference an
index.
```

---

## Image 010 - Diagram 10

**Source Image:** `erd_page_010.png`

### OCR Extracted Text
```
CLIENTS P3

[dbo] {ClientBankAccountDatas]

CONSTRAINT [PK dbo. ClientBankAccountDatas] CLUSTERED

{ClientBankAccountData_ID) [int] IDENTITY (1,1) NOT NULL

ClientBankAccounts
ClientBankAccount_ID

Calendars [ClientBankAccount_ID] [int] NOT NULL

Calendar_ID [Calendar_|D] [int] NOT NULL

[ReceivedDate] [datetime] NULL

[BookedDate] [datetime] NULL

[Amount] [decimal](18, 2) NULL

[Comment] [varchar](255) NULL

[DateWorked] [datetime] NULL

[ExpiryDateWorked] [datetime] NULL

[RecordCreatedDate] [datetime] NULL

[ClientBankAccountData_ID] ASC
```

---

## Image 011 - LicensingAuthLocations

**Source Image:** `erd_page_011.png`

**Tables in this diagram:** LicensingAuths, LicensingAuthLocations

### OCR Extracted Text
```
LICENSING

[dbo].[LicensingAuthLocations]
CONSTRAINT [PK_dbo.LicensingAuthLocations

LicensingAuthLocation_ID] [int] IDENTITY(1,1) NOT 'PK | [LicensingAuth_ID] [int] IDENTITY(1,1) NOT NULL

[dbo].[LicensingAuths]

Px | CONSTRAINT [PK_dbo.LicensingAuths] CLUSTE

LicensingAuth_ID] [int] NOT NULL LicensingAuthName] [varchar](255) NOT NULL
Location_ID] [int] NOT NULL LicenseNumber] [varchar(50) NULL
EffectiveDate] [datetime] NOT NULL Taxl DNumber] [varchar](20) NULL

ExpirationDate] [datetime] NOT NULL Domicile] [varchar\255) NULL

SourceLicensingAuthL ocationCode] [nvarchar](max) LicensingAuth_ID] ASC

LicensingAuthLocation_ID] ASC.

Locations

Location_ID
```

---

## Image 012 - RALContacts

**Source Image:** `erd_page_012.png`

**Tables in this diagram:** RALContacts

### OCR Extracted Text
```
RAL CONTACTS

[dbo]. [ClientRALContacts] [dbo].[RALContacts]

Client_ID] [int] NOT NULL ContactlD] [int] IDENTITY(1,1) NOT NULL
ContactlD] [int] NOT NULL Name] [varchar(255) NOT NULL
FamilyRelationship] [varchar](100) NULL Address 1] [varchar](255) NULL
OwnershipPerc] [decimal](18, 2) NULL Address2] [varchar](255) NULL
BankAccountSign] [bit] NULL City] [varchar](100) NULL
PrimaryContactFlag] [bit] NULL State] [varchar](100) NULL
DealershipProducerFlag] [bit] NULL Zip] [varchar](5) NULL
RICShareholderFlag] [bit] NULL Email] [varchar](100) NULL
DirectorFlag] [bit] NULL Phone] [varchar](20) NULL

OfficerFlag] [bit] NULL Fax] [varchar(20) NULL

RegisteredAgent] [bit] NULL DOB] [datetime] NULL

OfficerTitle] [varchar](25) NULL SSN] [varchar](11) NULL

PresidentFlag] [bit] NULL EIN] [varchar\11) NULL

VicePresidentFlag] [bit] NULL ContactID] ASC

SecretaryFlag] [bit] NULL

TreasurerFlag] [bit] NULL .
Clients

ClassBStockFl bit] NULL Client_ID

Classification_ int] NULL

CONSTRAINT [UNQ_CLientContact] UNIQUE NONq Classifications

Classification_ID

ContactID] ASC

Client_ID] ASC
```

---

## Image 013 - Diagram 13

**Source Image:** `erd_page_013.png`

### OCR Extracted Text
```
TASKS

[dbo]. [Taskltems] [dbo]. [TaskNotes]

Px | CONSTRAINT [PK_dbo.Taskltems] CLUSTERED Px | CONSTRAINT [PK_dbo.TaskNotes] CLUSTERED
Taskltem_ID] [int] IDENTITY(1,1) NOT NULL TaskNotes_|D] [int] IDENTITY(1,1) NOT NULL

TaskName] [varchar](255) NOT NULL Project_ID] [int] NOT NULL

TaskDescription] [varchar](3000) NULL

ProjectTask_ID] [int] NOT NULL
TaskAction_ID] [int] NOT NULL Taskltem_ID] [int] NOT NULL

TaskObject_ID] [int] NOT NULL ProjectTaskActivity_ID] [int] NOT NULL

DueDay_|D] [int] NOT NULL NoteCreateDate] [datetime] NOT NULL

UserRole_!ID] [int] NOT NULL NoteCreateUser_ID] [int] NOT NULL

Taskitem_ID] ASC NoteUpdateDate] [datetime] NOT NULL

NoteUpdateUser_ID] [int] NOT NULL

NoteHtml] [varchar(3000) NOT NULL

[dbo]. [TaskObjects]
Px | CONSTRAINT [PK_dbo.TaskObjects] CLUSTERED

[TaskObject_ID] [int] IDENTITY(1,1) NOT NULL

TaskNotes_ID] ASC

[TaskObjectName] [varchar](50) NOT NULL

UserRoles ProjectTaskActivities

[IsDefault] [bit] NOT NULL ProjectTaskActivity_ID

UserRole_ID

[TaskObject_ID] ASC

ProjectTasks DueDays

[dbo]. [TaskActions]
Px | CONSTRAINT [PK_dbo.TaskActions] CLUSTERED
[TaskAction_ID] [int] IDENTITY(1,1) NOT NULL (Projects

[ActionName] [varchar](50) NOT NULL Project_ID

[IsDefault] [bit] NOT NULL

[TaskAction_ID] ASC
```

---

## Image 014 - Diagram 14

**Source Image:** `erd_page_014.png`

### OCR Extracted Text
```
ACCOUNTANTS

[dbo]. [PublicAccountants] [dbo]. [PublicAccountantLocations]

Px | CONSTRAINT [PK_dbo.PublicAccountants] CLUSTERED

Px | CONSTRAINT [PK_dbo.PublicAccountantLocations] CLUSTERED

[PublicAccountant_ID] [int] IDENTITY (1,1) NOT NULL PK [PublicAccountantLocation_ID] [int] IDENTITY(4,1) NOT NULL

[PublicAccountantName] [varchar](255) NOT NULL FK | [PublicAccountant_ID] [int] NOT NULL

[PublicAccountant_ID] ASC. FK | [Location_ID] [int] NOT NULL

[EffectiveDate] [datetime] NOT NULL

; [ExpirationDate] [datetime] NOT NULL
Locations

[PublicAccountantLocation_ID] ASC

Location_ID
```

---

## Image 015 - ClientBankAccounts

**Source Image:** `erd_page_015.png`

**Tables in this diagram:** ClientBankAccounts, ClientLocations

### OCR Extracted Text
```
CLIENTS P2

[dbo]. [UpdatedClientattributes] [dbo].{ClientinsuranceTypes]
[.beniamel bertenteeniiUkh CONSTRAINT [PK dbo. ClientinsuranceTypes] CLUSTERED
[Manager] [varchar](255) NULL

[ClientInsuranceType_ID] [int] IDENTITY (1,1) NOT NULL
[Accountant] [varchar] (255) NULL
[Client_1D} {int} NOT NULL
[AccountingSupportSpecialist] [varchar](255) NULL
[InsuranceType_|D] [int] NOT NULL
[FormationSpecialist] [varchar](255) NULL
{[InsuredName] [varchar](255) NULL
[FormationSupport] [varchar] (255) NULL

[OtherType] [varchar](255) NULL
[LeadAccountant] [varchar](255) NULL
{Carrier_1D} fint] NOT NULL
[CompanyRelations] [varchar](255) NULL
[ClientInsuranceType_ID] ASC

[Client_1D} (float) NULL

[dbo] .[ClientTaxCalcHistory]
[dbo].[ClientBankAccounts]

CONSTRAINT [PK _ClientTaxCalcHistory] CLUSTERED

CONSTRAINT [PK_dbo.ClientBankAccounts] CLUSTERED
PK

[DataValueType] [varchar](255) NOT NULL

[ContactName] [varchar](255) NULL
[DataVValue] [sql_variant] NOT NULL
{ContactEmail] [varchar](255) NULL
[ClientNameFromWorkSheet] [varchar](255) NOT NULL
(BS_[D] fint] NOT NULL
[WorkSheetName] [varchar](255) NOT NULL
[ActiveFromDate] [datetime] NULL

PK | [ClientTaxCalcHistory_ID] fint] IDENTITY (41,1) NOT NULL
[ClientBankAccount_ID] [int] IDENTITY (1,1) NOT NULL
BB | [client_10) fin) NOT NULL
[Client_1D) {int} NOT NULL
[TaxYear] [int] NOT NULL
[BankAccount_ID] fint] NOT NULL
[ColurnnName] [varchar](255) NOT NULL
('sQuarterly] [bit] NOT NULL

[(ClientTaxCalcHistory_ID] ASC
[ActiveToDate] [datetime] NULL

[User_ID] [int] NOT NULL
[Sontacte| Py [int] NO EE. [dbo].[ClientLocations]
[RecordCreatedDate] [datetime] NULL

[BankCessionDelivery_1D] int) NULL PK CONSTRAINT [PK_ dbo. ClientLocations] CLUSTERED

[SurplusAccount] [bit] NULL [(ClientLocation_[D] fint] IDENTITY (1,1) NOT NULL

[ClientBankAccount_ID] ASC [Client_1D} {int} NOT NULL
{Location_ID] [int] NOT NULL
[EffectiveDate] [datetime] NOT NULL
(ExpirationDate] [datetime] NOT NULL

[ClientName] [varchar}(255) NULL [ClientLocation 1D] ASC

[Client_1D} ffloat] NULL

BankAccounts InsuranceTypes Carriers
ClientName BankAccount_ID InsuranceType_ID CarrierName
Client_ID

Location_ID Contact_ID BankCessionDelivery_ID
```

---

## Image 016 - Diagram 16

**Source Image:** `erd_page_016.png`

### OCR Extracted Text
```
FINAL RESULT 1

[dbo]. [FinalREsultt]

This is a Temporary

StatementType] [varchar](12) NOT NULL T;
able

ClientName] [varchar](255) NOT NULL

BankName] [varchar](255) NOT NULL It is generated as the result
BankAccountNumber] [varchar](255) NOT NULL of a stored procedure at run-
CarrierName] [varchar](1) NOT NULL time and is not used for

AdministratorN: h 1) NOT NULL 5 '
minisuatonvameg erenerih storing data otherwise.

InsuranceTypeName] [varchar](1) NOT NULL

ReceivedYearMonth] [varchar](61) NULL

BookedYearMonth] [varchar](61) NULL
Client_ID] [int] NOT NULL
AccountOrCession_|D] [int] NOT NULL
AcctName] [varchar](255) NULL
Comments] [varchar|(max) NULL
calrx] [int] NULL

calbx] [int] NULL

AgencyName] [varchar(255) NULL

sQuarterly] [bit] NOT NULL
Frequency] [varchar](9) NOT NULL
Delivery] [varchar](255) NULL

ContactEmail] [varchar](255) NULL
PercentRecieved] [int] NULL
PercentBooked] [int] NULL
PercentCompleted] [int] NULL

PercentRecievedCurrentYear] [int] NULL

PercentBookedCurrentYear] [int] NULL

PercentCompletedC urrentYear] [int] NULL
```

---

## Image 017 - ProjectTasks

**Source Image:** `erd_page_017.png`

**Tables in this diagram:** ProjectTemplateTasks, ProjectTasks

### OCR Extracted Text
```
PROJECT TASKS

[dbo]. [ProjectTaskActions]

CONSTRAINT [PK_dbo.ProjectTaskActions] CLUSTERED

[ProjectTaskAction_ID] [int] IDENTITY (1,1) NOT NULL

[dbo].[ProjectTasks]
CONSTRAINT [PK_dbo.ProjectTasks] CLUSTERED

[ProjectTask_[D] [int] IDENTITY (1,1) NOT NULL

[ProjectTask_ 1D] [int] NOT NULL [Project_ID) int] NOT NULL

[NextProjectTask_ID] fint] NOT NULL [UserRole_ID] [int] NOT NULL

[TaskResultFlag] [bit] NOT NULL (UserID) [int] NOT NULL

[ProjectTaskAction_ID] ASC [askAction_D] fint] NOT NULL

[DueDay_1D] [int] NOT NULL

[askObject_ID] [int] NOT NULL

[dbo]. [ProjectTaskActivities]

[TaskName] [varchar](255) NOT NULL
CONSTRAINT [PK_dbo.ProjectTaskActivities] CLUSTERED

[TaskDescription] [nvarchar](3000) NOT NULL

PK | [ProjectTaskActivity_ID] [int] IDENTITY (1,1) NOT NULL

[laskSequence] [int] NOT NULL
[Project_ID] [int] NOT NULL

[ProjectTask ID] ASC
[ProjectTask_ 1D] [int] NOT NULL

[Status_[D] fint] NOT NULL

[TaskResultFlag] [bit] NULL [dbo].[ProjectTemplateTasks]
[CreateDate] [datetime] NOT NULL CONSTRAINT [PK_dbo.ProjectTemplateTasks] CLUSTERED

[UpdateDate] [datetime] NOT NULL

[ProjectTemplateTask_ID] fint] IDENTITY (1,1) NOT NULL

(UserID) [int] NOT NULL [Project_ID] [int] NOT NULL

[EypassFlag] [bit] NULL [TemplateTask_ID) [int] NOT NULL

[ProjectTaskActivity_ID] ASC

L FK | [UserRole_ID) [int] NOT NULL

[UserID [nvarchar](max) NOT NULL

7 [ProjectTemplateTask_ID] ASC

TaskObjects Template Tasks UserRoles
TaskObject_ID TemplateTask_ID UserRole_ID

DueDays TaskActions

DueDay_ID TaskAction_ID

User_ID Project_ID

Status Tables

Status_ID
```

---

## Image 018 - Diagram 18

**Source Image:** `erd_page_018.png`

### OCR Extracted Text
```
CESSION INSURANCE

[dbo]. [InsuranceTypes]

[dbo] {CessioninsuranceTypes]

a CONSTRAINT [PK_dbo.CessioninsuranceTypes] CLUSTERED

[CessionInsuranceType_ID] [int] IDENTITY (1,1) NOT NULL

CONSTRAINT [PK dbo. InsuranceTypes] CLUSTERED

{InsuranceType_1D] [int] IDENTITY(1,1) NOT NULL

{(ClientCession_D] [int] NOT NULL {InsuranceTypeName] [varchar](255) NOT NULL

{InsuranceType_ID] [int] NOT NULL [InsuranceType_ID] ASC

{CessionInsuranceTypeDesc] [varchar}(255) NULL

{CessionInsuranceType_ID] ASC

ClientCessions

ClientCession_ID

[dbo]. {CessionInsuranceTypePeriods]
{CessionInsuranceTypePeriod_ID] [int] IDENTITY(1,1) NOT NULL
{CessionInsuranceType_ID] [int] NOT NULL
{CreatedDate] [datetime] NOT NULL
[ActiveFromDate] [datetime] NULL
[ActiveToDate] [datetime] NULL

{FirstActivityDate] [datetime] NULL

[LastActivityDate] [datetime] NULL

[CessioninsuranceTypePeriod_ID] ASC
```

---

## Image 019 - Administrators

**Source Image:** `erd_page_019.png`

**Tables in this diagram:** AgencyLocations, Agencies, Administrators

### OCR Extracted Text
```
GENERAL P2

[dbo]. [Audiences]
Px | CONSTRAINT [PK_dbo.Audiences] CLUSTERED

[Clientid] [nvarchar](128) NOT NULL

[Base64Secret] [nvarchar](80) NOT NULL
[Name] [nvarchar](100) NOT NULL
[Clientid] ASC

[dbo].[Administrators]

Px | CONSTRAINT [PK_dbo.Administrators] CLUSTER

[Administrator_ID] [int] IDENTITY(1,1) NOT NULL
[AdministratorName] [varchar](255) NOT NULL
[Administrator_ID] ASC

[dbo].[Agencies]

Px | CONSTRAINT [PK_dbo.Agencies] CLUSTERED

Agency_ID] [int] IDENTITY(1,1) NOT NULL
AgencyName] [varchar(255) NOT NULL
LicenseN umber] [varchar(255) NULL
Tax|DNumber] [varchar](255) NULL
Location_ID] [int] NULL

Producer_ID] [int] NULL

SourceAgencyCode] [varchar](255) NULL
AgentAccountantUser_!D] [int] NOT NULL
Agency_ID] ASC

StatusTables Producers

Status_ID Producer_ID

Locations

User_ID Location_ID

EntityTypes

EntityType_ID

[dbo]. [AdministratorLocations]
[Px | comers essnnsmastscnontcusteco |

[AdministratorLocation_ID] [int] IDENTITY(1,1) NOT NULL

[Administrator_ID] [int] NOT NULL
[Location_ID] [int] NOT NULL

[EffectiveDate] [datetime] NOT NULL
[ExpirationDate] [datetime] NOT NULL
[AdministratorLocation_ID] ASC

[dbo].[AgencyLocations]
Px | CONSTRAINT [PK_dbo.AgencyLocations] CLUS’

[AgencyLocation_ID] [int] IDENTITY(1,1) NOT NULL
[Agency_ID] [int] NOT NULL

[Location_ID] [int] NOT NULL

[EffectiveDate] [datetime] NOT NULL
[ExpirationDate] [datetime] NOT NULL
[SourceAgencyLocationCode] [varchar](255) NULL
[AgencyLocation_ID] ASC

[dbo]. [Projects]

Px | CONSTRAINT [PK_dbo.Projects] CLUSTERED

Project_ID] [int] IDENTITY(1,1) NOT NULL
ProjectName] [varchar](255) NOT NULL
ProjectDesc] [varchar](255) NULL
Status_ID] [int] NOT NULL
ReasonNotCompleted] [varchar](100) NULL
AccountingYear] [int] NOT NULL

User_ID] [int] NOT NULL

Comments] [varchar](255) NULL
Entity_ID] [int] NOT NULL

EntityType_ID] [int] NOT NULL
ProjectType] [int] NOT NULL

Project_ID] ASC
```

---

## Image 021 - TaxCalcData2018

**Source Image:** `erd_page_021.png`

**Tables in this diagram:** TaxCalcData2018

### OCR Extracted Text
```
2018 TAX DATA

[dbo].[TaxCalcData2018]

Client] [varchar](255) NULL
‘Client_ID] [float] NULL
Overpayment] [money] NULL
Q1] [money] NULL

Q2] [money] NULL

Q3] [money] NULL

Q4] [money] NULL

InsuranceLicenceDate] [datetime] NULL

[dbo]. [TaxClientsNew2018]

[ClientName] [varchar](255) NULL

[BB | [Client_1D] [float] NULL

Clients

Client_ID
```

---

## Image 022 - ClientRoles

**Source Image:** `erd_page_022.png`

**Tables in this diagram:** ClientRoles

### OCR Extracted Text
```
PublicAccountants
PublicAccountant_ID CLIENTS

CONSTRAINT [PK dbo. Clients] CLUSTERED CONSTRAINT [PK dbo. ClientContacts] CLUSTERED

[Client_1D] [int] IDENTITY(1,1} NOT NULL [ClientContact_|D] [int] IDENTITY(1,1) NOT NULL.

[ClientName] [varchar](255) NOT NULL {Client_1D] {int} NOT NULL
[ClientDese] [varchar](255) NULL [Name] [varchar] 255) NOT NULL
[Company 1stChoiceName] [varchar] (255) NULL [Address1] [varchar](255) NULL
[Company2ndChoiceName] [varchar](255) NULL [Address2] [varchar}(255) NULL
[Company3rdChoiceName] [varchar] (255) NULL [City] [varchar](100) NULL
[Requestor] [varchar](255) NULL [State] [varchar](100) NULL
{CapitalSurplus] [money] NULL [Zip] (varchar](5) NULL
[AnnualMeetingDate] [datetime] NULL Email] [varchar](100) NULL
[VehiclesPerMonth] [int] NULL [Phone] [varchar](20) NULL
[QuotaSharePercentage] [decimal](18, 2) NULL [Fax] [varchar](20) NULL
(WizardComplete] [bit] NULL [DOB] [datetime] NULL
[Agency_ID] [int] NULL [SSN] [varchar](11) NULL
[LicensingAuth_ID] [int] NULL [FamilyRelationship] [varchar](100) NULL
[CreateFormationProject] [bit] NULL [OwnershipPerc] [decimal](18, 2) NULL
[FormationProjectCreated) [bit] NULL [BankAccountSign] [bit] NULL
[PaymentReceived] [bit] NULL [PrimaryContactFlag] [bit] NULL
[PaymentAmount] [decimal](18, 2) NULL [DealershipProducerFlag] [bit] NULL
[CheckNumber] [varchar](75) NULL [RICShareholderFlag] [bit] NULL
—

[DateCheckReceived] [datetime] NOT NULL [DirectorFlag] [bit] NULL

[IsActive] [bit] NULL [OfficerFlag] [bit] NULL
[CreateDate] [datetime] NULL [RegisteredAgent] [bit] NULL
[ActiveTax] [bit] NULL [OfficerTitle] (varchar](25) NULL
[TaxActiveFrom] [datetime] NULL [PresidentFlag] [bit] NULL
[TaxActiveTo] [datetime] NULL [VicePresidentFlag] [bit] NULL
[CharterRenewal] [bit] NULL [SecretaryFlag] [bit] NULL
[CharterRenewalActiveFrom] [datetime] NULL [TreasuretFlag] [bit] NULL
[CharterRenewalActiveTo] [datetime] NULL [ClassBStockFlag] [bit] NULL
(139530) [bit] NULL (EIN) [varchar](11) NULL
[PublicAccountant_ID] fint] NULL {(Classification_ID] [int] NULL
{(Classification_ID] [int] NULL [ClientContact_ID] ASC

[Domicile] [varchar](255) NULL
[dbo].[ClientRoles]

CONSTRAINT [PK_ dbo. ClientRoles] CLUSTERED

[ClientRoles_ID) [int] IDENTITY (1,1) NOT NULL

[axl Number] [varchar](20) NULL

[IncorporationDate] [datetime] NULL

[NAlCnumber] [nvarchar](50) NULL

[Client_1D} {int} NOT NULL
{LicenseNumber [nvarchar](50) NULL

[UserRole_ID] [int] NOT NULL
[date953D] [datetime] NULL

(UserID) [int] NOT NULL
[effectivedate953D] [datetime] NULL

[ClientRole_ClientRoles_ID) [int] NULL
[TaxFinalized] [bit] NULL

[ClientRoles_ID] ASC
[CorporateDoc] [varchar](100) NULL

[ReinsuranceManager] [varchar](50) NOT NULL
{ClientOrigin] [varchar}(50) NULL

[ClientClosing] [varchar](50) NULL

{Client_ID] ASC
```

---

## Image 023 - FinalResult

**Source Image:** `erd_page_023.png`

**Tables in this diagram:** FinalResult

### OCR Extracted Text
```
FINAL RESULT

[dbo].[FinalResult]

StatementType] [varchar](12) NOT NULL
ClientName] [varchar](255) NOT NULL
BankName] [varchar](255) NOT NULL
BankAccountNumber] [varchar](255) NOT NULL
CarrierName] [varchar](1) NOT NULL
AdministratorName] [varchar](1) NOT NULL
InsuranceTypeName] [varchar](1) NOT NULL
ReceivedYear] [sql_variant] NULL
ReceivedMonth] [sql_variant] NULL
BookedYear] [sql_variant] NULL
BookedMonth] [sql_variant] NULL

Client_ID] [int] NOT NULL
AccountOrCession_ID] [int] NOT NULL
AcctName] [varchar](255) NULL

Comments] [varchar(max) NULL

calrx] [int] NULL

calbx] [int] NULL

AgencyName] [varchar(255) NULL
IsQuarterly] [bit] NOT NULL

Frequency] [varchar](1) NOT NULL

Delivery] [varchar](255) NULL

ContactEmail] [varchar](255) NULL

This is a Temporary
Table

It is generated as the result
of a stored procedure at run-
time, and is not used for
storing data otherwise.
```

---

## Image 024 - States

**Source Image:** `erd_page_024.png`

**Tables in this diagram:** ContactLocations, States, Carriers

### OCR Extracted Text
```
GENERAL

[dbo].[States]

Px | CONSTRAINT [PK_dbo.States] CLUSTERED

[dbo]. [Classifications]

Px | CONSTRAINT [PK_dbo.Classifications] CLUSTER

[State_ID] [int] IDENTITY(1,1) NOT NULL [Classification_ID] [int] IDENTITY(1,1) NOT NULL

[StateName] [varchar100) NOT NULL [ClassificationDesc] [varchar(255) NOT NULL
[StateAbbreviation] [varchar](2) NOT NULL [ClassificationType] [varchar](20) NOT NULL

[State_ID] ASC [TaxldentifierType] [varchar](10) NULL

[Classification_ID] ASC

[dbo]. [Locations]

Px | CONSTRAINT [PK_dbo.Locations] CLUSTERED

[dbo]. [Contacts]

Location_ID] [int] IDENTITY(1,1) NOT NULL Px | CONSTRAINT [PK_dbo.Contacts] CLUSTERED
LocationName] [varchar](255) NULL Contact_ID] [int] IDENTITY(1,1) NOT NULL
Address1] [varchar](255) NULL FirstName] [varchar](255) NOT NULL

Address2] [varchar](255) NULL LastName] [varchar](255) NULL

City] [varchar](100) NULL MiddleName] [varchar](50) NULL

State] [varchar](100) NULL Title] [varchar](50) NULL

ZipCode] [varchar](5) NULL Email] [varchar(255) NULL
PhoneNumber] [varchar](20) NULL PhoneNumber1] [varchar(20) NULL
FaxNumber] [varchar](20) NULL PhoneNumber2] [varchar(20) NULL

Email] [varchar](120) NULL FaxNumber] [varchar](20) NULL

Location_ID] ASC ContactType] [int] NOT NULL

SelectedClient] [nvarchar(max) NULL

Contact_ID] ASC
[dbo].[Carriers]

Px | CONSTRAINT [PK_dbo.Carriers] CLUSTERED

[Carrier_ID] [int] IDENTITY(1,1) NOT NULL [dbo].[ContactLocations]

[CarrierName] [varchar](255) NOT NULL Px | CONSTRAINT [PK_dbo.ContactLocations] CLUS’

[CarrierName] [varchar](255) NOT NULL ContactLocation_ID] [int] IDENTITY(1,1) NOT NULL
[Carrier_ID] ASC Contact_ID] [int] NOT NULL

Location_ID] [int] NOT NULL

EffectiveDate] [datetime] NOT NULL

ExpirationDate] [datetime] NOT NULL

ContactLocation_ID] ASC
```

---

## Image 025 - Diagram 25

**Source Image:** `erd_page_025.png`

### OCR Extracted Text
```
PRODUCERS

[dbo]. [Producers]

Px | CONSTRAINT [PK_dbo.Producers] CLUSTERED

[dbo]. [ProducerLocations]

Px | CONSTRAINT [PK_dbo.ProducerLocations] CLUS

Producer_ID] [int] IDENTITY(1,1) NOT NULL ProducerLocation_ID] [int] IDENTITY(1,1) NOT NUL
ProducerName] [varchar](255) NOT NULL Producer_ID] [int] NOT NULL

ProducerType_|D] [int] NOT NULL FK | [Location_ID] [int] NOT NULL

CorporateStructure] [varchar(255) NULL EffectiveDate] [datetine] NOT NULL

EIN] [varchar\(15) NULL ExpirationDate] [datetime] NOT NULL

Producer_ID] ASC ProducerLocation_ID] ASC

Locations

[dbo]. [ProducerTypes]
Px | CONSTRAINT [PK_dbo.ProducerTypes] CLUSTER

[ProducerType_ID] [int] IDENTITY(1,1) NOT NULL

Location_ID

[ProducerTypeName] [varchar](255) NOT NULL

[ProducerType_ID] ASC
```

---

## Image 026 - Users

**Source Image:** `erd_page_026.png`

**Tables in this diagram:** UserActivityTokens, Users, UserRoleAssignments

### OCR Extracted Text
```
[dbo].[Users]

CONSTRAINT [PK_dbo.Users] CLUSTERED
User_ID] [int] IDENTITY(1,1) NOT NULL
FirstName] [varchar](255) NULL

LastName] [varchar](255) NULL

FullName] [varchar](510) NULL

Email] [varchar(255) NULL

UserName] [varchar](255) NULL

UserOrganizationld] [varchar](255) NULL

ASPNetUser_Id] [nvarchar](128) NULL

User_ID] ASC

[dbo].[UserRoleAssignments]

CONSTRAINT [PK_dbo.UserRoleAssignments] C!

UserRoleAssignment_ID] [int] IDENTITY(1,1) NOT
User_ID] [int] NOT NULL

UserRole_ID] [int] NOT NULL

EffectiveDate] [datetine] NOT NULL

ExpirationDate] [datetine] NOT NULL

UserRoleAssignment_ID] ASC

[dbo]. [Role Types]

CONSTRAINT [PK_dbo.RoleTypes] CLUSTERED

[RoleType_ID] [bigint] IDENTITY(1,1) NOT NULL
[RoleTypeName] [varchar](50) NOT NULL

[RoleType_ID] ASC

USERS

[dbo].[UserActivityTokens]
Px | CONSTRAINT [PK_dbo.UserActivityTokens] CLU$

UserActivityTokenId] [bigint] IDENTITY(1,1) NOT N

Userld] [nvarchar(max) NOT NULL

Token] [nvarchar}(max) NOT NULL

Timeout] [datetime2)(7) NOT NULL
ParentToken] [nvarchar}(max) NULL

UserActivityTokenld] ASC

[dbo]. [UserOrganizations]

Px | CONSTRAINT [PK_dbo.UserOrganizations] CLUS|

[UserOrganizationld] [nvarchar(128) NOT NULL

[Name] [nvarchar](max) NOT NULL

[EntityType_1D] [int] NOT NULL

[Entity_1D] [int] NOT NULL

[UserOrganizationld] ASC

[dbo]. [UserRoles]

Px | CONSTRAINT [PK_dbo.UserRoles] CLUSTERED

[UserRole_ID] [int] IDENTITY(1,1) NOT NULL

[RoleName] [varchar](50) NOT NULL

[RoleType_ID] [bigint] NOT NULL

[IsDefault] [bit] NOT NULL

[UserRole_ID] ASC

EntityTypes

EntityType_ID

AspNetUsers

Project_ID
```

---

## Image 027 - Diagram 27

**Source Image:** `erd_page_027.png`

### OCR Extracted Text
```
REINSURANCE
ASSOCIATES
```

---

## Image 028 - Diagram 28

**Source Image:** `erd_page_028.png`

### OCR Extracted Text
```
2016 TAX DATA

[dbo]. [TaxClientsNew2016]

PK | CONSTRAINT [PK_TaxClientsNew2016] CLUSTER
[ID] [int] IDENTITY(1,1) NOT NULL

Clients [ClientName] [varchar](255) NOT NULL

Client_ID

[Client_ID] [int] NULL

[ID] ASC
```

---

## Image 029 - BankLocations

**Source Image:** `erd_page_029.png`

**Tables in this diagram:** BankAccounts, BankLocations, Banks

### OCR Extracted Text
```
BAN

[dbo].[BankLocations]

CONSTRAINT [PK_dbo.BankLocations] CLUSTER

BankLocation_ID] [int] IDENTITY(1,1) NOT NULL
Bank_ID] [int] NOT NULL

Location_ID] [int] NOT NULL

EffectiveDate] [datetime] NOT NULL

ExpirationDate] [datetime] NOT NULL

BankLocation_ID] ASC

Locations

Locations_ID

KS

[dbo].[Banks]
CONSTRAINT [PK_dbo.Banks] CLUSTERED
[Bank_ID] [int] IDENTITY(1,1) NOT NULL
[BankName] [varchar](255) NOT NULL

[Bank_ID] ASC

[dbo].[BankAccounts]

PK

CONSTRAINT [PK_dbo.BankAccounts] CLUSTER

[BankAccount_ID] [int] IDENTITY(1,1) NOT NULL
[Bank_ID] [int] NOT NULL

[BankAccountNumber] [varchar](255) NOT NULL

[BankAccount_ID] ASC
```

---

## Image 030 - DueDayChanges

**Source Image:** `erd_page_030.png`

**Tables in this diagram:** DueDayChanges, DueDays

### OCR Extracted Text
```
DUE DAYS

[dbo].[DueDayChanges]
CONSTRAINT [PK_dbo.DueDayChanges] CLUSTE

DueDayChanges_ID] [int] IDENTITY(1,1) NOT NUL|
Project_ID] [int] NOT NULL

ProjectTask_ID] [int] NOT NULL

ProjectTaskActivity_ID

[int] NOT NULL
UpdateDate] [datetime] NOT NULL
User_ID] [int] NOT NULL
DueDayFromDate] [datetime] NOT NULL
DueDayToDate] [datetime] NOT NULL

NOT NULL

DueDay_ID_From] [int]

DueDay_ID_To] [int] NOT NULL

DueDayChanges_ID] ASC

RELATI

may NC

ONSHIE

NEED

[dbo].[DueDays]

Px | CONSTRAINT [PK_dbo.DueDaysn] CLUSTERED

[DueDay_ID] [int] IDENTITY(0,1) NOT NULL
[DueDayNum] [int] NOT NULL
[IsDefault] [bit] NOT NULL

[DueDay_ID] ASC

Projects

Project_ID

User_ID
```

---

## Image 031 - Diagram 31

**Source Image:** `erd_page_031.png`

### OCR Extracted Text
```
MISC

[dbo]. [Notes] [dbo]. [Attachments]
| Sosa se ERD oe

e_ID] [int] IDENTITY(1,1) NOT NULL Attachment_ID] [int] IDENTITY(1,1) NOT NULL

eType] [int] NOT NULL Project_ID] [int] NOT NUL
eCreateDate] [datetime] NOT NULL ProjectTask_ID] [int] NOT
eCreateUser_ID] [int] NOT NULL ProjectTaskActivity_ID] [in

eUpdate Date] [datetine] NOT NULL TaskNote_|D] [int] NULL

eUpdate User_ID] [int] NOT NULL AttachmentLocation] [varchar(255) NOT NULL

eType_ID] [int] NOT NULL FileName] [varchar](128) NOT NULL

eHtml] [varchar(3000) NULL achmentFile Type] [varchar(255) NOT NULL

e_ID]ASC FK achmentType_ID] [int] NOT NULL

achmentCreateDate] [datetime] NOT NULL

FileSize] [bigint] NOT NULL
[dbo]. [PrintReports]
CONSTRAINT [PK_dbo.PrintReports] CLUSTERED

; ; Entity_1D] [int] NOT NULL
[PrintReport_ID] [int] IDENTITY(1,1) NOT NULL

, AttachedFileExtension] [varchar(6) NOT NULL
[PrintReportName] [varchar](255) NOT NULL

FileDescription] [varchar](255) NULL
[StoredProcedureName] [varchar](255) NOT NULL

Attachment_ID] ASC
[PrintReport_ID] ASC =

[dbo]. [AttachmentTypes] TaskNotes
[saan || || [Fr =

[AttachmentType_ID] [int] IDENTITY(1,1) NOT NULL

[AttachmentTypeName] [varchar](50) NOT NULL
ProjectTaskActivities

EntityTypes

ProjectTasks

ProjectTask_ID
```

---

## Image 032 - ReinsuranceManagers

**Source Image:** `erd_page_032.png`

**Tables in this diagram:** ReinsuranceManagers, ReinsuranceManagerLocations

### OCR Extracted Text
```
REINSURANCE

[dbo].[ReinsuranceManagers]
[Px | coumarin detects |

[ReinsuranceManager_ID] [int] IDENTITY(4,1) NOT NULL

[ReinsuranceManagerName] [varchar{255) NOT NULL

[ReinsuranceManager_ID] ASC

Locations
Location_ID

[dbo].[ReinsuranceManagerLocations]

Px | CONSTRAINT [PK dbo. ReinsuranceManagerLocations] CLUSTERED.

[ReinsuranceManagerLocation_ID] fint] IDENTITY (4,1) NOT NULL
[ReinsuranceManager_|D) [int] NOT NULL

[Location_ID] {int} NOT NULL

[EffectiveDate] [datetime] NOT NULL

(ExpirationDate] [datetime] NOT NULL

[ReinsuranceManagerLocation_ID] ASC
```

---

## Image 033 - BankCessionDeliveries

**Source Image:** `erd_page_033.png`

**Tables in this diagram:** BankCessionFrequencies, ClientCessionDatas, BankCessionDeliveries, ClientCessions

### OCR Extracted Text
```
CESSIONS

[dbo].[BankCessionDeliveries]

[BankCessionDelivery_ID] ASC

[BankCessionDeliveryType] [varchar]( 255) NOT NULL

[dbo].[BankCessionFrequencies]

[BankCessionFrequencyType] [varchar](255) NOT NULL

[BankCessionFrequency_ID] ASC

[dbo].[ClientCessionDatas]

[ClientCession_1D] [int] NOT NULL

[Calendar_D] fint] NOT NULL

[ReceivedDate] [datetime] NULL

[BookedDate] [datetime] NULL

[Amount] [decimal}(18, 2) NULL

[Comment] [varchar](255) NULL

[DateWorked] [datetime] NULL

[ExpityDateWorked] [datetime] NULL

[RecordCreatedDate] [datetime] NULL

[ClientCessionData_ID] ASC

Calendar_ID Contact_ID

ClientBankAccounts

ClientBankAccount_ID

[dbo].[ClientCessions]

CONSTRAINT [PK_ dbo. BankCessionDeliveries] CLUSTERED CONSTRAINT [PK dbo. ClientCessions] CLUSTERED

[BankCessionDelivery_|D} [int] IDENTITY(1,1) NOT NULL

[ClientCession_ID] [int] IDENTITY (1,1) NOT NULL

[Client_1D] fint] NOT NULL

{InsuranceType_ID] [int] NULL

{Carrier_ID] [int] NULL

[Administrator_ID] [int] NULL

CONSTRAINT [PK_ dbo. BankCessionFrequencies] CLUSTERED [TrustClientBankAccount_ID] [int] NULL
t } [int] (14)

[BankCessionFrequency_|D] [int] IDENTITY(1,1) NOT NULL.

[nvestmentClientBankAccount_[D] [int] NULL

[sQuarterly} [bit] NOT NULL

[ContactName] [varchar](255) NULL

{ContactEmail] [varchar](255) NULL

[BS_[D] fint] NOT NULL

CONSTRAINT [PK_dbo.ClientCessionDatas] CLUSTERED [ActiveFromDate] [datetime] NULL.
PK ti

[ClientCessionData_ID) [int] IDENTITY (1,1) NOT NULL

[ActiveToDate] [datetime] NULL

[AdminDesc] [varchar](255) NULL

[ProductDes¢] [varchar}(255) NULL

{User_ID] [int] NOT NULL

[Contact_ID] {int] NULL

[RecordCreatedDate] [datetime] NULL

[BankCessionDelivery_1D] [int] NULL

[BankCessionFrequency_ID) [int] NULL

[InProcess] [bit] NULL

[FundsHeld] [bit] NULL

[ClientCession_ID] ASC

Administrators InsuranceTypes
Administrator_ID InsuranceType_ID
```

---

## Image 034 - TaxCalcData

**Source Image:** `erd_page_034.png`

**Tables in this diagram:** TaxClientFormLog, TaxCalcData

### OCR Extracted Text
```
[dbo].[TaxCalcData]
CONSTRAINT [PK_ClientTaxCalcHistoryffsd] CL!

TaxCalcData_ID] [int] IDENTITY(1,1) NOT NULL
Agency] [varchar](255) NULL

Client] [varchar](255) NULL

EIN] [varchar(255) NULL

Overpayment] [money] NULL

Overpayment2] [money] NULL

Q1] [money] NU
Q2] [money] NU

Q3] [money] NU

@4] [money] NU

Extension] [money] NULL

Withholding] [money] NULL

5 Payments] [varchar](255) NULL

2015 Estimated Tax] [varchar](255) NULL
Remaining 2016 Tax Due] [varchar](255) NULL
2015 Tax Liability] [varchar(255) NULL

2015 P&l] [varchar](255) NULL

5 Tax Due] [varchar(255) NULL

5 Credit] [varchar(255) NULL

Estimated 2017 tax liability] [varchar](255) NULL

2016 tax deposit due] [varchar(255) NULL

Client_ID] [int] NULL

TaxCalcData_ID] ASC

TAX CALC DATA

[dbo].[TaxClientFormLog]

Px | CONSTRAINT [PK_TaxClientFormLog1] CLUSTER

TaxClientFormLog_ID] [int] IDENTITY(1,1) NOT NU
Client_ID] [int] NOT NULL

Year] [int] NOT NULL

FormCreated] [int] NOT NULL

ProjectCreated] [int] NOT NULL

TaxClientFormLog_ID] ASC

Clients

Client_ID
```

---
