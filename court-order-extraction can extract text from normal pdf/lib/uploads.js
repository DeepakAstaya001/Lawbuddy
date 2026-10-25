import path from "path"

// Build a temp file path for an upload without trusting the client-supplied name.
// Strips directory components and unsafe characters so names like "../../x.pdf"
// can't escape the temp directory.
export function tempUploadPath(tempDir, originalName) {
  const baseName = path.basename(String(originalName || "upload")).replace(/[^\w.\- ()]/g, "_")
  const safeName = baseName.replace(/^\.+/, "") || "upload"
  return path.join(tempDir, `upload_${Date.now()}_${safeName}`)
}
