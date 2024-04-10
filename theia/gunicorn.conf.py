# NOTE: when building an image bind to 0.0.0.0
# for local development bind to localhost
# bind = "0.0.0.0:8080"
bind = "127.0.0.1:8080"
workers = 4
certfile = 'cert/certificate.pem'
keyfile = 'cert/key.pem'