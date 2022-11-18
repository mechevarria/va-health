import ayasdi.core as ac
from flask import jsonify

class StatusService():
  conn: ac.Api
  eureka_user: str
  eureka_url: str

  def __init__(self, conn, eureka_user, eureka_url):
    self.conn = conn
    self.eureka_user = eureka_user
    self.eureka_url =eureka_url

  def get(self):
    return jsonify(is_connected=self.conn.is_connected, eureka_user=self.eureka_user, eureka_url=self.eureka_url)

