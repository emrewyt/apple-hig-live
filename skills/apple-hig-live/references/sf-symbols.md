# SF Symbols

Apple's symbol library (7,000+ symbols) is an app and font; there is no JSON catalog of names. Rules for agents:

- Read the HIG page first: `hig.py page sf-symbols`.
- Use names from this file or from the user. For any other name write `verify in SF Symbols app`.
- Availability differs by OS version; check in the SF Symbols app before shipping.
- Browse: https://developer.apple.com/sf-symbols/

## Naming

Lowercase, dot-separated: `house`, `house.fill`, `person.crop.circle`.
Variants are suffixes: `.fill`, `.circle`, `.circle.fill`, `.square`, `.slash`, `.badge.plus`.

## Rendering modes

`monochrome` (one color), `hierarchical` (one color, layered opacity), `palette` (explicit colors per layer), `multicolor` (built-in colors).

## Usage

```swift
Image(systemName: "house.fill")
    .symbolRenderingMode(.hierarchical)
    .foregroundStyle(.tint)
    .font(.title2)                        // symbols scale with text styles

Label("Settings", systemImage: "gearshape")   // preferred: icon + text, adapts per context
Image(systemName: "heart").symbolVariant(.fill)
Image(systemName: "bell").symbolEffect(.bounce)   // iOS 17+
```

UIKit: `UIImage(systemName: "house.fill")`. AppKit: `NSImage(systemSymbolName: "house.fill", accessibilityDescription: "Home")`.

HTML mockups cannot render SF Symbols: use a neutral placeholder glyph and annotate it with the symbol name.

## Common symbols

| Area | Names |
|---|---|
| Navigation | `house` `house.fill` `magnifyingglass` `gearshape` `gearshape.fill` `sidebar.left` `line.3.horizontal` `list.bullet` `square.grid.2x2` `slider.horizontal.3` |
| Directions | `chevron.left` `chevron.right` `chevron.up` `chevron.down` `arrow.left` `arrow.right` `arrow.up` `arrow.down` `arrow.clockwise` `arrow.counterclockwise` |
| Actions | `plus` `plus.circle.fill` `minus` `xmark` `xmark.circle.fill` `checkmark` `checkmark.circle.fill` `trash` `pencil` `square.and.pencil` `square.and.arrow.up` `square.and.arrow.down` `doc.on.doc` `ellipsis` `ellipsis.circle` |
| Status | `info.circle` `exclamationmark.triangle` `questionmark.circle` `bell` `bell.fill` `lock` `lock.open` `eye` `eye.slash` |
| People | `person` `person.fill` `person.crop.circle` `person.2` |
| Content | `folder` `doc` `doc.text` `photo` `camera` `mic` `calendar` `clock` `envelope` `paperplane` `link` `globe` `tag` `flag` `bookmark` `bookmark.fill` `tray` |
| Media | `play.fill` `pause.fill` `forward.fill` `backward.fill` `speaker.wave.2` `music.note` |
| Social | `heart` `heart.fill` `star` `star.fill` `hand.thumbsup` `message` `phone` |
| Commerce | `cart` `bag` `creditcard` |
| Data | `chart.bar` `chart.line.uptrend.xyaxis` |
| Misc | `bolt.fill` `flame.fill` `sparkles` `map` `location` `wifi` `gamecontroller` `terminal` `wrench.and.screwdriver` |
