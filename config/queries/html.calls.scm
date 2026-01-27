; Start Tag Event Handlers
(element
  (start_tag
    (tag_name) @tag
    (attribute
      (attribute_name) @attr_name
      (quoted_attribute_value
        (attribute_value) @callee)
      (#match? @attr_name "^(OnClick|OnLoad|OnInit|OnPreRender|OnDataBinding|OnCommand|OnItemCommand|OnItemDataBound|OnSelectedIndexChanged|OnTextChanged|OnCheckedChanged|OnRowCommand|OnRowDataBound|OnPageIndexChanging|OnSorting)$"))))

; Self-closing Tag Event Handlers
(element
  (self_closing_tag
    (tag_name) @tag
    (attribute
      (attribute_name) @attr_name
      (quoted_attribute_value
        (attribute_value) @callee)
      (#match? @attr_name "^(OnClick|OnLoad|OnInit|OnPreRender|OnDataBinding|OnCommand|OnItemCommand|OnItemDataBound|OnSelectedIndexChanged|OnTextChanged|OnCheckedChanged|OnRowCommand|OnRowDataBound|OnPageIndexChanging|OnSorting)$"))))

; Direct method calls in attributes (Start Tag)
(element
  (start_tag
    (attribute
      (attribute_name) @attr
      (quoted_attribute_value
        (attribute_value) @callee)
      (#match? @callee ".*\\(.*\\).*"))))

; Direct method calls in attributes (Self Closing Tag)
(element
  (self_closing_tag
    (attribute
      (attribute_name) @attr
      (quoted_attribute_value
        (attribute_value) @callee)
      (#match? @callee ".*\\(.*\\).*"))))

; Script src references - capture script file imports
(element
  (start_tag
    (tag_name) @tag
    (attribute
      (attribute_name) @attr_name
      (quoted_attribute_value
        (attribute_value) @callee))
    (#eq? @tag "script")
    (#eq? @attr_name "src")))

; Link href references - capture CSS/resource imports  
(element
  (self_closing_tag
    (tag_name) @tag
    (attribute
      (attribute_name) @attr_name
      (quoted_attribute_value
        (attribute_value) @callee))
    (#eq? @tag "link")
    (#eq? @attr_name "href")))

; Image/iframe src - capture resource references
(element
  (start_tag
    (attribute
      (attribute_name) @attr_name
      (quoted_attribute_value
        (attribute_value) @callee))
    (#match? @attr_name "^(src|href|data-src|action)$")))

; ASP.NET control references (CodeBehind, Inherits, MasterPageFile)
(element
  (start_tag
    (attribute
      (attribute_name) @attr_name
      (quoted_attribute_value
        (attribute_value) @callee))
    (#match? @attr_name "^(CodeBehind|CodeFile|Inherits|MasterPageFile|Src)$")))
