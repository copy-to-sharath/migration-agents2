; ASP.NET server controls with IDs (Start Tag)
(element
  (start_tag
    (tag_name) @kind
    (attribute
      (attribute_name) @id_attr
      (quoted_attribute_value
        (attribute_value) @name)
      (#eq? @id_attr "ID")))
)

; ASP.NET server controls with IDs (Self Closing Tag)
(element
  (self_closing_tag
    (tag_name) @kind
    (attribute
      (attribute_name) @id_attr
      (quoted_attribute_value
        (attribute_value) @name)
      (#eq? @id_attr "ID")))
)

; Standard HTML elements with IDs (Start Tag)
(element
  (start_tag
    (tag_name) @kind
    (attribute
      (attribute_name) @id_attr
      (quoted_attribute_value
        (attribute_value) @name)
      (#eq? @id_attr "id")))
)

; Standard HTML elements with IDs (Self Closing Tag)
(element
  (self_closing_tag
    (tag_name) @kind
    (attribute
      (attribute_name) @id_attr
      (quoted_attribute_value
        (attribute_value) @name)
      (#eq? @id_attr "id")))
)
