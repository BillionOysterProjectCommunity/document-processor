# document-processor
Automatic document processing and data submission pipeline powered by Google Cloud's DocumentAI

The current FormParser version provided by Google Cloud is `pretrained-form-parser-v2.0-2022-11-10`

### Project Setup

```bash
git clone https://github.com/BillionOysterProjectCommunity/document-processor.git

cd document-processor

python3.11 -m venv .

pip install -r requirements.txt

pip install -e ./
```

**Authentication**

<a href=https://googleapis.dev/python/google-api-core/latest/auth.html#overview>Google Cloud Local Authentication Setup</a>

**Project configuration**

```toml
# ~/.config/billionoysterproject/document.toml

location = 'us'
project-id = "gcp-project-name"
processor-id = "gcp-project-id"
# Google Drive
master-datasheet-directory-id = "bop-master-sheet-google-drive-directory-id"
# Web
flask-secret-key = "supersecretkey"
# OAuth
oauth-client-id = "<google-oauth-client-id>.apps.googleusercontent.com"
oauth-client-secret = "oauth-client-secret"

```
