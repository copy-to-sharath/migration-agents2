package tree_sitter_vbnet_test

import (
	"testing"

	tree_sitter "github.com/tree-sitter/go-tree-sitter"
	tree_sitter_vbnet "github.com/gabriel-gubert/tree-sitter-vbnet.git/bindings/go"
)

func TestCanLoadGrammar(t *testing.T) {
	language := tree_sitter.NewLanguage(tree_sitter_vbnet.Language())
	if language == nil {
		t.Errorf("Error loading no grammar")
	}
}
