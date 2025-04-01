## Query Script for NI-GNN Homework 1

### Query 1: 
Objective: Retrieve officers (individual) overseeing a lot of companies as active workers
```Cypher
//Officers overseeing a lot of companies
CALL{
    MATCH 
        (ofc:officer) -[r1:officer_of]-> (ety:entity)
    WITH
        ofc.name as officer_name,
        ety.name as entity_name,
        r1.link as link
    WHERE 
        toLower(r1.link) CONTAINS ('director')
        OR toLower(r1.link) CONTAINS ('manager')
        AND ety.status = 'Active'
    RETURN officer_name, entity_name, link
}
WITH 
    count(*) AS n_position,
    officer_name,
    link AS position
WHERE n_position > 4
    AND NOT (
        toLower(officer_name) CONTAINS 'ltd'
        OR toLower(officer_name) CONTAINS 'limited'
        OR toLower(officer_name) CONTAINS 'inc') //And many more company filters
ORDER BY position, n_position DESC
RETURN officer_name, position, n_position 
// LIMIT 100
```

### Query 2: 
Objective: Retrieve officers (individual) working as officer and intermediary for the same company.
```Cypher
//Individuals as officer and intermediate for the same entity

MATCH (ofc:officer) -[r1:officer_of]-> (ety:entity), 
    (ofc) -[r2:similar]-> (itm:intermediary),
    (itm) -[r3]- (ety)
WHERE
    NOT r1.link CONTAINS 'shareholder' AND 
    NOT (toLower(ofc.name) CONTAINS 'ltd'
        OR toLower(ofc.name) CONTAINS 'limited'
        OR toLower(ofc.name) CONTAINS 'inc') //And many more company filters
    AND ety.status = 'Active'
RETURN ofc.name AS officer_name,
       ety.name AS entity_name, 
       collect(r1.link) as current_position 
// LIMIT 100
```

### Query 3: 
Objective: Retrieve residential addresses connected to a lot of officers.

```Cypher
// @Residential addresses connected to a lot of officers
MATCH (adr:address)<-[r1]-(ofc:officer)
WITH 
    adr.node_id AS address_id,
    r1.link AS address_type,
    adr.address AS address_name,
    collect (DISTINCT ofc.name) AS reg_officers,
    COUNT (DISTINCT ofc.name) AS ofc_count
WHERE ofc_count > 5 AND
    address_type CONTAINS 'resident' 
RETURN 
    address_id,
    collect(address_type) AS address_type,
    address_name,
    reg_officers, 
    ofc_count
ORDER BY ofc_count DESC
// LIMIT 100
```