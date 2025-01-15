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

import os

import sqlalchemy
from flask import Flask

app = Flask(__name__)

# lazy initialize global connection pool to improve cold-starts and share
# connections across requests
pool = None


@app.route("/")
def hello_world():
    """Example Hello World route."""
    global pool
    if pool is None:
        pool = sqlalchemy.create_engine(
            # Equivalent URL:
            # postgresql+psycopg://<my-user>:<my-pass>@<host>:<port>/<db-name>
            sqlalchemy.engine.url.URL.create(
                drivername="postgresql+psycopg",
                username="my-user",
                password="my-password",
                host="10.0.0.1",  # your Cloud SQL IP address
                port="5432",
                database="my-database",
            ),
            connect_args={"sslmode": "require"},
        )
    with pool.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT 'Hello World!'"))
        return result.scalar()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
