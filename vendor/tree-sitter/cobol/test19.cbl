       IDENTIFICATION DIVISION.
       PROGRAM-ID. TESTPGM.
       PROCEDURE DIVISION.
       MAIN-PARA.
           EXEC CICS RETURN
                     TRANSID (WS-TRANID)
           END-EXEC.
           STOP RUN.
