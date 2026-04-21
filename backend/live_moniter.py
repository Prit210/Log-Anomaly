import time
import csv
import os
import sys
from datetime import datetime

from parser import TemplateParser
from inference import DeepLogInference

LOG_FILE = "logs.txt"
CSV_FILE = "output.csv"
TEMPLATE_FILE = "HDFS.log_templates.csv"

SUMMARY_INTERVAL = 10


# =========================
# CSV INIT
# =========================
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "block_id", "event", "status"])


# =========================
# FOLLOW FILE
# =========================
def follow(file):
    file.seek(0)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.2)
            continue
        yield line


# =========================
# MAIN
# =========================
def main():
    print("🚀 DeepLog Monitor (Template-Based)")
    print("📡 Listening...\n")

    parser = TemplateParser(TEMPLATE_FILE)

    detector = DeepLogInference(
        model_path="deeplog_hdfs_model.pth",
        mapping_path="event2idx.json",
        window_size=10,
        top_k=9,
        device="cpu"
    )

    last_summary_time = time.time()
    interval_status = []

    with open(LOG_FILE, "r") as f:
        for line in follow(f):
            parsed = parser.parse_line(line)

            for block_id, event in parsed:
                result = detector.process_event(block_id, event)

                if result is None:
                    continue

                status = "ABNORMAL" if result == 1 else "NORMAL"
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # 🚨 Immediate anomaly
                if status == "ABNORMAL":
                    print(f"🚨 {timestamp} | {block_id} | {event} | ABNORMAL")
                    sys.stdout.flush()

                interval_status.append(status)

                # save CSV
                with open(CSV_FILE, "a", newline="") as fcsv:
                    writer = csv.writer(fcsv)
                    writer.writerow([timestamp, block_id, event, status])

            # ⏱ summary
            if time.time() - last_summary_time >= SUMMARY_INTERVAL:
                if not interval_status:
                    summary = "NO DATA"
                elif "ABNORMAL" in interval_status:
                    summary = "ABNORMAL"
                else:
                    summary = "NORMAL"

                print(f"📊 {datetime.now()} | SUMMARY: {summary}")
                sys.stdout.flush()

                interval_status = []
                last_summary_time = time.time()


if __name__ == "__main__":
    main()