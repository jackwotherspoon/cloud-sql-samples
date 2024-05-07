# Cloud SQL with Cloud Functions (Python)

```sh
  gcloud functions deploy hello-time-function \
    --gen2 \
    --runtime=python312 \
    --region=<REGION> \
    --source=. \
    --entry-point=hello_time \
    --trigger-http \
    --vpc-connector=<VPC_CONNECTOR> \
    --allow-unauthenticated
    ```

Replace `<REGION>` and `<VPC_CONNECTOR>` with the name of the Google Cloud
region where you want to deploy your function (for example, us-central1) and the
name of the serverless VPC connector.

The optional `--allow-unauthenticated` flag lets you reach your function
[without authentication](https://cloud.google.com/functions/docs/securing/managing-access-iam#allowing_unauthenticated_http_function_invocation).
