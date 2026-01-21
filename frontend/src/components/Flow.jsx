export default function Flow({ flow }) {
  return (
    <section className="panel" id="flow">
      <h2>System Flow</h2>
      <div className="flow">
        {flow.map((step, index) => (
          <div className="flow-step" key={step}>
            <span>{index + 1}</span>
            <p>{step}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
