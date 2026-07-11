/**
 * Builds changelog.json from `git log` (paths-first; no commit hash in output).
 * Optional: PARADIGM_CHANGELOG_STAGED_TOP=1 prepends a row from `git diff --cached`.
 *
 * Each entry includes `images`: { src, alt? }[] — keep image helpers aligned with:
 * paradigm-threat-files/scripts/generate-changelog.cjs
 */
const { execSync, execFileSync } = require('child_process')
const fs = require('fs')
const path = require('path')

const CHANGE_LIMIT = 8
const IGNORE_PATHS = new Set(['changelog.json', 'index.json', 'package.json', 'data/events.json'])
const REPO_ROOT = path.resolve(__dirname, '..')

const IMAGE_EXT = /\.(png|jpe?g|gif|webp|svg)$/i

function run(cmd) {
    return execSync(cmd, { encoding: 'utf8' }).trim()
}

function flattenEntries(nodes, out = []) {
    for (const node of nodes || []) {
        out.push(node)
        if (Array.isArray(node.children) && node.children.length > 0) {
            flattenEntries(node.children, out)
        }
    }
    return out
}

function loadEventMap() {
    /** Map content/*.md paths → evt-id from filename / frontmatter via build script. */
    try {
        const raw = execFileSync('python3', [path.join(__dirname, 'build_events_from_content.py'), '--json'], {
            encoding: 'utf8',
            maxBuffer: 20 * 1024 * 1024,
        })
        const parsed = JSON.parse(raw)
        const list = flattenEntries(parsed.entries || [])
        const map = new Map()
        for (const evt of list) {
            if (evt && typeof evt.md_path === 'string' && typeof evt.id === 'string') {
                map.set(evt.md_path, evt.id)
            }
        }
        return map
    } catch {
        return new Map()
    }
}

