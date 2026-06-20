
.MODEL SMALL
.STACK 100H

.DATA
    SEAT_MAP       DB 20 DUP(0)
    PASSENGER_TYPE DB 20 DUP(0)
    SEAT_FARES     DW 20 DUP(0)
    USER_NAME      DB 30 DUP('$')
    
    TOTAL_REVENUE  DW 0
    SEATS_SOLD     DW 0
    CURRENT_FARE   DW 0
    
    BOOK_QTY       DW 0
    BATCH_PRICE    DW 0
    BATCH_TOTAL    DW 0
    
    FARE_REG       DW 50
    FARE_STU       DW 30
    ADMIN_PASS     DW 1234

    TXT_HEADER     DB 10,13,'   =========================================',10,13,'        METRO BUS RESERVATION SYSTEM     ',10,13,'   =========================================$'
    TXT_LOGIN      DB 10,13,10,13,'   [1] PASSENGER LOGIN',10,13,'   [2] ADMIN LOGIN',10,13,'   [3] EXIT SYSTEM',10,13,10,13,'   >> SELECT OPTION: $'
    TXT_USER_MENU  DB 10,13,10,13,'   --- PASSENGER PANEL ---',10,13,'   [1] VIEW SEAT MAP',10,13,'   [2] BOOK TICKETS (BATCH)',10,13,'   [3] CANCEL TICKET',10,13,'   [4] SEARCH SEAT INFO',10,13,'   [5] LOGOUT',10,13,10,13,'   >> ENTER CHOICE: $'
    TXT_ADMIN_MENU DB 10,13,10,13,'   --- ADMIN DASHBOARD ---',10,13,'   [1] VIEW FINANCIAL REPORT',10,13,'   [2] VIEW PASSENGER MANIFEST',10,13,'   [3] LOGOUT',10,13,10,13,'   >> ENTER CHOICE: $'

    MSG_ASK_NAME   DB 10,13,10,13,'   [LOGIN] ENTER YOUR NAME: $'
    MSG_ASK_QTY    DB 10,13,10,13,'   [INPUT] HOW MANY TICKETS TO BUY? $'
    MSG_ASK_TYPE   DB 10,13,'   [INPUT] SELECT CATEGORY (1.STUDENT / 2.REGULAR): $'
    MSG_ASK_SEAT   DB 10,13,'   [INPUT] ENTER SEAT NUMBER: $'
    MSG_ASK_PASS   DB 10,13,10,13,'   [SECURITY] ENTER ADMIN PASSWORD: $'
    
    MSG_PAY_ASK    DB 10,13,10,13,'   >> KINDLY PAY BILL OF $'
    MSG_PAY_PIN    DB ' TAKA | ENTER PIN : $'
    MSG_PAY_FAIL   DB 10,13,'   >> ERROR: WRONG PIN! BOOKING CANCELLED.$'
    
    MSG_SUCCESS    DB 10,13,'   >> SUCCESS: TICKET PURCHASED FOR $' 
    MSG_REFUND     DB 10,13,'   >> SUCCESS: BOOKING CANCELLED & REFUNDED.$'
    
    MSG_ERR_TAKEN  DB 10,13,'   >> ERROR: SEAT TAKEN! TRY ANOTHER.$'
    MSG_ERR_INV    DB 10,13,'   >> ERROR: INVALID INPUT!$'
    MSG_ERR_EMP    DB 10,13,'   >> ERROR: SEAT IS ALREADY EMPTY.$'
    MSG_ERR_PASS   DB 10,13,'   >> ERROR: ACCESS DENIED!$'
    
    RPT_REV        DB 10,13,'   | TOTAL REVENUE:  $'
    RPT_SOLD       DB 10,13,'   | TICKETS SOLD:   $'
    
    MSG_BKD_INFO   DB 10,13,'   [STATUS] BOOKED | TYPE: $'
    MSG_AVL_INFO   DB 10,13,'   [STATUS] AVAILABLE$'
    TXT_STU        DB 'STUDENT$'
    TXT_REG        DB 'REGULAR$'
    MSG_PAUSE      DB 10,13,10,13,'   [PRESS ANY KEY TO CONTINUE]$'

    BUS_TOP        DB 10,13,'      ___________________________________',10,13,'     | [DRIVER]                   | EXIT |$'
    BUS_BOT        DB 10,13,'     |___________________________________|$'
    SPACE          DB '   $'
    NEWLINE        DB 10,13,'$'

