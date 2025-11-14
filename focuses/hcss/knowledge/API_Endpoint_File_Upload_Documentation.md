# API Endpoint File Upload Documentation

### Backend Access Points
- Stage Site: https://rallcstage.azurewebsites.net/api/

Production keys available upon request.

In order to upload a statement to the intake storage container for processing by the automation engine, \
the following endpoints in the order indicated will need to be utilized:

# Step 1: Get OAuth token 
The purpose of this step is to get the OAuth token required for accessing the endpoints below.

Request Type, POST: `/oauth/token`
Payload format, Form Data: 
as the form data object for the POST request with the Content-Type set as 'application/x-www-form-urlencoded' 

#### Parameters
- The `grant_type` represents the type of grant being accessed, use `client_credentials` as the value
- The `client_id` represents the audience id the backend recognizes as valid, use `a934a88b4bed4a12g7d888f5c43dcb68` as the value
- The `client_secret` represents the client secret utilized for generating the token, use `a1zdabwfPpFcFdMft6asfzLkO1aa_K9vKe9SJezPwWs` as the value

This endpoint returns returns a `200 response` with a client auth access_token field that will need to be included as the Header for all requests,
with the header as [Authorization:] and the text as [Bearer (token string text)].

## Step 2: Creating the `intakeDocument` record for an uploaded statement
The purpose of this step is to generate an `intakeDocument` record representing the document being uploaded.

Request Type, POST: `api/intakeDocument/` \
Payload Format, JSON: {originalFileName: "", OriginationSource: ""} 

#### Parameters, as JSON: 
- The `originalFileName` represents the name of the statement
- The `OriginationSource` represents the source the statement was derived from, ex: `Source: Uploaded by exampleUserName`
- Include Auth token in header, in format described in Step 1

#### Example: 
Here is an example of how this endpoint should be formatted: \
Endpoint: `https://rallcstage.azurewebsites.net/api/intakeDocument` \
Request Payload: \
{ \
&emsp; originalFileName: "exampleStatement.pdf", \
&emsp; OriginationSource: "email" \
} 

This endpoint will then create an intakeDocument record. After this record has been added,
the information returned by the `200 response` response code includes the `intakeDocument` record and will need to be utilized for the next step.

## Step 3: Creating the `intakeDocumentLog` record for an uploaded statement
The purpose of this step is to generate a log corresponding to the `intakeDocument` record,
these logs are used for tracking the progress of statements in the automation engine, and for debugging.

Request Type, POST: `api/intakeDocumentLog/` \
Payload Format, JSON: {status: "", type: "", description: "", filepath: "", filename: ""} \

#### Parameters, as JSON: 
- The `type` should remain `INTAKE` for all statement uploads, regardless of the step in the statement upload process the log represents. 
- The `filepath` corresponds to the environment the statement is being uploaded to. The two options being `ralstage` and `ralprod`.
- The `description` details the action being taken on the statement. Uploaded statements for this step should be logged in the following format: `Uploading file exampleFilename.pdf to intake`
- The `status` for this stage should be `UPLOADING`. The available status options are `UPLOADING`, `PARSING`, `FAULTED`, `COMMIT_ERROR`, `DISCARDED`, `ABORTED`, `FINISHED`, `COMMITTED`.
- The `filename` for this statement. The filename is *required* to be the GUID generated filename, returned in the 200 response from step 2
- Include Auth token in header, in format described in Step 1

#### Example: 
Here is an example of how this endpoint should be formatted: \
Endpoint: `https://rallcstage.azurewebsites.net/api/DocumentIntakeLogs` \
Request Payload: \
{ \
&emsp; status: `UPLOADING`, \
&emsp; type: `INTAKE`, \
&emsp; description: `Uploading file 05-File.pdf to intake`, \
&emsp; filepath: `ralstage`, \
&emsp; filename: `d377ce77-ee09-47a1-8110-a786a03da605.pdf`, \
}

This endpoint returns a `201 response` code and JSON with the `intakeDocument` record associated with this log entry, 
and the log entry itself, with all backend populated fields returned.

## Step 4: Uploading the statement
The purpose of this step is to send the uploaded file to the backend, which will then send it to the Azure intakeDocumentStorage file container, in order for processing by the automation engine.

Request Type, POST: `/api/files/uploadStatement/?name=` \
Payload Formats: Query string parameter, and Form Data object.

#### Parameters:
- Query String: The `?name=` of the statement being uploaded. The name is *required* to be the GUID generated filename, returned in the 200 response from step 2, appended to the request URL.
- Form Data (binary): The `file` being uploaded. This binary file represents the .pdf file being uploaded.
- Include Auth token in header, in format described in Step 1

#### Example: 
Here is an example of how this endpoint should be formatted: \
Endpoint: `https://rallcstage.azurewebsites.net/api/files/uploadStatement/?name=exampleDocUUID.pdf` \
Request Payload: \
In the payload of the POST request, the .pdf file needs to be sent as Form Data, in binary.

This endpoint returns an `200 response` code.

## Step 5: Update the `intakeDocument` record with a status of "Waiting"
The purpose of this step is to update the `intakeDocument` record, so that the automation engine knows that it should process, and parse the statement.

Request Type, PUT: `api/intakeDocument/` \
Payload Format, JSON (Represents intakeDocument object): \
{administrator: "", administrator_ID: "", adminstratorParsedValue: "", attachment: "", attachment_ID: "", bank: "", bankParsedValue: "",
bank_ID: "", client: "", clientBankAccount: "", clientBankAccountParsedValue: "", clientBankAccount_ID: "", clientCession: "",
clientCessionParsedValue: "", clientCession_ID: "", clientParsedValue: "", client_ID: "", completedOn: "", createdOn: "",
documentIntakeLogs: "", fileName: "", filePassword: "", filePath: "", filingDate: "", frequency_ID: "", intakeDocument_ID: "",
isManuallyMapped: "", modifiedOn: "", month: "", originalFileName: "", originationSource: "", provider: "", providerId: "",
source: "", startedOn: "", status: "", year: ""} 

#### Parameters:
- A JSON object containing all of the data associated with an `intakeDocument` record, this object would have been returned in step 2, and only needs the `status` field modified to `Waiting` before submitting this PUT request.
- Include Auth token in header, in format described in Step 1

#### Example: 
Here is an example of how this endpoint should be formatted: \
Endpoint: `https://rallcstage.azurewebsites.net/api/intakeDocument` \
Request Payload: \
{ \
&emsp; Full intakeDocument object returned in step #2, with the `status` changed from `Uploading` to `Waiting` \
}

This endpoint returns an `200 response` code, with an object representing the updated `intakeDocument` record.







