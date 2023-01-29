import "json"
import "http"

option task = {name: "example_task", cron: "*/1 * * * *", offset: 1m}

host = "example_host"
token = "example_token"

query_data =
    from(bucket: "example_bucket", host: host, token: token)
        |> range(start: -30m)
        |> filter(fn: (r) => r["_measurement"] == "command_feedback")
        |> filter(fn: (r) => r["site_id"] == "example_site")
        |> filter(fn: (r) => r["_field"] == "action_status")
        |> aggregateWindow(every: 30m, fn: max, createEmpty: false)
        |> filter(fn: (r) => r._value == 8.0)
        |> group(columns: ["site_id", "_measurement"], mode: "by")
        |> map(
            fn: (r) =>
                ({r with jsonStr:
                        string(
                            v:
                                json.encode(
                                    v: {
                                        "deviceId": r.id,
                                        "asset name": r.asset_name,
                                        "parameter name": r.param_name,
                                        "site id": r.site_id,
                                        "Timestamp": r._time,
                                    },
                                ),
                        ),
                }),
        )
        |> map(
            fn: (r) =>
                ({r with _value:
                        http.post(
                            url: "https://webhook.site/75407646-69e2-4241-81a1-665ec8caecef",
                            data: bytes(v: r.jsonStr),
                        ),
                }),
        )
        |> yield(name: "mean")