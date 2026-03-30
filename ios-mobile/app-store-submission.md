---
title: App Store Submission and Distribution
category: ios-mobile/distribution
tags: [app-store, distribution, apple-id, review, publishing, testflight]
---

# App Store Submission and Distribution

## Key Facts

- Apple ID sign-in is required in Xcode before publishing to the App Store
- Apple Developer Program membership ($99/year) is required for App Store distribution
- Free Apple ID allows: running on simulator, limited physical device testing, accessing documentation
- App icon must be 1024x1024px - Apple auto-generates all other required sizes
- iOS 18 supports custom dark mode and tinted app icons - optional, Apple handles it automatically if not provided
- Bundle Identifier must be globally unique (reverse domain + product name: `com.company.appname`)
- App Review: Apple reviews all submitted apps - consider the reviewer's experience when designing
- TestFlight: Apple's beta testing platform - distribute pre-release builds to testers
- Build Settings to verify before submission: Swift Language Version, Deployment Target, Supported Devices
- [[xcode-project-setup]] must be configured correctly before any submission attempt
- Consider multiple platforms: iOS, iPadOS, macOS, watchOS, tvOS, visionOS - SwiftUI code is largely shared

## Patterns

```
Pre-submission checklist:
  1. Apple Developer Program enrolled ($99/year)
  2. Apple ID signed into Xcode (Xcode > Settings > Accounts)
  3. Bundle Identifier set and unique
  4. App icon added (1024x1024)
  5. Deployment target set (minimum iOS version)
  6. Version and build number configured
  7. Required device capabilities declared
  8. Privacy usage descriptions added (camera, location, etc.)
  9. App tested on simulator AND physical device
  10. Archive built (Product > Archive)

Submission flow:
  Xcode Archive > Distribute App > App Store Connect > Submit for Review

TestFlight distribution:
  Xcode Archive > Distribute App > TestFlight > Invite Testers
```

```swift
// Info.plist privacy descriptions (required for system features)
// Camera access
"Privacy - Camera Usage Description" = "We need camera access to take photos"
// Location
"Privacy - Location When In Use Usage Description" = "We need your location for map features"
// Photo Library
"Privacy - Photo Library Usage Description" = "We need access to save images"
```

## Gotchas

- Forgetting privacy descriptions for system features (camera, location, contacts) causes automatic rejection
- App Store review can take 1-7 days; plan release timing accordingly
- Bundle ID cannot be changed after first submission - choose carefully
- Free Apple ID testing on physical devices has a 7-day certificate expiration
- App icon must not have transparency or alpha channel - will be rejected
- Screenshots in App Store listing must match the actual current version of the app
- Version numbers must always increment for new submissions
- Apple can reject for subjective reasons (design quality, usefulness) - not just technical issues
- SwiftUI previews and simulator testing do not catch all device-specific issues - always test on physical device before submission

## See Also

- [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [App Store Connect](https://developer.apple.com/app-store-connect/)
- [TestFlight](https://developer.apple.com/testflight/)
- [[xcode-project-setup]]
- [[app-architecture-patterns]]
