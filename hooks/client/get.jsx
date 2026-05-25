// @use-jsx
/**
 * Default Relay client GET hook — root layout for Paradigm Threat **timeline** (events JSON + content).
 * `@clevertree/markdown` → host `MarkdownRenderer` (relay-runtime md2jsx).
 */
import React, { useState } from 'react'
import { MarkdownRenderer } from '@clevertree/markdown'

export default function ParadigmTimelineRelayRoot () {
  const path = '/'
  const navigate = (_to) => {}

  // Relay runtime: no top-level `const` bindings from arrow templates; no useEffect/lazy useState.
  const [markdown] = useState(
    `# Paradigm Threat — timeline

**Current path:** \`${path}\`

---

Default GET hook at \`hooks/client/get.jsx\`. Load timeline content and event JSON by \`path\`, and render markdown bodies with \`<MarkdownRenderer />\`.`,
  )

  return (
    <div className="min-h-screen flex flex-col bg-[var(--bg-primary,#fafafa)] text-[var(--text-primary,#111)]">
      <header className="border-b border-[var(--border-color,#e5e7eb)] px-4 py-3 shadow-sm">
        <h1 className="text-xl font-semibold tracking-tight m-0">Paradigm Threat</h1>
        <p className="text-sm opacity-70 m-0 mt-1">Timeline — default Relay client hook</p>
      </header>
      <main className="flex-1 overflow-auto">
        <MarkdownRenderer content={markdown} navigate={navigate} />
      </main>
    </div>
  )
}
