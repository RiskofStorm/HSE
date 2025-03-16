import random
from datetime import datetime, timedelta

from hw_5_final.dags.db_conn import DbConnections, AirflowVariables

def load_to_mdb_datasets():
    def gen_user_sessions():
        delta = random.randint(1,600)
        start_time = datetime.now() - timedelta(days=delta)
        return {
            "session_id": str(random.randint(1, 10**6)),
            "user_id": random.randint(1, 10**5),
            "start_time": start_time,
            "end_time": start_time + timedelta(days=delta/2),
            "pages_visited": ["/checkout", "/product"],
            "device": {"type": "desktop", "os": "Windows 10", "browser": "Chrome"},
            "actions": ["add_to_cart", "view_product"],
        }

    def gen_product_price_history():
        pid = random.randint(1,10**5)
        delta = random.randint(1,600)
        price1 = random.randint(1,10**4)
        add_price = int(price1/2)
        return {
          'product_id': f"product_{pid}",
          'price_changes': [
             { "date":  datetime.now() - timedelta(days=delta), "price": price1  },
             { "date": datetime.now() - timedelta(days=int(delta/2)), "price": price1 + random.randint(-add_price, add_price)}
          ],
          "current_price": price1 + random.randint(-add_price, add_price),
          "currency": ["USD","EUR"][random.randint(0,1)]
       }

    mdb_conn = DbConnections.MongoDB.conn

    user_session = mdb_conn['user_session']
    product_price_history = mdb_conn['product_price_history']

    user_session.insert_many([
        gen_user_sessions() for _ in range(AirflowVariables.gen_data_number)
    ])
    product_price_history.insert_many([
         gen_product_price_history() for _ in range(AirflowVariables.gen_data_number)
    ])