# Set variables
$REGION = "us-central1"
$PROJECT_ID = (gcloud config get-value project)
$IMAGE_NAME = "flask-app-fiap-3"
$REPO_NAME = "flask-repo"

Write-Host "Selected project: $PROJECT_ID"
Write-Host "Region: $REGION"
Write-Host "Image name: $IMAGE_NAME"

# # Create image repository (ignore error if it already exists)
# Write-Host "Creating repository (if needed)..."
# gcloud artifacts repositories create $REPO_NAME `
#   --repository-format=docker `
#   --location=$REGION `
#   2>$null

# # Build and push Docker image
# Write-Host "Building the image and pushing to Artifact Registry..."
# gcloud builds submit --tag "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME" .

# # Deploy to Cloud Run
# Write-Host "Deploying to Cloud Run..."
# gcloud run deploy flask-service `
#   --image "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME" `
#   --platform managed `
#   --region $REGION `
#   --allow-unauthenticated

gcloud builds submit --tag "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME" .

gcloud run deploy flask-service \
  --image "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME" \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated