from flask import Flask, request, jsonify
from flask_cors import CORS
from email.mime.text import MIMEText
import smtplib
import numpy as np
import math
import joblib
import pandas as pd
import smtplib
import numpy as np
import requests
import traceback
app = Flask(__name__)
CORS(app)

# =====================================
# LOAD MODEL FILES
# =====================================

model = joblib.load("models/model.pkl")

site_encoder = joblib.load(
    "models/site_encoder.pkl"
)

camera_encoder = joblib.load(
    "models/camera_encoder.pkl"
)

target_encoder = joblib.load(
    "models/target_encoder.pkl"
)

junction_cameras = joblib.load(
    "models/junction_cameras.pkl"
)

traffic_data = pd.read_csv(
    "data/urbanwatch_master_processed.csv"
)

# =====================================
# HOME ROUTE
# =====================================

@app.route("/")
def home():

    return {
        "message":
        "TraffiCast Backend Running"
    }

# =====================================
# JUNCTION LIST ROUTE
# =====================================
@app.route(
    "/violation-peak-hours",
    methods=["POST"]
)
def violation_peak_hours():

    data = request.json
    junction = data["junction"]

    df = traffic_data[
        traffic_data["Site Name"] == junction
    ]

    violations = [
        "Violation of Red Light",
        "Triple Riding",
        "No Helmet",
        "Speed Violation"
    ]

    result = {}

    used_hours = set()

    for violation in violations:

        temp = df[
            df["Vio Description"] == violation
        ]

        if temp.empty:
            result[violation] = "-"
            continue

        hourly = (
            temp.groupby("hour")
            .size()
            .sort_values(
                ascending=False
            )
        )

        selected_hour = None

        for hour, count in hourly.items():

            hour = int(hour)

            if hour not in used_hours:

                selected_hour = hour
                used_hours.add(hour)
                break

        if selected_hour is None:
            result[violation] = "-"
            continue

        end_hour = (
            selected_hour + 2
        ) % 24

        def format_hour(h):

            suffix = (
                "AM"
                if h < 12
                else "PM"
            )

            display = h % 12

            if display == 0:
                display = 12

            return f"{display} {suffix}"

        result[violation] = (
            f"{format_hour(selected_hour)}"
            f" - "
            f"{format_hour(end_hour)}"
        )

    return jsonify(result)

@app.route("/junctions", methods=["GET"])
def get_junctions():

    junctions = list(
        site_encoder.classes_
    )

    return jsonify(junctions)

# =====================================
# JUNCTION COORDINATES
# =====================================

junction_coordinates = {

    "Attakulangara JN":
        {"lat": 8.4775, "lon": 76.9505},

    "Chanthavila":
        {"lat": 8.6035, "lon": 76.9185},

    "Chenkottukonam Jn":
        {"lat": 8.5670, "lon": 76.8900},

    "JAGATHY":
        {"lat": 8.5005, "lon": 76.9615},

    "Kaimanam Jn":
        {"lat": 8.4665, "lon": 76.9595},

    "Karakkamandapam Jn":
        {"lat": 8.4820, "lon": 76.9675},

    "Kazhakkoottam Jn":
        {"lat": 8.5585, "lon": 76.8755},

    "Kesavadasapuram JN":
        {"lat": 8.5265, "lon": 76.9440},

    "Kizhakke Mukkola":
        {"lat": 8.5385, "lon": 76.9865},

    "Kundamankadavu":
        {"lat": 8.5145, "lon": 76.9780},

    "MANNATHALLA":
        {"lat": 8.5480, "lon": 76.9465},

    "Mankuzhy":
        {"lat": 8.5185, "lon": 76.9505},

    "Nemom Jn":
        {"lat": 8.4235, "lon": 76.9895},

    "PATTOOR":
        {"lat": 8.4935, "lon": 76.9495},

    "Pappanamcode Jn":
        {"lat": 8.4705, "lon": 76.9610},

    "Poojapura Jn":
        {"lat": 8.4920, "lon": 76.9750},

    "Poonkulam Jn":
        {"lat": 8.4415, "lon": 76.9980},

    "STATUE NORTH":
        {"lat": 8.4923, "lon": 76.9478},

    "Shangumugham Jn":
        {"lat": 8.4825, "lon": 76.9125},

    "Statue South":
        {"lat": 8.4905, "lon": 76.9475},

    "Thirumala JN":
        {"lat": 8.5015, "lon": 76.9915},

    "VJT JN":
        {"lat": 8.4895, "lon": 76.9490},

    "Veli Bridge Rd":
        {"lat": 8.5060, "lon": 76.8890},

    "Vellayambalam":
        {"lat": 8.5065, "lon": 76.9610},

    "Vellayani Jn":
        {"lat": 8.4255, "lon": 76.9935}
}

@app.route(
    "/hourly-trend",
    methods=["POST"]
)
def hourly_trend():

    data = request.json

    junction = data["junction"]

    day = data["day"]

    filtered = traffic_data[
        (traffic_data["Site Name"] == junction)
        &
        (traffic_data["weekday"] == day)
    ]

    hour_counts = (
        filtered
        .groupby("hour")
        .size()
        .reset_index(name="count")
    )

    return jsonify(
        hour_counts.to_dict(
            orient="records"
        )
    )

@app.route(
    "/junction-coordinates",
    methods=["GET"]
)
def get_coordinates():

    return jsonify(
        junction_coordinates
    )
# =====================================
# HEATMAP ROUTE
# =====================================

@app.route(
    "/heatmap",
    methods=["GET"]
)
def heatmap():

    junction_counts = (
        traffic_data["Site Name"]
        .value_counts()
    )

    heatmap_data = []

    for junction, count in junction_counts.items():

        if str(junction) in junction_coordinates:

            heatmap_data.append(
                {
                    "junction": junction,

                    "lat":
                        junction_coordinates[str(junction)]["lat"],

                    "lon":
                        junction_coordinates[str(junction)]["lon"],

                    "score":
                        int(count)
                }
            )

    return jsonify(
        heatmap_data
    )
@app.route("/hour-ranking", methods=["POST"])
def hour_ranking():

    data = request.json

    time_range = data["range"]

    start, end = map(
        int,
        time_range.split("-")
    )

    df = traffic_data[
        (traffic_data["hour"] >= start)
        &
        (traffic_data["hour"] < end)
    ]

    ranking = (
        df.groupby("Site Name")
        .size()
        .reset_index(name="violations")
        .sort_values(
            by="violations",
            ascending=False
        )
    )

    result = []

    for _, row in ranking.iterrows():

        result.append({
            "junction":
            row["Site Name"],

            "violations":
            int(row["violations"])
        })

    return jsonify(result)

@app.route(
    "/heatmap/day",
    methods=["POST"]
)
def heatmap_day():

    data = request.json

    day = data["day"]

    filtered = traffic_data[
        traffic_data["weekday"] == day
    ]

    grouped = (

        filtered

        .groupby(
            [
                "Site Name",
                "Camera Location"
            ]
        )

        .size()

        .reset_index(
            name="count"
        )

    )

    junction_camera_counts = {}

    for junction in grouped[
        "Site Name"
    ].unique():

        camera_count = len(

            grouped[
                grouped["Site Name"]
                == junction
            ]

        )

        junction_camera_counts[
            junction
        ] = camera_count

    heat_points = []

    camera_position_tracker = {}

    for _, row in grouped.iterrows():

        junction = row[
            "Site Name"
        ]

        count = int(
            row["count"]
        )

        if junction not in junction_coordinates:

            continue

        lat = junction_coordinates[
            junction
        ]["lat"]

        lon = junction_coordinates[
            junction
        ]["lon"]

        if junction not in camera_position_tracker:

            camera_position_tracker[
                junction
            ] = 0

        camera_index = (

            camera_position_tracker[
                junction
            ]

        )

        camera_position_tracker[
            junction
        ] += 1

        camera_count = (

            junction_camera_counts[
                junction
            ]

        )

        angle = (

            2
            *
            math.pi
            *
            camera_index
            /
            camera_count

        )

        radius = 0.0008

        offset_lat = (

            radius
            *
            math.cos(angle)

        )

        offset_lon = (

            radius
            *
            math.sin(angle)

        )

        heat_points.append({

            "lat":
            lat + offset_lat,

            "lon":
            lon + offset_lon,

            "weight":
            count,

            "junction":
            junction

        })

    return jsonify(
        heat_points
    )

# =====================================
# PREDICT ROUTE
# =====================================

@app.route(
    "/risk-assessment",
    methods=["POST"]
)
def risk_assessment():

    data = request.json

    junction = data["junction"]

    day = data["day"]

    weekdays = [

        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"

    ]

    current_index = (
        weekdays.index(day)
    )

    previous_day = weekdays[
        (current_index - 1) % 7
    ]

    filtered = traffic_data[
        (traffic_data["Site Name"] == junction)
        &
        (traffic_data["weekday"] == day)
    ]

    if len(filtered) == 0:

        return jsonify({
            "error":
            "No data found"
        })

    junction_day_counts = (
        traffic_data
        .groupby(
            ["Site Name", "weekday"]
        )
        .size()
    )

    max_count = (
        junction_day_counts.max()
    )

    current_count = (
        len(filtered)
    )

    risk_score = round(
        (
            current_count
            /
            max_count
        ) * 100
    )

    hour_counts = (
        filtered["hour"]
        .value_counts()
    )

    peak_hour = (
        hour_counts.idxmax()
    )

    start_time = (
        pd.Timestamp(
            year=2025,
            month=1,
            day=1,
            hour=int(peak_hour)
        )
        .strftime("%I %p")
        .lstrip("0")
    )

    end_time = (
        pd.Timestamp(
            year=2025,
            month=1,
            day=1,
            hour=int(
                (peak_hour + 2) % 24
            )
        )
        .strftime("%I %p")
        .lstrip("0")
    )

    peak_hours = (
        f"{start_time} - {end_time}"
    )

    days_present = (
        filtered["Time"]
        .astype(str)
        .str[:10]
        .nunique()
    )

    expected_violations = round(
        current_count
        /
        max(days_present, 1)
    )

    previous_filtered = traffic_data[
        (traffic_data["Site Name"] == junction)
        &
        (traffic_data["weekday"] == previous_day)
    ]

    previous_count = len(
        previous_filtered
    )

    if previous_count > 0:

        trend_percentage = round(
            (
                current_count
                -
                previous_count
            )
            /
            previous_count
            * 100,
            1
        )

    else:

        trend_percentage = 0

    most_common_violation = (
        filtered[
            "Vio Description"
        ]
        .mode()[0]
    )

    highest_risk_camera = (
        filtered[
            "Camera Location"
        ]
        .value_counts()
        .idxmax()
    )

    return jsonify({

        "risk_score":
        int(risk_score),

        "peak_hours":
        peak_hours,

        "expected_violations":
        int(expected_violations),

        "trend_percentage":
        trend_percentage,

        "previous_day":
        previous_day,

        "most_common_violation":
        most_common_violation,

        "highest_risk_camera":
        highest_risk_camera

    })

@app.route(
    "/analytics",
    methods=["GET"]
)
def analytics():

    total_violations = len(
        traffic_data
    )

    top_junction = (

        traffic_data[
            "Site Name"
        ]

        .value_counts()

        .idxmax()

    )

    most_common_violation = (

        traffic_data[
            "Vio Description"
        ]

        .value_counts()

        .idxmax()

    )

    highest_risk_camera = (

        traffic_data[
            "Camera Location"
        ]

        .value_counts()

        .idxmax()

    )

    top5 = (

        traffic_data[
            "Site Name"
        ]

        .value_counts()

        .head(5)

        .reset_index()

    )

    top5.columns = [

        "junction",

        "violations"

    ]

    violation_distribution = (

        traffic_data[
            "Vio Description"
        ]

        .value_counts()

        .head(5)

        .reset_index()

    )

    violation_distribution.columns = [

        "name",

        "value"

    ]

    return jsonify({

        "total_violations":
        int(total_violations),

        "top_junction":
        top_junction,

        "most_common_violation":
        most_common_violation,

        "highest_risk_camera":
        highest_risk_camera,

        "top5":
        top5.to_dict(
            orient="records"
        ),

        "violation_distribution":
        violation_distribution.to_dict(
            orient="records"
        )

    })   
@app.route(
    "/expected-violations",
    methods=["POST"]
)
def expected_violations():

    data = request.json

    junction = data["junction"]
    day = data["day"]

    df = traffic_data[
        (traffic_data["Site Name"] == junction)
        &
        (traffic_data["day"] == day)
    ]

    violations = [
        "No Helmet",
        "Violation of Red Light",
        "Triple Riding",
        "Speed Violation"
    ]

    result = {}

    total = 0

    for violation in violations:

        temp = df[
    df["Vio Description"]
    .str.contains(
        violation,
        case=False,
        na=False
    )
]

        expected = len(temp)

        result[violation] = expected

        total += expected

    result["total"] = total

    return jsonify(result)



