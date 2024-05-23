SET application_name='partselect';

CREATE TABLE "models" (
  "id" varchar PRIMARY KEY,
  "name" varchar NOT NULL,
  "link" varchar NOT NULL,
  "created_at" timestamptz NOT NULL DEFAULT (now()),
  "updated_at" timestamptz NOT NULL DEFAULT (now())
);

CREATE TABLE "parts" (
  "id" varchar PRIMARY KEY,
  "name" varchar NOT NULL,
  "price" varchar,
  "manufacturer_part_number" varchar,
  "manufactured_by" varchar,
  "description" varchar,
  "fixes" varchar,
  "works_with_appliances" varchar,
  "works_with_brands" varchar,
  "part_replaces" varchar,
  "part_videos" varchar,
  "link" varchar NOT NULL,
  "created_at" timestamptz NOT NULL DEFAULT (now()),
  "updated_at" timestamptz NOT NULL DEFAULT (now())
);

CREATE TABLE "models_parts" (
  "part_id" varchar REFERENCES "parts" ("id") ON UPDATE CASCADE ON DELETE CASCADE,
  "model_id" varchar REFERENCES "models" ("id") ON UPDATE CASCADE ON DELETE CASCADE,
  "created_at" timestamptz NOT NULL DEFAULT (now()),
  "updated_at" timestamptz NOT NULL DEFAULT (now()),
  CONSTRAINT "models_parts_pk" PRIMARY KEY("part_id", "model_id")
);

CREATE INDEX ON "models" ("id");

CREATE INDEX ON "parts" ("id");

CREATE INDEX ON "models_parts" ("part_id", "model_id");

