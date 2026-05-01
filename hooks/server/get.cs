// =============================================================================
// server.hooks.get — CleverScript (.cs) dynamic GET hook (see SERVER_HOOKS.md).
// Raster ?w=: Rust `optimizeRasterFromGetContext`; else `next()` reads tree / 404 JSON.
// =============================================================================

import { optimizeRasterFromGetContext } from '@relay/image';

export default function run(ctx, next) {
  var optimized = optimizeRasterFromGetContext(ctx);
  /* CleverScript: Statement::Return inside if/for blocks is ignored; use one tail return + ternary. */
  return optimized !== null ? optimized : next();
}
