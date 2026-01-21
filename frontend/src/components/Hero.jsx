export default function Hero({ onRun }) {
  return (
    <header className="hero">
      <div className="hero-copy">
        <p className="eyebrow">Hybrid Multi-Agent RAG</p>
        <h1>Build grounded answers with local retrieval and Gemini planning.</h1>
        <p className="lead">
          This interface showcases the system architecture and lets you ingest data and run queries without the CLI.
        </p>
        <div className="hero-actions">
          <button className="btn primary" onClick={onRun}>Run Query</button>
          <a className="btn ghost" href="#ingest">Ingest Data</a>
        </div>
      </div>

      <div className="hero-card">
        <h3>System Snapshot</h3>
        <ul>
          <li>Agents: Aggregator + Retrieval + Tools + Web</li>
          <li>Vector DB: Chroma</li>
          <li>Memory: Short-term + SQLite</li>
          <li>LLM: Gemini Adapter</li>
        </ul>
      </div>
    </header>
  );
}
