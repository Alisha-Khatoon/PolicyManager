import { useState } from "react";
import api from "../services/api";

function UploadForm({ onUploadComplete }) {
  const [files, setFiles] = useState([]);
  const [status, setStatus] = useState("");

  const handleFileChange = (e) => {
    const newFiles = Array.from(e.target.files);
    setFiles((prevFiles) => [...prevFiles, ...newFiles]);
  };

  const handleUpload = async () => {
    if (!files.length) return;

    setStatus("Uploading...");
    const formData = new FormData();
    files.forEach((f) => formData.append("files", f));

    try {
      // CHANGED: Removed redundant /api and corrected endpoint to /policies/upload
      const res = await api.post("/policies/upload", formData);
      console.log("Upload response:", res.data);
      setStatus("Upload successful ✅");
      setFiles([]);
      onUploadComplete();
    } catch (err) {
      console.error("Upload failed:", err);
      setStatus("Upload failed ❌");
    }
  };

  const removeFile = (index) => {
    setFiles((prevFiles) => prevFiles.filter((_, i) => i !== index));
  };

  return (
    <div className="p-4 bg-white rounded shadow mb-6">
      <h2 className="text-lg font-semibold mb-2">Upload New Policies</h2>
      <input
        type="file"
        multiple
        accept=".pdf,.docx"
        onChange={handleFileChange}
        className="mb-2"
      />

      {files.length > 0 && (
        <div className="mb-4">
          <h3 className="text-sm font-medium mb-1">Selected files:</h3>
          <ul className="space-y-1">
            {files.map((file, index) => (
              <li
                key={index}
                className="flex items-center justify-between text-sm"
              >
                <span>{file.name}</span>
                <button
                  onClick={() => removeFile(index)}
                  className="text-red-500 hover:text-red-700"
                >
                  ×
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="flex items-center gap-4">
        <button
          onClick={handleUpload}
          className="px-4 py-2 bg-blue-600 text-white rounded"
          disabled={!files.length}
        >
          ⬆️ Upload
        </button>
        <span className="text-sm text-gray-600">{status}</span>
      </div>
    </div>
  );
}

export default UploadForm;