; ==============================================================================
; MACROS
; ==============================================================================

M_CLS MACRO
    MOV AH, 00H
    MOV AL, 03H
    INT 10H
ENDM

M_PRINT MACRO STR
    LEA DX, STR
    MOV AH, 9
    INT 21H
ENDM

M_CHAR MACRO C
    MOV DL, C
    MOV AH, 2
    INT 21H
ENDM

M_PRINT_SEAT MACRO
    LOCAL PRT_10, FINISH
    MOV BX, AX      
    CMP BX, 10
    JGE PRT_10
    M_CHAR '0'      
    MOV AX, BX
    ADD AL, 48
    M_CHAR AL
    JMP FINISH
    PRT_10:
    MOV AX, BX
    CALL PROC_PRINT_NUM
    FINISH:
ENDM

M_SCAN_NUM MACRO
    LOCAL I_LOOP, I_END
    PUSH BX
    PUSH CX
    PUSH DX
    XOR BX, BX
    I_LOOP:
        MOV AH, 1
        INT 21H
        CMP AL, 13
        JE I_END
        SUB AL, 48
        MOV AH, 0
        MOV CX, AX
        MOV AX, BX
        MOV DX, 10
        MUL DX
        ADD AX, CX
        MOV BX, AX
        JMP I_LOOP
    I_END:
        MOV AX, BX
        POP DX
        POP CX
        POP BX
ENDM

M_GET_NAME MACRO
    LOCAL N_LOOP, N_END
    LEA DI, USER_NAME
    MOV CX, 0
    N_LOOP:
        MOV AH, 1
        INT 21H
        CMP AL, 13
        JE N_END
        MOV [DI], AL
        INC DI
        JMP N_LOOP
    N_END:
        MOV BYTE PTR [DI], '$'
ENDM

.CODE

MAIN PROC
    MOV AX, @DATA
    MOV DS, AX
    
    LOGIN_SCREEN:
        M_CLS
        M_PRINT TXT_HEADER
        M_PRINT TXT_LOGIN
        
        MOV AH, 1
        INT 21H
        
        CMP AL, '1'
        JE GO_PASSENGER
        CMP AL, '2'
        JE GO_ADMIN
        CMP AL, '3'
        JE EXIT_SYS
        JMP LOGIN_SCREEN
        
    GO_PASSENGER:
        CALL PROC_PASSENGER_SESSION
        JMP LOGIN_SCREEN
        
    GO_ADMIN:
        CALL PROC_ADMIN_SESSION
        JMP LOGIN_SCREEN
        
    EXIT_SYS:
        MOV AX, 4C00H
        INT 21H
MAIN ENDP

PROC_PASSENGER_SESSION PROC
    M_CLS
    M_PRINT TXT_HEADER
    M_PRINT MSG_ASK_NAME
    M_GET_NAME
    
    PASS_MENU:
        M_CLS
        M_PRINT TXT_HEADER
        M_PRINT NEWLINE
        M_PRINT USER_NAME
        M_PRINT TXT_USER_MENU
        
        MOV AH, 1
        INT 21H
        
        CMP AL, '1'
        JE P_F1
        CMP AL, '2'
        JE P_F2
        CMP AL, '3'
        JE P_F3
        CMP AL, '4'
        JE P_F4
        CMP AL, '5'
        JE P_LOGOUT
        JMP PASS_MENU
        
    P_F1: CALL PROC_VIEW_MAP
          JMP P_WAIT
    P_F2: CALL PROC_BATCH_BOOKING
          JMP P_WAIT
    P_F3: CALL PROC_CANCEL_TICKET
          JMP P_WAIT
    P_F4: CALL PROC_SEARCH_SEAT
          JMP P_WAIT
          
    P_WAIT:
        M_PRINT MSG_PAUSE
        MOV AH, 7
        INT 21H
        JMP PASS_MENU
        
    P_LOGOUT:
        RET
PROC_PASSENGER_SESSION ENDP

