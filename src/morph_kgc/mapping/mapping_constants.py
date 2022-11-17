__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "arenas.guerrero.julian@outlook.com"


##############################################################################
#######################   MAPPING DATAFRAME COLUMNS   ########################
##############################################################################

MAPPINGS_DATAFRAME_COLUMNS = [
    'subject_map_type', 'subject_map_value',
    'predicate_map_type', 'predicate_map_value',
    'object_map_type', 'object_map_value',
    'graph_map_type', 'graph_map_value',
    'source_name', 'triples_map_id', 'triples_map_type', 'data_source',
    'subject_map', 'object_map', 'iterator', 'tablename', 'query',
    'subject_quoted', 'subject_termtype',
    'object_termtype', 'object_datatype', 'object_language',
    'object_quoted',
    'subject_join_conditions', 'object_join_conditions'
]


##############################################################################
########################   MAPPING PARSING QUERIES   #########################
##############################################################################

MAPPING_PARSING_QUERY = """
    prefix rr: <http://www.w3.org/ns/r2rml#>
    prefix rml: <http://semweb.mmlab.be/ns/rml#>

    SELECT DISTINCT
        ?triples_map_id ?triples_map_type ?data_source ?iterator ?tablename ?query ?subject_map ?object_map
        ?subject_quoted ?subject_termtype ?object_quoted
        ?object_termtype ?object_datatype ?object_language
        ?subject_map_type ?subject_map_value
        ?predicate_map_type ?predicate_map_value
        ?object_map_type ?object_map_value
        ?graph_map_type ?graph_map_value
        
    WHERE {
        ?triples_map_id rml:logicalSource ?_source .
        ?triples_map_id a ?triples_map_type .
        OPTIONAL { ?_source rml:source ?data_source . }
        OPTIONAL { ?_source rml:iterator ?iterator . }
        OPTIONAL { ?_source rr:tableName ?tablename . }
        OPTIONAL { ?_source rml:query ?query . }

    # Subject -------------------------------------------------------------------------
        ?triples_map_id rml:subjectMap ?subject_map .
        ?subject_map ?subject_map_type ?subject_map_value .
        FILTER ( ?subject_map_type IN ( rr:constant, rr:template, rml:reference, rml:quotedTriplesMap) ) .
        OPTIONAL { ?subject_map rml:quotedTriplesMap ?subject_quoted . }
        OPTIONAL { ?subject_map rr:termType ?subject_termtype . }

    # Predicate -----------------------------------------------------------------------
        OPTIONAL {
            ?triples_map_id rr:predicateObjectMap ?_predicate_object_map .
            
            ?_predicate_object_map rr:predicateMap ?_predicate_map .
            ?_predicate_map ?predicate_map_type ?predicate_map_value .
            FILTER ( ?predicate_map_type IN ( rr:constant, rr:template, rml:reference) ) .

    # Object --------------------------------------------------------------------------
            OPTIONAL {
                ?_predicate_object_map rml:objectMap ?object_map .
                ?object_map rml:quotedTriplesMap ?object_quoted .
                OPTIONAL { ?object_map rr:termType ?object_termtype . }
            } 
            OPTIONAL {
                ?_predicate_object_map rml:objectMap ?object_map .
                ?object_map ?object_map_type ?object_map_value .
                FILTER ( ?object_map_type IN ( rr:constant, rr:template, rml:reference, rml:quotedTriplesMap) ) .
                OPTIONAL { ?object_map rr:termType ?object_termtype . }
                OPTIONAL { ?object_map rr:datatype ?object_datatype . }
                OPTIONAL { ?object_map rr:language ?object_language . }
            } 
            OPTIONAL {
                ?_predicate_object_map rml:objectMap ?object_map .
                ?object_map rr:parentTriplesMap ?object_map_value .
                BIND(rr:parentTriplesMap AS ?object_map_type) .
            }
            OPTIONAL {
                ?_predicate_object_map rr:graphMap ?graph_map .
                ?graph_map ?graph_map_type ?graph_map_value .
                FILTER ( ?graph_map_type IN ( rr:constant, rr:template, rml:reference) ) .
            }
        }
    }
"""


JOIN_CONDITION_PARSING_QUERY = """
    prefix rr: <http://www.w3.org/ns/r2rml#>

    SELECT DISTINCT ?term_map ?join_condition ?child_value ?parent_value
    WHERE {
        ?term_map rr:joinCondition ?join_condition .
        ?join_condition rr:child ?child_value; rr:parent ?parent_value .
    }
"""