CREATE TABLE IF NOT EXISTS items (
  id TEXT PRIMARY KEY,
  source TEXT NOT NULL,
  sender TEXT NOT NULL,
  summary TEXT,
  type TEXT,
  status TEXT NOT NULL,
  routed_to TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_items_status ON items(status);

CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_id TEXT NOT NULL REFERENCES items(id),
  ts TEXT NOT NULL,
  event TEXT NOT NULL,
  note TEXT
);
CREATE INDEX IF NOT EXISTS idx_events_item_id ON events(item_id);
