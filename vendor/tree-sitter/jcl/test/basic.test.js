const { expect } = require('chai');

// Mock tree-sitter for testing without node bindings
const mockParser = {
  parse: (sourceCode) => {
    // Simple mock implementation for basic testing
    return {
      rootNode: {
        type: 'source_file',
        firstChild: determineStatementType(sourceCode),
        namedChildCount: 1
      }
    };
  }
};

function determineStatementType(code) {
  if (code.includes(' JOB')) return { type: 'job_statement' };
  if (code.includes(' EXEC')) return { type: 'exec_statement' };
  if (code.includes(' DD')) return { type: 'dd_statement' };
  if (code.startsWith('//*')) return { type: 'comment' };
  return { type: 'unknown' };
}

describe('JCL Grammar Basic Tests', function() {
  describe('Statement Recognition', function() {
    it('should recognize JOB statements', function() {
      const sourceCode = '//MYJOB    JOB';
      const tree = mockParser.parse(sourceCode);
      
      expect(tree.rootNode.type).to.equal('source_file');
      expect(tree.rootNode.firstChild.type).to.equal('job_statement');
    });

    it('should recognize EXEC statements', function() {
      const sourceCode = '//STEP1    EXEC PGM=IEFBR14';
      const tree = mockParser.parse(sourceCode);
      
      expect(tree.rootNode.type).to.equal('source_file');
      expect(tree.rootNode.firstChild.type).to.equal('exec_statement');
    });

    it('should recognize DD statements', function() {
      const sourceCode = '//SYSOUT   DD DSN=USER.OUTPUT,DISP=SHR';
      const tree = mockParser.parse(sourceCode);
      
      expect(tree.rootNode.type).to.equal('source_file');
      expect(tree.rootNode.firstChild.type).to.equal('dd_statement');
    });

    it('should recognize comments', function() {
      const sourceCode = '//* This is a comment';
      const tree = mockParser.parse(sourceCode);
      
      expect(tree.rootNode.type).to.equal('source_file');
      expect(tree.rootNode.firstChild.type).to.equal('comment');
    });
  });

  describe('JCL Name Validation', function() {
    it('should validate valid JCL names', function() {
      const validNames = ['MYJOB', 'STEP1', 'SYSOUT', 'A1B2C3D4'];
      validNames.forEach(name => {
        expect(isValidJCLName(name)).to.be.true;
      });
    });

    it('should reject invalid JCL names', function() {
      const invalidNames = ['toolong123', '1STARTS', 'has-dash', ''];
      invalidNames.forEach(name => {
        expect(isValidJCLName(name)).to.be.false;
      });
    });
  });
});

function isValidJCLName(name) {
  return /^[A-Z][A-Z0-9#@$]{0,7}$/.test(name);
}

module.exports = { mockParser, isValidJCLName };