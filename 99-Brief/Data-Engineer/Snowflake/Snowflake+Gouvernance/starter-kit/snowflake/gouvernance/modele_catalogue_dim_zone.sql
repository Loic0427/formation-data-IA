-- MODÈLE : la fiche de catalogue complète d'une table, écrite en SQL.
-- À exécuter une fois le schéma GOUVERNANCE et les trois tags créés (voir CONTRAT_GOUVERNANCE.md),
-- avec un rôle qui a le droit de modifier la table et de poser les tags.
-- Écrivez sur ce modèle un fichier par table à cataloguer.
--
-- Ce fichier est rejouable : COMMENT et SET TAG remplacent la valeur précédente.
-- À savoir : DIM_ZONE est recréée à chaque exécution du pipeline (CREATE OR REPLACE TABLE).
-- Une table recréée perd ses descriptions et ses tags : il faut donc rejouer ce fichier après.

-- 1. La table : ce qu'elle contient, d'où elle vient, à quel rythme elle change
COMMENT ON TABLE NYC_TAXI.MARTS.DIM_ZONE IS
  'Dimension des zones de taxi de New York : 1 ligne = 1 zone (265 lignes). Source : fichier taxi_zone_lookup.csv de la TLC, chargé une fois. Recréée à chaque exécution du pipeline mensuel. Responsable : équipe data.';

-- 2. Chaque colonne : sa signification, pas son nom répété
COMMENT ON COLUMN NYC_TAXI.MARTS.DIM_ZONE.zone_key        IS 'Identifiant de la zone, attribué par la TLC (1 à 265). Clé de la dimension.';
COMMENT ON COLUMN NYC_TAXI.MARTS.DIM_ZONE.zone_name       IS 'Nom de la zone, par exemple « JFK Airport ».';
COMMENT ON COLUMN NYC_TAXI.MARTS.DIM_ZONE.borough         IS 'Arrondissement de New York (Manhattan, Queens, Brooklyn, Bronx, Staten Island) ou EWR pour l''aéroport de Newark.';
COMMENT ON COLUMN NYC_TAXI.MARTS.DIM_ZONE.service_zone    IS 'Zone tarifaire de la TLC (Yellow Zone, Boro Zone, Airports, EWR).';
COMMENT ON COLUMN NYC_TAXI.MARTS.DIM_ZONE.is_airport      IS 'Vrai si la zone est un aéroport. Calculé à partir du nom de la zone et de l''arrondissement.';
COMMENT ON COLUMN NYC_TAXI.MARTS.DIM_ZONE.is_unknown_zone IS 'Vrai pour les zones 264 et 265, qui signifient « zone inconnue ».';

-- 3. Les tags : la sensibilité et la durée de conservation se posent sur la table (les colonnes en héritent)
ALTER TABLE NYC_TAXI.MARTS.DIM_ZONE SET TAG
  NYC_TAXI.GOUVERNANCE.SENSIBILITE        = 'public',
  NYC_TAXI.GOUVERNANCE.DUREE_CONSERVATION = 'sans limite : référentiel public';

-- Aucune colonne de cette table ne décrit une personne : le tag DONNEE_PERSONNELLE n'est pas posé.
-- Sur une colonne qui en contient, il se pose ainsi :
--   ALTER TABLE <table> MODIFY COLUMN <colonne> SET TAG NYC_TAXI.GOUVERNANCE.DONNEE_PERSONNELLE = 'email';

-- 4. Vérifier
SELECT column_name, comment FROM NYC_TAXI.INFORMATION_SCHEMA.COLUMNS
WHERE table_schema = 'MARTS' AND table_name = 'DIM_ZONE' ORDER BY ordinal_position;

SELECT level, column_name, tag_name, tag_value
FROM TABLE(NYC_TAXI.INFORMATION_SCHEMA.TAG_REFERENCES_ALL_COLUMNS('NYC_TAXI.MARTS.DIM_ZONE', 'table'));
