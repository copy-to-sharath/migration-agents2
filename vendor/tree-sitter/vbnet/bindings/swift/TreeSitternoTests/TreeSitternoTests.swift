import XCTest
import SwiftTreeSitter
import TreeSitterVbnet

final class TreeSitterVbnetTests: XCTestCase {
    func testCanLoadGrammar() throws {
        let parser = Parser()
        let language = Language(language: tree_sitter_vbnet())
        XCTAssertNoThrow(try parser.setLanguage(language),
                         "Error loading no grammar")
    }
}
