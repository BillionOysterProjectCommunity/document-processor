# document-processor
Automatic document processing and data submission pipeline powered by Google Cloud's DocumentAI for the Billion Oyster Project

The current FormParser version provided by Google Cloud is `pretrained-form-parser-v2.0-2022-11-10`

### Local Development Setup

```bash
git clone https://github.com/BillionOysterProjectCommunity/document-processor.git

cd document-processor

python3.11 -m venv .

pip install -r requirements.txt

pip install -e ./


---

# Create an uploads folder
mkdir theia/web/uplods
# insert the iam json file into theia/
```

**Google Cloud**

For local ADC configuration follow https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev

**Local SSL**
```
cd theia/cert

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem
```

**Project configuration**

```toml
# theia/config.toml

location = 'us'
project-id = "gcp-project-name"
processor-id = "gcp-project-id"
# Google Drive
master-datasheet-directory-id = "bop-master-sheet-google-drive-directory-id"
# Web
flask-secret-key = "supersecretkey"
iam-file-name = "<document-processor-service-account>.json"
# OAuth
oauth-client-id = "<google-oauth-client-id>.apps.googleusercontent.com"
oauth-client-secret = "oauth-client-secret"

debug = false/true

```

This project uses <a href="https://buildpacks.io/">Cloud Native Buildpack</a> to build images. To build an image use the <a href="https://github.com/buildpacks/pack">pack</a> CLI tool.
```bash
# gunicorn.conf.py depends on the debug state in config.toml

docker build . -t us-east1-docker.pkg.dev/ors-document-analysis/billionoysterproject/theia:prod

# Then, run the buildpack.
# Make sure to open 127.0.0.1 in the browser when developing locally

docker run --rm -p 127.0.0.1:8080:8080 theia:prod

docker push us-east1-docker.pkg.dev/ors-document-analysis/billionoysterproject/theia:prod
```
