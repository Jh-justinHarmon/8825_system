# RAL Portal OAuth 2.0 Implementation Guide

This document describes the OAuth 2.0 authentication flow for the RAL Portal API.

## Overview
The RAL Portal uses OAuth 2.0 for secure API authentication.

## Flow Steps
1. Request authorization token
2. Exchange for access token  
3. Use access token in API requests
4. Refresh token when expired

## Implementation Details
- Token endpoint: /oauth/token
- Authorization endpoint: /oauth/authorize
- Scopes: read, write, admin
