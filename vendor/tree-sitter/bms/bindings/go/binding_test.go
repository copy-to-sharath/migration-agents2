package tree_sitter_bms_test

import (
	"testing"

	tree_sitter "github.com/smacker/go-tree-sitter"
	"github.com/tree-sitter/tree-sitter-bms"
)

func TestCanLoadGrammar(t *testing.T) {
	language := tree_sitter.NewLanguage(tree_sitter_bms.Language())
	if language == nil {
		t.Errorf("Error loading Bms grammar")
	}
}
