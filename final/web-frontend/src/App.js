import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [selectedFileName, setSelectedFileName] = useState("");
  const [report, setReport] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false); // <-- loading state

  const handleFileChange = (e) => {
    if (e.target.files[0]) {
      setSelectedFileName(e.target.files[0].name);
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setReport("");
    setLoading(true); // <-- Start loading

    if (!file) {
      setError("Please select a file to audit.");
      setLoading(false);
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:5000/audit", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setReport(res.data.html_report);
    } catch (err) {
      setError(
        err.response?.data?.error ||
          "Audit failed: Network or server error."
      );
    } finally {
      setLoading(false); // <-- Stop loading
    }
  };

  return (
    <div className="App">
      <h2>Code Security Audit Tool</h2>
      <form onSubmit={handleSubmit}>
        {/* Custom file upload button */}
        <label className="custom-file-label" htmlFor="file-upload">
          Choose File
        </label>
        <input
          id="file-upload"
          type="file"
          accept=".py"
          onChange={handleFileChange}
        />
        <span className="selected-file-name">{selectedFileName}</span>
        <button type="submit" disabled={loading}>
          Run Audit
        </button>
      </form>
      {error && <div className="error">{error}</div>}
      {loading && (
        <div className="auditing-message">
          Auditing...
        </div>
      )}
      {report && !loading && (
        <div
          className="report-container"
          dangerouslySetInnerHTML={{ __html: report }}
        />
      )}
    </div>
  );
}

export default App;