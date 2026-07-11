// Prefer import — FTS/filter runs in the Rust sqlite plugin.
import { search } from '@relay/search/sqlite';

export default function run(ctx) {
  return search(ctx);
}
