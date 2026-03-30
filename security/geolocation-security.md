---
title: Geolocation in Security Systems
category: identification
tags: [geolocation, gps, ip-geolocation, timezone, location-spoofing]
---

# Geolocation in Security Systems

## Key Facts

- Geolocation methods: IP-based (GeoIP databases), GPS (mobile), Wi-Fi triangulation, cell tower triangulation, HTML5 Geolocation API
- IP geolocation accuracy: country ~99%, city ~70-80%, precise location unreliable without GPS
- [[anti-fraud-systems]] check consistency between IP geolocation, browser timezone, system language, and declared shipping/billing address
- Timezone mismatch between reported `Intl.DateTimeFormat().resolvedOptions().timeZone` and IP-derived timezone is a strong fraud signal
- Wi-Fi-based geolocation uses databases of known Wi-Fi BSSID positions (Google, Apple, Mozilla maintain these)
- [[network-identifiers]] reveal geolocation at the network level; browser APIs expose it at the application level

## Patterns

```javascript
// Browser geolocation API
navigator.geolocation.getCurrentPosition(
    (pos) => {
        console.log(`Lat: ${pos.coords.latitude}`);
        console.log(`Lon: ${pos.coords.longitude}`);
        console.log(`Accuracy: ${pos.coords.accuracy}m`);
    },
    (err) => console.error(err),
    { enableHighAccuracy: true, timeout: 5000 }
);

// Timezone detection (cannot be blocked by user)
const tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
// Returns e.g. "America/New_York"
// Must match IP geolocation for trusted session
```

```python
# Server-side geo consistency check
from math import radians, sin, cos, sqrt, atan2

def haversine_km(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in km"""
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1-a))

def check_geo_consistency(ip_geo: dict, browser_tz: str, gps: dict = None) -> dict:
    """
    Check if geolocation signals are consistent.
    ip_geo: {'lat': float, 'lon': float, 'country': str, 'timezone': str}
    """
    flags = []

    # Timezone mismatch
    if ip_geo['timezone'] != browser_tz:
        flags.append('timezone_mismatch')

    # If GPS available, check distance from IP location
    if gps:
        dist = haversine_km(ip_geo['lat'], ip_geo['lon'], gps['lat'], gps['lon'])
        if dist > 500:  # More than 500km apart
            flags.append('ip_gps_distance_anomaly')

    return {'consistent': len(flags) == 0, 'flags': flags}
```

## Gotchas

- GPS spoofing on Android is trivial with mock location apps; on iOS it requires jailbreak or Xcode developer tools
- Wi-Fi geolocation works even with GPS disabled and can be very accurate in urban areas (within 10-50 meters)
- Browser Geolocation API requires explicit user permission - but timezone and language are available without permission
- VPN geolocation mismatch is the single most common fraud signal detected by e-commerce platforms
- Mobile carriers sometimes report inaccurate geolocation due to IP address reassignment across regions
- Geolocation databases (MaxMind, IP2Location) have different accuracy levels and update frequencies

## See Also

- [MaxMind GeoIP2 Database](https://www.maxmind.com/en/geoip2-databases)
- [W3C Geolocation API Specification](https://www.w3.org/TR/geolocation/)
- [OWASP Geolocation Testing](https://owasp.org/www-project-web-security-testing-guide/)
