'use client';

import { useEffect, useMemo, useState } from 'react';

const projects = [
  {name:'CodeForge',tag:'AI / GENAI',num:'01',desc:'A security-conscious multi-agent engineering workspace for generating, testing, repairing and reviewing code.',stack:['Python','LangGraph','FastAPI','Docker'],repo:'https://github.com/shyamprakash534/Codeforge',live:'https://codeforge-3l85.onrender.com',metric:'MULTI-AGENT WORKSPACE',detail:'Designed as an engineering workflow rather than a chat demo: agents coordinate around code generation, testing, repair and review.'},
  {name:'NanoLink',tag:'BACKEND / SYSTEMS',num:'02',desc:'A distributed URL shortener engineered around caching, rate limiting, analytics and observability.',stack:['Go','Gin','PostgreSQL','Redis','ClickHouse'],repo:'https://github.com/shyamprakash534/nanolink1',live:'https://nanolink1.onrender.com',metric:'DISTRIBUTED SYSTEM',detail:'A systems-focused build exploring high-throughput API design, caching, persistence, analytics and operational visibility.'},
  {name:'Grounded RAG',tag:'GENAI / RAG',num:'03',desc:'A local-first RAG system that retrieves relevant knowledge and produces source-backed answers.',stack:['Python','FastAPI','ChromaDB','Ollama'],repo:'https://github.com/shyamprakash534/grounded-rag',live:'https://grounded-rag-oww5.onrender.com',metric:'SOURCE-GROUNDED AI',detail:'Built around retrieval quality and grounded generation, with a local-first stack for practical experimentation.'},
  {name:'AWS E-Commerce Pipeline',tag:'CLOUD / DATA',num:'04',desc:'A raw → curated → analytics workflow demonstrating practical AWS data engineering patterns.',stack:['S3','Glue','Athena','PySpark','Terraform'],repo:'https://github.com/shyamprakash534/aws-ecommerce-data-pipeline',live:'https://aws-ecommerce-data-pipeline.onrender.com',metric:'ETL / CLOUD DATA',detail:'A production-shaped data workflow covering ingestion, transformation, analytics and infrastructure as code.'},
  {name:'JobMatch AI',tag:'PYTHON / AI',num:'05',desc:'A source-first job matching product that parses resumes and ranks opportunities with weighted relevance.',stack:['Python','FastAPI','httpx','pypdf'],repo:'https://github.com/shyamprakash534/ai-job-application-tracker',live:'https://ai-job-application-tracker-o9vp.onrender.com',metric:'PRODUCT ENGINEERING',detail:'A practical automation product focused on extracting useful signals from resumes and job descriptions.'},
  {name:'AI Drug Recommendation',tag:'MACHINE LEARNING',num:'06',desc:'An end-to-end ML application combining prediction, model evaluation and explainability.',stack:['Python','Scikit-learn','Flask','SHAP'],repo:'https://github.com/shyamprakash534/drug-recommendation',live:'https://drug-recommendation-5uxr.onrender.com',metric:'PREDICTIVE ML',detail:'An end-to-end machine learning application taking a model from data and evaluation through a usable web interface.'}
];

const skills = ['Python','Go','SQL','AI / ML','GenAI & RAG','FastAPI','Flask','AWS','ETL','PostgreSQL','Redis','Docker','Terraform','GitHub Actions','Scikit-learn','LangGraph','Ollama','ChromaDB'];

const process = [
  ['01','DISCOVER','Problem → user → measurable outcome'],
  ['02','DESIGN','Architecture → data → interfaces'],
  ['03','BUILD','Python → services → product'],
  ['04','VERIFY','Tests → evaluation → review'],
  ['05','SHIP','Docker → CI/CD → cloud'],
  ['06','OPERATE','Logs → metrics → iteration']
];

function Arrow(){return <span aria-hidden="true">↗</span>}

