import { useEffect, useRef, useState } from 'react'

const exampleQueries = [
  'What changed near the river between the two dates?',
  'Identify buildings and roads in this scene.',
  'Describe the dominant land cover visible here.',
]

function App() {
  const [image, setImage] = useState(null)
  const [query, setQuery] = useState('')
  const [status, setStatus] = useState('idle')
  const [result, setResult] = useState(null)
  const fileInput = useRef(null)

  useEffect(() => {
    if (status !== 'analyzing') return undefined
    const timer = window.setTimeout(() => {
      setStatus('complete')
      setResult({
        title: 'Scene analysis complete',
        summary: 'The scene contains a vegetated river corridor with built-up areas along the eastern edge. The highlighted region is the strongest candidate for visible land-cover change.',
        confidence: 0.86,
        evidence: ['Optical scene interpretation', 'Spatial region proposal', 'Deterministic development fixture'],
      })
    }, 1600)
    return () => window.clearTimeout(timer)
  }, [status])

  const handleFile = (file) => {
    if (!file || !file.type.startsWith('image/')) return
    setImage({ name: file.name, url: URL.createObjectURL(file) })
    setResult(null)
    setStatus('idle')
  }

  const submit = () => {
    if (!image || !query.trim() || status === 'analyzing') return
    setStatus('analyzing')
    setResult(null)
  }

  return (
    <main className="workspace">
      <header className="topbar">
        <div className="brand-mark" aria-hidden="true">SQ</div>
        <div><p className="eyebrow">REMOTE SENSING INTELLIGENCE</p><h1>SatQuery <span>AI</span></h1></div>
        <div className="demo-badge"><i /> Development mode</div>
      </header>
      <section className="intro"><div><p className="eyebrow accent">ANALYSIS CONSOLE / 01</p><h2>Ask the landscape<br /><em>what changed.</em></h2></div><p className="intro-copy">Turn satellite imagery into grounded answers, mapped evidence, and a transparent reasoning trace.</p></section>
      <section className="console-grid">
        <aside className="control-panel panel">
          <div className="panel-heading"><span>01</span><h3>Input scene</h3></div>
          <input ref={fileInput} type="file" accept="image/*" hidden onChange={(event) => handleFile(event.target.files?.[0])} />
          <button className="upload-zone" onClick={() => fileInput.current?.click()} type="button">{image ? <img src={image.url} alt="Selected satellite scene" /> : <><strong>+</strong><span>Upload satellite image</span><small>PNG, JPG, or GeoTIFF preview</small></>}</button>
          {image && <p className="file-name">{image.name}<button onClick={() => setImage(null)} type="button">Remove</button></p>}
          <div className="panel-heading query-heading"><span>02</span><h3>Natural language query</h3></div>
          <textarea value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Ask a question about this scene..." rows="5" />
          <div className="suggestions">{exampleQueries.map((example) => <button key={example} type="button" onClick={() => setQuery(example)}>{example}</button>)}</div>
          <button className="primary-button" type="button" disabled={!image || !query.trim() || status === 'analyzing'} onClick={submit}>{status === 'analyzing' ? 'Analyzing scene...' : 'Run analysis'} <span>→</span></button>
        </aside>
        <section className="evidence-panel panel">
          <div className="panel-heading"><span>03</span><h3>Visual evidence</h3><small>OPTICAL / 10 M</small></div>
          <div className={`scene-view ${image ? 'has-image' : ''}`}>{image ? <img src={image.url} alt="Uploaded satellite scene" /> : <div className="scene-placeholder"><div className="crosshair">+</div><p>Upload an image to inspect<br />visual evidence here</p></div>}{status === 'complete' && <div className="evidence-region"><span>CHANGE REGION 01</span></div>}{status === 'analyzing' && <div className="scan-line" />}<div className="map-coordinates">77.2090° E&nbsp;&nbsp; / &nbsp;&nbsp;28.6139° N</div></div>
          <div className="legend"><span><i className="legend-dot purple" />Candidate change</span><span><i className="legend-dot green" />Vegetation</span><span>Zoom 12 · New Delhi</span></div>
        </section>
        <aside className="results-panel panel">
          <div className="panel-heading"><span>04</span><h3>Results</h3>{status === 'complete' && <b className="complete-label">COMPLETE</b>}</div>
          {status === 'idle' && <div className="empty-state"><div className="empty-icon">⌁</div><p>Your analysis answer and evidence trace will appear here.</p></div>}
          {status === 'analyzing' && <div className="progress-state"><div className="spinner" /><p>Orchestrating specialist models</p><small>Validating image · Planning tools · Fusing evidence</small></div>}
          {result && <div className="result-content"><p className="eyebrow accent">ANSWER</p><h4>{result.title}</h4><p>{result.summary}</p><div className="confidence"><div><span>Evidence confidence</span><strong>{Math.round(result.confidence * 100)}%</strong></div><div className="confidence-bar"><i style={{ width: `${result.confidence * 100}%` }} /></div></div><p className="eyebrow trace-title">EVIDENCE TRACE</p>{result.evidence.map((item, index) => <div className="trace-item" key={item}><i /> <span>{item}</span><small>{index === 0 ? '0.4s' : 'ready'}</small></div>)}</div>}
        </aside>
      </section>
      <footer>SatQuery AI <span>·</span> Development fixture. Results are indicative and require domain validation.</footer>
    </main>
  )
}

export default App
