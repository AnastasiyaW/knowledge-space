---
title: UIKit and Storyboards (Legacy)
category: ios-mobile/ui
tags: [uikit, storyboards, objective-c, uitableview, uiviewcontroller, legacy]
---

# UIKit and Storyboards (Legacy)

## Key Facts

- UIKit is Apple's older imperative UI framework - still widely used in existing codebases
- Storyboards are visual interface builders using drag-and-drop - selected as "Storyboard" interface in project setup
- Objective-C was Apple's primary language before Swift - UIKit works with both Objective-C and Swift
- `UIViewController` is the base class for screen management in UIKit (no equivalent needed in SwiftUI)
- `UITableView` is UIKit's list view (equivalent to SwiftUI's `List`) - requires delegates and data sources
- Auto Layout is UIKit's constraint-based layout system (SwiftUI handles layout declaratively instead)
- UIKit uses the MVC pattern natively; SwiftUI uses MVVM more naturally
- SwiftUI views can embed UIKit views via `UIViewRepresentable` for backward compatibility
- UIKit views can embed SwiftUI via `UIHostingController` for gradual migration
- Many companies still maintain UIKit codebases - knowing both is valuable for employment

## Patterns

```swift
// UIKit ViewController (imperative style)
class ViewController: UIViewController {
    @IBOutlet weak var tableView: UITableView!

    var items: [String] = ["Item 1", "Item 2", "Item 3"]

    override func viewDidLoad() {
        super.viewDidLoad()
        tableView.delegate = self
        tableView.dataSource = self
    }
}

extension ViewController: UITableViewDataSource {
    func tableView(_ tableView: UITableView,
                   numberOfRowsInSection section: Int) -> Int {
        return items.count
    }

    func tableView(_ tableView: UITableView,
                   cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(
            withIdentifier: "cell",
            for: indexPath
        )
        cell.textLabel?.text = items[indexPath.row]
        return cell
    }
}
```

```swift
// Wrapping UIKit view for use in SwiftUI
struct ActivityIndicator: UIViewRepresentable {
    @Binding var isAnimating: Bool

    func makeUIView(context: Context) -> UIActivityIndicatorView {
        UIActivityIndicatorView(style: .large)
    }

    func updateUIView(_ uiView: UIActivityIndicatorView, context: Context) {
        isAnimating ? uiView.startAnimating() : uiView.stopAnimating()
    }
}
```

## Gotchas

- UIKit requires significantly more boilerplate code than SwiftUI for the same functionality
- Storyboard files are XML under the hood - merge conflicts in teams are painful
- UIKit's delegate/datasource pattern is very different from SwiftUI's declarative approach
- Mixing UIKit and SwiftUI in one project works but adds complexity - plan migration carefully
- UIKit apps cannot use `@State`, `@Binding`, `@Observable` - these are SwiftUI-only property wrappers
- Many third-party tutorials and Stack Overflow answers still show UIKit solutions - verify framework before copying code
- Auto Layout constraints can cause ambiguous layout warnings - SwiftUI's stack-based layout avoids this entirely

## See Also

- [UIKit Documentation](https://developer.apple.com/documentation/uikit)
- [Migrating to SwiftUI](https://developer.apple.com/tutorials/swiftui)
- [[swiftui-views]]
- [[app-architecture-patterns]]
