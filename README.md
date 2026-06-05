# Deploying a FastAPI to the cloud
A project to familiarise myself with a turnkey cloud application leveraging Docker, OpenTofu, FastAPI, SQL ORM...

## How to use
1. Clone repository
2. Build bootstrap infrastructure with OpenTofu. This will bootstrap a GCP project and bucket to store the working project filestate.
3. Build working project infrastructure with OpenTofu. Currently this step will fail when initialising the cloud run service as the image needs to be pushed manually to the artifact registry. Rerun this step after step 4.
4. Build docker image and push to registry `docker buildx build --platform linux/amd64 \ 
  -t europe-west4-docker.pkg.dev/${gcp_project_id}/${gcp_artifact_registry_repository_id}/api_app-api:latest \
  --push .`. This command also specifies a build architecture to matches the one on Cloud Run. 

## Notes
When hosting a db in a container, set up the container name as the environment variable `DB_HOST`. Using `localhost` will output an error as the database is no longer running at local host but inside the container 