# Apple HIG JSON shape (DocC)

Endpoints:
- Table of contents: `https://developer.apple.com/tutorials/data/design/human-interface-guidelines.json`
- One page: `https://developer.apple.com/tutorials/data/design/human-interface-guidelines/<slug>.json`

Send a normal browser `User-Agent`. Only needed when `hig.py` cannot run.

## Top-level keys

| Key | Meaning |
|---|---|
| `metadata.title` | Page title |
| `metadata.customMetadata` | `supported-platforms`, `alert-date` (last update), `alert-text` |
| `abstract` | One-sentence summary (inline nodes) |
| `primaryContentSections[].content` | The page body: array of block nodes |
| `topicSections[].identifiers` | Child pages (collection pages and the TOC) |
| `references` | Lookup table for every identifier: `title`, `abstract`, `url`, `role`, `kind` |

## Block nodes (`type`)

`heading` (`level`, `text`, `anchor`), `paragraph` / `small` (`inlineContent`), `unorderedList` / `orderedList` (`items[].content`), `table` (`rows[][]` of cells, each cell an array of blocks), `aside` (`style`, `name`, `content`), `row` (`columns[].content`), `tabNavigator` (`tabs[].title`, `tabs[].content`), `links` (`items` = identifiers), `codeListing` (`syntax`, `code[]`). Images and videos can be ignored.

## Inline nodes

`text`, `strong`, `emphasis`, `codeVoice` (`code`), `reference` (`identifier`, optional `overridingTitle`), `image`.

## Identifiers

`doc://com.apple.HIG/design/Human-Interface-Guidelines/<slug>[#Anchor]` → the page `<slug>` (lowercase), anchor as in the Apple URL `…/<slug>#Anchor`. Other `doc://com.apple.documentation/...` identifiers are developer-documentation symbols and articles; resolve their `url` through `references`.

## Platform sections

Under the `Platform considerations` heading (level 2), each platform is a level-3 heading (`iOS`, `macOS`, `tvOS`, `visionOS`, `watchOS`, …). Read only the ones you target.
