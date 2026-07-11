// Thin QUERY router — sqlite plugin does FTS/filter in Rust.
export default function run(ctx) {
  return {
    plugin: "sqlite",
    collection: ctx.collection,
    query: ctx.query
  };
}
