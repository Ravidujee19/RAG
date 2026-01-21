export default function Ingest({
  uploadColumn,
  setUploadColumn,
  uploadStatus,
  dbConn,
  setDbConn,
  dbQuery,
  setDbQuery,
  dbColumns,
  setDbColumns,
  dbStatus,
  onUpload,
  onDbIngest,
}) {
  return (
    <section className="panel" id="ingest">
      <h2>Ingest Data</h2>

      <div className="ingest-grid">
        <form className="ingest-card" onSubmit={onUpload}>
          <h3>Upload CSV, PDF, DOCX, TXT</h3>
          <label>File</label>
          <input name="file" type="file" />
          <label>CSV Text Column (optional)</label>
          <input
            value={uploadColumn}
            onChange={(e) => setUploadColumn(e.target.value)}
          />
          <button className="btn primary">Upload & Index</button>
          <div className="status">{uploadStatus}</div>
        </form>

        <form className="ingest-card" onSubmit={onDbIngest}>
          <h3>Database Ingest</h3>
          <label>Connection String</label>
          <input value={dbConn} onChange={(e) => setDbConn(e.target.value)} />
          <label>SQL Query</label>
          <textarea rows="3" value={dbQuery} onChange={(e) => setDbQuery(e.target.value)} />
          <label>Columns</label>
          <input value={dbColumns} onChange={(e) => setDbColumns(e.target.value)} />
          <button className="btn primary">Index Database</button>
          <div className="status">{dbStatus}</div>
        </form>
      </div>
    </section>
  );
}
