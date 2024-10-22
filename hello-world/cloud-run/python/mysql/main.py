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

import atexit
import os

import pymysql
import sqlalchemy
from flask import Flask
from google.cloud.sql.connector import Connector

app = Flask(__name__)

# lazy initialize global connection pool to improve cold-starts and share
# connections across requests
pool = None
connector = None


def init_connection_pool(connector: Connector) -> sqlalchemy.engine.Engine:
    """Helper function to initialize SQLAlchemy connection pool engine with
    given Cloud SQL Python Connector object."""

    def getconn() -> pymysql.Connection:
        return connector.connect(
            "my-project:my-region:my-instance",  # Cloud SQL instance connection name
            "pymysql",
            user="my-user",
            password="my-password",
            db="my-database",
            ip_type="public",  # can also be one of "private" or "psc"
        )

    return sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )


@atexit.register
def shutdown() -> None:
    """Gracefully close Cloud SQL Python Connector object on app shutdown."""
    global connector
    if connector is not None:
        connector.close()


@app.route("/")
def hello_world():
    """Example Hello World route."""
    global pool, connector
    if connector is None:
        connector = Connector(refresh_strategy="lazy")
    if pool is None:
        pool = init_connection_pool(connector)
    with pool.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT 'Hello World!'"))
        return result.scalar()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
