       IDENTIFICATION DIVISION.
       PROGRAM-ID. TESTPGM.
       PROCEDURE DIVISION.
       MAIN-PARA.
           EVALUATE TRUE
               WHEN WS-A = 1
                   DISPLAY 'ONE'
               WHEN WS-A = 2
                   DISPLAY 'TWO'
               WHEN OTHER
                   DISPLAY 'OTHER'
           END-EVALUATE.
           STOP RUN.