PROC_ADMIN_SESSION PROC
    M_CLS
    M_PRINT TXT_HEADER
    M_PRINT MSG_ASK_PASS
    M_SCAN_NUM
    
    CMP AX, ADMIN_PASS
    JNE ADM_FAIL
    
    ADM_MENU:
        M_CLS
        M_PRINT TXT_HEADER
        M_PRINT TXT_ADMIN_MENU
        
        MOV AH, 1
        INT 21H
        
        CMP AL, '1'
        JE A_F1_STATS
        CMP AL, '2'
        JE A_F2_MANIFEST
        CMP AL, '3'
        JE A_LOGOUT
        JMP ADM_MENU
        
    A_F1_STATS:
        M_CLS
        M_PRINT TXT_HEADER
        M_PRINT RPT_REV
        MOV AX, TOTAL_REVENUE
        CALL PROC_PRINT_NUM
        M_PRINT RPT_SOLD
        MOV AX, SEATS_SOLD
        CALL PROC_PRINT_NUM
        JMP A_WAIT
        
    A_F2_MANIFEST:
        M_CLS
        M_PRINT TXT_HEADER
        MOV CX, 20
        MOV SI, 0
        MAN_LOOP:
            MOV AL, SEAT_MAP[SI]
            CMP AL, 1
            JNE MAN_NEXT
            
            M_PRINT NEWLINE
            M_PRINT SPACE
            M_CHAR '['
            MOV AX, SI
            INC AX
            M_PRINT_SEAT
            M_PRINT MSG_BKD_INFO
            
            MOV AL, PASSENGER_TYPE[SI]
            CMP AL, 1
            JE MAN_STU
            M_PRINT TXT_REG
            JMP MAN_NEXT
            MAN_STU: M_PRINT TXT_STU
        MAN_NEXT:
            INC SI
            LOOP MAN_LOOP
        JMP A_WAIT
        
    A_WAIT:
        M_PRINT MSG_PAUSE
        MOV AH, 7
        INT 21H
        JMP ADM_MENU
        
    A_LOGOUT: RET
    ADM_FAIL: M_PRINT MSG_ERR_PASS
              M_PRINT MSG_PAUSE
              MOV AH, 7
              INT 21H
              RET
PROC_ADMIN_SESSION ENDP

PROC_PRINT_NUM PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    MOV CX, 0
    MOV BX, 10
    DL1: MOV DX, 0
         DIV BX
         PUSH DX
         INC CX
         CMP AX, 0
         JNE DL1
    PL1: POP DX
         ADD DL, 48
         MOV AH, 2
         INT 21H
         LOOP PL1
    POP DX
    POP CX
    POP BX
    POP AX
    RET
PROC_PRINT_NUM ENDP

PROC_VIEW_MAP PROC
    M_CLS
    M_PRINT TXT_HEADER
    M_PRINT BUS_TOP
    MOV CX, 5
    MOV SI, 0
    ROW_L:
        M_PRINT NEWLINE
        M_PRINT SPACE
        CALL PROC_DRAW
        INC SI
        CALL PROC_DRAW
        INC SI
        M_PRINT SPACE
        CALL PROC_DRAW
        INC SI
        CALL PROC_DRAW
        INC SI
        LOOP ROW_L
    M_PRINT BUS_BOT
    RET
PROC_VIEW_MAP ENDP

PROC_DRAW PROC
    M_CHAR '['
    MOV AX, SI
    INC AX
    M_PRINT_SEAT
    M_CHAR ':'
    MOV AL, SEAT_MAP[SI]
    CMP AL, 1
    JE DRAW_B
    M_CHAR 'E'
    JMP DRAW_E
    DRAW_B: M_CHAR 'B'
    DRAW_E: M_CHAR ']'
    M_CHAR ' '
    RET
PROC_DRAW ENDP

