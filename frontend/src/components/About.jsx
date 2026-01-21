export default function About({ sections }) {
  return (
    <section className="panel">
      <h2>About This App</h2>
      <div className="about-grid">
        {sections.map((section) => (
          <article key={section.title} className="about-card">
            <h3>{section.title}</h3>
            <p>{section.body}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
