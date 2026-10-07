'use client';

import { useEffect, useState } from 'react';

const projects = [
  {name:'CodeForge',tag:'AI / GENAI',num:'01',desc:'A security-conscious multi-agent engineering workspace for generating, testing, repairing and reviewing code.',stack:'Python · LangGraph · FastAPI · Docker',repo:'https://github.com/shyamprakash534/Codeforge',live:'https://codeforge-3l85.onrender.com',metric:'MULTI-AGENT WORKSPACE'},
  {name:'NanoLink',tag:'BACKEND / SYSTEMS',num:'02',desc:'A distributed URL shortener engineered around caching, rate limiting, analytics and observability.',stack:'Go · Gin · PostgreSQL · Redis · ClickHouse',repo:'https://github.com/shyamprakash534/nanolink1',live:'https://nanolink1.onrender.com',metric:'DISTRIBUTED SYSTEM'},
  {name:'Grounded RAG',tag:'GENAI / RAG',num:'03',desc:'A local-first RAG system that retrieves relevant knowledge and produces source-backed answers.',stack:'Python · FastAPI · ChromaDB · Ollama',repo:'https://github.com/shyamprakash534/grounded-rag',live:'https://grounded-rag-oww5.onrender.com',metric:'SOURCE-GROUNDED AI'},
  {name:'AWS E-Commerce Pipeline',tag:'CLOUD / DATA',num:'04',desc:'A raw → curated → analytics workflow demonstrating practical AWS data engineering patterns.',stack:'S3 · Glue · Athena · PySpark · Terraform',repo:'https://github.com/shyamprakash534/aws-ecommerce-data-pipeline',live:'https://aws-ecommerce-data-pipeline.onrender.com',metric:'ETL / CLOUD DATA'},
  {name:'JobMatch AI',tag:'PYTHON / AI',num:'05',desc:'A source-first job matching product that parses resumes and ranks opportunities with weighted relevance.',stack:'Python · FastAPI · httpx · pypdf',repo:'https://github.com/shyamprakash534/ai-job-application-tracker',live:'https://ai-job-application-tracker-o9vp.onrender.com',metric:'PRODUCT ENGINEERING'},
  {name:'AI Drug Recommendation',tag:'MACHINE LEARNING',num:'06',desc:'An end-to-end ML application combining prediction, model evaluation and explainability.',stack:'Python · Scikit-learn · Flask · SHAP',repo:'https://github.com/shyamprakash534/drug-recommendation',live:'https://drug-recommendation-5uxr.onrender.com',metric:'PREDICTIVE ML'}
];

const skills = ['Python','Go','SQL','AI / ML','GenAI & RAG','FastAPI','Flask','AWS','ETL','PostgreSQL','Redis','Docker','Terraform','GitHub Actions','Scikit-learn','LangGraph','Ollama','ChromaDB'];

function Arrow(){ return <span aria-hidden="true">↗</span>; }

