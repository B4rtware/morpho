from pathlib import Path
import sys
import sqlite3
import datetime
import waitress
from threading import Thread
import falcon
from dataclasses import dataclass
import dataclasses
from multiprocessing import Process
from typing import Tuple, Optional
import json

sys.path.append(str(Path(".").resolve()))

from dtaservice.dtaservice_pb2 import TransformDocumentResponse
from dtaservice.dtaservice_pb2_grpc import DTAServerStub
from services.services import DTAServer

db_path = Path(__file__).parent / Path("traces.db")


@dataclass
class Trace:
    created: str
    app_name: str
    is_unittest: bool


class Traces(object):
    def on_get(self, req, resp):
        conn = sqlite3.connect(db_path.absolute())
        c = conn.cursor()

        res = c.execute("SELECT * FROM traces").fetchall()

        # print(res.fetchall())
        # fast serialize
        traces = [dataclasses.asdict(Trace(*r)) for r in res]

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(traces, indent=4)

    def on_put(self, req, resp):
        conn = sqlite3.connect(db_path.absolute())
        c = conn.cursor()

        print(req)



app = falcon.API()
traces = Traces()
app.add_route("/traces", traces)


class QDS_DATABASE(DTAServer):
    def __init__(self):
        print("setup database")
        db_exists = db_path.exists()
        self.conn = sqlite3.connect(db_path.absolute(), check_same_thread=False)

        if not db_exists:
            c = self.conn.cursor()
            c.execute(
                """CREATE TABLE traces (created text, app_name text, is_unittest int)"""
            )

        print("start trace server")
        self.web_thread = Thread(target=waitress.serve, args=(app,), daemon=True)
        self.web_thread.start()
        print("still running")

    def work(self, request, context) -> Tuple[str, Optional[str]]:
        c = self.conn.cursor()
        cur_datetime = datetime.datetime.now().isoformat()
        print(f"INSERT INTO traces VALUES ({cur_datetime}, {request.service_name}, 0)")
        c.execute(
            f"INSERT INTO traces VALUES ('{cur_datetime}', '{request.service_name}', 0)"
        )

        self.conn.commit()

        return ("Added new database entry.", None)

    def __del__(self):
        self.web_thread.join()
        print("closed web thread")


QDS_DATABASE.run(50053)
