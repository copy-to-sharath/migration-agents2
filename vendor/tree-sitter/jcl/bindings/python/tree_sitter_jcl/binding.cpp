#include <pybind11/pybind11.h>

typedef struct TSLanguage TSLanguage;

extern "C" TSLanguage *tree_sitter_jcl();

namespace py = pybind11;

PYBIND11_MODULE(tree_sitter_jcl, m) {
    m.doc() = "Tree-sitter grammar for JCL";
    m.def("language", &tree_sitter_jcl, "Get the tree-sitter language for JCL");
}