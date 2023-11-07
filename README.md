# document-processor
Automatic document processing and data submission pipeline powered by Google Cloud's DocumentAI

The current FormParser version provided by Google Cloud is `pretrained-form-parser-v2.0-2022-11-10`

### Project Setup

```bash
git clone https://github.com/BillionOysterProjectCommunity/document-processor.git

virtualenv .

pip install -r requirements.txt
```

**Authentication**

<a href=https://googleapis.dev/python/google-api-core/latest/auth.html#overview>Google Cloud Local Authentication Setup</a>

**Project configuration**

```toml
# ~/.config/billionoysterproject/document.toml

location = 'us'
processorid = 'processor-id'
project-id = 'project-id'
```
