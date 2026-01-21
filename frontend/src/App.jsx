import { useMemo, useState } from "react";
import Hero from "./components/Hero";
import About from "./components/About";
import Flow from "./components/Flow";
import Ingest from "./components/Ingest";
import Query from "./components/Query";
import { sections, flow } from "./constants";

const apiBase =
  location.hostname === "localhost" || location.hostname === "127.0.0.1"
    ? "http://127.0.0.1:8000"
    : location.origin;

export default function App() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [steps, setSteps] = useState([]);

  const [uploadStatus, setUploadStatus] = useState("Awaiting upload...");
  const [dbStatus, setDbStatus] = useState("Awaiting database input...");
  const [resetStatus, setResetStatus] = useState("System is ready.");
  const [cacheStatus, setCacheStatus] = useState("Cache ready.");

  const [uploadColumn, setUploadColumn] = useState("");
  const [dbConn, setDbConn] = useState("");
  const [dbQuery, setDbQuery] = useState("");
  const [dbColumns, setDbColumns] = useState("");

  const renderSteps = useMemo(() => {
    if (!steps.length) return "No steps yet.";
    return steps
      .map((s, i) => `${i + 1}. ${s.action || "action"}: ${s.output || ""}`)
      .join("\n");
  }, [steps]);

  const handleRun = async () => {
    if (!query.trim()) {
      setAnswer("Enter a query to run.");
      return;
    }
    setAnswer("Running...");
    try {
      const res = await fetch(`${apiBase}/api/v1/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail);
      setAnswer(data.answer || "");
      setSteps(data.steps || []);
    } catch (e) {
      setAnswer(`FAIL: ${e.message}`);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    const file = e.target.elements.file.files[0];
    if (!file) {
      setUploadStatus("Select a file to upload.");
      return;
    }
    setUploadStatus("Uploading...");
    const form = new FormData();
    form.append("file", file);
    if (uploadColumn.trim()) form.append("text_column", uploadColumn.trim());

    try {
      const res = await fetch(`${apiBase}/api/v1/ingest/upload`, {
        method: "POST",
        body: form,
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail);
      setUploadStatus(`OK: indexed ${data.indexed}`);
    } catch (e) {
      setUploadStatus(`FAIL: ${e.message}`);
    }
  };

  const handleDbIngest = async (e) => {
    e.preventDefault();
    if (!dbConn || !dbQuery || !dbColumns) {
      setDbStatus("Fill all fields.");
      return;
    }
    setDbStatus("Indexing...");
    try {
      const res = await fetch(`${apiBase}/api/v1/ingest/db`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          connection_string: dbConn,
          query: dbQuery,
          columns: dbColumns.split(",").map(c => c.trim()),
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail);
      setDbStatus(`OK: indexed ${data.indexed}`);
    } catch (e) {
      setDbStatus(`FAIL: ${e.message}`);
    }
  };

  const handleReset = async () => {
    setResetStatus("Resetting...");
    const res = await fetch(`${apiBase}/api/v1/reset`, { method: "POST" });
    const data = await res.json();
    if (res.ok) {
      setSteps([]);
      setAnswer("");
      setResetStatus("OK: system reset");
    } else {
      setResetStatus(`FAIL: ${data.detail}`);
    }
  };

  const handleCacheReset = async () => {
    setCacheStatus("Clearing...");
    const res = await fetch(`${apiBase}/api/v1/reset-cache`, { method: "POST" });
    const data = await res.json();
    setCacheStatus(res.ok ? "OK: cache cleared" : `FAIL: ${data.detail}`);
  };

  return (
    <div className="page">
      <Hero onRun={handleRun} />
      <About sections={sections} />
      <Flow flow={flow} />
      <Ingest
        uploadColumn={uploadColumn}
        setUploadColumn={setUploadColumn}
        uploadStatus={uploadStatus}
        dbConn={dbConn}
        setDbConn={setDbConn}
        dbQuery={dbQuery}
        setDbQuery={setDbQuery}
        dbColumns={dbColumns}
        setDbColumns={setDbColumns}
        dbStatus={dbStatus}
        onUpload={handleUpload}
        onDbIngest={handleDbIngest}
      />
      <Query
        query={query}
        setQuery={setQuery}
        answer={answer}
        renderSteps={renderSteps}
        onRun={handleRun}
        onReset={handleReset}
        resetStatus={resetStatus}
        onCacheReset={handleCacheReset}
        cacheStatus={cacheStatus}
      />
    </div>
  );
}