export default function Home(){
  const [mouse, setMouse] = useState({x:50,y:50});
  const [active, setActive] = useState(0);

  useEffect(()=>{
    const move=(e)=>setMouse({x:(e.clientX/window.innerWidth)*100,y:(e.clientY/window.innerHeight)*100});
    window.addEventListener('pointermove',move);
    return ()=>window.removeEventListener('pointermove',move);
  },[]);

  return <main id="top" style={{'--mx':`${mouse.x}%`,'--my':`${mouse.y}%`}}>
    <div className="noise" />
    <nav className="nav">
      <a className="brand" href="#top"><span>VSP</span><i>●</i></a>
      <div className="navlinks"><a href="#about">About</a><a href="#work">Work</a><a href="#process">Process</a><a href="#stack">Stack</a></div>
      <a className="availability" href="mailto:shyamprakash271@gmail.com"><b></b> Available for opportunities <Arrow/></a>
    </nav>

    <section className="hero">
      <div className="hero-grid" />
      <div className="hero-spotlight" />
      <div className="hero-copy">
        <div className="eyebrow"><span className="pulse"/> PYTHON · AI/ML · GENAI · BACKEND · CLOUD <span className="year">/ 2026</span></div>
        <div className="hero-layout">
          <div>
            <p className="hero-overline">SOFTWARE ENGINEER / AI BUILDER</p>
            <h1>Build smart.<br/><em>Ship real.</em></h1>
            <p className="hero-lead">I’m <strong>Vemula Syam Prakash</strong> — building practical AI products, backend systems and cloud/data workflows that move from idea to production.</p>
            <div className="hero-actions"><a className="magnetic primary" href="#work">Explore selected work <Arrow/></a><a className="outline-btn" href="https://github.com/shyamprakash534" target="_blank" rel="noreferrer">GitHub <Arrow/></a><a className="text-link" href="https://www.linkedin.com/in/shyam-prakash-vemula-721029263/" target="_blank" rel="noreferrer">LinkedIn <Arrow/></a></div>
          </div>
          <div className="hero-system" aria-label="Interactive engineering system visual">
            <div className="system-ring ring-one"/><div className="system-ring ring-two"/><div className="system-ring ring-three"/>
            <div className="system-core"><span>VSP</span><small>BUILD / DEPLOY</small></div>
            <div className="node node-a"><b>PY</b><span>Python</span></div><div className="node node-b"><b>AI</b><span>GenAI</span></div><div className="node node-c"><b>API</b><span>Backend</span></div><div className="node node-d"><b>AWS</b><span>Cloud</span></div>
          </div>
        </div>
      </div>
      <div className="hero-bottom"><span>SCROLL TO EXPLORE</span><i/><span>01 / 06</span></div>
    </section>

    <section className="intro section" id="about">
      <div className="section-kicker"><span>01</span> ABOUT / ENGINEERING MINDSET</div>
      <div className="intro-grid"><h2>Software with<br/><em>intent.</em></h2><div className="intro-copy"><p className="big-copy">MCA graduate with a Statistics background, combining quantitative thinking with software engineering to build useful technology.</p><p>I work across AI/ML, GenAI, Python backends, APIs, databases, ETL, cloud infrastructure and deployment.</p><div className="principles"><span>01 / Evidence over hype</span><span>02 / Practical AI</span><span>03 / Reproducible systems</span><span>04 / Security + maintainability</span></div></div></div>
    </section>

    <section className="work section" id="work">
      <div className="section-kicker"><span>02</span> SELECTED WORK / LIVE SYSTEMS</div>
      <div className="work-head"><div><p className="mini-label">06 PRODUCTS / 06 DIFFERENT PROBLEMS</p><h2>Built in<br/><em>public.</em></h2></div><p>Real repositories. Live deployments. No imaginary case studies — just systems built to solve specific problems.</p></div>
      <div className="project-grid">{projects.map((p,i)=><article className={`project-card ${active===i?'is-active':''}`} onMouseEnter={()=>setActive(i)} key={p.name}>
        <div className="card-top"><span>{p.num}</span><small>{p.tag}</small></div>
        <div className="project-art"><div className="art-grid"/><div className="art-orbit orbit-a"/><div className="art-orbit orbit-b"/><div className="art-core"><span>{['AI','↗','RAG','AWS','AI','ML'][i]}</span></div><div className="art-label">{p.metric}</div></div>
        <div className="project-info"><div className="project-title"><h3>{p.name}</h3><a href={p.live} target="_blank" rel="noreferrer" aria-label={`Open ${p.name} live demo`}><Arrow/></a></div><p>{p.desc}</p><div className="project-bottom"><span>{p.stack}</span><div><a href={p.repo} target="_blank" rel="noreferrer">Repo <Arrow/></a><a href={p.live} target="_blank" rel="noreferrer">Live <Arrow/></a></div></div></div>
      </article>)}</div>
    </section>

    <section className="process section" id="process">
      <div className="section-kicker"><span>03</span> ENGINEERING / FROM IDEA TO LIVE</div>
      <div className="process-head"><h2>Think.<br/><em>Build.</em><br/>Ship.</h2><p>A practical loop I use across projects: understand the problem, design the system, build the smallest useful version, then make it reliable enough to run.</p></div>
      <div className="process-line">{[['01','IDEA','Problem → user → outcome'],['02','ARCHITECTURE','APIs → data → models'],['03','BUILD','Python → services → UI'],['04','VERIFY','Tests → evaluation → review'],['05','DEPLOY','Docker → CI/CD → cloud'],['06','OPERATE','Logs → metrics → iteration']].map(([n,t,d])=><div className="process-step" key={n}><span>{n}</span><b>{t}</b><p>{d}</p></div>)}</div>
    </section>

    <section className="journey section">
      <div className="section-kicker"><span>04</span> JOURNEY / WHAT SHAPED THE BUILDER</div>
      <div className="journey-grid"><h2>Statistics<br/>to <em>systems.</em></h2><div className="timeline">{[['2022','BSc Statistics','Quantitative foundation and analytical thinking.'],['2026','MCA Graduate','Software engineering, data structures, cloud and applications.'],['NOW','AI / ML + Python','Building practical products across GenAI, backend and data.']].map(([year,title,desc])=><div className="timeline-item" key={year}><span>{year}</span><div><h3>{title}</h3><p>{desc}</p></div></div>)}</div></div>
    </section>

    <section className="stack-section section" id="stack">
      <div className="section-kicker"><span>05</span> TOOLKIT / TECHNOLOGIES</div>
      <div className="stack-layout"><h2>The stack<br/><em>behind it.</em></h2><div className="skill-cloud">{skills.map((s,i)=><span className={i%5===0?'featured':''} key={s}>{s}</span>)}</div></div>
      <div className="cert-grid"><div className="cert"><span>AWS</span><b>Cloud Practitioner</b><small>CLF-C02</small></div><div className="cert"><span>GOOGLE</span><b>AI Professional Certificate</b><small>AI / PRODUCTIVITY</small></div><div className="cert"><span>ORACLE</span><b>Agentic AI Foundations</b><small>CERTIFIED ASSOCIATE</small></div></div>
      <div className="marquee"><div>PYTHON · AI/ML · GENAI · BACKEND · AWS · DATA ENGINEERING · DOCKER · TERRAFORM · PYTHON · AI/ML · GENAI · BACKEND · AWS · DATA ENGINEERING ·</div></div>
    </section>

    <section className="now section"><div className="now-card"><div><span className="live-dot"/> CURRENTLY BUILDING</div><h2>Turning AI ideas into<br/><em>useful software.</em></h2><p>Focused on Python engineering, GenAI/RAG, backend systems and cloud-ready data workflows — with a strong bias toward shipping and learning from real systems.</p><div className="now-tags"><span>PYTHON</span><span>GENAI</span><span>RAG</span><span>BACKEND</span><span>AWS</span></div></div></section>

    <section className="contact section" id="contact"><div className="contact-panel"><div className="section-kicker"><span>06</span> CONTACT / LET’S BUILD</div><h2>Have a problem<br/>worth <em>building?</em></h2><p>Open to Python, AI/ML, GenAI, backend, cloud and data engineering opportunities.</p><div className="contact-actions"><a className="contact-button" href="mailto:shyamprakash271@gmail.com">shyamprakash271@gmail.com <Arrow/></a><a className="contact-side" href="https://www.linkedin.com/in/shyam-prakash-vemula-721029263/" target="_blank" rel="noreferrer">LinkedIn <Arrow/></a></div></div></section>

    <footer><span>VSP © 2026</span><span>PYTHON · AI/ML · GENAI · BACKEND · CLOUD</span><a href="#top">Back to top ↑</a></footer>
  </main>;
}
