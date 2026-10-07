const projects = [
  ['CodeForge','A security-conscious multi-agent engineering workspace for generating, testing, repairing and reviewing code.','Python · LangGraph · FastAPI · Docker','https://github.com/shyamprakash534/Codeforge','https://codeforge-3l85.onrender.com','01','AI / GENAI'],
  ['NanoLink','A distributed URL shortener engineered around caching, rate limiting, analytics and observability.','Go · Gin · PostgreSQL · Redis · ClickHouse','https://github.com/shyamprakash534/nanolink1','https://nanolink1.onrender.com','02','BACKEND / SYSTEMS'],
  ['Grounded RAG','A local-first RAG system that retrieves relevant knowledge and produces source-backed answers.','Python · FastAPI · ChromaDB · Ollama','https://github.com/shyamprakash534/grounded-rag','https://grounded-rag-oww5.onrender.com','03','GENAI / RAG'],
  ['AWS E-Commerce Pipeline','A raw → curated → analytics data workflow demonstrating practical AWS data engineering patterns.','S3 · Glue · Athena · PySpark · Terraform','https://github.com/shyamprakash534/aws-ecommerce-data-pipeline','https://aws-ecommerce-data-pipeline.onrender.com','04','CLOUD / DATA'],
  ['JobMatch AI','A source-first job matching product that parses resumes and ranks opportunities with weighted relevance.','Python · FastAPI · httpx · pypdf','https://github.com/shyamprakash534/ai-job-application-tracker','https://ai-job-application-tracker-o9vp.onrender.com','05','PYTHON / AI'],
  ['AI Drug Recommendation','An end-to-end ML application combining prediction, model evaluation and explainability.','Python · Scikit-learn · Flask · SHAP','https://github.com/shyamprakash534/drug-recommendation','https://drug-recommendation-5uxr.onrender.com','06','MACHINE LEARNING']
];

const skills = ['Python','Go','SQL','AI / ML','GenAI & RAG','FastAPI','Flask','AWS','ETL','PostgreSQL','Redis','Docker','Terraform','GitHub Actions','Scikit-learn','LangGraph','Ollama','ChromaDB'];

export default function Home() {
  return <main id="top">
    <div className="noise" />
    <nav className="nav">
      <a className="brand" href="#top"><span>VSP</span><i>●</i></a>
      <div className="navlinks"><a href="#about">About</a><a href="#work">Work</a><a href="#stack">Stack</a><a href="#contact">Contact</a></div>
      <a className="availability" href="mailto:shyamprakash271@gmail.com"><b></b> Available for opportunities</a>
    </nav>

    <section className="hero">
      <div className="hero-grid" />
      <div className="hero-glow glow-a" /><div className="hero-glow glow-b" />
      <div className="hero-copy">
        <div className="status"><span className="pulse" /> PYTHON · AI/ML · GENAI · BACKEND · CLOUD</div>
        <h1>Building digital<br/><span>systems that matter.</span></h1>
        <p className="hero-lead">I’m <strong>Vemula Syam Prakash</strong> — a Python developer and AI/ML engineer focused on practical products, intelligent workflows and reliable backend systems.</p>
        <div className="hero-actions"><a className="magnetic primary" href="#work">Explore my work <span>↘</span></a><a className="text-link" href="https://github.com/shyamprakash534" target="_blank">GitHub ↗</a><a className="text-link" href="https://www.linkedin.com/in/shyam-prakash-vemula-721029263/" target="_blank">LinkedIn ↗</a></div>
      </div>
      <div className="scroll-cue"><span>SCROLL</span><i /></div>
      <div className="hero-index">01 <span>/</span> 04</div>
    </section>

    <section className="intro section" id="about">
      <div className="section-kicker"><span>01</span> ABOUT</div>
      <div className="intro-grid">
        <h2>Software with<br/><em>intent.</em></h2>
        <div className="intro-copy"><p className="big-copy">MCA graduate with a Statistics background, combining quantitative thinking with software engineering to build useful technology.</p><p>I work across AI/ML, GenAI, Python backends, APIs, databases, ETL, cloud infrastructure and deployment.</p><p className="dim">Evidence over hype. Practical AI over unnecessary AI. Systems that are reproducible, secure and maintainable.</p></div>
      </div>
    </section>

    <section className="work section" id="work">
      <div className="section-kicker"><span>02</span> SELECTED WORK</div>
      <div className="work-head"><h2>Built in<br/><em>public.</em></h2><p>Six projects. Different problems. One obsession: making complex engineering feel useful.</p></div>
      <div className="project-grid">{projects.map(([name,desc,stack,repo,live,num,tag],i)=><article className={`project-card card-${i+1}`} key={name}><div className="card-top"><span>{num}</span><small>{tag}</small></div><div className="project-art"><div className="art-orbit"/><div className="art-core">{i===0?'AI':i===1?'↗':i===2?'RAG':i===3?'AWS':i===4?'AI':'ML'}</div></div><div className="project-info"><h3>{name}</h3><p>{desc}</p><div className="project-bottom"><span>{stack}</span><div><a href={repo} target="_blank">Repo ↗</a><a href={live} target="_blank">Live ↗</a></div></div></div></article>)}</div>
    </section>

    <section className="stack-section section" id="stack">
      <div className="section-kicker"><span>03</span> TOOLKIT</div>
      <div className="stack-layout"><h2>The stack<br/><em>behind it.</em></h2><div className="skill-cloud">{skills.map((s,i)=><span className={i%5===0?'featured':''} key={s}>{s}</span>)}</div></div>
      <div className="marquee"><div>PYTHON · AI/ML · GENAI · BACKEND · AWS · DATA ENGINEERING · DOCKER · TERRAFORM · PYTHON · AI/ML · GENAI · BACKEND ·</div></div>
    </section>

    <section className="contact section" id="contact">
      <div className="contact-panel"><div className="section-kicker"><span>04</span> CONTACT</div><h2>Have a problem<br/>worth <em>building?</em></h2><p>Open to Python, AI/ML, GenAI, backend, cloud and data engineering opportunities.</p><a className="contact-button" href="mailto:shyamprakash271@gmail.com">shyamprakash271@gmail.com <span>↗</span></a></div>
    </section>

    <footer><span>VSP © 2026</span><span>Designed & built with Next.js</span><a href="#top">Back to top ↑</a></footer>
  </main>;
}
