#!/bin/bash

# Deployment script for Text Extractor Web Application

echo "Deploying Text Extractor Web Application..."

# Create a static website directory
DEPLOY_DIR="/home/ubuntu/text_extractor/web/static_site"
mkdir -p $DEPLOY_DIR

# Copy the web interface files
cp -r /home/ubuntu/text_extractor/web/templates/* $DEPLOY_DIR/
cp -r /home/ubuntu/text_extractor/web/static/* $DEPLOY_DIR/

# Create a simple index.html that redirects to the Flask app
cat > $DEPLOY_DIR/index.html << EOF
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url=http://5000-ibhduli6wyiih6csaa49t-8bb4aa19.manus.computer">
    <title>Text Extractor Tool</title>
</head>
<body>
    <p>Redirecting to Text Extractor Tool...</p>
    <p>If you are not redirected, <a href="http://5000-ibhduli6wyiih6csaa49t-8bb4aa19.manus.computer">click here</a>.</p>
</body>
</html>
EOF

echo "Static site prepared for deployment."
