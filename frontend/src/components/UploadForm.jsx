import { useState } from "react";

function UploadForm({ onUploadComplete }) {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const handleUpload = async () => {
    if (!file) return;

    setStatus("Uploading...");
    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch("http://localhost:8000/api/policies/upload", {
          method: "POST",
          body: formData,
        });

      if (!res.ok) throw new Error("Upload failed");

      const _result = await res.json();
      setStatus("Upload successful ✅");
      setFile(null);
      onUploadComplete(); // Trigger refresh
    } catch (err) {
      console.error(err);
      setStatus("Upload failed ❌");
    }
  };

  return (
    <div className="p-4 bg-white rounded shadow mb-6">
      <h2 className="text-lg font-semibold mb-2">Upload New Policy</h2>
      <input
        type="file"
        accept=".pdf,.docx"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-2"
      />
      <div className="flex items-center gap-4">
        <button
          onClick={handleUpload}
          className="px-4 py-2 bg-blue-600 text-white rounded"
          disabled={!file}
        >
          ⬆️ Upload
        </button>
        <span className="text-sm text-gray-600">{status}</span>
      </div>
    </div>
  );
}

export default UploadForm;
