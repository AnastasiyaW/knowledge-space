---
title: Behavioral Analysis in Security
category: fraud-prevention
tags: [behavioral-analysis, mouse-tracking, bot-detection, user-behavior, biometrics]
---

# Behavioral Analysis in Security

## Key Facts

- Behavioral analysis identifies users by HOW they interact - mouse movements, typing patterns, scroll behavior, navigation flow
- PayPal pioneered MAP (Mouse Activity Pattern) system in 2013-2014 to distinguish humans from automated tools
- Behavioral biometrics are much harder to spoof than static identifiers like [[browser-fingerprinting]] or [[network-identifiers]]
- Key behavioral signals: mouse movement velocity/acceleration curves, click precision, typing cadence (dwell time + flight time), scroll patterns, touch pressure (mobile)
- Bot detection systems analyze timing regularity - bots produce unnaturally consistent intervals between actions
- [[anti-fraud-systems]] combine behavioral signals with device/network identifiers for comprehensive risk scoring

## Patterns

```javascript
// Client-side mouse movement tracking
const movements = [];
document.addEventListener('mousemove', (e) => {
    movements.push({
        x: e.clientX,
        y: e.clientY,
        t: Date.now(),
        type: 'move'
    });
});

document.addEventListener('click', (e) => {
    movements.push({
        x: e.clientX,
        y: e.clientY,
        t: Date.now(),
        type: 'click'
    });
});

// Send to server for analysis
function analyzeMovement(data) {
    // Calculate velocity between points
    // Human movements follow Fitts's Law
    // Bot movements are linear with constant velocity
    const velocities = [];
    for (let i = 1; i < data.length; i++) {
        const dx = data[i].x - data[i-1].x;
        const dy = data[i].y - data[i-1].y;
        const dt = data[i].t - data[i-1].t;
        const dist = Math.sqrt(dx*dx + dy*dy);
        velocities.push(dist / dt);
    }
    // High variance = human, low variance = bot
    return standardDeviation(velocities);
}
```

```python
# Server-side typing cadence analysis
def analyze_typing_pattern(keystrokes: list[dict]) -> dict:
    """
    keystrokes: [{'key': 'a', 'down': 1000, 'up': 1050}, ...]
    """
    dwell_times = []  # How long key is held
    flight_times = []  # Time between releasing one key and pressing next

    for i, ks in enumerate(keystrokes):
        dwell_times.append(ks['up'] - ks['down'])
        if i > 0:
            flight_times.append(ks['down'] - keystrokes[i-1]['up'])

    return {
        'avg_dwell': sum(dwell_times) / len(dwell_times),
        'std_dwell': statistics.stdev(dwell_times),
        'avg_flight': sum(flight_times) / len(flight_times),
        'std_flight': statistics.stdev(flight_times),
        # Low std = bot, high std = human
    }
```

## Gotchas

- Behavioral patterns can be replayed if recorded from a real user session - sophisticated attacks use captured human behavior
- Mobile behavioral analysis differs significantly from desktop - touch events, accelerometer data, gyroscope replace mouse/keyboard patterns
- Accessibility tools (screen readers, switch controls) produce patterns similar to bots - systems must account for this to avoid false positives
- VPN latency affects timing measurements and can distort behavioral signals
- Browser automation tools (Puppeteer, Playwright) increasingly support human-like mouse movement simulation

## See Also

- [BioCatch behavioral biometrics](https://www.biocatch.com/)
- [OWASP Testing Guide - Session Management](https://owasp.org/www-project-web-security-testing-guide/)
- [Fitts's Law applied to security](https://en.wikipedia.org/wiki/Fitts%27s_law)
