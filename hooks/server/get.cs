// =============================================================================
// server.hooks.get — CleverScript (.cs) dynamic GET hook (see SERVER_HOOKS.md).
// Raster ?w=: Rust `optimizeRasterFromGetContext`; else `next()` reads tree / 404 JSON.
// =============================================================================

import { resolveIpfsFromGetContext } from '@relay/ipfs';
import { queryWidth, optimizeRasterFromGetContext } from '@relay/image';

export default function run(ctx, next) {
  /* IPFS before raster: ?w= on raster pointers defers to optimizeRaster (fetch CID, then WebP). */
  var ipfs = resolveIpfsFromGetContext(ctx);
  /* optimizeRaster requires opts.width — a bare ctx call always returns null. */
  var maxW = queryWidth(ctx);
  var optimized = maxW !== null ? optimizeRasterFromGetContext(ctx, null, { width: maxW }) : null;
  /* CleverScript: Statement::Return inside if/for blocks is ignored; use one tail return + ternary. */
  return ipfs !== null ? ipfs : optimized !== null ? optimized : next();
}