export default function Home(){
  const [mouse,setMouse]=useState({x:50,y:50});
  const [active,setActive]=useState(null);
  const [menu,setMenu]=useState(false);
  const [progress,setProgress]=useState(0);

  useEffect(()=>{
    const move=e=>setMouse({x:e.clientX/window.innerWidth*100,y:e.clientY/window.innerHeight*100});
    const scroll=()=>setProgress(window.scrollY/(document.documentElement.scrollHeight-window.innerHeight)*100);
    const key=e=>{if(e.key==='Escape'){setMenu(false);setActive(null)}};
    window.addEventListener('pointermove',move); window.addEventListener('scroll',scroll,{passive:true}); window.addEventListener('keydown',key);
    scroll(); return()=>{window.removeEventListener('pointermove',move);window.removeEventListener('scroll',scroll);window.removeEventListener('keydown',key)};
  },[]);

  const featured=useMemo(()=>projects.slice(0,3),[]);

  return <main id="top" style={{'--mx':`${mouse.x}%`,'--my':`${mouse.y}%`,'--progress':`${progress}%`}}>
    <div className="progress"/><div className="noise"/>
    <nav className="nav">
      <a className="brand" href="#top"><span>VSP</span><i>●</i></a>
      <div className="navlinks"><a href="#work">Work</a><a href="#system">System</a><a href="#stack">Stack</a><a href="#contact">Contact</a></div>
      <div className="nav-right"><span className="status"><b/> Open to opportunities</span><button className="menu-button" onClick={()=>setMenu(true)} aria-label="Open navigation">⌘ K</button></div>
    </nav>

    {menu&&<div className="command-overlay" role="dialog" aria-modal="true" onClick={()=>setMenu(false)}><div className="command" onClick={e=>e.stopPropagation()}><div className="command-top"><span>QUICK NAVIGATION</span><button onClick={()=>setMenu(false)}>ESC</button></div>{[['#work','Selected work'],['#system','Engineering system'],['#stack','Toolkit & certifications'],['#contact','Contact'],['https://github.com/shyamprakash534','GitHub']].map(([href,label])=><a key={label} href={href} target={href.startsWith('http')?'_blank':undefined} rel="noreferrer" onClick={()=>setMenu(false)}><span>{label}</span><Arrow/></a>)}</div></div>}

    <section className="hero">
      <div className="hero-grid"/><div className="hero-glow"/>
      <div className="hero-content">
        <div className="eyebrow"><span className="pulse"/> PYTHON · AI/ML · GENAI · BACKEND · CLOUD <span>/ 2026</span></div>
        <div className="hero-main">
          <div className="hero-copy">
            <p className="overline">SOFTWARE ENGINEER / AI BUILDER</p>
            <h1>Build smart.<br/><em>Ship real.</em></h1>
            <p className="hero-lead">I’m <strong>Vemula Syam Prakash</strong> — an MCA graduate with a Statistics foundation, building practical AI products, backend systems and cloud/data workflows.</p>
            <div className="actions"><a className="button primary" href="#work">Explore work <Arrow/></a><a className="button ghost" href="https://github.com/shyamprakash534" target="_blank" rel="noreferrer">GitHub <Arrow/></a><a className="quiet-link" href="https://www.linkedin.com/in/shyam-prakash-vemula-721029263/" target="_blank" rel="noreferrer">LinkedIn <Arrow/></a></div>
            <div className="hero-meta"><span>BASED IN INDIA</span><span>06 LIVE PROJECTS</span><span>OPEN TO BUILD</span></div>
          </div>
          <div className="terminal-wrap">
            <div className="terminal-glow"/>
            <div className="terminal">
              <div className="terminal-bar"><span/><span/><span/><b>vsp / portfolio</b></div>
              <div className="terminal-body"><p><i>01</i><span>$</span> whoami</p><h3>Vemula Syam Prakash</h3><p><i>02</i><span>$</span> focus --now</p><div className="terminal-tags"><b>PYTHON</b><b>GENAI</b><b>BACKEND</b><b>AWS</b></div><p><i>03</i><span>$</span> status</p><p className="ok">● shipping real systems</p><p><i>04</i><span>$</span> <strong className="cursor">_</strong></p></div>
            </div>
          </div>
        </div>
      </div>
      <div className="hero-bottom"><span>SCROLL / EXPLORE</span><div/><span>01—06</span></div>
    </section>

    <section className="statement section">
      <div className="kicker"><span>01</span> THE BUILDER</div>
      <div className="statement-grid"><h2>Software with<br/><em>intent.</em></h2><div><p className="statement-big">I like the space between an idea and a working system.</p><p className="muted">My work crosses AI/ML, GenAI, Python backends, APIs, databases, ETL, cloud infrastructure and deployment. The goal is simple: useful software that can actually run.</p><div className="principles"><span>01 / Evidence over hype</span><span>02 / Practical AI</span><span>03 / Reproducible systems</span><span>04 / Security + maintainability</span></div></div></div>
    </section>

    <section className="work section" id="work">
      <div className="kicker"><span>02</span> SELECTED WORK / REAL SYSTEMS</div>
      <div className="section-head"><div><small>06 PRODUCTS · 06 PROBLEMS</small><h2>Built in<br/><em>public.</em></h2></div><p>Repositories you can inspect. Deployments you can open. Systems built around actual problems — not imaginary case studies.</p></div>
      <div className="featured-grid">{featured.map((p,i)=><article className="featured-card" key={p.name} onClick={()=>setActive(p)}>
        <div className="card-top"><span>{p.num}</span><small>{p.tag}</small></div><div className={`project-visual v${i}`}><div className="visual-grid"/><div className="visual-ring r1"/><div className="visual-ring r2"/><div className="visual-core">{i===0?'AI':i===1?'API':'RAG'}</div><span className="visual-code">{p.metric}</span></div>
        <div className="card-body"><div className="card-title"><h3>{p.name}</h3><span>↗</span></div><p>{p.desc}</p><div className="chips">{p.stack.map(x=><span key={x}>{x}</span>)}</div><div className="card-foot"><span>OPEN CASE STUDY</span><Arrow/></div></div>
      </article>)}</div>
      <div className="project-list">{projects.slice(3).map(p=><button className="list-project" key={p.name} onClick={()=>setActive(p)}><span>{p.num}</span><strong>{p.name}</strong><small>{p.tag}</small><i>{p.metric}</i><Arrow/></button>)}</div>
    </section>

    {active&&<div className="modal-backdrop" onClick={()=>setActive(null)}><article className="project-modal" onClick={e=>e.stopPropagation()}><button className="close" onClick={()=>setActive(null)} aria-label="Close">×</button><div className="modal-kicker">{active.num} / {active.tag}</div><h2>{active.name}</h2><p className="modal-desc">{active.detail}</p><div className="modal-stack">{active.stack.map(x=><span key={x}>{x}</span>)}</div><div className="modal-actions"><a className="button primary" href={active.live} target="_blank" rel="noreferrer">Open live <Arrow/></a><a className="button ghost" href={active.repo} target="_blank" rel="noreferrer">Source code <Arrow/></a></div></article></div>}

    <section className="system section" id="system">
      <div className="kicker"><span>03</span> ENGINEERING SYSTEM / HOW I SHIP</div>
      <div className="system-head"><h2>Think.<br/><em>Build.</em><br/>Ship.</h2><p>A repeatable engineering loop: understand the problem, design the system, build the smallest useful version, verify it, deploy it and learn from what happens next.</p></div>
      <div className="process-grid">{process.map(([n,t,d])=><div className="process" key={n}><span>{n}</span><b>{t}</b><p>{d}</p><i>↘</i></div>)}</div>
      <div className="system-diagram"><div className="diagram-center"><strong>PRODUCT</strong><small>VALUE / RELIABILITY</small></div>{[['AI','MODEL'],['API','SERVICE'],['DATA','PIPELINE'],['OPS','CLOUD']].map(([a,b],i)=><div className={`diagram-node dn${i}`} key={a}><b>{a}</b><span>{b}</span></div>)}</div>
    </section>

    <section className="journey section"><div className="kicker"><span>04</span> JOURNEY / FOUNDATION</div><div className="journey-grid"><h2>Statistics<br/>to <em>systems.</em></h2><div className="timeline">{[['2022','BSc Statistics','Quantitative foundation and analytical thinking.'],['2026','MCA Graduate','Software engineering, data structures, cloud and applications.'],['NOW','AI / ML + Python','Building practical products across GenAI, backend and data.']].map(([year,title,desc])=><div className="timeline-item" key={year}><span>{year}</span><div><h3>{title}</h3><p>{desc}</p></div></div>)}</div></div></section>

    <section className="stack section" id="stack"><div className="kicker"><span>05</span> TOOLKIT / TECHNOLOGIES</div><div className="stack-head"><h2>The stack<br/><em>behind it.</em></h2><p>Tools chosen to solve the problem in front of me — from model experiments and retrieval to APIs, data platforms and deployment.</p></div><div className="skill-cloud">{skills.map((s,i)=><span className={i%5===0?'featured':''} key={s}>{s}</span>)}</div><div className="cert-grid"><div><small>AWS</small><b>Cloud Practitioner</b><span>CLF-C02</span></div><div><small>GOOGLE</small><b>AI Professional Certificate</b><span>AI / PRODUCTIVITY</span></div><div><small>ORACLE</small><b>Agentic AI Foundations</b><span>CERTIFIED ASSOCIATE</span></div></div></section>

    <section className="now section"><div className="now-card"><div className="now-top"><span className="pulse"/> CURRENTLY BUILDING</div><h2>Turning AI ideas into<br/><em>useful software.</em></h2><p>Focused on Python engineering, GenAI/RAG, backend systems and cloud-ready data workflows — with a strong bias toward shipping and learning from real systems.</p><div className="now-tags"><span>PYTHON</span><span>GENAI</span><span>RAG</span><span>BACKEND</span><span>AWS</span></div></div></section>

    <section className="contact section" id="contact"><div className="contact-panel"><div className="kicker"><span>06</span> CONTACT / LET’S BUILD</div><h2>Have a problem<br/>worth <em>building?</em></h2><p>Open to Python, AI/ML, GenAI, backend, cloud and data engineering opportunities.</p><div className="contact-actions"><a className="button primary" href="mailto:shyamprakash271@gmail.com">shyamprakash271@gmail.com <Arrow/></a><a className="quiet-link" href="https://www.linkedin.com/in/shyam-prakash-vemula-721029263/" target="_blank" rel="noreferrer">LinkedIn <Arrow/></a></div></div></section>

    <footer><span>VSP © 2026</span><span>BUILT WITH PYTHON, AI & CURIOSITY</span><a href="#top">BACK TO TOP ↑</a></footer>
  </main>;
}
