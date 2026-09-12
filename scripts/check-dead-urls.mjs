#!/usr/bin/env node
/** Thin wrapper: probe this Relay catalog via the files-repo checker. */
import { spawn } from 'node:child_process'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const timelineRoot = resolve(here, '..')
const checker = resolve(here, '..', '..', 'paradigm-threat-files', 'scripts', 'check-dead-urls.mjs')
const child = spawn(process.execPath, [checker, '--root', timelineRoot, ...process.argv.slice(2)], {
  stdio: 'inherit',
})
child.on('exit', (code) => process.exit(code ?? 1))