function toTimelineHref(filePath, eventMap) {
    const clean = filePath.replace(/\\/g, '/').replace(/^\.\//, '')
    if (/^content\/.+\.mdx?$/i.test(clean)) {
        const evt = eventMap.get(clean)
        if (evt) return `/timeline/${evt}`
    }
    return '/timeline'
}

function parseNameStatusOutput(output, eventMap) {
    if (!output) return []
    const changes = []
    for (const rawLine of output.split('\n')) {
        const line = rawLine.trim()
        if (!line) continue

        const cols = line.split(/\t+/)
        const status = cols[0] || ''
        const code = status[0]
        if (!['A', 'M', 'R'].includes(code)) continue

        const filePath = code === 'R' ? cols[2] : cols[1]
        if (!filePath) continue

        if (IGNORE_PATHS.has(filePath)) continue

        changes.push({
            status: code,
            path: filePath,
            href: toTimelineHref(filePath, eventMap)
        })
    }
    return changes
}

function parseChangedFiles(hash, eventMap) {
    const output = run(`git show --pretty="" --name-status --find-renames ${hash}`)
    return parseNameStatusOutput(output, eventMap)
}

function filePathToRootSrc(filePath) {
    const clean = filePath.replace(/\\/g, '/').replace(/^\.\//, '')
    const withSlash = clean.startsWith('/') ? clean : `/${clean}`
    const q = withSlash.indexOf('?')
    return q >= 0 ? withSlash.slice(0, q) : withSlash
}

function stripTrailingCloseParenFromMdUrlToken(tok) {
    let t = String(tok || '').trim()
    while (t.endsWith(')') && /\.(png|jpe?g|gif|webp|svg)\)/i.test(t)) {
        t = t.slice(0, -1)
    }
    return t
}

function resolveMarkdownUrl(raw, mdFilePath) {
    let u = stripTrailingCloseParenFromMdUrlToken(String(raw || '').split(/\s+/)[0] || '')
    if (!u) return null
    const q = u.indexOf('?')
    const pathOnly = q >= 0 ? u.slice(0, q) : u
    if (/^https?:\/\//i.test(pathOnly)) return pathOnly
    if (pathOnly.startsWith('/')) return pathOnly
    const dir = path.posix.dirname(mdFilePath.replace(/\\/g, '/'))
    let combined = path.posix.normalize(`${dir}/${pathOnly.replace(/^\.\//, '')}`)
    if (!combined.startsWith('/')) combined = `/${combined}`
    return combined
}

function extractImagesFromMarkdown(body, mdFilePath) {
    if (!body) return []
    const out = []
    const seen = new Set()

    const mdImg = /!\[([^\]]*)\]\(\s*(\S+)/g
    let m
    while ((m = mdImg.exec(body)) !== null) {
        const alt = (m[1] || '').trim()
        const resolved = resolveMarkdownUrl(m[2], mdFilePath)
        if (resolved && !seen.has(resolved)) {
            seen.add(resolved)
            out.push({ src: resolved, alt: alt || undefined })
        }
    }

    const htmlImg = /<img\s[^>]*\bsrc=["']([^"']+)["']/gi
    while ((m = htmlImg.exec(body)) !== null) {
        const resolved = resolveMarkdownUrl(m[1], mdFilePath)
        if (resolved && !seen.has(resolved)) {
            seen.add(resolved)
            out.push({ src: resolved, alt: undefined })
        }
    }

    return out
}

function gitShowTextAtCommit(hash, filePath) {
    try {
        return execFileSync('git', ['show', `${hash}:${filePath.replace(/\\/g, '/')}`], {
            encoding: 'utf8',
            maxBuffer: 20 * 1024 * 1024
        })
    } catch {
        return null
    }
}

function readWorkingTreeText(filePath) {
    try {
        const abs = path.join(REPO_ROOT, filePath)
        return fs.readFileSync(abs, 'utf8')
    } catch {
        return null
    }
}

function buildImagesForEntry(files, hash, isStaged) {
    const direct = []
    const fromMd = []
    const seen = new Set()

    for (const f of files || []) {
        const p = f.path || ''
        if (!p || !IMAGE_EXT.test(p)) continue
        const src = filePathToRootSrc(p)
        if (src && !seen.has(src)) {
            seen.add(src)
            direct.push({ src })
        }
    }

    for (const f of files || []) {
        const p = f.path || ''
        if (!/\.mdx?$/i.test(p)) continue
        const body = isStaged ? readWorkingTreeText(p) : hash ? gitShowTextAtCommit(hash, p) : null
        if (!body) continue
        for (const img of extractImagesFromMarkdown(body, p)) {
            const src = /^https?:\/\//i.test(img.src)
                ? img.src
                : filePathToRootSrc(img.src.replace(/^\//, ''))
            if (src && !seen.has(src)) {
                seen.add(src)
                fromMd.push({ src, alt: img.alt })
            }
        }
    }

    return [...direct, ...fromMd]
}

function maybeStagedTopEntry(eventMap) {
    if (process.env.PARADIGM_CHANGELOG_STAGED_TOP !== '1') return null
    try {
        const output = run('git diff --cached --name-status --find-renames')
        const files = parseNameStatusOutput(output, eventMap)
        if (files.length === 0) return null
        const images = buildImagesForEntry(files, null, true)
        return {
            repo: 'paradigm-threat-timeline',
            date: new Date().toISOString(),
            message: '(staged)',
            files,
            images
        }
    } catch {
        return null
    }
}

function generateChangelog() {
    try {
        const eventMap = loadEventMap()
        const stagedTop = maybeStagedTopEntry(eventMap)
        const logData = run(`git log -n ${CHANGE_LIMIT} --pretty=format:"%H|%at|%s"`)
        const fromLog = logData
            .split('\n')
            .filter(Boolean)
            .map((line) => {
                const [hash, timestamp, ...msgParts] = line.split('|')
                const files = parseChangedFiles(hash, eventMap)
                const images = buildImagesForEntry(files, hash, false)
                return {
                    repo: 'paradigm-threat-timeline',
                    date: new Date(Number(timestamp) * 1000).toISOString(),
                    message: msgParts.join('|'),
                    files,
                    images
                }
            })

        let entries = fromLog
        if (stagedTop) {
            entries = [stagedTop, ...fromLog].slice(0, CHANGE_LIMIT)
        }

        const outputPath = path.resolve(__dirname, '../changelog.json')
        fs.writeFileSync(outputPath, JSON.stringify(entries, null, 2) + '\n')
        console.log('Successfully generated changelog.json')
    } catch (error) {
        console.error('Error generating changelog:', error.message)
        process.exitCode = 1
    }
}

generateChangelog()
