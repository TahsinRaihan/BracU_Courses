; =================================================================
; PROJECT: LUXURY CITY BUS RESERVATION SYSTEM (FINAL VERSION)
; FEATURES:
;   1. SECURE LOGIN (8-Digit ID Check)
;   2. GRAPHICAL BUS MAP (2+2 Layout with Aisle)
;   3. SMART SEAT STATUS (Shows Number if Empty, 'XX' if Booked)
;   4. DYNAMIC FARE SYSTEM (Student/Regular Logic)
;   5. CANCELLATION SYSTEM (Restores Inventory)
;   6. ADMIN DASHBOARD (Revenue & Stats)
; =================================================================

.MODEL SMALL
.STACK 100H

.DATA
    ; --- SYSTEM MEMORY ---
    SEATS       DB 20 DUP(0)     ; Array for 20 Seats (0=Empty, 1=Booked)
    TOTAL_REV   DW 0             ; Total Revenue Counter
    
    ; --- LOGIN CONFIGURATION ---
    AUTH_ID     DB '20231045'    ; ADMIN/STUDENT ID
    INPUT_BUFF  DB 10, ?, 10 DUP('$') ; Input Buffer
    
    ; --- ARTISTIC UI ELEMENTS ---
    BORDER_TOP  DB 10,13, ' .------------------------------------------.', 10,13, '$'
    BORDER_MID  DB 10,13, ' |                                          |', 10,13, '$'
    BORDER_BOT  DB 10,13, ' *------------------------------------------*', 10,13, '$'
    
    APP_TITLE   DB        ' |       PREMIUM BUS RESERVATION SYSTEM     |', 10,13, '$'
    LOGIN_TXT   DB 10,13, ' |      PLEASE ENTER YOUR 8-DIGIT ID        |', 10,13, '$'
    PROMPT_ID   DB 10,13, '        > USER ID: $'
    DENIED_MSG  DB 10,13, ' [!] ACCESS DENIED. ID NOT FOUND.', 10,13, '$'
    
    ; --- MENU OPTIONS ---
    M_OPT1      DB 10,13, ' |  [1] VIEW LIVE BUS MAP (Graphic View)    |', 10,13, '$'
    M_OPT2      DB 10,13, ' |  [2] BOOK A TICKET                       |', 10,13, '$'
    M_OPT3      DB 10,13, ' |  [3] CANCEL A RESERVATION                |', 10,13, '$'
    M_OPT4      DB 10,13, ' |  [4] ADMIN: REVENUE REPORT               |', 10,13, '$'
    M_OPT5      DB 10,13, ' |  [5] EXIT SYSTEM                         |', 10,13, '$'
    M_SELECT    DB 10,13, '        > SELECT OPTION: $'

    ; --- BUS GRAPHICS ---
    BUS_ROOF    DB 10,13, '      __________________________________ ', 10,13
                DB        '     /  [ DRIVER ]                      \', 10,13, '$'
    BUS_FLOOR   DB        '     |__________________________________|', 10,13
                DB        '       (O)                          (O)  ', 10,13, '$'
    AISLE_SPC   DB '     ', '$'   ; The gap between seats
    LEFT_WALL   DB '     |  ', '$'
    RIGHT_WALL  DB '  |', 10,13, '$'
    
    ; --- INTERACTION MESSAGES ---
    ASK_SEAT    DB 10,13, ' > ENTER SEAT NUMBER (1-20): $'
    ASK_TYPE    DB 10,13, ' > TICKET CLASS: [1] STUDENT(50tk) [2] REGULAR(100tk): $'
    
    SUCCESS_BK  DB 10,13, ' [OK] TICKET CONFIRMED! HAVE A SAFE TRIP.', 10,13, '$'
    SUCCESS_CN  DB 10,13, ' [OK] RESERVATION CANCELLED. REFUND PROCESSED.', 10,13, '$'
    ERR_FULL    DB 10,13, ' [!] ERROR: THIS SEAT IS ALREADY BOOKED (XX).', 10,13, '$'
    ERR_RANGE   DB 10,13, ' [!] ERROR: INVALID INPUT.', 10,13, '$'
    REV_HEADER  DB 10,13, ' $$$ TODAY TOTAL EARNINGS: TK. $'

; --- MACROS FOR CLEANER CODE ---
PRINT MACRO MSG
    LEA DX, MSG
    MOV AH, 09H
    INT 21H
ENDM

CLEAR_SCREEN MACRO
    MOV AX, 03H
    INT 10H
ENDM

.CODE
MAIN PROC
    ; --- INITIALIZATION ---
    MOV AX, @DATA
    MOV DS, AX
    MOV ES, AX      ; CRITICAL: Set Extra Segment for String Compare
    CLD

    ; =============================================================
    ; FEATURE 1: SECURE LOGIN INTERFACE
    ; =============================================================
