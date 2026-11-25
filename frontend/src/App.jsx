import { useEffect, useState } from "react";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function App() {
  const [tests, setTests] = useState([]);
  const [executions, setExecutions] = useState([]);
  const [message, setMessage] = useState("Loading platform data...");
  const [busy, setBusy] = useState(false);

  async function refresh() {
    try {
      const [testResponse, executionResponse] = await Promise.all([
        fetch(`${API}/api/tests`),
        fetch(`${API}/api/executions`)
      ]);
      if (!testResponse.ok || !executionResponse.ok) throw new Error("API request failed");
      const testData = await testResponse.json();
      const executionData = await executionResponse.json();
      setTests(testData.items);
      setExecutions(executionData.items);
      setMessage("Connected to Turbo Practice API");
    } catch {
      setMessage("Cannot connect to API. Start the FastAPI backend on port 8000.");
    }
  }

  async function runSuite() {
    setBusy(true);
    try {
      const response = await fetch(`${API}/api/executions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ suite: "Authentication" })
      });
      if (!response.ok) throw new Error("Could not create execution");
      setMessage("Execution request queued. This starter version records the request; test-runner integration is a later phase.");
      await refresh();
    } catch {
      setMessage("Execution request failed. Check that the backend is running.");
    } finally {
      setBusy(false);
    }
  }

  useEffect(() => { refresh(); }, []);

  const passed = executions.reduce((sum, item) => sum + item.passed, 0);
  const failed = executions.reduce((sum, item) => sum + item.failed, 0);

  return (
    <main className="shell">
      <header className="topbar">
        <div><span className="eyebrow">QA AUTOMATION PLATFORM</span><h1>Turbo Test Automation</h1></div>
        <button onClick={refresh}>Refresh data</button>
      </header>
      <p className="status">{message}</p>
      <section className="metrics">
        <article><span>Test cases</span><strong>{tests.length}</strong></article>
        <article><span>Executions</span><strong>{executions.length}</strong></article>
        <article><span>Passed</span><strong>{passed}</strong></article>
        <article><span>Failed</span><strong>{failed}</strong></article>
      </section>
      <section className="panel">
        <div className="panel-heading"><div><h2>Test cases</h2><p>Available automated test scenarios</p></div><button disabled={busy} onClick={runSuite}>{busy ? "Queueing..." : "Run authentication suite"}</button></div>
        <div className="table-wrap"><table><thead><tr><th>ID</th><th>Test name</th><th>Suite</th></tr></thead>
          <tbody>{tests.map(test => <tr key={test.id}><td>{test.id}</td><td>{test.name}</td><td>{test.suite}</td></tr>)}</tbody>
        </table></div>
      </section>
      <section className="panel">
        <h2>Execution history</h2>
        {executions.length === 0 ? <p className="empty">No executions yet. Start the authentication suite to create one.</p> :
          <div className="table-wrap"><table><thead><tr><th>Execution ID</th><th>Suite</th><th>Status</th><th>Created</th></tr></thead>
            <tbody>{executions.map(item => <tr key={item.id}><td>{item.id.slice(0, 8)}</td><td>{item.suite}</td><td><span className="pill">{item.status}</span></td><td>{new Date(item.created_at).toLocaleString()}</td></tr>)}</tbody>
          </table></div>}
      </section>
      <footer>Turbo Practice Project · Learning implementation</footer>
    </main>
  );
}
