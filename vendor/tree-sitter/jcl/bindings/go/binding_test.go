package tree_sitter_jcl_test

import (
	"testing"

	tree_sitter "github.com/smacker/go-tree-sitter"
	"github.com/tree-sitter/tree-sitter-jcl"
)

func TestCanLoadGrammar(t *testing.T) {
	language := tree_sitter.NewLanguage(tree_sitter_jcl.Language())
	if language == nil {
		t.Errorf("Error loading Jcl grammar")
	}
}