LOGIN_SCREEN:
    CLEAR_SCREEN
    PRINT BORDER_TOP
    PRINT APP_TITLE
    PRINT BORDER_BOT
    PRINT LOGIN_TXT
    PRINT PROMPT_ID
    
    ; Capture Input
    MOV AH, 0AH
    LEA DX, INPUT_BUFF
    INT 21H
    
    ; Validate Logic
    LEA SI, INPUT_BUFF + 1
    MOV AL, [SI]
    CMP AL, 8              ; Strict 8-digit check
    JNE LOGIN_FAIL
    
    LEA SI, INPUT_BUFF + 2
    LEA DI, AUTH_ID
    MOV CX, 8
    REPE CMPSB
    JZ MAIN_MENU
    
LOGIN_FAIL:
    PRINT DENIED_MSG
    MOV AH, 1
    INT 21H
    JMP LOGIN_SCREEN

    ; =============================================================
    ; MAIN DASHBOARD
    ; =============================================================
MAIN_MENU:
    CLEAR_SCREEN
    PRINT BORDER_TOP
    PRINT APP_TITLE
    PRINT BORDER_MID
    PRINT M_OPT1
    PRINT M_OPT2
    PRINT M_OPT3
    PRINT M_OPT4
    PRINT M_OPT5
    PRINT BORDER_BOT
    PRINT M_SELECT
    
    MOV AH, 1
    INT 21H
    
    CMP AL, '1'
    JE GO_MAP
    CMP AL, '2'
    JE GO_BOOK
    CMP AL, '3'
    JE GO_CANCEL
    CMP AL, '4'
    JE GO_ADMIN
    CMP AL, '5'
    JE EXIT_APP
    
    JMP MAIN_MENU

; --- JUMP TABLES ---
GO_MAP:
    CALL DRAW_BUS_GRAPHIC
    MOV AH, 1       ; Pause to let user see map
    INT 21H
    JMP MAIN_MENU

GO_BOOK:
    CALL BOOKING_SYSTEM
    JMP MAIN_MENU

GO_CANCEL:
    CALL CANCEL_SYSTEM
    JMP MAIN_MENU

GO_ADMIN:
    CALL ADMIN_VIEW
    MOV AH, 1
    INT 21H
    JMP MAIN_MENU

EXIT_APP:
    MOV AX, 4C00H
    INT 21H
MAIN ENDP

; =============================================================
; FEATURE 2: ADVANCED LIVE SEAT MAP (GRAPHICAL)
; =============================================================
DRAW_BUS_GRAPHIC PROC
    CLEAR_SCREEN
    PRINT BUS_ROOF      ; Draw the front/driver section
    
    LEA SI, SEATS       ; Start of Array
    MOV CX, 5           ; 5 Rows (for 20 seats, 4 per row)
    MOV BL, 1           ; Seat Number Counter

ROW_LOOP:
    PRINT LEFT_WALL     ; Draw side of bus
    
    ; --- SEAT 1 (Left Window) ---
    CALL DRAW_SINGLE_SEAT
    INC SI
    INC BL
    
    ; --- SEAT 2 (Left Aisle) ---
    CALL DRAW_SINGLE_SEAT
    INC SI
    INC BL
    
    PRINT AISLE_SPC     ; Draw the walkway
    
    ; --- SEAT 3 (Right Aisle) ---
    CALL DRAW_SINGLE_SEAT
    INC SI
    INC BL
    
    ; --- SEAT 4 (Right Window) ---
    CALL DRAW_SINGLE_SEAT
    INC SI
    INC BL
    
    PRINT RIGHT_WALL    ; Draw side of bus
    LOOP ROW_LOOP
    
    PRINT BUS_FLOOR     ; Draw wheels
    RET
DRAW_BUS_GRAPHIC ENDP

; --- HELPER: DRAWS [01] or [XX] ---
DRAW_SINGLE_SEAT PROC
    PUSH AX
    PUSH DX
    
    MOV AL, [SI]        ; Check Status
    CMP AL, 1
    JE DRAW_X
    
    ; Draw Empty [Number]
    MOV DL, '['
    MOV AH, 2
    INT 21H
    
    ; Print Number Logic (BL holds number)
    MOV AL, BL
    AAM                 ; ASCII Adjust for Multiplication (Splits AL into AH, AL)
    ADD AX, 3030H       ; Convert to ASCII digits
    MOV DX, AX          ; Swap for printing order
    MOV AH, 2
    PUSH DX
    MOV DL, DH          ; Print Tens
    INT 21H
    POP DX
    MOV DL, DL          ; Print Units
    INT 21H
    
    MOV DL, ']'
    INT 21H
    JMP END_DRAW

