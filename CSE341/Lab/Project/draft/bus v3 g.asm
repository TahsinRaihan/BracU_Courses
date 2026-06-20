; ==============================================================================
; PROJECT: CITY BUS RESERVATION SYSTEM (FINAL PROFESSIONAL BUILD)
; GROUP MEMBERS: 2
; ------------------------------------------------------------------------------
; MEMBER A: System Architect (Macros, UI Design, Input/Output Handlers)
; MEMBER B: Logic Engineer (Procedures, Array Manipulation, Core Algorithms)
; ==============================================================================

.MODEL SMALL
.STACK 100H

.DATA
    ; ======================= DATA SEGMENT =======================
    ; --- SYSTEM VARIABLES ---
    TOTAL_REVENUE DW 0
    SEATS_SOLD    DW 0
    CURRENT_FARE  DW 0
    
    ; --- ARRAYS (CORE DATA STRUCTURES) ---
    ; Seat Map: 0 = Empty, 1 = Booked
    SEAT_MAP      DB 20 DUP(0)  
    ; Passenger Type: 0 = None, 1 = Student, 2 = Regular
    PASSENGER_TYPE DB 20 DUP(0) 
    ; Fare Archive: Stores the exact fare paid for each seat (for refunds)
    SEAT_FARES    DW 20 DUP(0)  
    
    ; --- CONSTANTS ---
    FARE_REGULAR  DW 50
    FARE_STUDENT  DW 30
    ADMIN_PASS    DB '1234'     ; Admin Password
    
    ; --- MEMBER A: UI STRINGS ---
    HEADER_MAIN   DB 10,13,'============================================',10,13,'      CITY BUS RESERVATION SYSTEM v2.0      ',10,13,'============================================$'
    HEADER_USER   DB 10,13,'-------------- USER PANEL --------------$'
    HEADER_ADMIN  DB 10,13,'-------------- ADMIN DASHBOARD --------------$'
    
    MSG_MAIN_MENU DB 10,13,'[1] User Panel (Book/Cancel)',10,13,'[2] Admin Panel (Revenue/Reports)',10,13,'[3] Exit System',10,13,10,13,'Select Option: $'
    MSG_USER_MENU DB 10,13,'   1. View Bus Map',10,13,'   2. Book a Ticket',10,13,'   3. Cancel a Ticket',10,13,'   4. Check Seat Status',10,13,'   5. Logout',10,13,10,13,'   Enter Choice: $'
    
    MSG_LOGIN     DB 10,13,'ENTER USERNAME: $'
    MSG_PASS      DB 10,13,'ENTER ADMIN PASSWORD: $'
    MSG_WELCOME   DB 10,13,'>> WELCOME, GUEST! Access Granted.$'
    MSG_ACCESS    DB 10,13,'>> ACCESS GRANTED. Loading Dashboard...$'
    MSG_DENIED    DB 10,13,'>> ACCESS DENIED. Invalid Password.$'
    
    MSG_BOOK_NUM  DB 10,13,'[BOOKING] Enter Seat Number (1-20): $'
    MSG_TYPE      DB 10,13,'[CATEGORY] 1. Student (30tk) | 2. Regular (50tk): $'
    MSG_SUCCESS   DB 10,13,'>> SUCCESS: Ticket Confirmed. Thank you!$'
    MSG_ERR_TAKEN DB 10,13,'>> ERROR: Seat is already booked!$'
    MSG_ERR_INV   DB 10,13,'>> ERROR: Invalid Input provided.$'
    
    MSG_CANCEL    DB 10,13,'[CANCEL] Enter Seat Number to Refund: $'
    MSG_REFUND    DB 10,13,'>> REFUND SUCCESSFUL. Amount Returned.$'
    MSG_NOT_BKD   DB 10,13,'>> ERROR: This seat was not booked.$'
    
    MSG_SEARCH    DB 10,13,'[SEARCH] Enter Seat Number: $'
    MSG_ST_BKD    DB ' -> STATUS: BOOKED | TYPE: $'
    MSG_ST_EMP    DB ' -> STATUS: AVAILABLE$'
    MSG_ST_STD    DB 'Student$'
    MSG_ST_REG    DB 'Regular$'
    
    MSG_REV_TOT   DB 10,13,'   $$ TOTAL REVENUE GENERATED: $'
    MSG_SOL_TOT   DB 10,13,'   ## TOTAL SEATS SOLD: $'
    
    TXT_ENTER     DB 10,13,'Press ENTER to continue...$'
    NEWLINE       DB 10,13,'$'
    
    ; Temp buffer for username input (just for show)
    USER_BUFFER   DB 20 DUP('$')

