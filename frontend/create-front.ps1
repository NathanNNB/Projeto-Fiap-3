# deploy-frontend.ps1

# Set variables
$BUCKET_NAME = "soccer-scout-fiap-3"
$REGION = "us-central1"
$BUILD_DIR = "dist"

Write-Host "Starting frontend deploy to Google Cloud Storage..."

# 1. Build frontend (assumindo que você está na pasta do frontend)
Write-Host "Running 'npm run build' to generate static files..."
npm run build

# 2. Create bucket if not exists
Write-Host "Creating GCS bucket if it doesn't exist..."
$bucketExists = gsutil ls -b "gs://$BUCKET_NAME" 2>$null
if (-not $bucketExists) {
    gsutil mb -l $REGION "gs://$BUCKET_NAME"
    Write-Host "Bucket $BUCKET_NAME created."
} else {
    Write-Host "Bucket $BUCKET_NAME already exists."
}

# 3. Configure bucket for static website hosting
Write-Host "Configuring bucket for static website hosting..."
gsutil web set -m index.html -e 404.html "gs://$BUCKET_NAME"

# 4. Upload build files to bucket
Write-Host "Uploading static files to bucket..."
gsutil -m cp -r "$BUILD_DIR/*" "gs://$BUCKET_NAME"

# 5. Make files publicly readable
Write-Host "Setting public read permissions on bucket objects..."
gsutil iam ch allUsers:objectViewer "gs://$BUCKET_NAME"

Write-Host "Deploy finished!"
Write-Host "Your frontend is available at: http://storage.googleapis.com/$BUCKET_NAME/index.html"
