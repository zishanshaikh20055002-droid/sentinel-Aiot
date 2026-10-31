# Sentinel AIoT Smart Sensor Laboratory

Interactive student-project simulation of a privacy-aware AIoT smart sensing system.

## Run locally

Serve `dist` with any static web server. The application is self-contained and uses synthetic telemetry.

## Demonstration workflow

1. Select Normal operation, Poor air quality event, or Heat anomaly event.
2. Select Start stream to generate secure telemetry from four virtual sensors.
3. Observe the digital twin, graph, pseudonymous telemetry table, latency, processing audit, and ML score.
4. Use an anomaly scenario to show a review alert and recommended action.
5. Select Show protected fields to compare excluded raw values with the analytics-safe representation.

## Multi-page project console

- **Operations Lab**: virtual building, sensors, live packets, data stream, and action alerts.
- **Analytics Centre**: continuous feature-vector stream, anomaly chart, data quality, drift, and model-service health.
- **Security Centre**: device registry, certificate status, security-event stream, retention, and privacy control view.
- **Project Guide**: architecture and a presentation-ready demonstration workflow.

## Demonstrated controls

- Five virtual edge and gateway devices mapped in a smart-building digital twin
- mTLS/TLS 1.3 communication concept and device verification
- Data minimisation, zone-level location, and pseudonymous identifiers
- Continuous cloud preprocessing and anomaly-based decision support
- Retention, role-based access, alert policy, and human override indicators