; ==============================================================================
; MEMBER A WORK: MACROS & UI ENGINE
; "I ensure the interface looks complex and handles low-level I/O."
; ==============================================================================

; --- MACRO: CLEAR SCREEN ---
M_CLS MACRO
    MOV AH, 00H
    MOV AL, 03H
    INT 10H
ENDM

; --- MACRO: PRINT STRING ---
M_PRINT MACRO STR
    LEA DX, STR
    MOV AH, 9
    INT 21H
ENDM

; --- MACRO: READ KEY (NO ECHO) ---
M_GETCH MACRO
    MOV AH, 7
    INT 21H
ENDM

; --- MACRO: READ KEY (WITH ECHO) ---
M_INPUT MACRO
    MOV AH, 1
    INT 21H
ENDM

; --- MACRO: PAUSE SCREEN ---
M_PAUSE MACRO
    M_PRINT TXT_ENTER
    M_GETCH
ENDM

; --- MACRO: PRINT NUMBER (AX) ---
; Handles multi-digit number printing
M_SHOW_NUM MACRO
    LOCAL D_LOOP, P_LOOP, P_ZERO, FIN
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    CMP AX, 0
    JE P_ZERO
    
    MOV CX, 0
    MOV BX, 10
    
    D_LOOP:
        MOV DX, 0
        DIV BX
        PUSH DX
        INC CX
        CMP AX, 0
        JNE D_LOOP
        
    P_LOOP:
        POP DX
        ADD DL, 48
        MOV AH, 2
        INT 21H
        LOOP P_LOOP
        JMP FIN
        
    P_ZERO:
        MOV DL, '0'
        MOV AH, 2
        INT 21H
        
    FIN:
        POP DX
        POP CX
        POP BX
        POP AX
ENDM

; --- MACRO: MULTI-DIGIT INPUT ---
; Reads string, converts to number in AX
M_GET_NUM MACRO
    LOCAL IN_LP, END_IN
    PUSH BX
    PUSH CX
    PUSH DX
    
    XOR BX, BX  ; Result
    XOR CX, CX
    
    IN_LP:
        MOV AH, 1
        INT 21H
        CMP AL, 13 ; Enter
        JE END_IN
        CMP AL, '0'
        JL END_IN
        CMP AL, '9'
        JG END_IN
        
        SUB AL, 48
        MOV CL, AL
        MOV CH, 0
        
        MOV AX, BX
        MOV DX, 10
        MUL DX
        ADD AX, CX
        MOV BX, AX
        JMP IN_LP
        
    END_IN:
        MOV AX, BX
        POP DX
        POP CX
        POP BX
ENDM

.CODE
; ==============================================================================
; MAIN PROCEDURE (THE HUB)
; ==============================================================================
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX
    
    SYSTEM_START:
        M_CLS
        M_PRINT HEADER_MAIN
        M_PRINT MSG_MAIN_MENU
        
        M_INPUT
        CMP AL, '1'
        JE GO_USER
        CMP AL, '2'
        JE GO_ADMIN
        CMP AL, '3'
        JE SYSTEM_EXIT
        JMP SYSTEM_START
        
    GO_USER:
        CALL USER_LOGIN_PROC
        CALL USER_PANEL_PROC
        JMP SYSTEM_START
        
    GO_ADMIN:
        CALL ADMIN_LOGIN_PROC
        JMP SYSTEM_START
        
    SYSTEM_EXIT:
        MOV AX, 4C00H
        INT 21H
MAIN ENDP

; ==============================================================================
; MEMBER B WORK: LOGIC PROCEDURES & ALGORITHMS
; "I handle the flow, arrays, stacks, and business logic."
; ==============================================================================

; --- FEATURE 1 (PART A): USER LOGIN ---
USER_LOGIN_PROC PROC
    M_CLS
    M_PRINT HEADER_MAIN
    M_PRINT MSG_LOGIN
    
    ; Simulate reading a string (Just for UI effect)
    MOV AH, 0AH
    LEA DX, USER_BUFFER
    INT 21H
    
    M_PRINT MSG_WELCOME
    M_PAUSE
    RET
USER_LOGIN_PROC ENDP