DRAW_X:
    ; Draw Booked [XX]
    MOV DL, '['
    MOV AH, 2
    INT 21H
    MOV DL, 'X'
    INT 21H
    MOV DL, 'X'
    INT 21H
    MOV DL, ']'
    INT 21H

END_DRAW:
    POP DX
    POP AX
    RET
DRAW_SINGLE_SEAT ENDP

; =============================================================
; FEATURE 3 & 4: BOOKING & FARE CALCULATION
; =============================================================
BOOKING_SYSTEM PROC
    ; Show map first so they know what to pick
    CALL DRAW_BUS_GRAPHIC 
    
    PRINT ASK_SEAT
    CALL GET_USER_NUMBER ; Returns inputs in AX
    
    ; Validate 1-20
    CMP AX, 1
    JL BAD_INPUT
    CMP AX, 20
    JG BAD_INPUT
    
    ; Convert Seat Number to Array Index
    LEA SI, SEATS
    ADD SI, AX
    DEC SI              ; Array is 0-indexed
    
    ; Check if Booked
    MOV BL, [SI]
    CMP BL, 1
    JE IS_FULL
    
    ; Mark as Booked
    MOV [SI], 1
    
    ; Ask Pricing Type
    PRINT ASK_TYPE
    MOV AH, 1
    INT 21H
    
    CMP AL, '1'
    JE ADD_STUDENT_FARE
    
    ; Regular
    ADD TOTAL_REV, 100
    JMP FINISH_BOOK

ADD_STUDENT_FARE:
    ADD TOTAL_REV, 50
    
FINISH_BOOK:
    PRINT SUCCESS_BK
    MOV AH, 1
    INT 21H
    RET

IS_FULL:
    PRINT ERR_FULL
    MOV AH, 1
    INT 21H
    RET

BAD_INPUT:
    PRINT ERR_RANGE
    MOV AH, 1
    INT 21H
    RET
BOOKING_SYSTEM ENDP

; =============================================================
; FEATURE 5: CANCELLATION LOGIC
; =============================================================
CANCEL_SYSTEM PROC
    PRINT ASK_SEAT
    CALL GET_USER_NUMBER
    
    CMP AX, 1
    JL BAD_INPUT
    CMP AX, 20
    JG BAD_INPUT
    
    LEA SI, SEATS
    ADD SI, AX
    DEC SI
    
    MOV BL, [SI]
    CMP BL, 0
    JE ALREADY_FREE
    
    ; Free the seat
    MOV [SI], 0
    PRINT SUCCESS_CN
    MOV AH, 1
    INT 21H
    RET

ALREADY_FREE:
    PRINT ERR_RANGE ; "Already empty" treated as input error here for brevity
    MOV AH, 1
    INT 21H
    RET
CANCEL_SYSTEM ENDP

; =============================================================
; FEATURE 6: ADMIN REVENUE VIEW
; =============================================================
ADMIN_VIEW PROC
    CLEAR_SCREEN
    PRINT BORDER_TOP
    PRINT REV_HEADER
    
    MOV AX, TOTAL_REV
    CALL PRINT_NUMBER_AX
    
    PRINT BORDER_BOT
    RET
ADMIN_VIEW ENDP

; =============================================================
; UTILITY PROCEDURES (INPUT/OUTPUT)
; =============================================================

; --- Read Multi-Digit Number to AX ---
GET_USER_NUMBER PROC
    PUSH BX
    PUSH CX
    PUSH DX
    XOR BX, BX      ; Result accumulator
READ_KEY:
    MOV AH, 1
    INT 21H
    CMP AL, 13      ; Check for Enter key
    JE DONE_READ
    SUB AL, '0'
    MOV AH, 0
    MOV CX, AX      ; New digit in CX
    MOV AX, BX
    MOV DX, 10
    MUL DX          ; AX = BX * 10
    ADD AX, CX      ; Add new digit
    MOV BX, AX      ; Save back to BX
    JMP READ_KEY
DONE_READ:
    MOV AX, BX
    POP DX
    POP CX
    POP BX
    RET
GET_USER_NUMBER ENDP

; --- Print 16-bit Number from AX ---
PRINT_NUMBER_AX PROC
    PUSH BX
    PUSH CX
    PUSH DX
    CMP AX, 0
    JNE NON_ZERO
    MOV DL, '0'
    MOV AH, 2
    INT 21H
    JMP EXIT_PRT
NON_ZERO:
    MOV CX, 0
    MOV BX, 10
DIV_LOOP:
    MOV DX, 0
    DIV BX
    PUSH DX
    INC CX
    CMP AX, 0
    JNE DIV_LOOP
PRT_LOOP:
    POP DX
    ADD DL, '0'
    MOV AH, 2
    INT 21H
    LOOP PRT_LOOP
EXIT_PRT:
    POP DX
    POP CX
    POP BX
    RET
PRINT_NUMBER_AX ENDP

END MAIN