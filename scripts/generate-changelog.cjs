const { execSync } = require('child_process')
const fs = require('fs')
const path = require('path')

const CHANGE_LIMIT = 8
const IGNORE_PATHS = new Set(['changelog.json', 'index.json', 'package.json', 'data/events.json'])

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
    try {
        const eventsPath = path.resolve(__dirname, '../data/events.json')
        const raw = fs.readFileSync(eventsPath, 'utf8')
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

function parseChangedFiles(hash, eventMap) {
    const output = run(`git show --pretty="" --name-status --find-renames ${hash}`)
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

function generateChangelog() {
    try {
        const eventMap = loadEventMap()
        const logData = run(`git log -n ${CHANGE_LIMIT} --pretty=format:"%H|%at|%s"`)
        const entries = logData
            .split('\n')
            .filter(Boolean)
            .map((line) => {
                const [hash, timestamp, ...msgParts] = line.split('|')
                return {
                    repo: 'paradigm-threat-timeline',
                    hash,
                    date: new Date(Number(timestamp) * 1000).toISOString(),
                    message: msgParts.join('|'),
                    files: parseChangedFiles(hash, eventMap)
                }
            })

        const outputPath = path.resolve(__dirname, '../changelog.json')
        fs.writeFileSync(outputPath, JSON.stringify(entries, null, 2) + '\n')
        console.log('Successfully generated changelog.json')
    } catch (error) {
        console.error('Error generating changelog:', error.message)
        process.exitCode = 1
    }
}

generateChangelog()