; --- USER PANEL MENU LOOP ---
USER_PANEL_PROC PROC
    USER_LOOP:
        M_CLS
        M_PRINT HEADER_USER
        M_PRINT MSG_USER_MENU
        
        M_INPUT
        MOV BL, AL
        
        CMP BL, '1'
        JE DO_MAP
        CMP BL, '2'
        JE DO_BOOK
        CMP BL, '3'
        JE DO_CANCEL
        CMP BL, '4'
        JE DO_SEARCH
        CMP BL, '5'
        JE EXIT_USER
        JMP USER_LOOP
        
    DO_MAP:
        CALL VIEW_MAP_PROC
        M_PAUSE
        JMP USER_LOOP
    DO_BOOK:
        CALL BOOK_TICKET_PROC
        M_PAUSE
        JMP USER_LOOP
    DO_CANCEL:
        CALL CANCEL_TICKET_PROC
        M_PAUSE
        JMP USER_LOOP
    DO_SEARCH:
        CALL SEARCH_SEAT_PROC
        M_PAUSE
        JMP USER_LOOP
        
    EXIT_USER:
        RET
USER_PANEL_PROC ENDP

; --- FEATURE 1 (PART B) & FEATURE 4: ADMIN LOGIN & DASHBOARD ---
ADMIN_LOGIN_PROC PROC
    M_CLS
    M_PRINT HEADER_ADMIN
    M_PRINT MSG_PASS
    
    ; Secure Password Input Logic
    XOR CX, CX      ; Counter
    MOV BX, 0       ; Correctness flag (0=Good)
    
    PASS_LOOP:
        M_GETCH     ; Read without echo
        CMP AL, 13  ; Enter key
        JE CHECK_PASS
        
        MOV DL, '*' ; Masking character
        MOV AH, 2
        INT 21H
        
        ; Verify against hardcoded password '1234'
        ; Simple verification logic for project scope
        ; (Note: In real assembly this would be an array compare)
        ; Here we just check 4 chars for simplicity or assume success if matches logic
        ; To make it robust, we compare:
        CMP CX, 0
        JNE CHK_2
        CMP AL, '1'
        JNE BAD_BIT
        JMP NXT_BIT
        
        CHK_2:
        CMP CX, 1
        JNE CHK_3
        CMP AL, '2'
        JNE BAD_BIT
        JMP NXT_BIT
        
        CHK_3:
        CMP CX, 2
        JNE CHK_4
        CMP AL, '3'
        JNE BAD_BIT
        JMP NXT_BIT
        
        CHK_4:
        CMP CX, 3
        JNE CHK_X
        CMP AL, '4'
        JNE BAD_BIT
        JMP NXT_BIT

        CHK_X:
        ; More than 4 chars
        MOV BX, 1
        JMP NXT_BIT
        
        BAD_BIT:
        MOV BX, 1   ; Flag as incorrect
        
        NXT_BIT:
        INC CX
        JMP PASS_LOOP
        
    CHECK_PASS:
        CMP BX, 0
        JNE ACCESS_DENIED
        CMP CX, 4   ; Must be length 4
        JNE ACCESS_DENIED
        
        ; IF SUCCESS:
        M_PRINT MSG_ACCESS
        M_PAUSE
        CALL ADMIN_DASH_PROC
        RET
        
    ACCESS_DENIED:
        M_PRINT MSG_DENIED
        M_PAUSE
        RET
ADMIN_LOGIN_PROC ENDP

ADMIN_DASH_PROC PROC
    DASH_LOOP:
        M_CLS
        M_PRINT HEADER_ADMIN
        
        M_PRINT MSG_SOL_TOT
        MOV AX, SEATS_SOLD
        M_SHOW_NUM
        
        M_PRINT MSG_REV_TOT
        MOV AX, TOTAL_REVENUE
        M_SHOW_NUM
        
        M_PRINT NEWLINE
        M_PRINT MSG_MAIN_MENU ; Reusing menu msg for exit option
        
        M_INPUT
        CMP AL, '3' ; Exit option
        JE EXIT_ADMIN
        JMP DASH_LOOP
        
    EXIT_ADMIN:
        RET
ADMIN_DASH_PROC ENDP