PROC_BATCH_BOOKING PROC
    M_PRINT MSG_ASK_QTY
    M_SCAN_NUM
    MOV BOOK_QTY, AX
    
    M_PRINT MSG_ASK_TYPE
    MOV AH, 1
    INT 21H
    
    CMP AL, '1'
    JE SET_STU
    MOV AX, FARE_REG
    JMP SAVE_PRICE
    SET_STU:
    MOV AX, FARE_STU
    
    SAVE_PRICE:
    MOV BATCH_PRICE, AX
    MOV AX, BATCH_PRICE
    MUL BOOK_QTY
    MOV BATCH_TOTAL, AX
    
    MOV CX, BOOK_QTY
    
    BOOK_LOOP:
        CMP CX, 0
        JE VERIFY_PAYMENT
        
        PUSH CX
        
        CALL PROC_VIEW_MAP
        M_PRINT MSG_ASK_SEAT
        M_SCAN_NUM
        
        CMP AX, 1
        JL BK_RETRY
        CMP AX, 20
        JG BK_RETRY
        
        DEC AX
        MOV SI, AX
        
        MOV AL, SEAT_MAP[SI]
        CMP AL, 1
        JE BK_TAKEN
        
        MOV SEAT_MAP[SI], 1
        MOV AX, BATCH_PRICE
        MOV SEAT_FARES[SI], AX
        
        MOV AX, BATCH_PRICE
        CMP AX, FARE_STU
        JNE SET_REG_TYPE
        MOV PASSENGER_TYPE[SI], 1
        JMP PUSH_SI
        SET_REG_TYPE:
        MOV PASSENGER_TYPE[SI], 2
        
        PUSH_SI:
        PUSH SI
        
        POP CX
        DEC CX
        JMP BOOK_LOOP
        
    BK_RETRY:
        M_PRINT MSG_ERR_INV
        POP CX
        JMP BOOK_LOOP
        
    BK_TAKEN:
        M_PRINT MSG_ERR_TAKEN
        POP CX
        JMP BOOK_LOOP
        
    VERIFY_PAYMENT:
        M_PRINT MSG_PAY_ASK
        MOV AX, BATCH_TOTAL
        CALL PROC_PRINT_NUM
        M_PRINT MSG_PAY_PIN
        
        M_SCAN_NUM
        CMP AX, 1234
        JE PAYMENT_OK
        
        ; ROLLBACK LOGIC
        MOV CX, BOOK_QTY
        ROLLBACK_LOOP:
            POP SI
            MOV SEAT_MAP[SI], 0
            MOV SEAT_FARES[SI], 0
            MOV PASSENGER_TYPE[SI], 0
            LOOP ROLLBACK_LOOP
            
        M_PRINT MSG_PAY_FAIL
        RET
        
    PAYMENT_OK:
        ; CLEAR STACK
        MOV CX, BOOK_QTY
        CLEAR_STK:
            POP SI
            LOOP CLEAR_STK
            
        MOV AX, BATCH_TOTAL
        ADD TOTAL_REVENUE, AX
        MOV AX, BOOK_QTY
        ADD SEATS_SOLD, AX
        
        M_PRINT MSG_SUCCESS
        M_PRINT USER_NAME
        RET
PROC_BATCH_BOOKING ENDP

PROC_CANCEL_TICKET PROC
    CALL PROC_VIEW_MAP
    M_PRINT MSG_ASK_SEAT
    M_SCAN_NUM
    CMP AX, 1
    JL CN_ERR
    CMP AX, 20
    JG CN_ERR
    DEC AX
    MOV SI, AX
    MOV AL, SEAT_MAP[SI]
    CMP AL, 0
    JE CN_EMP
    MOV AX, SEAT_FARES[SI]
    SUB TOTAL_REVENUE, AX
    DEC SEATS_SOLD
    MOV SEAT_MAP[SI], 0
    MOV SEAT_FARES[SI], 0
    MOV PASSENGER_TYPE[SI], 0
    M_PRINT MSG_REFUND
    RET
    CN_EMP: M_PRINT MSG_ERR_EMP
            RET
    CN_ERR: M_PRINT MSG_ERR_INV
            RET
PROC_CANCEL_TICKET ENDP

PROC_SEARCH_SEAT PROC
    M_CLS
    M_PRINT MSG_ASK_SEAT
    M_SCAN_NUM
    DEC AX
    MOV SI, AX
    MOV AL, SEAT_MAP[SI]
    CMP AL, 1
    JE SRCH_BKD
    M_PRINT MSG_AVL_INFO
    RET
    SRCH_BKD:
    M_PRINT MSG_BKD_INFO
    MOV AL, PASSENGER_TYPE[SI]
    CMP AL, 1
    JE SRCH_STU
    M_PRINT TXT_REG
    RET
    SRCH_STU: M_PRINT TXT_STU
    RET
PROC_SEARCH_SEAT ENDP

END MAIN