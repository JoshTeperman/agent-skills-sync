CREATE TABLE IF NOT EXISTS items (
  external_id TEXT PRIMARY KEY NOT NULL,
  source_email TEXT NOT NULL,
  rfc822_id TEXT,
  summary TEXT,
  status TEXT NOT NULL,
  routed_to TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_items_status ON items(status);
CREATE INDEX IF NOT EXISTS idx_items_source_email ON items(source_email);

CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_id TEXT NOT NULL REFERENCES items(external_id),
  timestamp TEXT NOT NULL,
  event TEXT NOT NULL,
  note TEXT
);
CREATE INDEX IF NOT EXISTS idx_events_item_id ON events(item_id);