; --- FEATURE 1: VIEW SEAT MAP LOGIC ---
VIEW_MAP_PROC PROC
    PUSH AX
    PUSH CX
    PUSH SI
    
    M_PRINT NEWLINE
    MOV CX, 20
    MOV SI, 0
    
    MAP_ITERATION:
        ; Visual Logic: [ 01:E ]
        MOV DL, '['
        MOV AH, 2
        INT 21H
        
        MOV AX, SI
        INC AX
        M_SHOW_NUM
        
        MOV DL, ':'
        MOV AH, 2
        INT 21H
        
        ; Array Access
        MOV AL, SEAT_MAP[SI]
        CMP AL, 1
        JE DRAW_BOOKED
        
        MOV DL, 'E'
        MOV AH, 2
        INT 21H
        JMP CLOSE_ITEM
        
    DRAW_BOOKED:
        MOV DL, 'B'
        MOV AH, 2
        INT 21H
        
    CLOSE_ITEM:
        MOV DL, ']'
        MOV AH, 2
        INT 21H
        MOV DL, ' '
        INT 21H
        
        ; Formatting: 4 seats per row
        MOV AX, SI
        INC AX
        MOV BL, 4
        DIV BL
        CMP AH, 0
        JNE CONTINUE_MAP
        M_PRINT NEWLINE
        
    CONTINUE_MAP:
        INC SI
        CMP SI, 20
        JL MAP_ITERATION
        
    POP SI
    POP CX
    POP AX
    RET
VIEW_MAP_PROC ENDP

; --- FEATURE 2 & 3: BOOKING LOGIC ---
BOOK_TICKET_PROC PROC
    M_PRINT MSG_BOOK_NUM
    M_GET_NUM           ; Returns AX
    
    ; Validation
    CMP AX, 1
    JL BOOK_ERR
    CMP AX, 20
    JG BOOK_ERR
    
    DEC AX
    MOV SI, AX          ; SI = Index
    
    ; Check Availability
    MOV AL, SEAT_MAP[SI]
    CMP AL, 1
    JE BOOK_TAKEN
    
    ; Select Type
    M_PRINT MSG_TYPE
    M_INPUT
    
    CMP AL, '1'
    JE TYPE_STU
    
    ; Regular
    MOV AX, FARE_REGULAR
    MOV PASSENGER_TYPE[SI], 2
    JMP FINALIZE_BOOK
    
    TYPE_STU:
    MOV AX, FARE_STUDENT
    MOV PASSENGER_TYPE[SI], 1
    
    FINALIZE_BOOK:
    MOV SEAT_FARES[SI], AX   ; Save specific fare
    ADD TOTAL_REVENUE, AX
    INC SEATS_SOLD
    MOV SEAT_MAP[SI], 1      ; Update Status
    
    M_PRINT MSG_SUCCESS
    RET
    
    BOOK_TAKEN:
    M_PRINT MSG_ERR_TAKEN
    RET
    
    BOOK_ERR:
    M_PRINT MSG_ERR_INV
    RET
BOOK_TICKET_PROC ENDP

; --- FEATURE 5: CANCELLATION LOGIC ---
CANCEL_TICKET_PROC PROC
    M_PRINT MSG_CANCEL
    M_GET_NUM
    
    CMP AX, 1
    JL CANCEL_ERR
    CMP AX, 20
    JG CANCEL_ERR
    
    DEC AX
    MOV SI, AX
    
    ; Check if booked
    MOV AL, SEAT_MAP[SI]
    CMP AL, 0
    JE CANCEL_EMPTY
    
    ; Refund
    MOV AX, SEAT_FARES[SI]
    SUB TOTAL_REVENUE, AX
    DEC SEATS_SOLD
    
    ; Reset Data
    MOV SEAT_MAP[SI], 0
    MOV PASSENGER_TYPE[SI], 0
    MOV SEAT_FARES[SI], 0
    
    M_PRINT MSG_REFUND
    RET
    
    CANCEL_EMPTY:
    M_PRINT MSG_NOT_BKD
    RET
    
    CANCEL_ERR:
    M_PRINT MSG_ERR_INV
    RET
CANCEL_TICKET_PROC ENDP

; --- FEATURE 6: SEARCH LOGIC ---
SEARCH_SEAT_PROC PROC
    M_PRINT MSG_SEARCH
    M_GET_NUM
    
    DEC AX
    MOV SI, AX
    
    MOV AL, SEAT_MAP[SI]
    CMP AL, 0
    JE SEARCH_EMPTY
    
    M_PRINT MSG_ST_BKD
    MOV AL, PASSENGER_TYPE[SI]
    CMP AL, 1
    JE PRT_STU
    
    M_PRINT MSG_ST_REG
    RET
    
    PRT_STU:
    M_PRINT MSG_ST_STD
    RET
    
    SEARCH_EMPTY:
    M_PRINT MSG_ST_EMP
    RET
SEARCH_SEAT_PROC ENDP

END MAIN