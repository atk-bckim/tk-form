# Resources (images)

Image resources embedded as base64 data URLs. Declared under `resources[]`. Widgets reference them by `id` via `props.image`.

## Shape

```jsonc
"resources": [
  {
    "id": "img-logo",
    "name": "logo",
    "type": "image",
    "dataUrl": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
  }
]
```

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Stable unique id. Referenced from `props.image` on widgets. |
| `name` | yes | Display name. Converted to a Python identifier for the resource attribute (`invalid_resource_name` if it can't be converted). Avoid spaces/symbols. |
| `type` | yes | Always `"image"`. No other resource types are currently supported. |
| `dataUrl` | no | Base64 data URL. Validated as base64 + checked for size. Empty string is allowed (engine treats as no-op). |

## Referencing from widgets

```jsonc
{
  "id": "label-logo",
  "type": "Label",
  "name": "logo_label",
  "props": {
    "image": "img-logo",          // references resources[].id
    "compound": "left",
    "text": "Branded label"
  }
}
```

If `props.image` references an id not present in `resources[]` → `missing_image_resource`.

## ⚠️ Validation rules

| Check | Code | Severity |
|---|---|---|
| `name` cannot be converted to a Python identifier | `invalid_resource_name` | error |
| `dataUrl` is not valid base64 | `invalid_image_data` | error |
| Decoded image bytes exceed the limit | `image_upload_too_large` | error |
| `props.image` references a missing resource | `missing_image_resource` | error |

## Size limit

Decoded image payload must be **≤ 5 MB** (`MAX_IMAGE_UPLOAD_BYTES` = 5 × 1024 × 1024 in `project_limits.py:2`). The base64 string itself will be ~33% larger.

The whole project payload (JSON) is capped at 8 MB (`MAX_PROJECT_PAYLOAD_BYTES`), so practically you can fit one ~5 MB image plus modest widget definitions.

## Generating the dataUrl

If you need to author a resource programmatically (not common from an AI authoring standpoint, but here for completeness), read the file and emit:

```
data:image/<ext>;base64,<base64-encoded-bytes>
```

Where `<ext>` is `png`, `jpeg`, `gif`, etc. Tkinter's `PhotoImage` accepts `png`, `gif`, `pgm`, `ppm` natively; other formats depend on the Tcl/Tk build.

## Minimal example

```jsonc
{
  "resources": [
    { "id": "img-logo", "name": "logo", "type": "image", "dataUrl": "data:image/png;base64,..." }
  ],
  "widgets": [
    { "id": "label-logo", "type": "Label", "name": "logo_label", "parentId": null,
      "x": 0, "y": 0, "width": 64, "height": 64,
      "props": { "image": "img-logo" } }
  ]
}
```
