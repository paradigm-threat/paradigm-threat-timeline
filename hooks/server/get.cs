// =============================================================================
// server.hooks.get — CleverScript (.cs) dynamic GET hook (see SERVER_HOOKS.md).
// Raster ?w=: Rust `optimizeRasterFromGetContext`; else `next()` reads tree / 404 JSON.
// =============================================================================

import { optimizeRasterFromGetContext } from '@relay/image';

export default function run(ctx, next) {
  var optimized = optimizeRasterFromGetContext(ctx);
  if (optimized !== null) return optimized;
  return next();
}
