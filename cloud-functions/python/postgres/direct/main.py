# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functions_framework
import psycopg


@functions_framework.http
def hello_time(request):
    """Hello world style Cloud Function that returns the current time.
    
    Update below values to connect to your Cloud SQL instance.
    """
    # create a connection to the Cloud SQL instance's private IP address
    with psycopg.connect(
        host="10.0.0.1",  # Cloud SQL private IP address
        port="5432",
        user="postgres",
        password="my-password",
        dbname="my-database",
        sslmode="require",  # Use SSL for secure connection
    ) as conn:
        # Open a cursor to perform database operations
        with conn.cursor() as cur:

            # Execute a query
            cur.execute("SELECT NOW()")

            # Fetch the result
            result = cur.fetchone()

    # Return the result as a string
    return str(result[0])





