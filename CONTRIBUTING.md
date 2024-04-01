## Architecture

Document Processor consists of 3 primary components:
- Document Analysis
- Document Processing
- User Authentication

**Document Analysis**

The Document Analysis stage uses Google Clouds <a href="https://cloud.google.com/document-ai">Document AI</a> service to
extract the data points from an Oyster Research Station Data Sheet. The Document AI client can be found in `theia/document/processor.py`

**Document Processing**

Document Processing consists of the form inputs when `/f/form` is accessed.

`asyncio` is used here to create a "job" like abstraction to handle the multiple different categories to be processed. Similar to a rudementary implementation of Spotify's <a href="https://github.com/spotify/luigi">luigi</a> data processing pipeline library, there is a `PipelineJob` class which carries an asynchronous `run()` method that must be implemented by every job. 

Every `PipelineJob` returns a `PipelineResult` which carries a `name` attribute and a `DataFrame` to be able to store the processed data.

At the end of processing, all `PipelineResult`(s) converge into one singular dataframe output to be used for analysis.

**User Authentication**

User authentication is two stage process.

1. The user logs into a Google Account via OAuth
2. The email from the `userinfo` OAuth scope is cross-referenced within the **firestores** `users` collection to check if they have been registered by an admin user.

Only users with an `admin` role in a users `roles` field can access `/admin/*` to add and remove users from using the application.

## Project Setup
1. Google Cloud Services
    - Document AI
    - OAuth
    - Cloud Storage
    - Firebase
    - IAM Service Account
    - Cloud Run (Work in Progress)
2. Configuration
3. Packaging
4. Deployment

Before any of these steps can be completed, follow the guide on <a href="https://developers.google.com/workspace/guides/create-project">setting up a Google Cloud Project</a>

Throughout this guide, keep in mind of the **Important Environment Variables** as they will be used when setting up `config.toml`


**Google Cloud Services**

1. Document AI
    
    For Document AI, a Form Parser is used to pare the Billion Oyster Project Data Sheet fields. To setup the processor follow the <a href="https://cloud.google.com/document-ai/docs/process-documents-form-parser">Process documents with Form Parser</a> guide to setup a processor.

    Once setup, in the `Manage Versions` section of your newly created processor, make sure `pretrained-form-parser-v2.0-2022-11-10` is the processor deployed for usage.

    **Important Environment Variables**

    `location`: (example: location = 'us')

    `processor-id`: (example: processor-id = '5213421080g14395')


2. OAuth

    Follow <a href="https://support.google.com/cloud/answer/6158849?hl=en">Setting up OAuth 2.0</a> to add OAuth capability to the application.

    **Important Environment Variables**

    `oauth-client-id` (Client ID)

    `oauth-client-secret` (Client secret)




