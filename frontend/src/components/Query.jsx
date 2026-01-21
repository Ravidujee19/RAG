export default function Query({
  query,
  setQuery,
  answer,
  renderSteps,
  onRun,
  onReset,
  resetStatus,
  onCacheReset,
  cacheStatus,
}) {
  return (
    <section className="panel" id="query">
      <h2>Ask the System</h2>

      <div className="query-card">
        <label>Your Query</label>
        <div className="query-row">
          <input value={query} onChange={(e) => setQuery(e.target.value)} />
          <button className="btn primary" onClick={onRun}>Run</button>
        </div>

        <div className="output">
          <strong>Answer</strong>
          <p>{answer || "No answer yet."}</p>
          <strong>Steps</strong>
          <pre>{renderSteps}</pre>
        </div>

        <div className="reset-row">
          <button className="btn ghost" onClick={onReset}>Reset System</button>
          <span>{resetStatus}</span>
        </div>

        <div className="reset-row">
          <button className="btn ghost" onClick={onCacheReset}>Clear LLM Cache</button>
          <span>{cacheStatus}</span>
        </div>
      </div>
    </section>
  );
}
