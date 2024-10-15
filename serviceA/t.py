import time
import requests
from collections import deque
from flask import Flask, jsonify
from flask_cors import CORS
import threading
from types_defs import BitcoinPriceIndexResponse

app = Flask(__name__)
CORS(app)


BITCOIN_PRICE_URL = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
PRICE_SAMPLES_BATCH_SIZE = 10
POLL_INTERVAL_LENGTH_SECONDS = 1

UNAVERAGED_PRICE_BATCH = deque(maxlen=10)


def print_average_price():
    avg_price = sum(UNAVERAGED_PRICE_BATCH) / PRICE_SAMPLES_BATCH_SIZE
    print(f"Average Bitcoin Price over last 10 minutes: ${avg_price}")


def fetch_bitcoin_price() -> BitcoinPriceIndexResponse:
    return requests.get(BITCOIN_PRICE_URL).json()


def track_bitcoin_usd_price():
    while True:
        try:
            bitcoin_price_data = fetch_bitcoin_price()
            price = float(bitcoin_price_data["bpi"]["USD"]["rate"].replace(",", ""))
            UNAVERAGED_PRICE_BATCH.append(price)
            print(f"{len(UNAVERAGED_PRICE_BATCH)}: Current Bitcoin Price: ${price}")

            if len(UNAVERAGED_PRICE_BATCH) == PRICE_SAMPLES_BATCH_SIZE:
                print_average_price()
                UNAVERAGED_PRICE_BATCH.clear()
        except Exception as e:
            print(f"Error fetching Bitcoin price: {e}")
        finally:
            time.sleep(POLL_INTERVAL_LENGTH_SECONDS)


@app.route("/average_price")
def get_average_price():
    if UNAVERAGED_PRICE_BATCH:
        avg_price = sum(UNAVERAGED_PRICE_BATCH) / len(UNAVERAGED_PRICE_BATCH)
        return jsonify({"average_price": avg_price})
    else:
        return jsonify({"message": "No prices available yet"}), 404


if __name__ == "__main__":
    fetch_thread = threading.Thread(target=track_bitcoin_usd_price, daemon=True)
    fetch_thread.start()
    app.run(host="0.0.0.0", port=80)