@app.route(
    "/weekday-analytics",
    methods=["GET"]
)
def weekday_analytics():

    weekday_counts = (

        traffic_data

        .groupby("weekday")

        .size()

        .reset_index(
            name="violations"
        )

    )

    return jsonify(

        weekday_counts.to_dict(
            orient="records"
        )

    )

@app.route(
    "/violation-stats",
    methods=["POST"]
)
def violation_stats():

    data = request.json

    junction = data["junction"]

    day = data["day"]

    filtered = traffic_data[
        (traffic_data["Site Name"] == junction)
        &
        (traffic_data["weekday"] == day)
    ]

    stats = {

        "No Helmet": 0,
        "Red Light": 0,
        "Speeding": 0,
        "Triple Riding": 0

    }

    for violation in stats.keys():

        stats[violation] = int(

            len(

                filtered[
                    filtered[
                        "Vio Description"
                    ]
                    .str.contains(
                        violation,
                        case=False,
                        na=False
                    )
                ]

            )

        )

    return jsonify(stats)


@app.route("/send-alert", methods=["POST"])
def send_alert():

    try:

        data = request.json

        day = data["day"]

        sender = "mxnshadow007@gmail.com"
        password = "fqsmqunarzjsksuk"

        receiver = "sivanandanajp1233@gmail.com"

        day_df = traffic_data[
            traffic_data["weekday"] == day
        ]

        violations = [
            "No Helmet",
            "Violation of Red Light",
            "Triple Riding",
            "Speed Violation"
        ]

        time_slots = [

            (0,2),
            (2,4),
            (4,6),
            (6,8),
            (8,10),
            (10,12),
            (12,14),
            (14,16),
            (16,18),
            (18,20),
            (20,22),
            (22,24)

        ]

        def slot_name(start,end):

            def convert(hour):

                suffix = "AM" if hour < 12 else "PM"

                display = hour % 12

                if display == 0:
                    display = 12

                return f"{display} {suffix}"

            return f"{convert(start)} - {convert(end%24)}"

        html = f"""
        <html>

        <body style="font-family:Arial">

        <h2>UrbanWatch Traffic Alert</h2>

        <h3>Weekday : {day}</h3>

        <table border="1"
               cellspacing="0"
               cellpadding="8"
               style="border-collapse:collapse;
               width:100%;text-align:left;">

        <tr style="background:#0d6efd;color:white;">

        <th>Time Slot</th>

        <th>No Helmet</th>

        <th>Violation of Red Light</th>

        <th>Triple Riding</th>

        <th>Speed Violation</th>

        </tr>
        """

        for start,end in time_slots:

            slot_df = day_df[
                (day_df["hour"] >= start)
                &
                (day_df["hour"] < end)
            ]

            html += "<tr>"

            html += f"<td><b>{slot_name(start,end)}</b></td>"

            for violation in violations:

                temp = slot_df[
                    slot_df["Vio Description"]
                    .str.contains(
                        violation,
                        case=False,
                        na=False
                    )
                ]

                ranking = (
                    temp.groupby("Site Name")
                    .size()
                    .sort_values(
                        ascending=False
                    )
                    .head(5)
                )

                cell = ""

                if ranking.empty:

                    cell = "No Violations"

                else:

                    for i,(junction,count) in enumerate(ranking.items(),1):

                        cell += f"{i}. {junction} ({count})<br>"

                html += f"<td>{cell}</td>"

            html += "</tr>"

        html += """
        </table>

        </body>

        </html>
        """

        msg = MIMEText(
            html,
            "html"
        )

        msg["Subject"] = f"UrbanWatch Ranking Report - {day}"

        msg["From"] = sender

        msg["To"] = receiver

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            sender,
            password
        )

        server.sendmail(
            sender,
            receiver,
            msg.as_string()
        )

        server.quit()

        return jsonify({

            "message":
            "Email sent successfully"

        })

    except Exception as e:

      traceback.print_exc()

      return jsonify({
        "message": str(e)
       }), 500
# =====================================
# START SERVER
# =====================================

if __name__ == "__main__":

    app.run(
        debug=True
    )