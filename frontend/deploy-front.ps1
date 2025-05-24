# Define variables
$BUCKET_NAME = "soccer-scout-fiap-3"

Write-Host "Starting frontend build with Vite..."

# Delete previous dist folder if it exists
if (Test-Path -Path "./dist") {
    Remove-Item -Recurse -Force "./dist"
}

# Run the Vite build command
yarn build

if ($LASTEXITCODE -ne 0) {
    Write-Error "Error during Vite build process."
    exit 1
}

# Sync the dist folder contents to the GCP bucket
Write-Host "Uploading files to bucket: $BUCKET_NAME"
gsutil -m rsync -R ./dist "gs://$BUCKET_NAME"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Deployment completed successfully!"
    Write-Host "You can access your app at:"
    Write-Host "https://storage.googleapis.com/$BUCKET_NAME/index.html"
} else {
    Write-Error "Failed to sync files to the GCP bucket."
}
